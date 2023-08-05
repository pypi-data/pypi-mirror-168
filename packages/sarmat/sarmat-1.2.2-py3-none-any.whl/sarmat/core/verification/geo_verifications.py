"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.

Веификация гео объектов.
"""
from typing import List, Dict

from sarmat.core.exceptions import SarmatException
from sarmat.core.constants import ErrorCode, LocationType
from sarmat.core.context.containers import GeoContainer

from .base_verifications import VerifyOnEmptyValues


class GeoVerifier(VerifyOnEmptyValues):
    """Класс верификации гео объектов"""

    attributes: List[str] = ['name', 'location_type']

    # NOTE: Проверка на правильность построения иерархии.
    #       У страны не может быть родительских записей.
    #       Для республик, областей и районов в качестве родителя может выступать только страна.
    possible_parent_types: Dict[LocationType, List[LocationType]] = {
        LocationType.COUNTRY: [],
        LocationType.DISTRICT: [LocationType.COUNTRY],
        LocationType.REGION: [LocationType.COUNTRY],
        LocationType.PROVINCE: [LocationType.COUNTRY],
        LocationType.AREA: [LocationType.COUNTRY, LocationType.DISTRICT, LocationType.PROVINCE],
    }

    def verify(self, subject: GeoContainer) -> None:    # type: ignore[override]
        super().verify(subject)

        if subject.parent:
            parent_location_types: List[LocationType] = self.possible_parent_types[subject.location_type]
            if subject.parent.location_type not in parent_location_types:
                raise SarmatException(
                    f'Wrong parent type of location: {subject.parent.location_type}',
                    err_code=ErrorCode.WRONG_VALUE,
                )

            if subject.parent.id == subject.id:
                raise SarmatException(
                    "Geo object can't be a parent for themself",
                    err_code=ErrorCode.WRONG_VALUE,
                )


class DestinationPointVerifier(VerifyOnEmptyValues):
    """Класс верификации пунктов назначения"""

    attributes = ['name', 'state', 'point_type']


class DirectionVerifier(VerifyOnEmptyValues):
    """Класс верификации направлений"""

    attributes = ['name']


class RoadNameVerifier(VerifyOnEmptyValues):
    """Класс верификации наименований дорог"""

    attributes = ['cypher']
