"""base database class"""

from dataclasses import dataclass
from sqlalchemy.future.engine import Engine


@dataclass
class Database:

    @property
    def engine(self) -> Engine:
        pass
    
    def insert(self, csv: bytes, table: type) -> None:
        pass