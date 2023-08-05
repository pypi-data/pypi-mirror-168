"""
helper functions for defining stores
"""

from pathlib import Path
from .base import Database
from .sqlite import File, MEMORY
from .google import BIGQUERY
from enum import Enum, auto
from typing import Optional
from nysmix.config.base import VarEnv
from logging import info
from sqlalchemy import case
from sqlalchemy.sql.elements import Case
from .orm import Snapshot
from nysmix.concepts import SimpleFuel


class TypeDatabase(Enum):
    MEMORY = auto()
    LOCAL = auto()
    GOOGLE = auto()


def get_database(type_database: TypeDatabase) -> Optional[Database]:
    database: Optional[Database] = None
    if type_database == TypeDatabase.MEMORY:
        database = MEMORY
    if type_database == TypeDatabase.LOCAL:
        database = File(Path("./nysmix.db"))
    elif type_database == TypeDatabase.GOOGLE:
        database = BIGQUERY
    else:
        info("database not found")
    info(f"getting database {database}")
    return database


def get_database_from_env() -> Optional[Database]:
    return get_database(
        type_database=TypeDatabase[VarEnv.TYPE_DB.value],
    )


case_simple_fuel: Case = case(
    *[simple_fuel.entry_case(Snapshot.fuel) for simple_fuel in SimpleFuel],
    else_=Snapshot.fuel,
)
