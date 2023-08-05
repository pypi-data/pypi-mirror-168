"""
Sarmat.

Описание сущностей.

Модели для описания географических объектов.
"""
from dataclasses import dataclass
from typing import Optional

from sarmat.core.constants import LocationType, SettlementType
from sarmat.core.verification import DestinationPointVerifier, GeoVerifier

from .sarmat_models import BaseIdModel
from ..containers import (
    DestinationPointContainer,
    DirectionContainer,
    GeoContainer,
    RoadNameContainer,
)


@dataclass
class GeoModel(BaseIdModel):
    """Модель географического справочника"""

    name: str                               # наименование
    location_type: LocationType             # тип образования
    latin_name: str = ""                    # латинское название
    mapping_data: Optional[dict] = None     # данные геолокации
    tags: Optional[dict] = None             # тэги
    parent: Optional['GeoModel'] = None     # родительский объект

    @classmethod
    def from_container(cls, geo_container: GeoContainer) -> 'GeoModel':     # type: ignore[override]
        GeoVerifier().verify(geo_container)

        return cls(
            id=geo_container.id or 0,
            name=geo_container.name,
            latin_name=geo_container.latin_name,
            location_type=geo_container.location_type,
            mapping_data=geo_container.mapping_data,
            tags=geo_container.tags,
            parent=GeoModel.from_container(geo_container.parent) if geo_container.parent else None,
        )

    def raw(self) -> GeoContainer:      # type: ignore[override]
        return GeoContainer(
            id=self.id,
            name=self.name,
            latin_name=self.latin_name,
            location_type=self.location_type,
            mapping_data=self.mapping_data,
            tags=self.tags,
            parent=self.parent.raw() if self.parent else None,
        )


@dataclass
class DestinationPointModel(BaseIdModel):
    """Модель для описания пунктов назначения"""

    name: str                       # наименование
    state: GeoModel                 # территориальное образование
    point_type: SettlementType      # тип поселения

    @classmethod
    def from_container(cls, container: DestinationPointContainer) -> 'DestinationPointModel':   # type: ignore[override]
        DestinationPointVerifier().verify(container)

        return cls(
            id=container.id or 0,
            name=container.name,
            state=GeoModel.from_container(container.state),
            point_type=container.point_type,
        )

    def raw(self) -> DestinationPointContainer:     # type: ignore[override]
        return DestinationPointContainer(
            id=self.id,
            name=self.name,
            state=self.state.raw(),
            point_type=self.point_type,
        )


@dataclass
class DirectionModel(BaseIdModel):
    """Модель для описания направления"""

    name: str           # наименование
    cypher: str = ""    # шифр (системное имя)

    @classmethod
    def from_container(cls, container: DirectionContainer) -> 'DirectionModel':     # type: ignore[override]
        return cls(
            id=container.id or 0,
            name=container.name,
            cypher=container.cypher,
        )

    def raw(self) -> DirectionContainer:    # type: ignore[override]
        return DirectionContainer(
            id=self.id,
            name=self.name,
            cypher=self.cypher,
        )


@dataclass
class RoadNameModel(BaseIdModel):
    """Модель для описания дороги"""

    cypher: str
    name: str = ''

    @classmethod
    def from_container(cls, container: RoadNameContainer) -> 'RoadNameModel':       # type: ignore[override]
        return cls(
            id=container.id or 0,
            name=container.name,
            cypher=container.cypher,
        )

    def raw(self) -> RoadNameContainer:    # type: ignore[override]
        return RoadNameContainer(
            id=self.id,
            name=self.name,
            cypher=self.cypher,
        )
