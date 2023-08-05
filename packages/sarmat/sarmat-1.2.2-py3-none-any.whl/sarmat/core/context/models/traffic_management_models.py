"""
Sarmat.

Описание сущностей.

Модели для построения маршрутной сети.
"""
from dataclasses import dataclass
from datetime import time, date
from typing import List, Optional

from sarmat.core.constants import RoadType, StationType, JourneyType
from sarmat.core.verification import (
    JourneyBunchItemVerifier,
    JourneyBunchVerifier,
    JourneyVerifier,
    RouteItemVerifier,
    RouteVerifier,
    StationVerifier,
)

from .geo_models import DirectionModel, DestinationPointModel, RoadNameModel
from .sarmat_models import BaseIdModel
from ..containers import (
    JourneyBunchContainer,
    JourneyBunchItemContainer,
    JourneyContainer,
    RoadContainer,
    RouteContainer,
    RouteItemContainer,
    StationContainer,
)


@dataclass
class StationModel(BaseIdModel):
    """Станции (пункты посадки-высадки пассажиров)"""

    station_type: StationType           # тип станции
    name: str                           # наименование
    point: DestinationPointModel        # ближайший населенный пункт
    address: str = ''                   # почтовый адрес

    @classmethod
    def from_container(cls, container: StationContainer) -> 'StationModel':     # type: ignore[override]
        StationVerifier().verify(container)

        return cls(
            id=container.id,
            station_type=container.station_type,
            name=container.name,
            point=DestinationPointModel.from_container(container.point),
            address=container.address or '',
        )

    def raw(self) -> StationContainer:      # type: ignore[override]
        return StationContainer(
            id=self.id,
            station_type=self.station_type,
            name=self.name,
            point=self.point.raw(),
            address=self.address,
        )


@dataclass
class RoadModel(BaseIdModel):
    """Дороги"""

    start_point: DestinationPointModel          # начало дороги
    end_point: DestinationPointModel            # конец дороги
    direct_travel_time_min: int                 # время прохождения в прямом направлении
    reverse_travel_time_min: int                # время прохождения в обратном направлении
    direct_len_km: float                        # расстояние в прямом направлении
    reverse_len_km: float                       # расстояние в обратном направлении
    road_type: RoadType                         # тип дорожного покрытия
    road_name: Optional[RoadNameModel] = None   # классификация дороги

    @classmethod
    def from_container(cls, container: RoadContainer) -> 'RoadModel':   # type: ignore[override]
        return cls(
            id=container.id,
            start_point=DestinationPointModel.from_container(container.start_point),
            end_point=DestinationPointModel.from_container(container.end_point),
            direct_travel_time_min=container.direct_travel_time_min,
            reverse_travel_time_min=container.reverse_travel_time_min,
            direct_len_km=container.direct_len_km,
            reverse_len_km=container.reverse_len_km,
            road_type=container.road_type,
            road_name=RoadNameModel.from_container(container.road_name) if container.road_name else None,
        )

    def raw(self) -> RoadContainer:     # type: ignore[override]
        return RoadContainer(
            id=self.id,
            start_point=self.start_point.raw(),
            end_point=self.end_point.raw(),
            direct_travel_time_min=self.direct_travel_time_min,
            reverse_travel_time_min=self.reverse_travel_time_min,
            direct_len_km=self.direct_len_km,
            reverse_len_km=self.reverse_len_km,
            road_type=self.road_type,
            road_name=self.road_name.raw() if self.road_name else None,
        )


@dataclass
class RouteItemModel(BaseIdModel):
    """Состав маршрута"""

    length_from_last_km: float                      # расстояние от предыдущего пункта
    travel_time_min: int                            # время движения от предыдущего пункта в минутах
    road: Optional[RoadModel] = None                # дорога
    order: int = 1                                  # порядок следования
    station: Optional[StationModel] = None          # станция
    point: Optional[DestinationPointModel] = None   # ближайший населенный пункт
    stop_time_min: Optional[int] = None             # время стоянки в минутах

    @classmethod
    def from_container(cls, container: RouteItemContainer) -> 'RouteItemModel':     # type: ignore[override]
        RouteItemVerifier().verify(container)

        return cls(
            id=container.id,
            length_from_last_km=container.length_from_last_km,
            travel_time_min=container.travel_time_min,
            road=RoadModel.from_container(container.road) if container.road else None,
            order=container.order,
            station=StationModel.from_container(container.station) if container.station else None,
            point=DestinationPointModel.from_container(container.point) if container.point else None,
            stop_time_min=container.stop_time_min,
        )

    def raw(self) -> RouteItemContainer:    # type: ignore[override]
        return RouteItemContainer(
            id=self.id,
            length_from_last_km=self.length_from_last_km,
            travel_time_min=self.travel_time_min,
            road=self.road.raw() if self.road else None,
            order=self.order,
            station=self.station.raw() if self.station else None,
            point=self.point.raw() if self.point else None,
            stop_time_min=self.stop_time_min,
        )


