"""
Sarmat.

Описание сущностей.

Базовый класс для описания моделей.
"""
from dataclasses import asdict, dataclass, fields
from typing import List, Optional

from sarmat.core.constants import PeriodType
from sarmat.core.context.containers.sarmat_containers import SarmatContainer, PeriodItemContainer, PeriodContainer


@dataclass
class BaseModel:

    @property
    def sarmat_fields(self):
        return [fld.name for fld in fields(self)]

    @property
    def as_dict(self):
        return asdict(self)

    @classmethod
    def from_container(cls, container: SarmatContainer) -> 'BaseModel':
        raise NotImplementedError

    def raw(self) -> SarmatContainer:
        raise NotImplementedError


@dataclass
class BaseIdModel(BaseModel):

    id: Optional[int]


@dataclass
class BaseUidModel(BaseModel):

    uid: Optional[str]


@dataclass
class PersonModel(BaseModel):
    """Данные человека"""

    last_name: str      # фамилия
    first_name: str     # имя
    middle_name: str    # отчество
    male: bool          # пол: М


@dataclass
class PeriodItemModel(BaseIdModel):
    """Элементы сложного периода"""

    period_type: PeriodType     # тип периода
    cypher: str                 # шифр (константа)
    name: str                   # название
    value: List[int]            # список значений
    is_active: bool             # период активности

    @classmethod
    def from_container(cls, container: PeriodItemContainer) -> 'PeriodItemModel':   # type: ignore[override]
        return cls(
            id=container.id,
            period_type=container.period_type,
            cypher=container.cypher,
            name=container.name,
            value=container.value,
            is_active=container.is_active,
        )

    def raw(self) -> PeriodItemContainer:       # type: ignore[override]
        return PeriodItemContainer(
            id=self.id,
            period_type=self.period_type,
            cypher=self.cypher,
            name=self.name,
            value=self.value,
            is_active=self.is_active,
        )


@dataclass
class PeriodModel(BaseIdModel):
    """Период"""

    cypher: str                                         # системное имя
    name: str                                           # константа
    periods: Optional[List[PeriodItemModel]] = None     # описание сложного периода
    period: Optional[PeriodItemModel] = None            # описание простого периода

    @classmethod
    def from_container(cls, container: PeriodContainer) -> 'PeriodModel':       # type: ignore[override]
        period, periods = None, []
        if container.periods:
            periods = [PeriodItemModel.from_container(item) for item in container.periods]
        if container.period:
            period = PeriodItemModel.from_container(container.period)

        return cls(
            id=container.id,
            cypher=container.cypher,
            name=container.name,
            periods=periods,
            period=period,
        )

    def raw(self) -> PeriodContainer:   # type: ignore[override]
        return PeriodContainer(
            id=self.id,
            cypher=self.cypher,
            name=self.name,
            periods=[item.raw() for item in self.periods] if self.periods else None,
            period=self.period.raw() if self.period else None,
        )
