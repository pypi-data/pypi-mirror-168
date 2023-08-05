"""
Sarmat.

Ядро пакета.

Фабрика классов.

Базовый класс-фабрика.
"""
from collections import defaultdict
from typing import Any, Dict, List

from sarmat.core.actions import (
    ADestinationPointMixin,
    AGeoLocationMixin,
)
from sarmat.core.behavior import (
    BhDestinationPoint,
    BhDirection,
    BhGeo,
    BhNoAction,
    BhPeriod,
    BhPeriodItem,
    BhRoadName,
)
from sarmat.core.context.containers import (
    PeriodItemContainer,
    PeriodContainer,
)
from sarmat.core.context.models import (
    DestinationPointModel,
    DirectionModel,
    GeoModel,
    PeriodItemModel,
    PeriodModel,
    RoadNameModel,
)


class SarmatCreator:
    """Базовый класс-фабрика."""

    # хранилище тегов
    role_tags: Dict[str, List[BhNoAction]] = defaultdict(list)

    @classmethod
    def register_class(cls, tag: str, cls_behavior: Any) -> None:
        """
        Регистрация поведенческого класса
        Args:
            tag: тэг
            cls_behavior: поведенческий класс
        """
        sub_tags = tag.split('.')

        for sub_tag in sub_tags:
            classes = cls.role_tags[sub_tag]

            if classes and cls_behavior in classes:
                idx = classes.index(cls_behavior)
                cls.role_tags[sub_tag][idx] = cls_behavior
            else:
                cls.role_tags[sub_tag].append(cls_behavior)

    def _get_behavior_classes(self, tag: str) -> List[BhNoAction]:
        """Получение списка поведенческих классов по тегу"""
        sub_tags = tag.split('.')

        roles: list = []
        for item in sub_tags:
            role = self.role_tags.get(item)
            if role:
                roles.extend(role)

        return roles or [BhNoAction]


class SarmatBaseCreator(SarmatCreator):
    """Класс-фабрика для базовых объектов"""

    def create_period_item(self, tag: str, container: PeriodItemContainer) -> PeriodItemModel:
        """Создание объекта 'Период'"""
        period_item_model = PeriodItemModel.from_container(container)
        return self.make_period_item_from_model(tag, period_item_model)

    def make_period_item_from_model(self, tag: str, model: PeriodItemModel) -> PeriodItemModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhPeriodItem, *classes, PeriodItemModel])

        PeriodItem = type('PeriodItem', parents, {"permission_tag": tag, "controller": self})   # type: ignore
        return PeriodItem(**model.as_dict)

    def create_period(self, tag: str, container: PeriodContainer) -> PeriodModel:
        period_model = PeriodModel.from_container(container)
        return self.make_period_from_model(tag, period_model)

    def make_period_from_model(self, tag: str, model: PeriodModel) -> PeriodModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhPeriod, *classes, PeriodModel])

        Period = type('Period', parents, {"permission_tag": tag, "controller": self})   # type: ignore

        period = None
        if model.period:
            period = self.make_period_item_from_model(tag, model.period)

        periods = []
        if model.periods:
            periods = [self.make_period_item_from_model(tag, item) for item in model.periods]

        return Period(
            **{
                **model.as_dict,
                'period': period,
                'periods': periods,
            },
        )


class RoadNameCreatorMixin(SarmatCreator):
    def make_road_name_from_model(self, tag: str, model: RoadNameModel) -> RoadNameModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([BhRoadName, *classes, RoadNameModel])

        RoadName = type('RoadName', parents, {"permission_tag": tag, "controller": self})  # type: ignore

        return RoadName(**model.as_dict)


class DirectionCreatorMixin(SarmatCreator):
    def make_direction_from_model(self, tag: str, model: DirectionModel) -> DirectionModel:
        classes: List[BhNoAction] = self._get_behavior_classes(tag)
        parents = tuple([BhDirection, *classes, DirectionModel])

        Direction = type('Direction', parents, {"permission_tag": tag, "controller": self})  # type: ignore
        return Direction(**model.as_dict)


class GeoObjectCreatorMixin(SarmatCreator):
    def make_geo_object_from_model(self, tag: str, model: GeoModel) -> GeoModel:
        classes = self._get_behavior_classes(tag)
        parents = tuple([AGeoLocationMixin, BhGeo, *classes, GeoModel])

        GeoObject = type('GeoObject', tuple(parents), {"permission_tag": tag, "controller": self})  # type: ignore

        parent = None
        if model.parent:
            parent = self.make_geo_object_from_model(tag, model.parent)

        return GeoObject(
            **{
                **model.as_dict,
                'parent': parent,
            },
        )


class DestinationPointCreatorMixin(GeoObjectCreatorMixin):
    def make_destination_point_from_model(self, tag: str, model: DestinationPointModel) -> DestinationPointModel:
        classes: List[BhNoAction] = self._get_behavior_classes(tag)
        parents = tuple([ADestinationPointMixin, BhDestinationPoint, *classes, DestinationPointModel])

        DestinationPoint = type(
            'DestinationPoint',
            parents,  # type: ignore
            {"permission_tag": tag, "controller": self},
        )

        state = None
        if model.state:
            state = self.make_geo_object_from_model(tag, model.state)

        return DestinationPoint(
            **{
                **model.as_dict,
                'state': state,
            },
        )
