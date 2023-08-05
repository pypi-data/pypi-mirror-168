"""
Sarmat.

Описание действий с объектами.

Классы для работы с объектами маршрутной сети.
"""
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import List, Optional

from sarmat.core.constants import JourneyType, StationType
from sarmat.core.constants.sarmat_constants import MAX_SUBURBAN_ROUTE_LENGTH
from sarmat.core.context.containers import JourneyBunchItemContainer, JourneyContainer, RouteContainer
from sarmat.core.context.models import DirectionModel, JourneyBunchItemModel, StationModel, RouteItemModel
from sarmat.core.exceptions import WrongValueError
from sarmat.tools.geo_tools import get_geo_objects_projection

from .bases import ActionMixin


@dataclass
class RouteMetrics:
    point: str
    station: str
    arrive: datetime
    stop: int
    depart: Optional[datetime]
    length: float
    total_length: int
    spent_time: int


class AStationMixin(ActionMixin):
    """Действия с пунктами назначения"""

    name: str
    station_type: StationType
    point: object
    address: str

    def copy(self):
        return self.__class__(
            id=0,
            station_type=self.station_type,
            name=f"Копия {self.name}",
            point=self.point,
            address=self.address,
        )


class RouteMixin:
    """Миксин для использования при работе с маршрутами и рейсами"""

    id: int
    number: str
    first_station: StationModel
    structure: List[RouteItemModel]
    name: str
    direction: Optional[List[DirectionModel]]
    comments: str

    def get_real_journey_type(self) -> JourneyType:
        """Метод возвращает вычисленный тип рейса"""
        route_length = 0.

        region_changed, country_changed = False, False
        _, base_region, base_country = get_geo_objects_projection(self.first_station.point.state)
        for route_item in self.structure:
            item = route_item.station.point if route_item.station else route_item.point
            if not item:
                raise WrongValueError(
                    'Route item must have station or destination point',
                )

            _, item_region, item_country = get_geo_objects_projection(item.state)

            if base_region and item_region:
                region_changed = base_region != item_region
            if base_country and item_country:
                country_changed = base_country != item_country

            if region_changed or country_changed:
                break
            route_length += route_item.length_from_last_km

        if country_changed:
            journey_type = JourneyType.INTERNATIONAL
        elif region_changed:
            journey_type = JourneyType.INTER_REGIONAL
        elif route_length >= MAX_SUBURBAN_ROUTE_LENGTH:
            journey_type = JourneyType.LONG_DISTANCE
        else:
            journey_type = JourneyType.SUBURBAN

        return journey_type

    def get_route_metrics(self):
        """Метрика состава маршрута"""
        now = self.get_base_depart_date_time()
        route_length = 0
        spent_time_in_minutes = 0

        for item in self.structure[:-1]:
            spent_time_in_minutes += item.travel_time_min
            spent_time_in_minutes += (item.stop_time_min or 0)
            now += timedelta(minutes=item.travel_time_min)
            depart_delta = timedelta(minutes=item.stop_time_min or 0)
            route_length += item.length_from_last_km
            if item.station:
                point_name, station_name = item.station.point.name, item.station.name
            else:
                point_name, station_name = item.point.name, ''

            yield RouteMetrics(
                point=point_name,
                station=station_name,
                arrive=now,
                stop=item.stop_time_min,
                depart=(now + depart_delta),
                length=item.length_from_last_km,
                total_length=route_length,
                spent_time=spent_time_in_minutes,
            )
            now += depart_delta

        last_item = self.structure[-1]
        route_length += last_item.length_from_last_km
        spent_time_in_minutes += last_item.travel_time_min
        now += timedelta(minutes=last_item.travel_time_min)

        if last_item.station:
            point_name, station_name = last_item.station.point.name, last_item.station.name
        else:
            point_name, station_name = last_item.point.name, ''

        yield RouteMetrics(
            point=point_name,
            station=station_name,
            arrive=now,
            stop=0,
            depart=None,
            length=last_item.length_from_last_km,
            total_length=route_length,
            spent_time=spent_time_in_minutes,
        )

    def get_base_depart_date_time(self) -> datetime:
        today = date.today()
        return datetime(today.year, today.month, today.day, 0, 0)