@dataclass
class RouteModel(BaseIdModel):
    """Описание маршрута"""

    name: str                                           # наименование
    first_station: StationModel                         # станция отправления
    structure: List[RouteItemModel]                     # состав маршрута
    direction: Optional[List[DirectionModel]] = None    # направления
    comments: Optional[str] = None                      # комментарий к маршруту
    number: Optional[int] = None                        # номер маршрута
    literal: str = ''                                   # литера
    is_active: bool = True                              # признак активности маршрута

    @classmethod
    def from_container(cls, container: RouteContainer) -> 'RouteModel':     # type: ignore[override]
        RouteVerifier().verify(container)

        directions = None
        if container.direction:
            directions = [DirectionModel.from_container(item) for item in container.direction]

        return cls(
            id=container.id,
            name=container.name,
            first_station=StationModel.from_container(container.first_station),
            structure=[RouteItemModel.from_container(item) for item in container.structure],
            direction=directions,
            number=container.number,
            literal=container.literal,
            is_active=container.is_active,
            comments=container.comments,
        )

    def raw(self) -> RouteContainer:    # type: ignore[override]
        return RouteContainer(
            id=self.id,
            name=self.name,
            first_station=self.first_station.raw(),
            structure=[item.raw() for item in self.structure],
            direction=[item.raw() for item in self.direction] if self.direction else None,
            number=self.number,
            literal=self.literal,
            is_active=self.is_active,
            comments=self.comments,
        )


@dataclass
class JourneyModel(BaseIdModel):
    """Атрибуты рейса"""

    name: str                                           # наименование
    first_station: StationModel                         # пункт отправления
    structure: List[RouteItemModel]                     # состав рейса
    journey_type: JourneyType                           # тип рейса
    departure_time: time                                # время отправления
    number: Optional[int] = None                        # номер рейса
    literal: Optional[str] = None                       # литера
    is_chartered: bool = False                          # признак заказного рейса
    need_control: bool = False                          # признак именной продажи и мониторинга
    season_begin: Optional[date] = None                 # начало сезона
    season_end: Optional[date] = None                   # окончание сезона
    direction: Optional[List[DirectionModel]] = None    # направления
    comments: Optional[str] = None                      # комментарии по рейсу
    is_active: bool = True                              # признак активности рейса

    @classmethod
    def from_container(cls, container: JourneyContainer) -> 'JourneyModel':     # type: ignore[override]
        JourneyVerifier().verify(container)

        direction = None
        if container.direction:
            direction = [DirectionModel.from_container(item) for item in container.direction]

        return cls(
            id=container.id,
            number=container.number,
            name=container.name,
            first_station=StationModel.from_container(container.first_station),
            structure=[RouteItemModel.from_container(item) for item in container.structure],
            journey_type=container.journey_type,
            departure_time=container.departure_time,
            literal=container.literal,
            is_chartered=container.is_chartered,
            need_control=container.need_control,
            season_begin=container.season_begin,
            season_end=container.season_end,
            direction=direction,
            comments=container.comments,
            is_active=container.is_active,
        )

    def raw(self) -> JourneyContainer:      # type: ignore[override]
        return JourneyContainer(
            id=self.id,
            number=self.number,
            name=self.name,
            first_station=self.first_station.raw(),
            structure=[item.raw() for item in self.structure],
            journey_type=self.journey_type,
            departure_time=self.departure_time,
            literal=self.literal,
            is_chartered=self.is_chartered,
            need_control=self.need_control,
            season_begin=self.season_begin,
            season_end=self.season_end,
            direction=[item.raw() for item in self.direction] if self.direction else None,
            comments=self.comments,
            is_active=self.is_active,
        )


@dataclass
class JourneyBunchItemModel(BaseIdModel):
    """Атрибуты элемента из связки рейсов"""

    journey: JourneyModel     # рейс
    stop_interval: int        # время простоя в часах

    @classmethod
    def from_container(cls, container: JourneyBunchItemContainer) -> 'JourneyBunchItemModel':   # type: ignore[override]
        JourneyBunchItemVerifier().verify(container)

        return cls(
            id=container.id,
            journey=JourneyModel.from_container(container.journey),
            stop_interval=container.stop_interval,
        )

    def raw(self) -> JourneyBunchItemContainer:     # type: ignore[override]
        return JourneyBunchItemContainer(
            id=self.id,
            journey=self.journey.raw(),
            stop_interval=self.stop_interval,
        )


@dataclass
class JourneyBunchModel(BaseIdModel):
    """Атрибуты связки рейсов"""

    journeys: List[JourneyBunchItemModel]     # элементы связки
    name: Optional[str] = None                # наименование связки

    @classmethod
    def from_container(cls, container: JourneyBunchContainer) -> 'JourneyBunchModel':    # type: ignore[override]
        JourneyBunchVerifier().verify(container)

        return cls(
            id=container.id,
            journeys=[JourneyBunchItemModel.from_container(item) for item in container.journeys],
            name=container.name,
        )

    def raw(self) -> JourneyBunchContainer:     # type: ignore[override]
        return JourneyBunchContainer(
            id=self.id,
            journeys=[item.raw() for item in self.journeys] if self.journeys else None,
            name=self.name,
        )
