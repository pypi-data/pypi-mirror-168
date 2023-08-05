"""general configuration
"""

from enum import Enum, auto
from typing import NamedTuple, Optional
from os import getenv

YEAR_START = 2015
MONTH_START = 12
DAY_START = 9


class ParamsVarEnv(NamedTuple):
    key: str

    @property
    def value(self) -> Optional[str]:
        return getenv(self.key)


class VarEnv(ParamsVarEnv, Enum):
    TYPE_STORE = ParamsVarEnv(key="NYSMIX_STORE")
    FOLDER_ZIP = ParamsVarEnv(key="NYSMIX_FOLDER_ZIP")
    FOLDER_CSV = ParamsVarEnv(key="NYSMIX_FOLDER_CSV")
    TYPE_DB = ParamsVarEnv(key="NYSMIX_DB")