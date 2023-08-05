"""
Sarmat.

Константы.

Константы бизнес логики.
"""
from enum import Enum
from typing import Any, Dict


class SarmatAttribute(Enum):
    """Встроенные значения атрибутов в Sarmat."""

    __description__: Dict[Any, str] = {}    # описание
    __cypher__: Dict[Any, str] = {}         # текстовое представление значения (строковая константа)

    @classmethod
    def as_text(cls, value: Any) -> str:
        """Описание значения."""
        if isinstance(value, cls):
            return cls.__description__.get(value.value) or ''

        return ''

    @classmethod
    def as_cypher(cls, value: Any) -> str:
        """Получение строковой константы."""
        if isinstance(value, cls):
            return cls.__cypher__.get(value.value) or ''

        return ''


class RoadType(SarmatAttribute):
    """Тип дорожного покрытия"""
    PAVED = 1
    DIRT = 2
    HIGHWAY = 3

    __description__ = {
        PAVED: 'Дорога с твердым покрытием',
        DIRT: 'Грунтовая дорога',
        HIGHWAY: 'Магистраль',
    }


class PeriodType(SarmatAttribute):
    """Тип периода"""
    MINUTE = 1
    HOUR = 2
    DAY = 3
    WEEK = 4
    MONTH = 5
    YEAR = 6
    EVEN = 7
    ODD = 8
    DAYS = 9
    DAYS_OF_WEEK = 10

    __description__ = {
        MINUTE: 'По минутам',
        HOUR: 'По часам',
        DAY: 'По дням',
        WEEK: 'По неделям',
        MONTH: 'По месяцам',
        YEAR: 'По годам',
        EVEN: 'По четным дням месяца',
        ODD: 'По нечетным дням месяца',
        DAYS: 'По числам месяца',
        DAYS_OF_WEEK: 'По дням недели',
    }

    __cypher__ = {
        MINUTE: 'minute',
        HOUR: 'hour',
        DAY: 'day',
        WEEK: 'week',
        MONTH: 'month',
        YEAR: 'year',
        EVEN: 'even',
        ODD: 'odd',
        DAYS: 'days',
        DAYS_OF_WEEK: 'dow',
    }


class LocationType(SarmatAttribute):
    """Тип территориального образования"""
    COUNTRY = 1
    DISTRICT = 2
    REGION = 3
    PROVINCE = 4
    AREA = 5

    __description__ = {
        COUNTRY: 'Страна',
        DISTRICT: 'Республика',
        REGION: 'Край',
        PROVINCE: 'Область',
        AREA: 'Район',
    }

    __cypher__ = {
        COUNTRY: '',
        DISTRICT: 'респ.',
        REGION: 'кр.',
        PROVINCE: 'обл.',
        AREA: 'р-н',
    }


class SettlementType(SarmatAttribute):
    """Тип населенного пункта"""
    CITY = 1
    SETTLEMENT = 2
    TOWNSHIP = 3
    HAMLET = 4
    STANITSA = 5
    FARM = 6
    VILLAGE = 7

    __description__ = {
        CITY: 'Город',
        SETTLEMENT: 'Поселок',
        TOWNSHIP: 'Село',
        HAMLET: 'Деревня',
        STANITSA: 'Станица',
        FARM: 'Хутор',
        VILLAGE: 'Слобода',
    }

    __cypher__ = {
        CITY: 'г.',
        SETTLEMENT: 'пос.',
        TOWNSHIP: 'с.',
        HAMLET: 'дер.',
        STANITSA: 'ст.',
        FARM: 'х.',
        VILLAGE: 'сл.',
    }


class StationType(SarmatAttribute):
    """Типы станций"""
    STATION = 1
    TERMINAL = 2
    TICKET_OFFICE = 3
    PLATFORM = 4

    __description__ = {
        STATION: 'Автовокзал',
        TERMINAL: 'Автостанция',
        TICKET_OFFICE: 'Автокасса',
        PLATFORM: 'Остановочная платформа',
    }

    __cypher__ = {
        STATION: 'АВ',
        TERMINAL: 'АС',
        TICKET_OFFICE: 'АК',
        PLATFORM: 'ОП',
    }


