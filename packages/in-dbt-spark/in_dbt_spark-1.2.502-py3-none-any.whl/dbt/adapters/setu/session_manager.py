from dbt.events import AdapterLogger
from typing import Any, Dict, List, Optional
from threading import Lock
from dbt.adapters.setu.client import SetuClient, Auth, Verify
from dbt.adapters.setu.session import SetuSession
from dbt.adapters.setu.constants import (
    SPARK_RESOURCE_KEYS,
    DEFAULT_DRIVER_MEMORY,
    DEFAULT_EXECUTOR_MEMORY,
    DEFAULT_NUM_EXECUTORS,
    DEFAULT_EXECUTOR_CORES,
    DEFAULT_DRIVER_CORES,
    DEFAULT_SPARK_VERSION,
    DEFAULT_SPARK_APPLICATION_NAME,
    DEFAULT_YARN_QUEUE,
    DEFAULT_HEARTBEAT_TIMEOUT,
)
from dbt.adapters.setu.utils import (
    generate_unique_session_name,
    get_execution_tags_with_defaults,
    get_spark_conf_with_defaults,
)

logger = AdapterLogger("Spark")


class SetuSessionManager:
    session_id: Optional[int] = None
    session_lock = Lock()
    """
    Manages creation and closing of SETU sessions
    """

    @classmethod
    def create_session(
        cls,
        url: str,
        auth: Auth = None,
        verify: Verify = False,
        proxy_user: str = None,
        jars: List[str] = None,
        py_files: List[str] = None,
        archives: List[str] = None,
        files: List[str] = None,
        manifest_file_location: str = None,
        queue: str = DEFAULT_YARN_QUEUE,
        setu_session_name: str = DEFAULT_SPARK_APPLICATION_NAME,
        spark_version: str = DEFAULT_SPARK_VERSION,
        execution_tags: Dict[str, Any] = dict(),
        spark_conf: Dict[str, Any] = dict(),
        metadata: Dict[str, Any] = dict(),
        heartbeat_timeout: int = DEFAULT_HEARTBEAT_TIMEOUT,
        enable_ssl: bool = False,
    ) -> "SetuSession":
        """Create a new SETU session.

        Ivy's for jars, py_files, files and archives arguments are all copied to
        the same working directory on the Spark cluster.

        The driver_memory and executor_memory arguments have the same format as
        JVM memory strings with a size unit suffix ("k", "m", "g" or "t") (e.g.
        512m, 2g).

        See https://spark.apache.org/docs/latest/configuration.html for more
        information on Spark configuration properties.

        :param url: SETU server URL.
        :param auth: A requests-compatible auth object to use when making
            requests.
        :param verify: Either a boolean, in which case it controls whether we
            verify the server’s TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use. Defaults to ``True``.
        :param proxy_user: User to impersonate when starting the session.
        :param jars: Ivy's of jars to be used in this session.
        :param py_files: URLs of Python files to be used in this session.
        :param files: URLs of files to be used in this session.
        :param archives: URLs of archives to be used in this session.
        :param queue: The name of the YARN queue to which submitted.
        :param setu_session_name: The name of this session.
        :param spark_conf: Spark configuration properties.
        :param heartbeat_timeout: Optional Timeout in seconds to which session
            be automatically orphaned if no heartbeat is received.
        :param metadata: Dict of metadata for this SETU session
        :param enable_ssl: enable ssl configurations on driver and executors
        :param execution_tags: Dict of tags to be inferred by Infra
        :param spark_version: version of the spark session
        :param manifest_file_location: location of manifest file with all the dependencies
        """
        with cls.session_lock:
            if cls.session_id is not None:
                logger.info(f"use existing session with id = {cls.session_id}")
                try:
                    logger.info("check if existing Setu session is active")
                    existing_setu_session = SetuSessionManager.get_session_if_active(
                        url=url,
                        session_id=cls.session_id,
                        verify=False,
                    )
                    if existing_setu_session is not None:
                        logger.info(f"existing Setu session {cls.session_id} is already active")
                        return existing_setu_session
                except Exception as ex:
                    logger.error(f"Error while checking {cls.session_id} session exists : {ex}")
            logger.info("creating new Setu session")
            with SetuClient(url=url, auth=auth, verify=verify) as client:
                session = client.create_session(
                    proxy_user=proxy_user,
                    jars=jars,
                    py_files=py_files,
                    files=files,
                    archives=archives,
                    manifest_file_location=manifest_file_location,
                    driver_memory=spark_conf.get(
                        SPARK_RESOURCE_KEYS.get("driver_memory"), DEFAULT_DRIVER_MEMORY
                    ),
                    driver_cores=spark_conf.get(
                        SPARK_RESOURCE_KEYS.get("driver_cores"), DEFAULT_DRIVER_CORES
                    ),
                    executor_memory=spark_conf.get(
                        SPARK_RESOURCE_KEYS.get("executor_memory"),
                        DEFAULT_EXECUTOR_MEMORY,
                    ),
                    executor_cores=spark_conf.get(
                        SPARK_RESOURCE_KEYS.get("executor_cores"),
                        DEFAULT_EXECUTOR_CORES,
                    ),
                    num_executors=spark_conf.get(
                        SPARK_RESOURCE_KEYS.get("num_executors"), DEFAULT_NUM_EXECUTORS
                    ),
                    queue=queue,
                    session_name=generate_unique_session_name(setu_session_name),
                    spark_version=spark_version,
                    execution_tags=get_execution_tags_with_defaults(execution_tags),
                    spark_conf=get_spark_conf_with_defaults(spark_conf),
                    metadata=metadata,
                    heartbeat_timeout=heartbeat_timeout,
                    enable_ssl=enable_ssl,
                )
                cls.session_id = session.session_id
                return SetuSession(
                    url,
                    session.session_id,
                    auth,
                    verify,
                )

    @classmethod
    def close_session(
        cls,
        url: str,
        auth: Auth = None,
        verify: Verify = False,
    ):
        """Close the managed SETU session."""
        if cls.session_id is None:
            logger.info(" No setu session active ")
        with cls.session_lock:
            with SetuClient(url, auth, verify) as client:
                session = client.get_session(cls.session_id)
                if session is not None:
                    client.cancel_session(cls.session_id)
                    cls.session_id = None
                    logger.info(f"cancelled session : {cls.session_id}")

    @classmethod
    def get_session_if_active(
        cls,
        url: str,
        session_id: int,
        auth: Auth = None,
        verify: Verify = False,
    ):
        """get SETU session if still active."""
        with SetuClient(url, auth, verify) as client:
            session = client.get_session(session_id)
        if session is not None:
            return SetuSession(url, session.session_id, auth, verify)
        return None
