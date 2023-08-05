"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.

Веификация объектов для работы с подвижным составом.
"""
from sarmat.core.constants import ErrorCode
from sarmat.core.context.containers import CrewContainer, PermitContainer
from sarmat.core.exceptions import WrongValueError

from .base_verifications import VerifyOnEmptyValues


class VehicleVerifier(VerifyOnEmptyValues):
    """Класс верификации подвижного состава"""

    attributes = ['vehicle_type', 'vehicle_name', 'state_number', 'seats']


class CrewVerifier(VerifyOnEmptyValues):
    """Класс верификации экипажа"""

    attributes = ['crew_type', 'last_name', 'first_name']

    def verify(self, subject: CrewContainer) -> None:  # type: ignore[override]
        super().verify(subject)

        if subject.male is None:
            raise WrongValueError('Crew gender is undefined')


class PermitVerifier(VerifyOnEmptyValues):
    """Верификауия путевых листов"""

    attributes = ['number', 'permit_type', 'depart_date']

    def verify(self, subject: PermitContainer) -> None:      # type: ignore[override]
        super().verify(subject)
        verify_code = ErrorCode.NOT_FILLED

        if not subject.crew:
            raise WrongValueError(
                'Crew must be filled',
                err_code=verify_code,
            )

        if not subject.vehicle:
            raise WrongValueError(
                'Vehicle must be filled',
                err_code=verify_code,
            )
