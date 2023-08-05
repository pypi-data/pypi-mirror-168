"""
Sarmat.

Описание поведения объектов.

Объекты геолокации.
"""
from sarmat.core.constants import LocationType, SettlementType
from sarmat.core.exceptions import IncomparableTypesError

from .bases import BhCompare


class BhDirection(BhCompare):
    """Базовое поведение объекта 'Направления'"""
    compare_error_message = 'Направления сравнению не подлежат'
    contains_error_message = 'Направления проверке на вхождение не подлежат'

    name: str

    def __eq__(self, other):
        """Сравнение на равенство направлений"""
        super().__eq__(other)
        return self.name == other.name

    def __ne__(self, other):
        """Проверка на неравенство направлений"""
        super().__ne__(other)
        return self.name != other.name

    def __lt__(self, item):
        """Проверка сравнение не имеет смысла для направлений"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка сравнение не имеет смысла для направлений"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, item):
        """Проверка сравнение не имеет смысла для направлений"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, item):
        """Проверка сравнение не имеет смысла для направлений"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на вхождение не имеет смысла для направлений"""
        raise IncomparableTypesError(self.contains_error_message)

    def _compare_classes(self, other):
        return isinstance(other, BhDirection)


class BhRoadName(BhDirection):
    """Методы сравнения объекта Дорога"""
    compare_error_message = 'Дороги сравнению не подлежат'
    contains_error_message = 'Дороги проверке на вхождение не подлежат'

    def _compare_classes(self, other):
        return isinstance(other, BhRoadName)


class BhGeo(BhCompare):
    """Методы сравнения объекта 'Географический объект'"""

    name: str
    location_type: LocationType

    def __eq__(self, other):
        """Сравнение на равенство географических объектов.
           Сравнение происходит либо по идентификаторам,
           либо по полям Наименование и Тип объекта.
        """
        super().__eq__(other)
        return self.location_type == other.location_type and self.name == other.name

    def __ne__(self, other):
        """Определение неравенства.
           Сравнение происходит либо по идентификаторам,
           либо по полям Наименование и Тип объекта.
        """
        super().__ne__(other)
        return self.location_type != other.location_type or self.name != other.name

    def __lt__(self, other):
        """Проверка на <.
           Анализируется тип гео. образования.
        """
        super().__lt__(other)
        same_types = [LocationType.DISTRICT, LocationType.REGION]

        if self.location_type in same_types and other.location_type in same_types:
            return False

        # NOTE: крупные территориальные образования имеют меньший индекс
        return self.location_type.value > other.location_type.value

    def __gt__(self, other):
        """Проверка на >.
           Анализируется тип гео. образования.
        """
        super().__gt__(other)
        same_types = [LocationType.DISTRICT, LocationType.REGION]

        if self.location_type in same_types and other.location_type in same_types:
            return False

        # NOTE: крупные территориальные образования имеют меньший индекс
        return self.location_type.value < other.location_type.value

    def __le__(self, other):
        """Проверка на <=.
           Анализируется тип гео. образования.
        """
        super().__le__(other)
        same_types = [LocationType.DISTRICT, LocationType.REGION]

        if self.location_type in same_types and other.location_type in same_types:
            return True

        # NOTE: крупные территориальные образования имеют меньший индекс
        return self.location_type.value >= other.location_type.value

    def __ge__(self, other):
        """Проверка на >=.
           Анализируется тип гео. образования.
        """
        super().__ge__(other)
        same_types = [LocationType.DISTRICT, LocationType.REGION]

        if self.location_type in same_types and other.location_type in same_types:
            return True

        # NOTE: крупные территориальные образования имеют меньший индекс
        return self.location_type.value <= other.location_type.value

    def __contains__(self, item):
        """Проверка на вхождение во множество.
           Для объекта гео локации происходит проверка родителя.
        """
        if not item.parent:
            return False

        return item.parent == self

    def _compare_classes(self, other):
        return isinstance(other, BhGeo)


class BhDestinationPoint(BhCompare):
    """Методы сравнения объекта 'Пункт назначения'"""
    compare_error_message = 'Пункты назначения сравнивать нельзя'

    name: str
    point_type: SettlementType
    state: object

    def __eq__(self, other):
        """Сравнение на равенство пунктов назначения.
           Сравнение происходит либо по идентификаторам,
           либо по полям Наименование и Тип поселения и Территориальное образование.
        """
        super().__eq__(other)
        return self.name == other.name and self.state == other.state and self.point_type == other.point_type

    def __ne__(self, other):
        """Проверка на неравенство пунктов назначения.
           Проверка происходит либо по идентификатору объекта, либо по наименованию, типу поселения
           и территориальному образованию.
        """
        super().__ne__(other)
        return self.name != other.name or self.point_type != other.point_type or self.state != other.state

    def __lt__(self, other):
        """Проверка на строгое неравенство не имеет смысла для пунктов назначения"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, other):
        """Проверка на строгое неравенство не имеет смысла для пунктов назначения"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на нестрогое неравенство не имеет смысла для пунктов назначения"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на нестрогое неравенство не имеет смысла для пунктов назначения"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на вхождение не имеет смысла для пунктов назначения"""
        raise IncomparableTypesError('Пункты назначения проверке на вхождение не подлежат')

    def _compare_classes(self, other):
        return isinstance(other, BhDestinationPoint)
