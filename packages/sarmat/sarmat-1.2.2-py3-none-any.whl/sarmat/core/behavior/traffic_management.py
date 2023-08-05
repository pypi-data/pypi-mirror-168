"""
Sarmat.

Описание поведения объектов.

Объекты управления перевозками.
"""
from datetime import date, datetime, time, timedelta
from typing import Generator, List

from sarmat.core.constants import PeriodType, RoadType, StationType
from sarmat.core.context.models import (
    DestinationPointModel,
    JourneyModel,
    PeriodItemModel,
    RouteItemModel,
    StationModel,
)
from sarmat.core.exceptions import IncomparableTypesError, WrongValueError

from .bases import BhCompare, ScheduleItem, ScheduleSlice


class BhStation(BhCompare):
    """Базовое поведение объекта Станция"""
    compare_error_message = 'Сравнение станций не предусмотрено'

    id: int
    name: str
    point: DestinationPointModel
    station_type: StationType

    def __eq__(self, other):
        """Сравнение на равенство станций"""
        super().__eq__(other)

        if self.id and other.id:
            return self.id == other.id

        if not(self.id or other.id):
            return self.station_type == other.station_type and self.point == other.point and self.name == other.name

        return False

    def __ne__(self, other):
        """Проверка на неравенство станций"""
        super().__ne__(other)

        if self.id and other.id:
            return self.id != other.id

        if not(self.id or other.id):
            return self.station_type != other.station_type or self.point != other.point or self.name != other.name

        return True

    def __lt__(self, item):
        """Проверка на превосходство объекта перед станцией не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка на превосходство станции над объектом не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на непревосходство станции над объектом не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед станцией не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на принадлежность станции к населенному пункту"""
        raise IncomparableTypesError('Станции проверке на вхождение не подлежат')

    def _compare_classes(self, other):
        return isinstance(other, BhStation)


class BhRoad(BhCompare):
    """Базовое поведение объекта 'Дорога'"""
    compare_error_message = 'Сравнение дорог не предусмотрено'

    id: str
    direct_len_km: int
    direct_travel_time_min: int
    reverse_len_km: int
    reverse_travel_time_min: int
    road_type: RoadType

    def __eq__(self, other):
        """Сравнение на равенство дорог"""
        super().__eq__(other)

        if self.id and other.id:
            return self.id == other.id

        if not(self.id or other.id):
            return all([
                self.direct_travel_time_min == other.direct_travel_time_min,
                self.reverse_travel_time_min == other.reverse_travel_time_min,
                self.direct_len_km == other.direct_len_km,
                self.reverse_len_km == other.reverse_len_km,
                self.road_type == other.road_type,
            ])

        return False

    def __ne__(self, other):
        """Проверка на неравенство дорог"""
        super().__ne__(other)

        if self.id and other.id:
            return self.id != other.id

        if not(self.id or other.id):
            return any([
                self.direct_travel_time_min != other.direct_travel_time_min,
                self.reverse_travel_time_min != other.reverse_travel_time_min,
                self.direct_len_km != other.direct_len_km,
                self.reverse_len_km != other.reverse_len_km,
                self.road_type != other.road_type,
                ])

        return True

    def __lt__(self, item):
        """Проверка на превосходство объекта перед дорогой"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка на превосходство над объектом дорога"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на непревосходство над объектом дорога"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед дорогой"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на принадлежность дороги"""
        raise IncomparableTypesError('Проверка на вхождение для дорог не предусмотрена')

    def _compare_classes(self, other):
        return isinstance(other, BhRoad)


class BhRouteItem(BhCompare):
    """Базовое поведение объекта 'Пункт маршрута'"""
    compare_error_message = 'Для пунктов маршрута не предусмотрены операции сравнения'

    id: int
    station: StationModel
    point: DestinationPointModel

    def __eq__(self, other):
        """Сравнение на равенство пунктов маршрута"""
        super().__eq__(other)

        if self.id and other.id:
            return self.id == other.id

        if not(self.id and other.id):
            return self.station == other.station and self.point == other.point

        return False

    def __ne__(self, other):
        """Проверка на неравенство пунктов маршрута"""
        super().__ne__(other)

        if self.id and other.id:
            return self.id != other.id

        if not(self.id or other.od):
            return self.station != other.station or self.point != other.point

        return True

    def __lt__(self, item):
        """Проверка на превосходство объекта перед пунктом маршрута"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка на превосходство над объектом пункт маршрута"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на непревосходство над объектом пункт маршрута"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед пунктом маршрута"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на принадлежность объекта к пункту маршрута"""
        if isinstance(item, StationModel):
            return self.station == item

        if isinstance(item, DestinationPointModel):
            return self.point == item

        raise IncomparableTypesError(f'Для объекта {item} проверка на вхождение в пункт маршрута не предусмотрена')

    def _compare_classes(self, other):
        return isinstance(other, BhRouteItem)


