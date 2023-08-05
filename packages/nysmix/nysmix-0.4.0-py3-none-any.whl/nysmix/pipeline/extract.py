"""
defining pipelines
"""

from dataclasses import dataclass
from nysmix.store.base import Store
from nysmix.base import Day, DAY_START, from_name_file_csv
from typing import List
from logging import info
from pathlib import Path

@dataclass
class Extract:
    store_zip: Store
    store_csv: Store

    @property
    def days_next(self) -> List[Day]:
        info("finding next csvs to extract")
        days_next: List[Day] = []
        names_files_zip = [
            name_file
            for name_file in self.store_zip.names_files
            if Path(name_file).suffix == ".zip"
        ]
        names_files_csv = [
            name_file
            for name_file in self.store_csv.names_files
            if Path(name_file).suffix == ".csv"
        ]

        if len(names_files_zip) == 0:
            return []

        # add the latest day
        day_latest = (
            from_name_file_csv(max(names_files_csv))
            if len(names_files_csv) > 0
            else DAY_START
        )
        days_next.append(day_latest)
        # add all later days in the same month
        yearmonth_latest = day_latest.yearmonth
        yearmonth_latest.set_store(self.store_zip)
        days_next.extend(
            [
                from_name_file_csv(name_file_csv)
                for name_file_csv in yearmonth_latest.names_files_archived
                if name_file_csv > day_latest.name_file_csv
            ]
        )
        yearmonth = yearmonth_latest.next
        # add all days from later months
        while yearmonth.name_file_zip in names_files_zip:
            yearmonth.set_store(self.store_zip)
            days_next.extend(
                [
                    from_name_file_csv(name_file_csv)
                    for name_file_csv in yearmonth.names_files_archived
                ]
            )
            yearmonth = yearmonth.next
        info(f"next days to pull: {days_next}")
        return days_next

    def add_next(self) -> None:
        for day in self.days_next:
            day.set_store(self.store_csv)
            day.store_extract_from_zip(store_zip=self.store_zip)