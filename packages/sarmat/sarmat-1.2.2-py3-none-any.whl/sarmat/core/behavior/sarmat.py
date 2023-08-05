"""
Sarmat.

Описание поведения объектов.

Объекты общего назначения.
"""
from typing import Optional

from .bases import BhCompare
from ..exceptions import IncomparableTypesError


class BhPerson(BhCompare):
    """Методы сравнения учетных записей"""
    compare_error_message = 'Учетные записи сравнению не подлежат'
    contains_error_message = 'Учетные записи проверке на вхождение не подлежат'

    first_name: str
    last_name: str
    middle_name: Optional[str]

    def __eq__(self, other):
        """Сравнение учетных записей"""
        super().__eq__(other)
        equal_names = self.last_name == other.last_name and self.first_name == other.first_name

        if equal_names:
            equal_middle = (self.middle_name is not None) and (other.middle_name is not None)
            return equal_middle and self.middle_name == other.middle_name
        return False

    def __ne__(self, other):
        """Проверка на неравенство учетных записей"""
        super().__ne__(other)
        ne_names = self.last_name != other.last_name or self.first_name != other.first_name
        ne_middles = (self.middle_name is None) and (other.middle_name is None)
        if ne_middles:
            ne_middles = self.middle_name != other.middle_name

        return ne_names or ne_middles

    def __lt__(self, other):
        """Сравнение учетных записей не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __gt__(self, other):
        """Сравнение учетных записей не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __le__(self, other):
        """Сравнение учетных записей не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __ge__(self, other):
        """Сравнение учетных записей не имеет смысла"""
        raise IncomparableTypesError(self.compare_error_message)

    def __contains__(self, item):
        """Проверка на вхождение учетных записей не имеет смысла"""
        raise IncomparableTypesError(self.contains_error_message)

    def _compare_classes(self, other):
        return isinstance(other, BhPerson)
