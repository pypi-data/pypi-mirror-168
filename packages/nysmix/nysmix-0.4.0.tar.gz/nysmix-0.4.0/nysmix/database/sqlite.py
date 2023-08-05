from .base import Database
from dataclasses import dataclass
from pandas import read_csv, to_datetime
from functools import cached_property
from sqlalchemy import create_engine
from sqlalchemy.future.engine import Engine
from io import BytesIO
from pathlib import Path

@dataclass
class Sqlite(Database):

    def insert(self, csv: bytes, table: type) -> None:
        with BytesIO(csv) as f:
            df = read_csv(f)
        df.columns = ["timestamp", "timezone", "fuel", "gen_mw"]
        df["timestamp"] = to_datetime(df["timestamp"])
        df.to_sql(table.__tablename__, self.engine, if_exists="append", index=False)

@dataclass
class File(Sqlite):
    """sqlite as file"""
    path: Path

    @property
    def engine(self) -> Engine:
        return create_engine(f"sqlite:///{self.path}", echo=True, future=True)


@dataclass
class Memory(Sqlite):
    """sqlite in memory"""

    @cached_property
    def engine(self) -> Engine:
        return create_engine("sqlite://", echo=True, future=True)

MEMORY = Memory()
