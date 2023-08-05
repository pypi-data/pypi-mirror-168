"""
general concepts
"""

from enum import Enum
from typing import NamedTuple, Set, Tuple
from sqlalchemy.orm.attributes import InstrumentedAttribute


class ParamsSimpleFuel(NamedTuple):
    label: str
    values: Set[str]

    def entry_case(self, field: InstrumentedAttribute) -> Tuple:
        return (field.in_(self.values), self.label)

class SimpleFuel(ParamsSimpleFuel, Enum):
    FOSSIL_FUEL = ParamsSimpleFuel(
        label="Fossil fuel", values={"Natural Gas", "Dual Fuel", "Other Fossil Fuels"}
    )
    RENEWABLE = ParamsSimpleFuel(
        label="Renewable", values={"Hydro", "Wind", "Other Renewables"}
    )
    NUCLEAR = ParamsSimpleFuel(label="Nuclear", values={"Nuclear"})