class JourneyType(SarmatAttribute):
    """Типы рейсов"""
    SUBURBAN = 1
    LONG_DISTANCE = 2
    INTER_REGIONAL = 3
    INTERNATIONAL = 4

    __description__ = {
        SUBURBAN: 'Пригородный',
        LONG_DISTANCE: 'Междугородный',
        INTER_REGIONAL: 'Межрегиональный',
        INTERNATIONAL: 'Международный',
    }


class JourneyClass(SarmatAttribute):
    """Классификация рейсов"""
    BASE = 1
    TRANSIT = 2
    ARRIVING = 3

    __description__ = {
        BASE: 'Формирующийся',
        TRANSIT: 'Транзитный',
        ARRIVING: 'Прибывающий',
    }


class JourneyState(SarmatAttribute):
    """Состояния рейсов"""
    READY = 0               # рейс активен
    ARRIVED = 1             # прибыл
    ON_REGISTRATION = 2     # на регистрации
    DEPARTED = 3            # отправлен
    CANCELLED = 4           # отменен (разовая операция)
    CLOSED = 5              # закрыт (массовая отмена на продолжительное время)
    DISRUPTED = 6           # сорван (по тех. неисправности и т.д.)

    __description__ = {
        READY: 'Активен',
        ARRIVED: 'Прибыл',
        ON_REGISTRATION: 'На регистрации',
        DEPARTED: 'Отправлен',
        CANCELLED: 'Отменен',
        CLOSED: 'Закрыт',
        DISRUPTED: 'Сорван',
    }


class VehicleType(SarmatAttribute):
    """Тип транспортного средства"""
    BUS = 1
    SMALL_BUS = 2
    CAR = 3
    TRUCK = 4
    TRAILER = 5
    SPECIAL = 6

    __description__ = {
        BUS: 'Автобус',
        SMALL_BUS: 'Автобус малой вместимости',
        CAR: 'Легковой автомобиль',
        TRUCK: 'Грузовой автомобиль',
        TRAILER: 'Прицеп',
        SPECIAL: 'Спецтехника',
    }


class CrewType(SarmatAttribute):
    """Тип участника экипажа"""
    DRIVER = 1
    TRAINEE = 2

    __description__ = {
        DRIVER: 'Водитель',
        TRAINEE: 'Стажер',
    }


class PermitType(SarmatAttribute):
    """Тип путевого листа"""
    BUS_PERMIT = 1
    CAR_PERMIT = 2
    TRUCK_PERMIT = 3
    CUSTOM_PERMIT = 4

    __description__ = {
        BUS_PERMIT: 'Путевой лист автобуса',
        CAR_PERMIT: 'Путевой лист легкового автомобиля',
        TRUCK_PERMIT: 'Путевой лист грузового автомобиля',
        CUSTOM_PERMIT: 'Заказной путевой лист',
    }


class PlaceKind(SarmatAttribute):
    """Тип места"""
    PASSANGERS_SEAT = 1
    BAGGAGE = 2

    __description__ = {
        PASSANGERS_SEAT: 'Пассажирское место',
        BAGGAGE: 'Багажное место',
    }


class PlaceType(SarmatAttribute):
    """Вид пассажирского места"""
    STANDING = 1
    SITTING = 2

    __description__ = {
        STANDING: 'Место для стоящих пассажиров',
        SITTING: 'Место для сидящих пассажиров',
    }


class PlaceState(SarmatAttribute):
    """Состояние места"""
    FREE = 1
    BOOKED = 2
    CLOSED = 3
    SOLD = 4
    LOCKED = 5
    TRANSFERRED = 6

    __description__ = {
        FREE: 'Свободно',
        BOOKED: 'Забронировано',
        CLOSED: 'Закрыто',
        SOLD: 'Продано',
        LOCKED: 'Заблокировано',
        TRANSFERRED: 'Произведена пересадка',
    }


MAX_SUBURBAN_ROUTE_LENGTH = 50      # Максимальная льина пригородных маршрутов (в километрах)
