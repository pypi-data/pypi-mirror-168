"""
Sarmat.

Описание действий с объектами.

Базовые классы.
"""


class ActionMixin:
    """Базовый класс-примесь для описания работы с объектами"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def copy(self):
        raise NotImplementedError
