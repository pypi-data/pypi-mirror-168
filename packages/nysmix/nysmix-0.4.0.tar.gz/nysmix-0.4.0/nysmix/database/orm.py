"""
database orm
"""

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, Date, case
from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql.elements import Case
from nysmix.concepts import SimpleFuel

mapper_registry = registry()

# @mapper_registry.mapped
# class Fuel:
#     __tablename__ = "fuel"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(20))


@mapper_registry.mapped
class SnapshotStage:
    __tablename__ = "snapshot_stage"
    __schema__ = "nysmix"

    # id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    timezone = Column(String(3), primary_key=True)
    # fuel_id = Column(Integer, ForeignKey("fuel.id")) # following https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    fuel = Column(String(40), primary_key=True)  # relationship("Fuel")
    gen_mw = Column(Float)


@mapper_registry.mapped
class Snapshot:
    __tablename__ = "snapshot"
    __schema__ = "nysmix"

    # id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    timezone = Column(String(3), primary_key=True)
    # fuel_id = Column(Integer, ForeignKey("fuel.id")) # following https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    fuel = Column(String(40), primary_key=True)  # relationship("Fuel")
    gen_mw = Column(Float)