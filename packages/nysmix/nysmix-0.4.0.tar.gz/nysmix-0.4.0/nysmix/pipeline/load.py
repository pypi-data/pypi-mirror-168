from dataclasses import dataclass
from nysmix.store.base import Store
from nysmix.base import Day, from_name_file_csv
from typing import List
from logging import info
from pathlib import Path
from nysmix.database.base import Database
from sqlalchemy.future.engine import Engine
from nysmix.database.orm import mapper_registry, SnapshotStage, Snapshot
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, cast, Date, insert
from sqlalchemy.sql.functions import max

NAME_TABLE_MAIN: str = "main"
NAME_TABLE_STAGE: str = "stage"


@dataclass
class Load:
    database: Database
    store_csv: Store
    num_days: int

    def create_tables(self) -> None:
        info("creating tables")
        mapper_registry.metadata.create_all(self.database.engine)

    @property
    def days_next(self) -> List[Day]:
        info("finding next csvs to load")
        days_next: List[Day] = []
        names_files_csv = [
            name_file
            for name_file in self.store_csv.names_files
            if Path(name_file).suffix == ".csv"
        ]
        if len(names_files_csv) == 0:
            info("no csvs found")
            return []
        days = [from_name_file_csv(name_file_csv) for name_file_csv in names_files_csv]
        with Session(self.database.engine) as session:
            num_records_snapshot = session.query(Snapshot).count()
        info(f"num records in Snapshot table: {num_records_snapshot}")
        if num_records_snapshot == 0:
            info("no records in Snapshot table, adding all csvs")
            days_next = days
        else:
            with Session(self.database.engine) as session:
                stmt_datetime_max = select(max(Snapshot.timestamp))
                res_datetime_max = session.execute(stmt_datetime_max)
                datetime_max = list(res_datetime_max)[0][0]
            day_max = Day(
                year=datetime_max.year, month=datetime_max.month, day=datetime_max.day
            )
            days_next = [day for day in days if day >= day_max]

        return days_next

    def stage_next(self) -> None:
        info(f"staging next days for {self}")
        days_next = sorted(self.days_next)[:self.num_days] # need to limit to avoid hitting quotas
        info(f"days next to add: {days_next}")
        with Session(self.database.engine) as session:
            num_rows_deleted = session.execute(delete(SnapshotStage).where(True))
        info(f"Rows deleted from stage: {num_rows_deleted}")
        for day in days_next:
            info(f"adding {day} to stage")
            day.set_store(self.store_csv)
            self.database.insert(csv=day.bytes_csv_from_store, table=SnapshotStage)

    def add_next(self) -> None:
        info(f"loading next days for {self}")
        self.create_tables()
        self.stage_next()

        with Session(self.database.engine) as session:
            num_records_snapshot_stage = session.query(SnapshotStage).count()
        info(f"num records in Snapshot stage table: {num_records_snapshot_stage}")

        with Session(self.database.engine) as session:
            num_records_snapshot = session.query(Snapshot).count()
        info(f"num records in Snapshot table: {num_records_snapshot}")
        if num_records_snapshot == 0:
            info("no records in Snapshot table, adding all of stage")
            stmt_select = select(
                [
                    SnapshotStage.timestamp,
                    SnapshotStage.timezone,
                    SnapshotStage.fuel,
                    SnapshotStage.gen_mw,
                ]
            )
        else:
            stmt_select = select(
                [
                    SnapshotStage.timestamp,
                    SnapshotStage.timezone,
                    SnapshotStage.fuel,
                    SnapshotStage.gen_mw,
                ]
            ).where(SnapshotStage.timestamp > select(max(Snapshot.timestamp)))

        with Session(self.database.engine) as session:
            stmt_insert = insert(Snapshot).from_select(
                [
                    Snapshot.timestamp,
                    Snapshot.timezone,
                    Snapshot.fuel,
                    Snapshot.gen_mw,
                ],
                stmt_select,
            )
            session.execute(stmt_insert)
            session.commit()

        with Session(self.database.engine) as session:
            num_records_snapshot = session.query(Snapshot).count()
        info(f"new num records in Snapshot table: {num_records_snapshot}")
