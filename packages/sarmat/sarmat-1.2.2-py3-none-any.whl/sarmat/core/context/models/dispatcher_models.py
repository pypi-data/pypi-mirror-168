"""
Sarmat.

Описание сущностей.

Диспетчерские объекты.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from sarmat.core.constants import JourneyClass, JourneyState

from .sarmat_models import BaseIdModel, BaseUidModel, PeriodModel
from .traffic_management_models import DestinationPointModel, JourneyModel, StationModel
from .vehicle_models import PermitModel
from ..containers import IntervalContainer, JourneyProgressContainer, JourneyScheduleContainer


@dataclass
class IntervalModel(BaseIdModel):
    """График выполнения рейсов"""

    journey: JourneyModel   # рейс
    start_date: date        # дата начала
    interval: PeriodModel   # интервал движения

    @classmethod
    def from_container(cls, container: IntervalContainer) -> 'IntervalModel':   # type: ignore[override]
        return cls(
            id=container.id,
            journey=JourneyModel.from_container(container.journey),
            start_date=container.start_date,
            interval=PeriodModel.from_container(container.interval),
        )

    def raw(self) -> IntervalContainer:     # type: ignore[override]
        return IntervalContainer(
            id=self.id,
            journey=self.journey.raw(),
            start_date=self.start_date,
            interval=self.interval.raw(),
        )


@dataclass
class JourneyProgressModel(BaseUidModel):
    """Атрибуты рейсовой ведомости"""

    depart_date: date           # дата отправления в рейс
    journey: JourneyModel       # рейс
    permit: PermitModel         # номер путевого листа

    @classmethod
    def from_container(cls, container: JourneyProgressContainer) -> 'JourneyProgressModel':     # type: ignore[override]
        return cls(
            uid=container.uid,
            depart_date=container.depart_date,
            journey=JourneyModel.from_container(container.journey),
            permit=PermitModel.from_container(container.permit),
        )

    def raw(self) -> JourneyProgressContainer:      # type: ignore[override]
        return JourneyProgressContainer(
            uid=self.uid,
            depart_date=self.depart_date,
            journey=self.journey.raw(),
            permit=self.permit.raw(),
        )


@dataclass
class JourneyScheduleModel(BaseUidModel):
    """Процесс прохождения рейса по автоматизированным точкам"""

    journey_progress: JourneyProgressModel                       # рейсовая ведомость
    journey_class: JourneyClass                                  # классификация рейса в данном пункте
    station: Optional[StationModel]                              # станция
    point: Optional[DestinationPointModel]                       # точка прохождения маршрута
    state: JourneyState                                          # состояние рейса
    plan_arrive: Optional[datetime] = None                       # плановое время прибытия
    fact_arrive: Optional[datetime] = None                       # фактическое время прибытия
    plan_depart: Optional[datetime] = None                       # плановое время отправления
    fact_depart: Optional[datetime] = None                       # фактическое время отправления
    platform: str = ''                                           # платформа
    comment: str = ''                                            # комментарий к текущему пункту
    last_items: Optional[List['JourneyScheduleModel']] = None    # оставшиеся активные пункты прохождения рейса

    @classmethod
    def from_container(cls, container: JourneyScheduleContainer) -> 'JourneyScheduleModel':     # type: ignore[override]
        last_items = None
        if container.last_items:
            last_items = [JourneyScheduleModel.from_container(item) for item in container.last_items]

        return cls(
            uid=container.uid,
            journey_progress=JourneyProgressModel.from_container(container.journey_progress),
            journey_class=container.journey_class,
            station=StationModel.from_container(container.station) if container.station else None,
            point=DestinationPointModel.from_container(container.point) if container.point else None,
            state=container.state,
            plan_arrive=container.plan_arrive,
            fact_arrive=container.fact_arrive,
            plan_depart=container.plan_depart,
            fact_depart=container.fact_depart,
            platform=container.platform,
            comment=container.comment,
            last_items=last_items,
        )

    def raw(self) -> JourneyScheduleContainer:      # type: ignore[override]
        return JourneyScheduleContainer(
            uid=self.uid,
            journey_progress=self.journey_progress.raw(),
            journey_class=self.journey_class,
            station=self.station.raw() if self.station else None,
            point=self.point.raw() if self.point else None,
            state=self.state,
            plan_arrive=self.plan_arrive,
            fact_arrive=self.fact_arrive,
            plan_depart=self.plan_depart,
            fact_depart=self.fact_depart,
            platform=self.platform,
            comment=self.comment,
            last_items=[item.raw() for item in self.last_items] if self.last_items else None,
        )
