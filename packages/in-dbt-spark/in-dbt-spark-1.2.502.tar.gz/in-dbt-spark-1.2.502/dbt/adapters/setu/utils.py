import pandas
import uuid
from typing import Iterable, Iterator, Dict, Any, List

from dbt.adapters.setu.models import StatementState

from dbt.adapters.setu.constants import (
    DEFAULT_EXECUTION_TAGS,
    DEFAULT_SPARK_CONF,
    SPARK_CONF_APPEND_KEYS,
)


def get_dataframe_from_json_output(json_output: dict) -> pandas.DataFrame:
    """return the pandas dataframe from json output"""
    try:
        fields = json_output["schema"]["fields"]
        columns = [field["name"] for field in fields]
        data = json_output["data"]
    except KeyError:
        raise ValueError("json output does not match expected structure")
    return pandas.DataFrame(data, columns=columns)


def get_data_from_json_output(json_output: dict) -> dict:
    """return the data from json output"""
    try:
        data = json_output["data"]
    except KeyError:
        raise ValueError("json output does not match expected structure")
    return data


def get_execution_tags_with_defaults(execution_tags: Dict[str, Any]) -> Dict[str, Any]:
    """Add defaults to user missed execution tags"""
    for key in DEFAULT_EXECUTION_TAGS.keys():
        execution_tags.setdefault(key, DEFAULT_EXECUTION_TAGS[key])
    return execution_tags


def get_spark_conf_with_defaults(spark_conf: Dict[str, Any]) -> Dict[str, Any]:
    """Add defaults to user missed spark configs"""
    # To support conf.spark as prefix for passing spark configs
    for key in list(spark_conf):
        if key.startswith("conf."):
            new_key = key.replace("conf.", "", 1)
            spark_conf[new_key] = spark_conf.pop(key)

    for key in DEFAULT_SPARK_CONF.keys():
        if key in SPARK_CONF_APPEND_KEYS and key in spark_conf:
            user_config = spark_conf[key].split(",")
            default_config = DEFAULT_SPARK_CONF[key].split(",")
            user_config.extend(default_config)
            spark_conf[key] = ",".join(user_config)
        else:
            spark_conf.setdefault(key, DEFAULT_SPARK_CONF[key])
    return spark_conf


def generate_unique_session_name(session_name: str) -> str:
    """Append UUID4 to user provided session name"""
    return "_".join([session_name, uuid.uuid4().hex])


def create_setu_session_dependency_body(
    jars: List[str] = None,
    py_files: List[str] = None,
    files: List[str] = None,
    archives: List[str] = None,
    manifest_file_location: str = None,
) -> Dict[str, Any]:
    """
    util to create dependency dict for new SETU session creation
    """
    body: Dict[str, Any] = {"dependencies": []}
    if manifest_file_location is not None:
        body["manifestFileLocation"] = manifest_file_location
    if jars is not None:
        for jar in jars:
            body["dependencies"].append(jar)
    if py_files is not None:
        for py_file in py_files:
            body["dependencies"].append(py_file)
    if files is not None:
        for file in files:
            body["dependencies"].append(file)
    if archives is not None:
        for archive in archives:
            body["dependencies"].append(archive)
    return body


def create_setu_session_config_body(
    proxy_user: str,
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
) -> Dict[str, Any]:
    """
    util to create config dict for new SETU session creation
    """
    body: Dict[str, Any] = {"jobType": "SPARK", "interactiveSessionKind": "spark"}
    if proxy_user is not None:
        body["proxyUser"] = proxy_user
    if session_name is not None:
        body["sessionName"] = session_name
    if execution_tags is not None:
        body["executionTags"] = execution_tags
    if metadata is not None:
        body["metadata"] = metadata
    body["enableSsl"] = enable_ssl
    body["sparkParameters"] = {}
    if heartbeat_timeout is not None:
        body["heartbeatTimeoutInSeconds"] = heartbeat_timeout
    if driver_memory is not None:
        body["sparkParameters"]["driverMemory"] = driver_memory
    if driver_cores is not None:
        body["sparkParameters"]["driverCores"] = driver_cores
    if executor_memory is not None:
        body["sparkParameters"]["executorMemory"] = executor_memory
    if executor_cores is not None:
        body["sparkParameters"]["executorCores"] = executor_cores
    if num_executors is not None:
        body["sparkParameters"]["numExecutors"] = num_executors
    if spark_version is not None:
        body["sparkParameters"]["sparkVersion"] = spark_version
    if queue is not None:
        spark_conf["spark.yarn.queue"] = queue
    if spark_conf is not None:
        body["otherConfs"] = spark_conf
    return body


def polling_intervals(
    start: Iterable[float], rest: float, max_duration: float = None
) -> Iterator[float]:
    def _intervals():
        yield from start
        while True:
            yield rest

    cumulative = 0.0
    for interval in _intervals():
        cumulative += interval
        if max_duration is not None and cumulative > max_duration:
            break
        yield interval


def waiting_for_output(statement):
    not_finished = statement.state in {
        StatementState.WAITING,
        StatementState.RUNNING,
    }
    available = statement.state == StatementState.AVAILABLE
    return not_finished or (available and statement.output is None)
