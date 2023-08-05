"""
Sarmat.

Описание поведения объектов.

Подвижной состав.
"""
from datetime import date
from typing import List

from sarmat.core.constants import CrewType, PermitType, VehicleType
from sarmat.core.context.models import CrewModel, VehicleModel

from .bases import BhCompare
from .sarmat import BhPerson
from ..exceptions import IncomparableTypesError


class BhVehicle(BhCompare):
    """Методы сравнения объекта 'Транспортное средство'"""

    vehicle_type: VehicleType
    vehicle_name: str
    state_number: str
    seats: int
    stand: int
    capacity: int

    def __eq__(self, other):
        """Сравнение двух транспортных средств"""
        super().__eq__(other)
        condition1 = self.vehicle_type == other.vehicle_type and self.vehicle_name == other.vehicle_name
        condition2 = self.state_number == other.state_number
        return condition1 and condition2

    def __ne__(self, other):
        """Проверка на неравенство двух транспортных средств"""
        super().__ne__(other)
        return any(
            [
                self.state_number != other.state_number,
                self.vehicle_type != other.vehicle_type,
                self.vehicle_name != other.vehicle_name,
            ],
        )

    def __lt__(self, other):
        """Сравнение транспортных средств по вместимости.
           Количество посадочных мест, количество мест стоя, вместимость багажного отделения
        """
        super().__lt__(other)
        return (self.seats, self.stand, self.capacity) < (other.seats, other.stand, other.capacity)

    def __gt__(self, other):
        """Сравнение транспортных средств по вместимости.
           Количество посадочных мест, количество мест стоя, вместимость багажного отделения
        """
        super().__gt__(other)
        return (self.seats, self.stand, self.capacity) > (other.seats, other.stand, other.capacity)

    def __le__(self, other):
        """Сравнение транспортных средств по вместимости.
           Количество посадочных мест, количество мест стоя, вместимость багажного отделения
        """
        super().__le__(other)
        return (self.seats, self.stand, self.capacity) <= (other.seats, other.stand, other.capacity)

    def __ge__(self, other):
        """Сравнение транспортных средств по вместимости.
           Количество посадочных мест, количество мест стоя, вместимость багажного отделения
        """
        super().__ge__(other)
        return (self.seats, self.stand, self.capacity) >= (other.seats, other.stand, other.capacity)

    def __contains__(self, item):
        """Проверка на вхождение для транспортного средства не имеет смысла"""
        raise IncomparableTypesError('Проверка на вхождение для транспортного средства не производится')

    def _compare_classes(self, other):
        return isinstance(other, BhVehicle)


class BhCrew(BhPerson):
    """Методы сравнения сведений об экипаже"""

    crew_type: CrewType

    def __eq__(self, other):
        person_compare = super().__eq__(other)
        return person_compare and self.crew_type == other.crew_type

    def __ne__(self, other):
        person_compare = super().__ne__(other)
        return person_compare or self.crew_type != other.crew_type

    def _compare_classes(self, other):
        return isinstance(other, BhCrew)


class BhPermit(BhCompare):
    """Методы сравнения путевых листов"""
    compare_error_message = 'Путевые листы сравнению не подлежат'

    number: str
    depart_date: date
    permit_type: PermitType
    crew: List[CrewModel]
    vehicle: List[VehicleModel]

    def __eq__(self, other):
        """Сравнение путевых листов"""
        super().__eq__(other)
        return all(
            [
                self.number == other.number,
                self.permit_type == other.permit_type,
                self.depart_date == other.depart_date,
            ],
        )

    def __ne__(self, other):
        """Проверка на неравенство путевых листов"""
        super().__ne__(other)
        return any(
            [
                self.number != other.number,
                self.permit_type != other.permit_type,
                self.depart_date != other.depart_date,
            ],
        )

    def __lt__(self, other):
        """Проверка сравнение не имеет смысла для путевых листов"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, other):
        """Проверка сравнение не имеет смысла для путевых листов"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка сравнение не имеет смысла для путевых листов"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка сравнение не имеет смысла для путевых листов"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на вхождение транспортного средства или водителя в состав экипажа"""

        if isinstance(item, BhCrew):
            if self.crew is None:
                return False
            return item in self.crew

        if isinstance(item, BhVehicle):
            if self.vehicle is None:
                return False
            return item in self.vehicle

        raise IncomparableTypesError(f'Тип {item.__class__} не предназначен для проверки на вхождение в состав экипажа')

    def _compare_classes(self, other):
        return isinstance(other, BhPermit)
