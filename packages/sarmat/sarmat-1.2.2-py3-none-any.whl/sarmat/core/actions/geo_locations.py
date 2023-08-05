"""
Sarmat.

Описание действий с объектами.

Классы для работы с объектами гео локации.
"""
from sarmat.core.constants import LocationType, SettlementType

from .bases import ActionMixin


class AGeoLocationMixin(ActionMixin):
    """Действия с объектами гео локации"""

    name: str
    latin_name: str
    mapping_data: dict
    tags: str
    location_type: LocationType
    parent: object

    def copy(self):
        return self.__class__(
            id=0,
            name=f"Копия {self.name}",
            location_type=self.location_type,
            latin_name=f"Copy of {self.latin_name}" if self.latin_name else "",
            mapping_data=self.mapping_data,
            tags=self.tags,
            parent=self.parent,
        )


class ADestinationPointMixin(ActionMixin):
    """Действия с пунктами назначения"""

    name: str
    state: object
    point_type: SettlementType

    def copy(self):
        return self.__class__(
            id=0,
            name=f"Копия {self.name}",
            state=self.state,
            point_type=self.point_type,
        )