class BhPeriodItem(BhCompare):
    """Базовое поведение объекта 'Элемент периода'"""

    period_type: PeriodType
    value: int

    def __eq__(self, other):
        """Сравнение на равенство периодов"""
        super().__eq__(other)

        return self.period_type == other.period_type and self.value == other.value

    def __ne__(self, other):
        """Проверка на неравенство периодов"""
        super().__ne__(other)

        return self.period_type != other.period_type or self.value != other.value

    def __lt__(self, item):
        """Проверка на превосходство объекта перед периодом"""
        super().__lt__(item)
        if self.period_type != item.period_type:
            raise IncomparableTypesError('Периоды разных типов сравнивать нельзя')

        return self.value < item.value

    def __gt__(self, item):
        """Проверка на превосходство периода над объектом"""
        super().__gt__(item)
        if self.period_type != item.period_type:
            raise IncomparableTypesError('Периоды разных типов сравнивать нельзя')

        return self.value > item.value

    def __le__(self, other):
        """Проверка на непревосходство над объектом периода"""
        super().__le__(other)
        if self.period_type != other.period_type:
            raise IncomparableTypesError('Периоды разных типов сравнивать нельзя')

        return self.value <= other.value

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед периодом"""
        super().__ge__(other)
        if self.period_type != other.period_type:
            raise IncomparableTypesError('Периоды разных типов сравнивать нельзя')

        return self.value >= other.value

    def __contains__(self, item):
        """Проверка на принадлежность объекта к периоду не имеет смысла"""
        raise IncomparableTypesError('Проверка на вхождение для периода не предусмотрена')

    def _compare_classes(self, other):
        return isinstance(other, BhPeriodItem)


class BhPeriod(BhCompare):
    """Базовое поведение объекта 'Период'"""

    compare_error_message = 'Сравнение периодов не предусматривается'

    period: PeriodItemModel
    periods: List[PeriodItemModel]

    def __eq__(self, other):
        """Сравнение на равенство периодов"""
        super().__eq__(other)

        if self.period and other.period:
            return self.period == other.period

        if self.periods and other.periods:
            if len(self.periods) == len(other.periods):
                pairs = zip(self.periods, other.periods)
                return all([i == j for i, j in pairs])

        return False

    def __ne__(self, other):
        """Проверка на неравенство периодов"""
        super().__eq__(other)

        if self.period and other.period:
            return self.period != other.period

        if self.periods and other.periods:
            if len(self.periods) != len(other.periods):
                return True

            pairs = zip(self.periods, other.periods)
            return not all([i == j for i, j in pairs])

        return True

    def __lt__(self, other):
        """Проверка на превосходство объекта перед периодом"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка на превосходство над объектом периода"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на непревосходство над объектом периода"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед периодом"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на принадлежность объекта к периоду"""
        if isinstance(item, PeriodItemModel):
            return item in self.periods

        raise IncomparableTypesError(f'Объект {item} неподходящего типа')

    def __len__(self):
        """Длина составной части периода"""
        return len(self.periods) if self.periods else 0

    def __getitem__(self, item: int) -> PeriodItemModel:
        """Получение элемента из сложного периода"""
        try:
            int(item)
        except (ValueError, TypeError):
            raise WrongValueError('Индекс элемента должен быть числом')

        if abs(item) >= len(self.periods):
            raise WrongValueError('Индекс превышает размер составного периода')

        return self.periods[item]

    def _compare_classes(self, other):
        return isinstance(other, BhPeriod)


class BhRoute(BhCompare):
    """Базовые методы маршрутов"""

    first_station: StationModel
    structure: List[RouteItemModel]

    def __eq__(self, other):
        """Сравнение на равенство маршрутов"""
        super().__eq__(other)
        return self.first_station == other.first_station and self.structure == other.structure

    def __ne__(self, other):
        """Проверка на неравенство маршрутов"""
        super().__ne__(other)
        return self.first_station != other.first_station or self.structure != other.structure

    def __lt__(self, item):
        """Проверка на превосходство объекта перед маршрутом"""
        super().__lt__(item)
        return len(self.structure) < len(item.structure)

    def __gt__(self, item):
        """Проверка на превосходство над объектом маршрут"""
        super().__gt__(item)
        return len(self.structure) > len(item.structure)

    def __le__(self, other):
        """Проверка на непревосходство над объектом маршрут"""
        super().__le__(other)
        return len(self.structure) <= len(other.structure)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед маршрутом"""
        super().__ge__(other)
        return len(self.structure) >= len(other.structure)

    def __contains__(self, item):
        """Проверка на принадлежность объекта к маршруту"""
        if isinstance(item, StationModel):
            stations = [self.first_station] + [i.station for i in self.structure]
            return item in stations

        if isinstance(item, DestinationPointModel):
            return item in [i.point for i in self.structure]

        if isinstance(item, RouteItemModel):
            return item in self.structure

        raise IncomparableTypesError(f'Для объекта {item} проверка на принадлежность к маршруту не выполняется')

    def __getitem__(self, item: int) -> ScheduleItem:
        if isinstance(item, slice):
            return self._get_slice(item)

        try:
            int(item)
        except (TypeError, ValueError):
            raise WrongValueError('Индекс элемента должен быть числом')

        if len(self.structure) < abs(item):
            raise WrongValueError(f'Длина маршрута меньше {item}')

        schedule = list(self.get_schedule())
        return schedule[item]

    def __len__(self) -> int:
        return len(self.structure) + 1

    def get_schedule(self) -> Generator[ScheduleItem, None, None]:
        """
        Расчет расписания по маршруту
        Returns: генератор списка пунктов прохождения по маршруту
        """
        length_from_start: float = 0.
        travel_min_from_start: int = 0

        yield ScheduleItem(
            station=self.first_station,
            point=self.first_station.point,
            len_from_start=length_from_start,
            len_from_last=0,
            arrive=None,
            depart=None,
            time_from_start=travel_min_from_start,
            time_from_last=0,
            stop_time=0,
        )

        for item in sorted(self.structure, key=lambda x: x.order):
            length_from_start += item.length_from_last_km or 0
            travel_min_from_start += item.travel_time_min or 0
            yield ScheduleItem(
                station=item.station,
                point=item.point,
                len_from_start=length_from_start,
                len_from_last=item.length_from_last_km,
                arrive=None,
                depart=None,
                time_from_start=travel_min_from_start,
                time_from_last=item.travel_time_min,
                stop_time=item.stop_time_min or 0,
            )

    def _compare_classes(self, other):
        return isinstance(other, BhRoute)

    def _get_slice(self, item: slice) -> ScheduleSlice:
        route: List[ScheduleItem] = list(self.get_schedule())[item]

        if not route:
            raise WrongValueError('Неверно указаны пункты отправления и назначения')

        if len(route) == 1:
            return ScheduleSlice(
                station=route[0].station.name if route[0].station else '',
                point=route[0].point.name if route[0].point else '',
                len_from_start=route[0].len_from_start,
                len_from_last=route[0].len_from_last,
                time_from_start=route[0].time_from_start,
                time_from_last=route[0].time_from_last,
                depart=route[0].depart,
                arrive=route[0].arrive,
                stop_time=route[0].stop_time,
            )

        start_point: ScheduleItem = route[0]
        end_point: ScheduleItem = route[-1]

        length, travel_time, stop_time = 0., 0, 0
        for i in route[1:]:
            length += i.len_from_last
            travel_time += i.time_from_last
            stop_time += i.stop_time or 0

        if stop_time:
            stop_time -= end_point.stop_time or 0

        first_station_name = start_point.station.name if start_point.station else ''
        end_station_name = end_point.station.name if end_point.station else ''
        start_point_name = start_point.point.name if start_point.point else ''
        end_point_name = end_point.point.name if end_point.point else ''
        return ScheduleSlice(
            station=f'{first_station_name} - {end_station_name}',
            point=f'{start_point_name} - {end_point_name}',
            len_from_start=end_point.len_from_start - start_point.len_from_start,
            len_from_last=length,
            arrive=None,
            depart=None,
            time_from_start=end_point.time_from_start - start_point.time_from_start,
            time_from_last=travel_time,
            stop_time=stop_time,
        )


