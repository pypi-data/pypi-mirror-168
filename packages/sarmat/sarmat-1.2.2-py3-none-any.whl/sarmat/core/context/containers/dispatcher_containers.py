"""
Sarmat.

Описание сущностей.

Диспетчерские объекты.
"""
from datetime import date, datetime
from typing import List, Optional

from pydantic import validator

from sarmat.core.constants import JourneyClass, JourneyState

from .traffic_management_containers import DestinationPointContainer, JourneyContainer, StationContainer
from .sarmat_containers import BaseIdSarmatContainer, BaseUidSarmatContainer, PeriodContainer
from .vehicle_containers import PermitContainer


class IntervalContainer(BaseIdSarmatContainer):
    """График выполнения рейсов"""

    journey: JourneyContainer   # рейс
    start_date: date            # дата начала
    interval: PeriodContainer   # интервал движения

    @validator('start_date', pre=True)
    def parse_start_date(cls, val):
        if val and isinstance(val, str):
            return cls._parse_date(val)
        return val


class JourneyProgressContainer(BaseUidSarmatContainer):
    """Атрибуты рейсовой ведомости"""

    depart_date: date               # дата отправления в рейс
    journey: JourneyContainer       # рейс
    permit: PermitContainer         # номер путевого листа

    @validator('depart_date', pre=True)
    def parse_depart_date(cls, val):
        if val and isinstance(val, str):
            return cls._parse_date(val)
        return val


class JourneyScheduleContainer(BaseUidSarmatContainer):
    """Процесс прохождения рейса по автоматизированным точкам"""

    journey_progress: JourneyProgressContainer                      # рейсовая ведомость
    journey_class: JourneyClass                                     # классификация рейса в данном пункте
    station: Optional[StationContainer]                             # станция
    point: Optional[DestinationPointContainer]                      # точка прохождения маршрута
    state: JourneyState                                             # состояние рейса
    plan_arrive: Optional[datetime] = None                          # плановое время прибытия
    fact_arrive: Optional[datetime] = None                          # фактическое время прибытия
    plan_depart: Optional[datetime] = None                          # плановое время отправления
    fact_depart: Optional[datetime] = None                          # фактическое время отправления
    platform: str = ''                                              # платформа
    comment: str = ''                                               # комментарий к текущему пункту
    last_items: Optional[List['JourneyScheduleContainer']] = None   # оставшиеся активные пункты прохождения рейса

    @validator('plan_arrive', pre=True)
    def parse_plan_arrive(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @validator('fact_arrive', pre=True)
    def parse_fact_arrive(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @validator('plan_depart', pre=True)
    def parse_plan_depart(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @validator('fact_depart', pre=True)
    def parse_fact_depart(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val
