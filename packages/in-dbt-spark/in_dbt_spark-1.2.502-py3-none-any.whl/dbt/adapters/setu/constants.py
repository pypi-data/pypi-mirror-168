from dbt.adapters.setu.models import StatementKind

DEFAULT_SPARK_VERSION = "3.1"
DEFAULT_DRIVER_MEMORY = "4G"
DEFAULT_DRIVER_CORES = 2
DEFAULT_EXECUTOR_MEMORY = "8G"
DEFAULT_EXECUTOR_CORES = 2
DEFAULT_NUM_EXECUTORS = 10
DEFAULT_SPARK_APPLICATION_NAME = "DBT_Default_Session_Name"
DEFAULT_YARN_QUEUE = "misc_default"
DEFAULT_HEARTBEAT_TIMEOUT = 900
DEFAULT_EXECUTION_TAGS = {"gpu": False, "pool": "dev"}

DEFAULT_SPARK_CONF = {
    "spark.master": "yarn-cluster",
    "spark.yarn.security.credentials.hive.enabled": "true",
    "spark.security.credentials.hive.enabled": "true",
    "spark.pyspark.python": "/export/apps/python/3.7/bin/python3",
    "spark.jars.ivy": "ivy2-repo",
    "spark.sql.adaptive.enabled": "true",
    "spark.submit.deployMode": "cluster",
    "spark.sql.sources.partitionOverwriteMode": "DYNAMIC",
    "spark.hadoop.hive.exec.dynamic.partition": "true",
    "spark.hadoop.hive.exec.dynamic.partition.mode": "nonstrict",
    "hive.exec.dynamic.partition.mode": "nonstrict",
    "spark.dynamicAllocation.enabled": "true",
    "spark.dynamicAllocation.initialExecutors": DEFAULT_NUM_EXECUTORS,
    "spark.dynamicAllocation.maxExecutors": 900,
    "spark.dynamicAllocation.minExecutors": 1,
}

SPARK_CONF_APPEND_KEYS = [
    "spark.jars.packages",
]

SPARK_RESOURCE_KEYS = {
    "driver_memory": "spark.driver.memory",
    "driver_cores": "spark.driver.cores",
    "executor_memory": "spark.executor.memory",
    "executor_cores": "spark.executor.cores",
    "num_executors": "spark.executor.instances",
}

SERIALISE_DATAFRAME_TEMPLATE_SPARK = "{}.toJSON.collect.foreach(println)"

VALID_STATEMENT_KINDS = {
    StatementKind.SPARK,
    StatementKind.PYSPARK,
    StatementKind.SQL,
    StatementKind.SPARKR,
}
