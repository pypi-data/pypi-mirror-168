from dataclasses import dataclass
from datetime import datetime
from .yearmonth import TZ, Year
from typing import List, Optional
from nysmix.config.base import YEAR_START
from joblib import Memory
from functools import cached_property
from pandas import DataFrame, concat
from logging import info


@dataclass
class Summary:
    memory: Memory

    @cached_property
    def years(self) -> List[Year]:
        now = datetime.now(TZ)
        return [
            Year(memory=self.memory, year=year)
            for year in range(YEAR_START, now.year + 1)
        ]

    @cached_property
    def last_modified(self) -> str:
        return self.years[-1].last_modified

    @cached_property
    def df(self) -> DataFrame:
        print("grabbing summary")
        return self.memory.cache(summarize)(
            summary=self, last_modified=self.last_modified
        )


def summarize(summary: Summary, last_modified: Optional[str] = None) -> DataFrame:
    return concat([year.summary for year in summary.years])
