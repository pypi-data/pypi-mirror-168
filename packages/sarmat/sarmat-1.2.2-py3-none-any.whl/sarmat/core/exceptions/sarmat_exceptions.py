"""
Sarmat.

Ядро пакета.

Описание ошибок.

Кастомные ошибки.
"""
from __future__ import absolute_import

from sarmat.core.constants import ErrorCode

from .exceptions import SarmatException


class IncomparableTypesError(SarmatException):

    def __init__(self, *args, err_code=None):
        super().__init__(*args, err_code=ErrorCode.WRONG_TYPE)


class WrongValueError(SarmatException):
    def __init__(self, *args, err_code=None):
        super().__init__(*args, err_code=ErrorCode.WRONG_VALUE)


class ImpossibleOperationError(SarmatException):
    def __init__(self, *args, err_code=None):
        super().__init__(*args, err_code=ErrorCode.IMPOSSIBLE_OPERATION)