class BhJourney(BhRoute):
    """Базовые методы рейсов"""

    departure_time: time

    def __eq__(self, other):
        """Сравнение на равенство рейсов"""
        return super().__eq__(other) and (self.departure_time == other.departure_time)

    def __ne__(self, other):
        """Проверка на неравенство рейсов"""
        return super().__ne__(other) or (self.departure_time != other.departure_time)

    def get_journey_schedule(self, start_date: date) -> Generator[ScheduleItem, None, None]:
        """
        Расчет расписания по рейсу
        Returns: генератор списка пунктов прохождения по рейсу
        """
        stop_time = 0
        hour, minute = self.departure_time.hour, self.departure_time.minute
        departure_date_time = datetime(*start_date.timetuple()[:3], hour, minute)

        for item in list(super().get_schedule()):
            yield ScheduleItem(
                station=item.station,
                point=item.point,
                len_from_start=item.len_from_start,
                len_from_last=item.len_from_last,
                arrive=departure_date_time + timedelta(minutes=item.time_from_start + stop_time),
                depart=departure_date_time + timedelta(
                    minutes=(item.time_from_start + stop_time + (item.stop_time or 0)),
                ),
                time_from_start=item.time_from_start,
                time_from_last=item.time_from_last,
                stop_time=item.stop_time,
            )

            stop_time += (item.stop_time or 0)

    def _compare_classes(self, other):
        return isinstance(other, BhJourney)


