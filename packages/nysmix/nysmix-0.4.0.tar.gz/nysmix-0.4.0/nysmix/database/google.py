from functools import cached_property
from .base import Database
from dataclasses import dataclass
from sqlalchemy.future.engine import Engine, create_engine
from nysmix.config.google import VarEnv
from google.cloud.bigquery import Client, LoadJobConfig, WriteDisposition, SourceFormat
from google.oauth2.service_account import Credentials
from io import BytesIO
from pandas import read_csv, to_datetime


@dataclass
class BigQuery(Database):
    @property
    def engine(self) -> Engine:
        return create_engine(
            f"bigquery://{VarEnv.PROJECT_BIGQUERY.value}/{VarEnv.DATASET_BIGQUERY.value}",
            credentials_path=VarEnv.PATH_TO_CRED.value,
            echo=True,
        )

    @cached_property
    def cred(self) -> Credentials:
        return Credentials.from_service_account_file(VarEnv.PATH_TO_CRED.value)

    @cached_property
    def client(self) -> Client:
        return Client(credentials=self.cred)

    @property
    def loadjobconfig_insert(self) -> LoadJobConfig:
        return LoadJobConfig(
            write_disposition=WriteDisposition.WRITE_APPEND,
            source_format=SourceFormat.CSV,
            skip_leading_rows=1,
        )

    def insert(self, csv: bytes, table: type) -> None:
        with BytesIO(csv) as f:
            df = read_csv(f)
        df.columns = ["timestamp", "timezone", "fuel", "gen_mw"]
        df["timestamp"] = to_datetime(df["timestamp"])
        with BytesIO() as f:
            df.to_csv(f, index=False)
            f.seek(0)
            self.client.load_table_from_file(
                f,
                f"{VarEnv.PROJECT_BIGQUERY.value}.{VarEnv.DATASET_BIGQUERY.value}.{table.__tablename__}",
                job_config=self.loadjobconfig_insert,
            ).result()


BIGQUERY = BigQuery()
