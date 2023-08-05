"""base classes for nyiso fuel mix data
"""


from dataclasses import dataclass
from datetime import datetime, date, timedelta, timezone
from logging import info
from requests import get
from .store.base import Store
from typing import Optional, Set
from .config.base import YEAR_START, MONTH_START, DAY_START as DAY_START_config
from zipfile import ZipFile
from io import BytesIO

FORMAT_DATE = "%Y%m%d"
TZ = timezone(timedelta(hours=-5))


@dataclass
class Object:
    year: int
    month: int
    day: int = 1

    def __post_init__(self) -> None:
        self.store: Optional[Store] = None

    def set_store(self, store: Store) -> None:
        self.store = store

    @property
    def has_store(self) -> bool:
        has_store = self.store is not None
        if not has_store:
            info("no store set")
        else:
            info(f"store set: {self.store}")
        return has_store

    @property
    def date(self) -> date:
        return date(year=self.year, month=self.month, day=self.day)

    @property
    def str_date(self) -> str:
        return self.date.strftime(FORMAT_DATE)


@dataclass
class YearMonth(Object):
    @property
    def next(self):  # -> YearMonth
        if self.month == 12:
            return YearMonth(
                year=self.year + 1,
                month=1,
            )
        else:
            return YearMonth(
                year=self.year,
                month=self.month + 1,
            )

    @property
    def is_future(self) -> bool:
        return self.year > datetime.now(TZ).year or (
            self.year == datetime.now(TZ).year and self.month > datetime.now(TZ).month
        )

    @property
    def name_file_zip(self) -> str:
        return f"{self.str_date}rtfuelmix_csv.zip"

    @property
    def url(self) -> str:
        return f"http://mis.nyiso.com/public/csv/rtfuelmix/{self.name_file_zip}"

    @property
    def bytes_zip_from_site(self) -> bytes:
        info(f"attempt to download {self.url}")
        with get(self.url) as r:
            content = r.content
        return content

    def store_zip_from_site(self) -> None:
        if self.has_store:
            assert self.store is not None
            self.store.put(content=self.bytes_zip_from_site, name=self.name_file_zip)

    @property
    def bytes_zip_from_store(self) -> bytes:
        if not self.has_store:
            raise Exception(f"no store set for {self}")
        assert self.store is not None
        return self.store.fetch(name=self.name_file_zip)

    @property
    def names_files_archived(self) -> Set[str]:
        with BytesIO(self.bytes_zip_from_store) as f:
            with ZipFile(f) as zf:
                names_files_archived = {info.filename for info in zf.filelist}
        return names_files_archived


YEARMONTH_START = YearMonth(YEAR_START, MONTH_START)


@dataclass(eq=True, order=True)
class Day(Object):
    @property
    def yearmonth(self) -> YearMonth:
        return YearMonth(year=self.year, month=self.month)

    @property
    def name_file_csv(self) -> str:
        return f"{self.str_date}rtfuelmix.csv"

    def bytes_csv_from_zip(self, store_zip: Store) -> bytes:
        yearmonth = self.yearmonth
        yearmonth.set_store(store_zip)
        with BytesIO(yearmonth.bytes_zip_from_store) as f:
            with ZipFile(f) as zf:
                content = zf.read(self.name_file_csv)
        return content

    def store_extract_from_zip(self, store_zip: Store) -> None:
        if self.has_store:
            assert self.store is not None
            self.store.put(content=self.bytes_csv_from_zip(store_zip=store_zip), name=self.name_file_csv)

    @property
    def bytes_csv_from_store(self) -> bytes:
        if not self.has_store:
            raise Exception(f"no store set for {self}")
        assert self.store is not None
        return self.store.fetch(name=self.name_file_csv)


DAY_START = Day(year=YEAR_START, month=MONTH_START, day=DAY_START_config)


def from_name_file_csv(name_file_csv: str) -> Day:
    date_name_file = datetime.strptime(name_file_csv[:8], FORMAT_DATE)
    return Day(
        year=date_name_file.year, month=date_name_file.month, day=date_name_file.day
    )
