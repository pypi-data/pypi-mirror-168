"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.

Классы базовой верификации.
"""
from abc import ABC, abstractmethod
from typing import List

from sarmat.core.context.containers import SarmatContainer
from sarmat.core.constants import ErrorCode
from sarmat.core.exceptions import SarmatException


class Verification(ABC):
    """Базовый класс проверки."""

    def __init__(self, parent=None):
        self._parent: 'Verification' = parent

    @abstractmethod
    def verify(self, subject: SarmatContainer) -> None:     # type: ignore[override]
        """Объект проверяет свои атрибуты."""
        if self._parent:
            self._parent.verify(subject)


class VerifyOnEmptyValues(Verification):
    """
    Проверка на непустоту атрибутов.

    Если атрибут отсутствует, будет вызвана ошибка.
    """

    attributes: List[str] = []

    def verify(self, subject: SarmatContainer) -> None:     # type: ignore[override]
        for attr in subject.sarmat_fields():
            if hasattr(subject, attr):
                if attr in self.attributes and not getattr(subject, attr):
                    raise SarmatException(attr, err_code=ErrorCode.NOT_FILLED)
            else:
                raise SarmatException(attr, err_code=ErrorCode.NO_ATTRIBUTE)

        super().verify(subject)
