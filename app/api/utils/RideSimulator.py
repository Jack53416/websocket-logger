import bisect
import numpy as np
from itertools import chain, pairwise
from typing import cast, List, Tuple

from collections import OrderedDict
from app.schemas.geojson import FeatureCollection, GeometryType


class RideSimulationException(Exception):
    pass


class RideSimulator(object):
    def __init__(self):
        self._coordinate_map: OrderedDict = OrderedDict()

    @property
    def route_length(self) -> float:
        return self._coordinate_map[next(reversed(self._coordinate_map))]

    def _find_coordinate_by_distance(self, point_distance: float) -> int:
        idx = bisect.bisect_left(list(self._coordinate_map.values()), point_distance)
        if idx != len(self._coordinate_map):
            return idx
        raise ValueError

    def load_route(self, route: FeatureCollection):
        line_strings = filter(lambda feature: feature.geometry.type == GeometryType.LINE_STRING, route.features)

        coordinates = chain.from_iterable(
            (cast(List[List[float]], line_string.geometry.coordinates) for line_string in line_strings)
        )

        self._coordinate_map = OrderedDict()

        try:
            for start, end in pairwise(coordinates):
                start, end = tuple(start), tuple(end)
                if start not in self._coordinate_map:
                    self._coordinate_map[start] = 0.0
                self._coordinate_map[end] = self._coordinate_map[start] + np.linalg.norm(
                    np.array(end) - np.array(start))
        except StopIteration:
            raise RideSimulationException("Route has no valid coordinates")

    def interpolate(self, normalized_distance: float) -> Tuple[float, float]:
        assert 0 <= normalized_distance <= 1, 'Normalized distance should have a value between 0 and 1'

        if normalized_distance == 0:
            return next(iter(self._coordinate_map))

        if normalized_distance == 1:
            return next(reversed(self._coordinate_map))

        idx = self._find_coordinate_by_distance(self.route_length * normalized_distance)
        coordinates = list(self._coordinate_map.keys())

        start = coordinates[idx - 1]
        end = coordinates[idx]

        d = self.route_length * normalized_distance - self._coordinate_map[start]
        return self.move_over_vector(start, end, d)

    @staticmethod
    def move_over_vector(v_start: Tuple[float, float],
                         v_end: Tuple[float, float],
                         dist: float) -> Tuple[float, float]:
        start, end = np.array(v_start), np.array(v_end)
        v = end - start
        u = v / np.linalg.norm(v)
        return tuple(start + dist * u)
