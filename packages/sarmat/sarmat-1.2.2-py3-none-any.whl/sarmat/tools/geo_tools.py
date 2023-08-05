"""
Sarmat.

Вспомогательные инструменты.

Инструменты для работы с гео объектами.
"""
from collections import namedtuple
from typing import List, Optional

from sarmat.core.constants import LocationType
from sarmat.core.context.models import GeoModel

GeoProjection = namedtuple("GeoProjection", "area region country")


def get_geo_objects_projection(geo_object: GeoModel) -> GeoProjection:
    """Определение проекции гео объекта и его родительских записей"""

    # NOTE: порядок развертывания проекции следующий: район, регион (республика, край, область), страна
    geo_projection_indices = {
        LocationType.COUNTRY: 2,
        LocationType.DISTRICT: 1,
        LocationType.REGION: 1,
        LocationType.PROVINCE: 1,
        LocationType.AREA: 0,
    }
    geo_projection: List[Optional[int]] = [None, None, None]
    current_object: Optional[GeoModel] = geo_object

    while current_object:
        idx = geo_projection_indices[current_object.location_type]
        geo_projection[idx] = current_object.id
        current_object = current_object.parent

    return GeoProjection(*geo_projection)
