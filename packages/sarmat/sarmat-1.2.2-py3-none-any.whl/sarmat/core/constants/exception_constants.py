"""
Sarmat.

Ядро пакета.

Описание ошибок.

Типы ошибок, коды, описание.
"""
from .sarmat_constants import SarmatAttribute


class ErrorType(SarmatAttribute):
    """Тип ошибки"""

    information = 0
    question = 1
    warning = 2
    error = 3
    critical = 4

    __description__ = {
        information: 'Информация',
        question: 'Вопрос',
        warning: 'Внимание!',
        error: 'Ошибка',
        critical: 'Критическая ошибка',
    }


class ErrorClass(SarmatAttribute):
    """Классификация ошибки"""

    UNKNOWN = ''
    SYSTEM = 'S'
    DATA = 'D'
    OPERATION = 'O'

    __description__ = {
        UNKNOWN: '',
        SYSTEM: 'Системная ошибка',
        DATA: 'Ошибка данных',
        OPERATION: 'Ошибка выполнения операции',
    }


class ErrorCode(SarmatAttribute):
    """Код ошибки"""

    UNKNOWN = (-1, ErrorClass.UNKNOWN)
    NO_ERROR = (0, ErrorClass.UNKNOWN)
    NO_ATTRIBUTE = (1, ErrorClass.DATA)
    NOT_FILLED = (2, ErrorClass.DATA)
    WRONG_TYPE = (3, ErrorClass.DATA)
    WRONG_VALUE = (4, ErrorClass.DATA)
    IMPOSSIBLE_OPERATION = (5, ErrorClass.OPERATION)

    __description__ = {
        UNKNOWN: 'Неизвестная ошибка',
        NO_ERROR: '',
        NO_ATTRIBUTE: 'Отсутствует атрибут объекта',
        NOT_FILLED: 'Атрибут не заполнен',
        WRONG_TYPE: 'Неподходящий тип атрибута',
        WRONG_VALUE: 'Неверное значение',
        IMPOSSIBLE_OPERATION: 'Невозможная операция',
    }
