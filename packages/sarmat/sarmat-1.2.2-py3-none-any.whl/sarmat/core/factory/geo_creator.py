"""
Sarmat.

Ядро пакета.

Фабрика классов.

Класс для создания географических объектов.
"""
from sarmat.core.context.containers import (
    DestinationPointContainer,
    DirectionContainer,
    GeoContainer,
    RoadNameContainer,
)
from sarmat.core.context.models import (
    DestinationPointModel,
    DirectionModel,
    GeoModel,
    RoadNameModel,
)

from .base_creator import (
    DestinationPointCreatorMixin,
    DirectionCreatorMixin,
    RoadNameCreatorMixin,
    SarmatCreator,
)


class SarmatGeoCreator(DestinationPointCreatorMixin, DirectionCreatorMixin, RoadNameCreatorMixin, SarmatCreator):
    """Фабрика для создания гео объектов."""

    def create_direction(self, tag: str, container: DirectionContainer) -> DirectionModel:
        """Создание объекта 'Направления'"""
        direction_model = DirectionModel.from_container(container)
        return self.make_direction_from_model(tag, direction_model)

    def create_destination_point(self, tag: str, container: DestinationPointContainer) -> DestinationPointModel:
        """Создание объекта 'Пункт назначения'"""
        destination_point_model = DestinationPointModel.from_container(container)
        return self.make_destination_point_from_model(tag, destination_point_model)

    def create_geo_object(self, tag: str, container: GeoContainer) -> GeoModel:
        """Создание объекта 'Географическая точка'"""
        geo_model = GeoModel.from_container(container)
        return self.make_geo_object_from_model(tag, geo_model)

    def create_road_name(self, tag: str, container: RoadNameContainer) -> RoadNameModel:
        """Создание объекта 'Описание дороги'"""
        road_name_model = RoadNameModel.from_container(container)
        return self.make_road_name_from_model(tag, road_name_model)
