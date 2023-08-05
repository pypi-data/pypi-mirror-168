"""
Sarmat.

Описание сущностей.

Контейнеры для описания географических объектов.
"""
from typing import Optional

from sarmat.core.constants import LocationType, SettlementType
from .sarmat_containers import BaseIdSarmatContainer


class GeoContainer(BaseIdSarmatContainer):
    """Контейнер для географического справочника"""

    name: str                                   # наименование
    location_type: LocationType                 # тип образования
    latin_name: str = ''                        # латинское название
    mapping_data: Optional[dict] = None         # данные геолокации
    tags: Optional[dict] = None                 # тэги
    parent: Optional['GeoContainer'] = None     # родительский объект


GeoContainer.update_forward_refs()


class DestinationPointContainer(BaseIdSarmatContainer):
    """Контейнер для описания пунктов назначения"""

    name: str                       # наименование
    state: GeoContainer             # территориальное образование
    point_type: SettlementType      # тип поселения


class DirectionContainer(BaseIdSarmatContainer):
    """Контейнер для описания направлений"""

    name: str           # наименование
    cypher: str = ''    # шифр (системное имя)


class RoadNameContainer(BaseIdSarmatContainer):
    """Контейнер для описания дороги"""

    cypher: str
    name: str = ''
