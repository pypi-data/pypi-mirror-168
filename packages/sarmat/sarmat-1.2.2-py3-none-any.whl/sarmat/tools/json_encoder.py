"""
Sarmat.

Вспомогательные инструменты.

Преобразование Sarmat объектов в JSON и обратно
"""
import json
from datetime import date, datetime, time
from decimal import Decimal

import sarmat.core.constants as constants
from sarmat.core.exceptions import WrongValueError


class SarmatEncoder(json.JSONEncoder):

    @classmethod
    def as_enum(cls, obj):
        return obj.value

    @classmethod
    def as_decimal(cls, obj):
        return str(obj)

    @classmethod
    def as_time(cls, obj):
        return obj.strftime(constants.FULL_TIME_FORMAT)

    @classmethod
    def as_date(cls, obj):
        return obj.strftime(constants.DATE_FORMAT)

    @classmethod
    def as_datetime(cls, obj):
        return obj.strftime(constants.FULL_DATETIME_FORMAT)

    def default(self, obj):
        if isinstance(obj, constants.sarmat_constants.SarmatAttribute):
            return self.as_enum(obj)
        if isinstance(obj, Decimal):
            return self.as_decimal(obj)
        if isinstance(obj, time):
            return self.as_time(obj)
        if isinstance(obj, date):
            return self.as_date(obj)
        if isinstance(obj, datetime):
            return self.as_datetime(obj)
        return json.JSONEncoder.default(self, obj)


def as_enum(dct):
    if "__enum__" in dct:
        name, member = dct["__enum__"].split(".")

        try:
            cls = getattr(constants.sarmat_constants, name)
        except AttributeError:
            raise WrongValueError(f"Неизвестный тип {name}")

        try:
            return getattr(cls, member)
        except AttributeError:
            raise WrongValueError(f"Неизвестное значение {member}")
    else:
        return dct
