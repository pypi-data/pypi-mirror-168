from .base import ParamsVarEnv
from enum import Enum

class VarEnv(ParamsVarEnv, Enum):
    PATH_TO_CRED = ParamsVarEnv(key="GCS_PATH_TO_CRED")
    NAME_BUCKET = ParamsVarEnv(key="GCS_BUCKET_NAME")
    PROJECT_BIGQUERY = ParamsVarEnv(key="GCS_BIGQUERY_PROJECT")
    DATASET_BIGQUERY = ParamsVarEnv(key="GCS_BIGQUERY_DATASET")