class ARouteMixin(RouteMixin, ActionMixin):
    """Действия с маршрутом"""

    def copy(self):
        return self.__class__(
            id=0,
            name=f'Копия {self.name}',
            first_station=self.first_station,
            structure=deepcopy(self.structure),
            direction=deepcopy(self.direction) if self.direction else None,
            comments=self.comments,
            number=0,
            literal='',
        )

    def create_journey_structure(self, departure_time: time) -> JourneyContainer:
        return JourneyContainer(
            id=0,
            number=self.number,
            name=self.name,
            first_station=self.first_station.raw(),
            structure=[item.raw() for item in self.structure],
            journey_type=self.get_real_journey_type(),
            departure_time=departure_time,
            bunch=None,
            literal="",
            is_chartered=False,
            need_control=False,
            season_begin=None,
            season_end=None,
            direction=[item.raw() for item in self.direction] if self.direction else None,
            comments=f'Создан из маршрута {self.number} ({self.id})',
        )

    def get_route_info(self) -> dict:
        """Информация о маршруте"""
        return {
            'attributes': self.as_dict,                                           # type: ignore
            'real_journey_type': self.get_real_journey_type(),
            'route_structure': [item.as_dict for item in self.structure],
            'metrics': self.get_route_metrics(),
        }


class AJourneyMixin(RouteMixin, ActionMixin):
    """Действия с рейсами"""

    journey_type: JourneyType
    departure_time: time
    bunch: object
    is_chartered: bool
    need_control: bool
    season_begin: Optional[date]
    season_end: Optional[date]

    def copy(self):
        return self.__class__(
            id=0,
            number=0,
            name=f"Копия {self.name}",
            first_station=self.first_station,
            structure=self.structure,
            journey_type=self.journey_type,
            departure_time=self.departure_time,
            literal="",
            is_chartered=self.is_chartered,
            need_control=self.need_control,
            season_begin=self.season_begin,
            season_end=self.season_end,
            direction=self.direction,
            comments=f'Создан из рейса {self.number} ({self.id})',
        )

    def get_base_depart_date_time(self) -> datetime:
        today = date.today()
        return datetime(today.year, today.month, today.day, self.departure_time.hour, self.departure_time.minute)

    def get_journey_info(self) -> dict:
        """Информация о рейсе"""
        return {
            'attributes': self.as_dict,                                       # type: ignore
            'real_journey_type': self.get_real_journey_type(),
            'route_structure': [item.as_dict for item in self.structure],
            'metrics': self.get_route_metrics(),
        }

    def create_route_structure(self) -> RouteContainer:
        return RouteContainer(
            id=0,
            name=self.name,
            first_station=self.first_station.raw(),
            structure=[item.raw() for item in self.structure],
            direction=[item.raw() for item in self.direction] if self.direction else None,
            comments=f'Создан из рейса {self.number} ({self.id})',
            number=self.number,
            literal='',
        )


class AJourneyBunchMixin(ActionMixin):
    """Действия со связкой рейсов"""

    controller: object
    permission_tag: str
    journeys: List[JourneyBunchItemModel]

    def add_journey_bunch_item(self, bunch_item: JourneyBunchItemModel) -> None:

        if bunch_item in self.journeys:
            raise WrongValueError('Item already in bunch')

        if bunch_item.journey in [item.journey for item in self.journeys]:
            raise WrongValueError('Journey already in bunch')

        self.journeys.append(bunch_item)

    def add_journey_into_bunch(self, journey: JourneyContainer, stop_interval: int = 0) -> None:
        new_bunch_item = self.controller.create_journey_bunch_item(     # type: ignore
            self.permission_tag,
            JourneyBunchItemContainer(
                journey=journey,
                stop_interval=stop_interval,
            ),
        )
        self.add_journey_bunch_item(new_bunch_item)

    def remove_journey_bunch_item(self, bunch_item_id: int) -> None:
        if self.journeys:
            for idx, bunch_item in enumerate(self.journeys):
                if bunch_item.id == bunch_item_id:
                    self.journeys.remove(self.journeys[idx])
                    break
            else:
                raise WrongValueError(
                    f'Journey bunch item {bunch_item_id}) is not in bunch',
                )
        else:
            raise WrongValueError("Journey bunch is empty")

    def get_finish_date_time(self, date_from: datetime) -> datetime:
        for item in self.journeys:
            journey = self.controller.create_journey(self.permission_tag, item.journey.raw())   # type: ignore
            route_metrics = list(journey.get_journey_info()["metrics"])
            journey_spent_time = route_metrics[-1].spent_time
            date_from += timedelta(minutes=journey_spent_time)

            if item.stop_interval:
                date_from += timedelta(hours=item.stop_interval)

        return date_from
