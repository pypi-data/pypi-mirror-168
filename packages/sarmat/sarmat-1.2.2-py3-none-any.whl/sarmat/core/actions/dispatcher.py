"""
Sarmat.

Описание поведения объектов.

Поведение объектов в режиме работы диспетчера.
"""
from abc import ABC, abstractmethod
from datetime import date, datetime, tzinfo
from typing import Dict, Optional, List, Union
from uuid import uuid4

from sarmat.core.constants import JourneyClass, JourneyState
from sarmat.core.context.models import (
    PermitModel,
    RouteItemModel,
    StationModel,
    JourneyProgressModel,
    JourneyScheduleModel,
    JourneyModel,
)
from sarmat.core.exceptions.sarmat_exceptions import ImpossibleOperationError

from sarmat.core.behavior.traffic_management import BhJourney


class Journey(BhJourney):
    """Поведение объекта Рейс"""

    def activate(
        self,
        start_date: date,
        permit: PermitModel,
    ) -> Dict[str, Union[JourneyProgressModel, List[JourneyScheduleModel]]]:
        """
        Активизация рейса (выписка рейсовой ведомости, создание расписания по рейсу)
        Args:
            start_date: дата начала выполнения рейса (отправление из начальной точки)
            permit: путевой лист

        Returns:
            рейсовая ведомость
            список активных пунктов маршрута

        """
        # атрибуты текущего рейса и список активных станций, через которые проходит рейс
        this_journey = JourneyModel.from_container(self.raw())      # type: ignore
        journey_stations = [item for item in self.get_journey_schedule(start_date) if item.station is not None]
        first_station, *middleware_stations, last_station = journey_stations

        journey_progress = JourneyProgressModel(  # Атрибуты рейсовой ведомости
            uid=str(uuid4()),                     # идентификатор ведомости
            depart_date=start_date,               # дата отправления в рейс
            journey=this_journey,                 # рейс
            permit=permit,                        # путевой лист
        )

        journey_schedule = [
            JourneyScheduleModel(
                uid=str(uuid4()),                      # идентификатор строки
                journey_progress=journey_progress,     # рейсовая ведомость
                journey_class=JourneyClass.BASE,       # класс рейса (формирующийся)
                station=first_station.station,         # станция
                point=first_station.point,             # пункт прохождения маршрута
                state=JourneyState.READY,              # состояние рейса
                plan_depart=first_station.depart,      # плановое время отправления
                platform='',                           # платформа
                comment='',                            # комментарий к текущему пункту
            )
        ]

        journey_schedule += [
            JourneyScheduleModel(
                uid=str(uuid4()),                       # идентификатор строки
                journey_progress=journey_progress,      # рейсовая ведомость
                journey_class=JourneyClass.TRANSIT,     # класс рейса (формирующийся)
                station=item.station,                   # станция
                point=item.point,                       # пункт прохождения маршрута
                state=JourneyState.READY,               # состояние рейса
                plan_arrive=item.arrive,                # плановое время прибытия
                plan_depart=item.depart,                # плановое время отправления
                platform='',                            # платформа
                comment='',                             # комментарий к текущему пункту
            )
            for item in middleware_stations
        ]

        journey_schedule.append(
            JourneyScheduleModel(
                uid=str(uuid4()),                           # идентификатор строки
                journey_progress=journey_progress,          # рейсовая ведомость
                journey_class=JourneyClass.ARRIVING,        # класс рейса (формирующийся)
                station=last_station.station,               # станция
                point=last_station.point,                   # пункт прохождения маршрута
                state=JourneyState.READY,                   # состояние рейса
                plan_arrive=last_station.arrive,            # плановое время прибытия
                platform='',                                # платформа
                comment='',                                 # комментарий к текущему пункту
            )
        )

        for idx, item in enumerate(journey_schedule):
            journey_schedule[idx].last_items = journey_schedule[idx+1:]

        return {
            'JourneyProgress': journey_progress,
            'JourneyScheduleStructure': journey_schedule,
        }


class JourneySchedule:
    """Поведение объекта Рейсовая ведомость в активном расписании"""

    journey_class: JourneyClass
    state: JourneyState
    fact_arrive: datetime
    fact_depart: datetime
    permit: Optional[PermitModel]
    platform: str
    comment: str
    last_items: List['JourneySchedule']
    current_item: RouteItemModel

    def make_departure(self, time_zone: Optional[tzinfo] = None) -> None:
        """Операция отправления на текущем пункте"""

        if self.journey_class == JourneyClass.ARRIVING:
            raise ImpossibleOperationError("На последнем пункте маршрута операция отправления не выполняется")

        self.state = JourneyState.DEPARTED
        self.fact_depart = datetime.now(time_zone)

    def make_registration(self,
                          permit: Optional[PermitModel] = None,
                          platform: Optional[str] = None,
                          comments: Optional[str] = None) -> None:
        """
        Операция по регистрации рейса. Заполнение реквизитов
        Args:
            permit: путевой лист
            platform: номер платформы
            comments: комментарии диспетчера
        """

        if permit and (permit != self.permit):
            self.permit = permit

        if platform and platform != self.platform:
            self.platform = platform

        # NOTE: комментарий дозволяется затереть
        if comments != self.comment:
            self.comment = comments or ''

    def make_arrival(self, time_zone: Optional[tzinfo] = None) -> None:
        """Операция прибытия на текущем пункте"""
        is_last = self.journey_class == JourneyClass.ARRIVING
        operational_time = datetime.now(time_zone)

        new_state = JourneyState.ARRIVED if is_last else JourneyState.ON_REGISTRATION
        self.state = new_state
        self.fact_arrive = operational_time

    def cancel_journey(self) -> None:
        """Отмена рейса"""
        self._set_state_for_items_chain(JourneyState.CANCELLED)

    def close_journey(self) -> None:
        """Закрытие рейса"""
        self._set_state_for_items_chain(JourneyState.CLOSED)

    def break_journey(self) -> None:
        """Отметка о срыве"""
        self._set_state_for_items_chain(JourneyState.DISRUPTED)

    @property
    def current_station(self) -> Optional[StationModel]:
        """Текущий пункт прохождения рейса"""
        return self.current_item.station if self.current_item else None

    def _set_state_for_items_chain(self, state: JourneyState) -> None:
        """Назначение состояния текущему элементу и всем последующим"""
        self.state = state
        for item in self.last_items:
            item.state = state


class JourneyHook(ABC):
    """Поведение объекта Рейсовая Ведомость"""

    @abstractmethod
    def lock_register(self):
        """Блокировка ведомости"""

    @abstractmethod
    def unlock_register(self):
        """Снятие блокировки с ведомости"""

    @abstractmethod
    def register_place(self):
        """Регистрация места на ведомости"""

    @abstractmethod
    def unregister_place(self):
        """Отмена регистрации места на ведомости"""
