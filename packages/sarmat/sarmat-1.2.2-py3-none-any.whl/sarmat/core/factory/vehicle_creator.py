"""
Sarmat.

Ядро пакета.

Фабрика классов.

Класс для создания объектов путевой документации.
"""
from sarmat.core.behavior import (
    BhCrew,
    BhPermit,
    BhVehicle,
)
from sarmat.core.context.containers import (
    CrewContainer,
    PermitContainer,
    VehicleContainer,
)
from sarmat.core.context.models import (
    CrewModel,
    PermitModel,
    VehicleModel,
)

from .base_creator import SarmatCreator


class SarmatVehicleCreator(SarmatCreator):
    """Класс-фабрика для создания объектов путевой документации."""

    def create_crew(self, tag: str, container: CrewContainer) -> CrewModel:
        crew_model = CrewModel.from_container(container)
        return self.make_crew_from_model(tag, crew_model)

    def make_crew_from_model(self, tag: str, model: CrewModel) -> CrewModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhCrew, *classes, CrewModel])

        Crew = type('Crew', parents, {"permission_tag": tag, "controller": self})    # type: ignore
        return Crew(**model.as_dict)

    def create_permit(self, tag: str, container: PermitContainer) -> PermitModel:
        """Создание объекта 'Путевой лист'"""
        permit_model = PermitModel.from_container(container)
        return self.make_permit_from_model(tag, permit_model)

    def make_permit_from_model(self, tag: str, model: PermitModel) -> PermitModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhPermit, *classes, PermitModel])

        Permit = type('Permit', parents, {"permission_tag": tag, "controller": self})   # type: ignore

        crew = []
        if model.crew:
            crew = [self.make_crew_from_model(tag, item) for item in model.crew]

        vehicle = []
        if model.vehicle:
            vehicle = [self.make_vehicle_from_model(tag, item) for item in model.vehicle]

        return Permit(
            **{
                **model.as_dict,
                'crew': crew,
                'vehicle': vehicle,
            },
        )

    def create_vehicle(self, tag: str, container: VehicleContainer) -> VehicleModel:
        """Создание объекта 'Транспортное средство'"""
        vehicle_model = VehicleModel.from_container(container)
        return self.make_vehicle_from_model(tag, vehicle_model)

    def make_vehicle_from_model(self, tag: str, model: VehicleModel) -> VehicleModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhVehicle, *classes, VehicleModel])

        Vehicle = type('Vehicle', parents, {"permission_tag": tag, "controller": self})     # type: ignore

        return Vehicle(**model.as_dict)
