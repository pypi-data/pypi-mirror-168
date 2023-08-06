import requests
import json
from typing import Any, Union, Dict, List, Tuple, Optional
from dbt.adapters.setu.models import StatementKind
from dbt.events import AdapterLogger
from dbt.adapters.setu.models import (
    Session,
    Statement,
)
from dbt.adapters.setu.utils import (
    create_setu_session_dependency_body,
    create_setu_session_config_body,
)

logger = AdapterLogger("Spark")
Auth = Union[requests.auth.AuthBase, Tuple[str, str]]
Verify = Union[bool, str]


class JsonClient:
    """A wrapper for a requests session for JSON formatted requests.

    This client handles appending endpoints on to a common hostname,
    deserializing the response as JSON and raising an exception when an error
    HTTP code is received.
    """

    def __init__(
        self,
        url: str,
        auth: Auth = None,
        verify: Verify = False,
        requests_session: requests.Session = None,
    ) -> None:
        self.url = url
        self.auth = auth
        self.verify = verify
        self.headers = {"Content-Type": "application/json"}
        if requests_session is None:
            self.session = requests.Session()
            self.managed_session = True
        else:
            self.session = requests_session
            self.managed_session = False

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        if self.managed_session:
            self.session.close()

    def get(self, endpoint: str = "", params: dict = None) -> dict:
        return self._request("GET", endpoint, params=params, headers=self.headers)

    def post(self, endpoint: str, data: dict = None) -> dict:
        return self._request("POST", endpoint, data, headers=self.headers)

    def delete(self, endpoint: str = "") -> dict:
        return self._request("DELETE", endpoint, headers=self.headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
    ) -> dict:
        url = self.url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = self.session.request(
            method,
            url,
            auth=self.auth,
            verify=self.verify,
            json=data,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


class SetuClient:
    """
    A Client wrapper for all SETU API interactions
    """

    def __init__(
        self,
        url: str,
        auth: Auth = None,
        verify: Verify = True,
    ) -> None:
        self._client = JsonClient(url=url, auth=auth, verify=verify)

    def __enter__(self) -> "SetuClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying requests session, if managed by this class."""
        self._client.close()

    def list_sessions(self) -> List[Session]:
        """List all the active sessions in SETU."""
        data = self._client.get("/sessions")
        return [Session.from_json(item) for item in data["sessions"]]

    def create_session(
        self,
        proxy_user: str,
        jars: List[str],
        py_files: List[str],
        files: List[str],
        archives: List[str],
        manifest_file_location: str,
        driver_memory: str,
        driver_cores: int,
        executor_memory: str,
        executor_cores: int,
        num_executors: int,
        queue: str,
        session_name: str,
        spark_version: str,
        execution_tags: Dict[str, Any],
        spark_conf: Dict[str, Any],
        metadata: Dict[str, Any],
        heartbeat_timeout: int,
        enable_ssl: bool,
    ) -> Session:
        """Create New SETU session. This is not a blocking call."""
        interactive_session_params: Dict[str, Any] = {
            "dependency": create_setu_session_dependency_body(
                jars, py_files, files, archives, manifest_file_location
            ),
            "config": create_setu_session_config_body(
                proxy_user,
                driver_memory,
                driver_cores,
                executor_memory,
                executor_cores,
                num_executors,
                queue,
                session_name,
                spark_version,
                execution_tags,
                spark_conf,
                metadata,
                heartbeat_timeout,
                enable_ssl,
            ),
        }
        body = interactive_session_params
        logger.info(
            f"Session create request body : \n {json.dumps(body, indent=4, sort_keys=True)}"
        )
        try:
            data = self._client.post("/sessions", data=body)
        except requests.HTTPError as e:
            logger.error(e)
            raise
        return Session.from_json(data)

    def get_session(self, session_id: int) -> Optional[Session]:
        """Get information about a session.
        :param session_id: The ID of the session.
        """
        try:
            data = self._client.get(f"/sessions/{session_id}")
        except requests.HTTPError as e:
            logger.error(e)
            if e.response.status_code == 404:
                return None
            else:
                raise
        return Session.from_json(data)

    def cancel_session(self, session_id: int) -> None:
        """Cancel a session.
        :param session_id: The ID of the session.
        """
        try:
            self._client.post(f"/sessions/{session_id}/cancel")
        except requests.HTTPError as e:
            logger.error(e)

    def list_statements(self, session_id: int) -> List[Statement]:
        """Get all the statements in a session.
        :param session_id: The ID of the session.
        """
        try:
            response = self._client.get(f"/sessions/{session_id}/statements")
        except requests.HTTPError as e:
            logger.error(e)
            raise
        return [Statement.from_json(session_id, response) for data in response["statements"]]

    def create_statement(
        self, session_id: int, code: str, kind: StatementKind = None
    ) -> Statement:
        """create a statement in a session. This is not a blocking call.
        :param session_id: The ID of the session.
        :param code: The code to execute.
        :param kind: The kind of code to execute.
        """
        data = {"code": code}
        if kind is not None:
            data["kind"] = kind.value
        try:
            response = self._client.post(f"/sessions/{session_id}/statements", data=data)
        except requests.HTTPError as e:
            logger.error(e)
            raise
        return Statement.from_json(session_id, response)

    def cancel_statement(self, session_id: int, statement_id: int):
        """cancel the statement
        :param session_id: The ID of the session.
        :param statement_id: The ID of the statement.
        """
        try:
            self._client.post(f"/sessions/{session_id}/statements/{statement_id}/cancel")
        except requests.HTTPError as e:
            logger.error(e)

    def get_statement(self, session_id: int, statement_id: int) -> Statement:
        """Get information about a statement in a session.
        :param session_id: The ID of the session.
        :param statement_id: The ID of the statement.
        """
        try:
            response = self._client.get(f"/sessions/{session_id}/statements/{statement_id}")
        except requests.HTTPError as e:
            logger.error(e)
            raise
        return Statement.from_json(session_id, response)
