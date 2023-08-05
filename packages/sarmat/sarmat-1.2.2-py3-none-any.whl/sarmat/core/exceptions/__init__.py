"""
Sarmat.

Ядро пакета.

Описание ошибок.
"""

__all__ = ('SarmatException', 'IncomparableTypesError', 'SarmatExceptionInfo', 'SarmatWarning', 'SarmatQuestion',
           'SarmatCritical', 'ImpossibleOperationError', 'WrongValueError')

from .exceptions import SarmatException, SarmatExceptionInfo, SarmatWarning, SarmatQuestion, SarmatCritical
from .sarmat_exceptions import ImpossibleOperationError, IncomparableTypesError, WrongValueError
