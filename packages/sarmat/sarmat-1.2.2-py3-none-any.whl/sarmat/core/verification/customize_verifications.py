from typing import Callable, Dict

from sarmat.core.context.containers import SarmatContainer

from .base_verifications import Verification


class CustomizedVerification(Verification):
    """Расширяемый класс верификации"""

    verification_map: Dict[str, Callable] = {}

    def verify(self, subject: SarmatContainer) -> None:     # type: ignore[override]
        for attr, call in self.verification_map.items():
            call(attr, subject)

        super().verify(subject)
