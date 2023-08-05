"""
Sarmat.

Описание сущностей.

Базовый класс для контейнеров.
"""
from datetime import date, datetime
from typing import Optional, List

import pydantic

from sarmat.core.constants.sarmat_constants import SarmatAttribute
from sarmat.core.constants import PeriodType, DATE_FORMAT, FULL_DATETIME_FORMAT
from sarmat.tools.json_encoder import SarmatEncoder


class SarmatContainer(pydantic.BaseModel):

    def sarmat_fields(self):
        return list(self.__fields__.keys())

    @classmethod
    def _parse_date(cls, value) -> date:
        return datetime.strptime(value, DATE_FORMAT).date()

    @classmethod
    def _parse_datetime(cls, value) -> datetime:
        return datetime.strptime(value, FULL_DATETIME_FORMAT)

    class Config:
        json_encoders = {
            SarmatAttribute: lambda v: SarmatEncoder.as_enum(v),
            date: lambda v: v.strftime(DATE_FORMAT) if v else None
        }


class BaseIdSarmatContainer(SarmatContainer):
    """Базовая модель с числовым идентификатором."""

    id: Optional[int] = 0


class BaseUidSarmatContainer(SarmatContainer):
    """Базовая модель с UUID идентификатором."""

    uid: Optional[str] = ''


class PeriodItemContainer(BaseIdSarmatContainer):
    """Элементы сложного периода"""

    period_type: PeriodType     # тип периода
    cypher: str                 # шифр (константа)
    name: str                   # название
    value: List[int]            # список значений
    is_active: bool             # период активности


class PeriodContainer(BaseIdSarmatContainer):
    """Период"""

    cypher: str                                           # системное имя
    name: str                                             # константа
    periods: Optional[List[PeriodItemContainer]] = None   # описание сложного периода
    period: Optional[PeriodItemContainer] = None          # описание простого периода


class BasePersonSarmatContainer(SarmatContainer):
    """Базовая модель для описания человека."""

    last_name: str                  # фамилия
    first_name: str                 # имя
    middle_name: Optional[str]      # отчество
    male: bool                      # пол
