"""
A year-month of nysmix data
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import cached_property
from io import BytesIO
from logging import info
from typing import Optional
from zipfile import ZipFile

from joblib import Memory
from pandas import DataFrame, read_csv, to_datetime, concat
from requests import get
from nysmix.config.base import DAY_START, YEAR_START, MONTH_START

FORMAT_DATE = "%Y%m%d"
TZ = timezone(timedelta(hours=-5))


@dataclass
class TimeUnit:
    memory: Memory
    year: int
    month: int = 1
    day: int = 1

    @property
    def date(self) -> date:
        return date(year=self.year, month=self.month, day=self.day)

    @property
    def str_date(self) -> str:
        return self.date.strftime(FORMAT_DATE)


@dataclass
class Year(TimeUnit):
    @cached_property
    def months(self):  # -> List[YearMonth]
        return [
            ym
            for ym in [
                YearMonth(memory=self.memory, year=self.year, month=month)
                for month in range(1, 13)
            ]
            if not ym.is_future and not ym.is_before_start
        ]

    @cached_property
    def last_modified(self) -> str:
        print(f"getting last modified for {self}")
        return self.months[-1].last_modified

    @cached_property
    def summary(self) -> DataFrame:
        print(f"grabbing summary for {self}")
        return self.memory.cache(summarize_months)(
            year=self, last_modified=self.last_modified
        )


def summarize_months(year: Year, last_modified: Optional[str] = None) -> DataFrame:
    return concat([ym.summary for ym in year.months])


@dataclass
class YearMonth(TimeUnit):
    @property
    def is_before_start(self) -> bool:
        return self.date < date(year=YEAR_START, month=MONTH_START, day=1)

    @property
    def is_future(self) -> bool:
        now = datetime.now(TZ)
        return self.date > date(year=now.year, month=now.month, day=1)

    @cached_property
    def zip(self) -> bytes:
        return self.memory.cache(get_zip)(
            yearmonth=self, last_modified=self.last_modified
        )

    @property
    def name_file_zip(self) -> str:
        return f"{self.str_date}rtfuelmix_csv.zip"

    @property
    def url(self) -> str:
        return f"http://mis.nyiso.com/public/csv/rtfuelmix/{self.name_file_zip}"

    @cached_property
    def last_modified(self) -> str:
        print(f"getting last modified for {self}")
        with get(self.url) as r:
            headers = r.headers
        return headers["Last-Modified"]

    @cached_property
    def days(self):  # -> List[Day]
        days = []
        current = Day.from_date(memory=self.memory, dt=self.date)
        while current.yearmonth == self:
            if not current.is_before_start and not current.is_future:
                days.append(current)
            current = current.next
        return days

    @cached_property
    def summary(self) -> DataFrame:
        print(f"grabbing summary for {self}")
        return self.memory.cache(summarize_days)(
            yearmonth=self, last_modified=self.last_modified
        )


def get_zip(yearmonth: YearMonth, last_modified: Optional[str] = None) -> bytes:
    info(f"attempt to download {yearmonth.url}")
    with get(yearmonth.url) as r:
        content = r.content
    return content


def summarize_days(
    yearmonth: YearMonth, last_modified: Optional[str] = None
) -> DataFrame:
    return concat([day.summary for day in yearmonth.days])


@dataclass
class Day(TimeUnit):
    @property
    def next(self):  # -> Day
        return Day.from_date(dt=self.date + timedelta(days=1), memory=self.memory)

    @property
    def is_before_start(self) -> bool:
        return self.date < date(year=YEAR_START, month=MONTH_START, day=DAY_START)

    @property
    def is_future(self) -> bool:
        now = datetime.now(TZ)
        return self.date > date(year=now.year, month=now.month, day=now.day)

    @cached_property
    def content(self) -> bytes:
        return self.memory.cache(get_content)(
            day=self, last_modified=self.last_modified
        )

    @cached_property
    def yearmonth(self) -> YearMonth:
        return YearMonth(memory=self.memory, year=self.year, month=self.month)

    @property
    def name_file_csv(self) -> str:
        return f"{self.str_date}rtfuelmix.csv"

    @cached_property
    def df(self) -> DataFrame:
        with BytesIO(self.content) as f:
            df = read_csv(f)
        return df

    @cached_property
    def name_field_gen_mw(self) -> Optional[str]:
        if "Gen MWh" in self.df.columns:
            return "Gen MWh"
        elif "Gen MW" in self.df.columns:
            return "Gen MW"
        else:
            return None

    @cached_property
    def summary(self) -> DataFrame:
        print(f"summarizing {self}")
        return self.memory.cache(summarize)(df=self.df, name_field_gen_mw=self.name_field_gen_mw)

    @cached_property
    def last_modified(self) -> str:
        print(f"getting last modified for {self}")
        return self.yearmonth.last_modified

    @staticmethod
    def from_date(dt: date, memory: Memory):  # -> Day:
        return Day(memory=memory, year=dt.year, month=dt.month, day=dt.day)


def get_content(day: Day, last_modified: Optional[str] = None) -> bytes:
    with BytesIO(day.yearmonth.zip) as f:
        with ZipFile(f) as zf:
            content = zf.read(day.name_file_csv)
    return content


def summarize(df: DataFrame, name_field_gen_mw: Optional[str] = None) -> DataFrame:
    assert name_field_gen_mw is not None
    df["date"] = to_datetime(df["Time Stamp"]).dt.date
    return df.groupby(["date", "Fuel Category"], as_index=False).agg(
        {name_field_gen_mw: "sum"}
    )
