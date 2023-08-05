"""
Sarmat.

Ядро пакета.

Фабрика классов.
"""

__all__ = [
    'SarmatCreator', 'SarmatBaseCreator', 'SarmatGeoCreator', 'SarmatTrafficManagementCreator', 'SarmatVehicleCreator',
]


from .base_creator import SarmatBaseCreator
from .geo_creator import SarmatGeoCreator
from .traffic_manager_creator import SarmatTrafficManagementCreator
from .vehicle_creator import SarmatVehicleCreator


class SarmatCreator(
    SarmatBaseCreator,
    SarmatGeoCreator,
    SarmatTrafficManagementCreator,
    SarmatVehicleCreator,
):
    """Класс являет собой композицию фабричных методов"""
