from imageObjects import ContourObject

from shapely.geometry import Polygon, GeometryCollection, mapping
from miscSupports import flatten, shapely_points_to_array
from vectorObjects.DefinedVectors import Vector2D


class PolySupport:
    def __init__(self, polygon):
        """
        Sometimes we will need the shapely library when working with images, to take advantage of its easy to use
        intersections or other abilities. This class adds a few extra methods for working with geospatial shapes,
        specifically geared towards options that maybe useful when a polygon has been create from images.

        :param polygon: The polygon or group of polygons via GeoCollection you wish to work with
        :type polygon: Polygon | GeometryCollection
        """
        self.polygon = polygon

    def position_extract(self, position, merge_nested=False):
        """
        Sometimes you may wish to extract the most extreme position of a Polygon, such as the left, right, top or bottom
        most point of it. This will extract this point for each shape within the polygon.

        If merge nested is set to be True, then only the most extreme point, of the list of extreme points, will be
        returned

        :param position: left - right - top - bottom
        :param merge_nested: By default all extreme positions of each shape is returned, if True then only the most
            extreme point is returned

        :return: A list of VectorObjects if not set to merge else a VectorObject
        :rtype: list[Vector2D] | Vector2D
        """
        assert position in ("left", "right", "top", "bottom"), "position takes the value of left, right, top or bottom"

        # For each possible shape within our collection of shapes, extract the extreme position
        points_list = []
        if isinstance(self.polygon, GeometryCollection):
            for shape in self.polygon:
                points_list.append(self._extract_extreme_position(position, shape))

        else:
            points_list.append(self._extract_extreme_position(position, self.polygon))

        # Flatten the list, return it if not set to merge otherwise construct another ContourObject and get the extreme
        # from this list of points
        points_list = flatten(points_list)
        if merge_nested:
            return getattr(ContourObject(shapely_points_to_array(points_list)), position)
        else:
            return points_list

    @staticmethod
    def _extract_extreme_position(position, shape):
        """Depending on the type of the mapped object this will return the position of each object"""
        map_dict = mapping(shape)

        if map_dict["type"] == "Polygon":
            return [getattr(ContourObject(shapely_points_to_array(part)), position)
                    for part in map_dict["coordinates"] if len(part) > 1]

        elif map_dict["type"] == "LineString":
            return [getattr(ContourObject(shapely_points_to_array(map_dict["coordinates"])), position)]

        elif map_dict["type"] == "Point":
            return [getattr(ContourObject(shapely_points_to_array([map_dict["coordinates"]])), position)]

        else:
            raise Exception(f"Unexpected type {map_dict['type']} found within _extract_extreme_position")
