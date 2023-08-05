"""
Sarmat.

Описание поведения объектов.

Базовые элементы.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sarmat.core.exceptions import IncomparableTypesError

from sarmat.core.context.models import DestinationPointModel, StationModel


@dataclass
class ScheduleItem:
    """Описание участка маршрута"""
    station: Optional[StationModel]             # станции отправления
    point: Optional[DestinationPointModel]      # крайние пункты
    len_from_start: float                       # расстояние от начального пункта
    len_from_last: float                        # расстояние от предыдущего пункта
    time_from_start: int                        # время от начального пункта
    time_from_last: int                         # время от предыдущего пункта
    depart: Optional[datetime]                  # время прибытия
    arrive: Optional[datetime]                  # время отправления
    stop_time: Optional[int]                    # время стоянки в минутах


@dataclass
class ScheduleSlice:
    """Описание среза по маршруту"""
    station: str
    point: str
    len_from_start: float                       # расстояние от начального пункта
    len_from_last: float                        # расстояние от предыдущего пункта
    time_from_start: int                        # время от начального пункта
    time_from_last: int                         # время от предыдущего пункта
    depart: Optional[datetime]                  # время прибытия
    arrive: Optional[datetime]                  # время отправления
    stop_time: Optional[int]                    # время стоянки в минутах


class BhNoAction:
    """Класс, запрещающий всякие действия над объектом"""


class BhCompare(BhNoAction):
    """Операции сравнения объектов"""

    def __eq__(self, other):
        """Сравнение на равенство"""
        self._check_type(other)

    def __ne__(self, other):
        """Определение неравенства"""
        self._check_type(other)

    def __lt__(self, other):
        """Проверка на <"""
        self._check_type(other)

    def __gt__(self, other):
        """Проверка на >"""
        self._check_type(other)

    def __le__(self, other):
        """Проверка на <="""
        self._check_type(other)

    def __ge__(self, other):
        """Проверка на >="""
        self._check_type(other)

    def __contains__(self, item):
        """Проверка на вхождение во множество"""

    def _compare_classes(self, other):
        return isinstance(other, self.__class__)

    def _check_type(self, other):
        """Проверка на соответствие типов. Объекты разных типов сравнивать нельзя"""
        if not self._compare_classes(other):
            message = f"Объекты {other.__class__} и {self.__class__} не сравнимы"
            raise IncomparableTypesError(message)
