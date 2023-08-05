"""
defining pipelines
"""

from dataclasses import dataclass
from nysmix.store.base import Store
from nysmix.base import YearMonth, YEARMONTH_START
from logging import info

@dataclass
class Pull:
    """
    keep the data files (zips) up to date
    """

    store: Store

    @property
    def yearmonth_next(self) -> YearMonth:
        info("finding next month to pull")
        names_files = self.store.names_files
        yearmonth_next = YEARMONTH_START
        while (
            yearmonth_next.name_file_zip in names_files and not yearmonth_next.next.is_future
        ):
            yearmonth_next = yearmonth_next.next
        info(f"next month to pull: {yearmonth_next}")
        return yearmonth_next

    def add_next(self) -> None:
        yearmonth_next = self.yearmonth_next
        yearmonth_next.set_store(self.store)
        yearmonth_next.store_zip_from_site()
