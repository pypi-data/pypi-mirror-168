"""
Sarmat.

Ядро пакета.

Фабрика классов.

Класс для создания объектов маршрутной сети.
"""
from sarmat.core.actions import (
    AJourneyBunchMixin,
    AJourneyMixin,
    ARouteMixin,
    AStationMixin,
)
from sarmat.core.behavior import (
    BhJourney,
    BhJourneyBunch,
    BhJourneyBunchItem,
    BhRoad,
    BhRoute,
    BhRouteItem,
    BhStation,
)
from sarmat.core.context.containers import (
    JourneyBunchContainer,
    JourneyBunchItemContainer,
    JourneyContainer,
    RoadContainer,
    RouteItemContainer,
    RouteContainer,
    StationContainer,
)
from sarmat.core.context.models import (
    JourneyBunchModel,
    JourneyBunchItemModel,
    JourneyModel,
    RoadModel,
    RouteItemModel,
    RouteModel,
    StationModel,
)

from .base_creator import (
    DestinationPointCreatorMixin,
    DirectionCreatorMixin,
    RoadNameCreatorMixin,
    SarmatCreator,
)


class SarmatTrafficManagementCreator(
    DestinationPointCreatorMixin,
    DirectionCreatorMixin,
    RoadNameCreatorMixin,
    SarmatCreator,
):
    """Фабрика для создания объектов маршрутной сети."""

    def create_route_item(self, tag: str, container: RouteItemContainer) -> RouteItemModel:
        """Создание объекта 'Пункт маршрута'"""
        route_item_model = RouteItemModel.from_container(container)
        return self.make_route_item_from_model(tag, route_item_model)

    def make_route_item_from_model(self, tag: str, model: RouteItemModel) -> RouteItemModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhRouteItem, *classes, RouteItemModel])

        RouteItem = type('RouteItem', parents, {"permission_tag": tag, "controller": self})  # type: ignore

        road, station, point = None, None, None
        if model.road:
            road = self.make_road_from_model(tag, model.road)
        if model.station:
            station = self.make_station_from_model(tag, model.station)
        if model.point:
            point = self.make_destination_point_from_model(tag, model.point)

        return RouteItem(
            **{
                **model.as_dict,
                'road': road,
                'station': station,
                'point': point,
            },
        )

    def create_route(self, tag: str, container: RouteContainer) -> RouteModel:
        """Создание объекта 'Маршрут'"""
        route_model = RouteModel.from_container(container)
        return self.make_route_from_model(tag, route_model)

    def make_route_from_model(self, tag: str, model: RouteModel) -> RouteModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([ARouteMixin, BhRoute, *classes, RouteModel])

        Route = type('Route', parents, {"permission_tag": tag, "controller": self})     # type: ignore

        directions = []
        if model.direction:
            directions = [self.make_direction_from_model(tag, item) for item in model.direction]

        return Route(
            **{
                **model.as_dict,
                'first_station': self.make_station_from_model(tag, model.first_station),
                'structure': [self.make_route_item_from_model(tag, item) for item in model.structure],
                'direction': directions,
            },
        )

    def create_station(self, tag: str, container: StationContainer) -> StationModel:
        """Создание объекта 'Станция'"""
        station_model = StationModel.from_container(container)
        return self.make_station_from_model(tag, station_model)

    def make_station_from_model(self, tag: str, model: StationModel) -> StationModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([AStationMixin, BhStation, *classes, StationModel])

        Station = type('Station', parents, {"permission_tag": tag, "controller": self})     # type: ignore

        return Station(
            **{
                **model.as_dict,
                'point': self.make_destination_point_from_model(tag, model.point),
            },
        )

    def create_journey(self, tag: str, container: JourneyContainer) -> JourneyModel:
        """Создание объекта 'Рейс'"""
        journey_model = JourneyModel.from_container(container)
        return self.make_journey_from_model(tag, journey_model)

    def make_journey_from_model(self, tag: str, model: JourneyModel) -> JourneyModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([AJourneyMixin, BhJourney, *classes, JourneyModel])

        Journey = type('Journey', parents, {"permission_tag": tag, "controller": self})     # type: ignore

        directions = []
        if model.direction:
            directions = [self.make_direction_from_model(tag, item) for item in model.direction]

        return Journey(
            **{
                **model.as_dict,
                'first_station': self.make_station_from_model(tag, model.first_station),
                'structure': [self.make_route_item_from_model(tag, item) for item in model.structure],
                'direction': directions,
            },
        )

    def create_road(self, tag: str, container: RoadContainer) -> RoadModel:
        """Создание объекта 'Дорога'"""
        road_model = RoadModel.from_container(container)
        return self.make_road_from_model(tag, road_model)

    def make_road_from_model(self, tag: str, model: RoadModel) -> RoadModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhRoad, *classes, RoadModel])

        Road = type('Road', parents, {"permission_tag": tag, "controller": self})       # type: ignore

        road_name = None
        if model.road_name:
            road_name = self.make_road_name_from_model(tag, model.road_name)

        return Road(
            **{
                **model.as_dict,
                'start_point': self.make_destination_point_from_model(tag, model.start_point),
                'end_point': self.make_destination_point_from_model(tag, model.end_point),
                'road_name': road_name,
            },
        )

    def create_journey_bunch_item(self, tag: str, container: JourneyBunchItemContainer) -> JourneyBunchItemModel:
        """Создание объекта 'Элемент связки'"""
        bunch_item_model = JourneyBunchItemModel.from_container(container)
        return self.make_journey_bunch_item_from_model(tag, bunch_item_model)

    def make_journey_bunch_item_from_model(self, tag: str, model: JourneyBunchItemModel) -> JourneyBunchItemModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhJourneyBunchItem, *classes, JourneyBunchItemModel])

        JourneyBunchItem = type(
            'JourneyBunchItem', parents, {"permission_tag": tag, "controller": self},   # type: ignore
        )

        return JourneyBunchItem(
            **{
                **model.as_dict,
                'journey': self.make_journey_from_model(tag, model.journey),
            },
        )

    def create_journey_bunch(self, tag: str, container: JourneyBunchContainer) -> JourneyBunchModel:
        """Создание объекта 'Связка рейсов'"""
        bunch_model = JourneyBunchModel.from_container(container)
        return self.make_journey_bunch_from_model(tag, bunch_model)

    def make_journey_bunch_from_model(self, tag: str, model: JourneyBunchModel) -> JourneyBunchModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([AJourneyBunchMixin, BhJourneyBunch, *classes, JourneyBunchModel])

        JourneyBunch = type('JourneyBunch', parents, {"permission_tag": tag, "controller": self})       # type: ignore

        return JourneyBunch(
            **{
                **model.as_dict,
                'journeys': [self.make_journey_bunch_item_from_model(tag, item) for item in model.journeys],
            },
        )
