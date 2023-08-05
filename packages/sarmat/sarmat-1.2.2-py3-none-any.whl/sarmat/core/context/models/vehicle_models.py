"""
Sarmat.

Описание сущностей.

Подвижной состав.
"""
from dataclasses import dataclass
from datetime import date
from typing import List

from sarmat.core.constants import CrewType, PermitType, VehicleType
from sarmat.core.verification import CrewVerifier, PermitVerifier, VehicleVerifier

from .sarmat_models import PersonModel, BaseIdModel, BaseUidModel
from ..containers import CrewContainer, PermitContainer, VehicleContainer


@dataclass
class VehicleModel(BaseIdModel):
    """Подвижной состав"""

    vehicle_type: VehicleType   # тип транспортного средства
    vehicle_name: str           # марка транспортного средства
    state_number: str           # гос. номер
    seats: int                  # количество мест для посадки
    stand: int = 0              # количество мест стоя
    capacity: int = 0           # вместимость багажного отделения

    @classmethod
    def from_container(cls, container: VehicleContainer) -> 'VehicleModel':     # type: ignore[override]
        VehicleVerifier().verify(container)

        return cls(
            id=container.id,
            vehicle_type=container.vehicle_type,
            vehicle_name=container.vehicle_name,
            state_number=container.state_number,
            seats=container.seats,
            stand=container.stand,
            capacity=container.capacity,
        )

    def raw(self) -> VehicleContainer:      # type: ignore[override]
        return VehicleContainer(
            id=self.id,
            vehicle_type=self.vehicle_type,
            vehicle_name=self.vehicle_name,
            state_number=self.state_number,
            seats=self.seats,
            stand=self.stand,
            capacity=self.capacity,
        )


@dataclass
class CrewModel(BaseIdModel, PersonModel):
    """Экипаж"""

    crew_type: CrewType     # тип члена экипажа
    is_main: bool = True    # признак главного члена экипажа

    @classmethod
    def from_container(cls, container: CrewContainer) -> 'CrewModel':   # type: ignore[override]
        CrewVerifier().verify(container)

        return cls(
            id=container.id,
            last_name=container.last_name,
            first_name=container.first_name,
            middle_name=container.middle_name or '',
            male=container.male,
            crew_type=container.crew_type,
            is_main=container.is_main,
        )

    def raw(self) -> CrewContainer:     # type: ignore[override]
        return CrewContainer(
            id=self.id,
            last_name=self.last_name,
            first_name=self.first_name,
            middle_name=self.middle_name,
            male=self.male,
            crew_type=self.crew_type,
            is_main=self.is_main,
        )


@dataclass
class PermitModel(BaseUidModel):
    """Путевой лист"""

    number: str                     # номер путевого листа
    permit_type: PermitType         # тип путевого листа
    depart_date: date               # дата выезда
    crew: List[CrewModel]           # экипаж
    vehicle: List[VehicleModel]     # подвижной состав

    @classmethod
    def from_container(cls, container: PermitContainer) -> 'PermitModel':   # type: ignore[override]
        PermitVerifier().verify(container)

        return cls(
            uid=container.uid,
            number=container.number,
            permit_type=container.permit_type,
            depart_date=container.depart_date,
            crew=[CrewModel.from_container(item) for item in container.crew],
            vehicle=[VehicleModel.from_container(item) for item in container.vehicle],
        )

    def raw(self) -> PermitContainer:       # type: ignore[override]
        return PermitContainer(
            uid=self.uid,
            number=self.number,
            permit_type=self.permit_type,
            depart_date=self.depart_date,
            crew=[item.raw() for item in self.crew],
            vehicle=[item.raw() for item in self.vehicle],
        )