class BhJourneyBunchItem(BhCompare):
    """Базовое поведение объекта 'Элемент связки рейсов'"""
    compare_error_message = 'Операция сравнения для элементов связок не предусмотрена'

    journey: JourneyModel
    stop_interval: int

    def __eq__(self, other):
        """Сравнение на равенство элементов связки"""
        super().__eq__(other)
        return self.journey == other.journey and self.stop_interval == other.stop_interval

    def __ne__(self, other):
        """Проверка на неравенство элементов связки"""
        super().__ne__(other)
        return self.journey != other.journey or self.stop_interval != other.stop_interval

    def __lt__(self, item):
        """Проверка на превосходство объекта перед элементом связки"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, item):
        """Проверка на превосходство над объектом элемент связки"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Проверка на непревосходство над объектом элемент связки"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед элементом связки"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на принадлежность объекта к элементу связки"""
        raise IncomparableTypesError('Проверка на вхождение для элементов связки не предусмотрена')

    def _compare_classes(self, other):
        return isinstance(other, BhJourneyBunchItem)


class BhJourneyBunch(BhCompare):
    """Базовое поведение объекта Связка рейсов"""
    compare_message_error = 'Сравнение связок не предусматривается'

    journeys: List[BhJourneyBunchItem]

    def __eq__(self, other):
        """Сравнение на равенство связок рейсов"""
        super().__eq__(other)
        return self.journeys == other.journeys

    def __ne__(self, other):
        """Проверка на неравенство связок рейсов"""
        super().__ne__(other)
        return self.journeys != other.journeys

    def __lt__(self, item):
        """Проверка на превосходство объекта перед связкой рейса"""
        raise IncomparableTypesError(self.compare_message_error)

    def __gt__(self, item):
        """Проверка на превосходство над объектом связка рейсов"""
        raise IncomparableTypesError(self.compare_message_error)

    def __le__(self, other):
        """Проверка на непревосходство над объектом связка рейсов"""
        raise IncomparableTypesError(self.compare_message_error)

    def __ge__(self, other):
        """Проверка на непревосходство объекта перед связкой рейсов"""
        raise IncomparableTypesError(self.compare_message_error)

    def __contains__(self, item):
        """Проверка на принадлежность объекта к связке рейсов"""
        if isinstance(item, BhJourneyBunchItem):
            return item in self.journeys
        elif isinstance(item, BhJourney):
            journeys = [i.journey for i in self.journeys]
            return item in journeys

        raise IncomparableTypesError(
            f'Для объекта {item} недопустима проверка на вхождение в связку рейсов'
        )

    def _compare_classes(self, other):
        return isinstance(other, BhJourneyBunch)
