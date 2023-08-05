"""
Sarmat.

Ядро пакета.

Описание ошибок.

Классы ошибок.
"""
from __future__ import absolute_import

from typing import Optional

from sarmat.core.constants import ErrorCode, ErrorType


class SarmatException(Exception):
    """Базовый класс ошибки."""

    error_type = ErrorType.error

    def __init__(self, *args, err_code: Optional[ErrorCode] = None):
        super().__init__(*args)

        self._err_code = err_code or ErrorCode.UNKNOWN
        self._code, self._err_class = self._err_code.value

    def __str__(self):
        message = '\n'.join([str(i) for i in self.args])
        error_description = self.error_type.as_text(self.error_type)
        class_description = self._err_class.as_text(self._err_class)
        code_description = self._err_code.as_text(self._err_code)
        return f'''
        ({self.error_type.value}) {error_description}
        {class_description}
        {self._code}: {code_description}
        {message}
        '''


class SarmatExceptionInfo(SarmatException):
    """Обработка информационного исключения"""

    error_type = ErrorType.information


class SarmatWarning(SarmatException):
    """Обработка предупреждающего исключения"""

    error_type = ErrorType.warning


class SarmatQuestion(SarmatException):
    """Обработка вопросительного исключения"""

    error_type = ErrorType.question


class SarmatCritical(SarmatException):
    """Обработка критического исключения"""

    error_type = ErrorType.critical
