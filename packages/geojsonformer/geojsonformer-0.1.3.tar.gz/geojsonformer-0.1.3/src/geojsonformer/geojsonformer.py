import shapely.geometry as geo
import numpy as np
import json

class Feature:
    def __init__(self, id: int) -> None:
        # Main feature group
        self.id = id
        # Additional customisible features
        self.additional_features = {}

    def add_feature(self, key: str, value) -> None:
        """
        Add additional feature with a key and value pair.
        If duplicate key is added, it will overwrite the last key.
        """
        self.additional_features[f'{key}'] = value

class GeoJSON:
    def __init__(self, epsg: str = '4326'):
        self._json = self._create_base_geojson(epsg=epsg)

    def _create_base_geojson(self, epsg: str) -> dict:
        return {
            'type': 'FeatureCollection',
            "crs": { "type": "name", "properties": { "name": f'urn:ogc:def:crs:EPSG::{epsg}' } },
            'features': []
        }

    def _create_base_object(self, feature: dict) -> dict:
        return {
            'type': 'Feature',
            'properties': feature,
            'geometry': {}
        }

    def _check_object_type(self, object, expected_type: str) -> bool:
        if object.geom_type == expected_type:
            return True
        else:
            return False

    def _get_properties_from_feature(self, feature: Feature) -> dict:
        properties = {
            'Id': feature.id
        }
        properties.update(feature.additional_features)
        return properties

    def write_to_file(self, file_path: str) -> None:
        with open(file=file_path, mode='w') as json_file:
            json.dump(self._json, json_file, indent=2)

    def add_point(self, point: geo.Point, feature: Feature = Feature(0)) -> None:
        """Adds point to object.
        If provided point of wrong type raises TypeError"""
        if not self._check_object_type(point, 'Point'):
            raise TypeError('Provided polygon not of shapely.geometry.Point type.')

        new_obj = self._create_base_object(self._get_properties_from_feature(feature=feature))
        geometry = new_obj['geometry']
        geometry['type'] = 'Point'
        geometry['coordinates'] = np.asarray(point.coords).tolist()[0]

        self._json['features'].append(new_obj)

    def add_polygon(self, polygon: geo.Polygon, feature: Feature = Feature(0)) -> None:
        """Adds polygon to object.
        If provided polygon of wrong type raises TypeError"""
        if not self._check_object_type(polygon, 'Polygon'):
            raise TypeError('Provided polygon not of shapely.geometry.polygon.Polygon type.')

        new_obj = self._create_base_object(self._get_properties_from_feature(feature=feature))
        geometry = new_obj['geometry']
        geometry['type'] = 'Polygon'
        geometry['coordinates'] = [np.array(polygon.exterior.coords).tolist()]

        self._json['features'].append(new_obj)

    def add_linestring(self, line_string: geo.LineString, feature: Feature = Feature(0)) -> None:
        """Adds LineString to object.
        If provided LineString of wrong type raises TypeError"""
        if not self._check_object_type(line_string, 'LineString'):
            raise TypeError('Provided polygon not of shapely.geometry.LineString type.')

        new_obj = self._create_base_object(self._get_properties_from_feature(feature=feature))
        geometry = new_obj['geometry']
        geometry['type'] = 'LineString'
        geometry['coordinates'] = np.array(line_string.coords).tolist()

        self._json['features'].append(new_obj)
