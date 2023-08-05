"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.

Веификация объектов для работы с маршрутной сетью.
"""
from collections import defaultdict

from sarmat.core.context.containers import (
    JourneyBunchContainer,
    RouteContainer,
    RouteItemContainer,
)
from sarmat.core.exceptions import WrongValueError

from .base_verifications import VerifyOnEmptyValues


class StationVerifier(VerifyOnEmptyValues):
    """Класс верификации станций"""

    attributes = ['station_type', 'name', 'point']


class RouteItemVerifier(VerifyOnEmptyValues):
    """Верификауия состава маршрута"""

    attributes = ['length_from_last_km', 'travel_time_min', 'order']

    def verify(self, subject: RouteItemContainer) -> None:  # type: ignore[override]
        super().verify(subject)

        if not(subject.station or subject.point):
            raise WrongValueError(
                'Route item must have station or destination point',
            )


class RouteVerifier(VerifyOnEmptyValues):
    """Верификауия маршрута"""

    attributes = ['name', 'first_station', 'structure']

    def verify(self, subject: RouteContainer) -> None:      # type: ignore[override]
        super().verify(subject)

        route_item_verifier = RouteItemVerifier()
        for idx, route_item in enumerate(subject.structure):
            route_item_verifier.verify(route_item)

            if route_item.order != idx+1:
                raise WrongValueError(
                    f'Wrong item number ({route_item.order}). Expected {idx+1}',
                )


class JourneyVerifier(RouteVerifier):
    """Верификация рейса"""

    attributes = RouteVerifier.attributes + ['journey_type', 'departure_time']


class JourneyBunchItemVerifier(VerifyOnEmptyValues):
    """Верификация элемента связки"""

    attributes = ['journey']


class JourneyBunchVerifier(VerifyOnEmptyValues):
    """Верификация связки"""

    attributes = ['journeys']

    def verify(self, subject: JourneyBunchContainer) -> None:       # type: ignore[override]
        super().verify(subject)
        journey_counters: defaultdict = defaultdict(int)

        journey_verifier = JourneyBunchItemVerifier()
        for journey in subject.journeys:
            journey_verifier.verify(journey)
            if journey.id:
                journey_counters[journey.id] += 1

        not_unique_journeys = [j for j, c in journey_counters.items() if c > 1]
        if not_unique_journeys:
            raise WrongValueError(f'Journeys {not_unique_journeys} has got more that one time')
