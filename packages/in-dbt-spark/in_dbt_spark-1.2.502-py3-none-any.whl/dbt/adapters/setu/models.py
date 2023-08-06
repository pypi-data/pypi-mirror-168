import ast
import json
import dbt.exceptions
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from dbt.events import AdapterLogger

logger = AdapterLogger("Spark")


@dataclass
class Output:
    json: Optional[dict]
    execution_success: bool
    error: Optional[str]

    @classmethod
    def from_json(cls, data: dict) -> "Output":
        if "outputData" not in data or not type(data.get("outputData")) is dict:
            try:
                data["outputData"] = json.loads(str(data.get("outputData")))
            except ValueError:
                logger.error(f"Error while json parsing outputData = {data.get('outputData')}")
                return cls(
                    None,
                    json.loads(str(data.get("executionSuccess")).lower()),
                    data.get("error"),
                )
        return cls(
            ast.literal_eval(str(data.get("outputData"))).get("application/json"),
            json.loads(str(data.get("executionSuccess")).lower()),
            data.get("error"),
        )

    def raise_for_status(self) -> None:
        if not self.execution_success:
            logger.error(f"Spark Runtime Error : {self.error}")
            components = []
            if self.error is not None:
                components.append(f"Error ={self.error}")
            raise dbt.exceptions.RuntimeException(f'({", ".join(components)})')


class StatementKind(Enum):
    SPARK = "spark"
    PYSPARK = "pyspark"
    SPARKR = "sparkr"
    SQL = "sql"


class StatementState(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    AVAILABLE = "available"
    ERROR = "error"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


@dataclass
class Statement:
    session_id: int
    statement_id: int
    state: StatementState
    code: str
    output: Optional[Output]
    progress: Optional[float]

    @classmethod
    def from_json(cls, session_id: int, data: dict) -> "Statement":
        if data["outputData"] is None:
            output = None
        else:
            output = Output.from_json(data)

        return cls(
            session_id,
            data["id"],
            StatementState(data["state"]),
            data["code"],
            output,
            data.get("progress"),
        )


class SessionState(Enum):
    NOT_STARTED = "not_started"
    STARTING = "starting"
    RECOVERING = "recovering"
    IDLE = "idle"
    RUNNING = "running"
    BUSY = "busy"
    SHUTTING_DOWN = "shutting_down"
    ERROR = "error"
    DEAD = "dead"
    KILLED = "killed"
    SUCCESS = "success"


SESSION_STATE_NOT_READY = {SessionState.NOT_STARTED, SessionState.STARTING}
SESSION_STATE_FINISHED = {
    SessionState.ERROR,
    SessionState.DEAD,
    SessionState.KILLED,
    SessionState.SUCCESS,
}


@dataclass
class SessionAppInfo:
    driverLogUrl: str
    sparkUiUrl: str
    yarnQueue: str

    @classmethod
    def from_json(cls, data: dict) -> "SessionAppInfo":
        return cls(data["driverLogUrl"], data["sparkUiUrl"], data["yarnQueue"])


@dataclass
class Session:
    session_id: int
    proxy_user: str
    state: SessionState
    application_id: str
    app_info: Optional[SessionAppInfo]

    @classmethod
    def from_json(cls, data: dict) -> "Session":
        if data["appInfo"] is None:
            output = None
        else:
            output = SessionAppInfo.from_json(data["appInfo"])
        return cls(
            data["id"],
            data["proxyUser"],
            SessionState(data["state"]),
            data["appId"],
            output,
        )
