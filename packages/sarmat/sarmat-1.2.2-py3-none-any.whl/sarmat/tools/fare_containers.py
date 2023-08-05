"""
Sarmat.

Описание сущностей.

Объекты для расчета стоимости.
"""
from dataclasses import dataclass, field
from decimal import Decimal

from sarmat.core.behavior import BhRoute
from sarmat.core.context.sarmat import BaseSarmatStructure


@dataclass
class FareContainer(BaseSarmatStructure):
    base_passenger_price: Decimal
    base_baggage_price: Decimal
    permanent_passenger_price: Decimal = Decimal(0)
    volatile_passenger_price: Decimal = Decimal(0)
    permanent_baggage_price: Decimal = Decimal(0)
    volatile_baggage_price: Decimal = Decimal(0)
    custom_passenger_price: dict = None
    custom_baggage_price: dict = None

    def _check_attribute(self, item, item_type):
        if item is not None:
            if not isinstance(item, item_type):
                item = item_type(item)

        return item

    def __post_init__(self):
        self.base_passenger_price = self._check_attribute(self.base_passenger_price, Decimal)
        self.base_baggage_price = self._check_attribute(self.base_baggage_price, Decimal)
        self.permanent_passenger_price = self._check_attribute(self.permanent_passenger_price, Decimal)
        self.volatile_passenger_price = self._check_attribute(self.volatile_passenger_price, Decimal)
        self.permanent_baggage_price = self._check_attribute(self.permanent_baggage_price, Decimal)
        self.volatile_baggage_price = self._check_attribute(self.volatile_baggage_price, Decimal)


@dataclass
class FareArguments(BaseSarmatStructure):
    route: BhRoute
    point_from: int
    point_to: int
    other_arguments: dict
    base_pas_price: Decimal = field(default_factory=Decimal)
    base_bag_price: Decimal = field(default_factory=Decimal)
    prm_pas_price: Decimal = field(default_factory=Decimal)
    prm_bag_price: Decimal = field(default_factory=Decimal)
    vlt_pas_price: Decimal = field(default_factory=Decimal)
    vlt_bag_price: Decimal = field(default_factory=Decimal)
    customer_pas_price: dict = None
    customer_bag_price: dict = None
