from map.utilities import JSON_ENCODER_FIX
from addict import Dict
import os
import json


class Geojson:
    """
     Get geo json format
    """
    common_json = Dict({
        "type": "FeatureCollection",
        "features": []
    })

    # TODO will look for optimizing
    @staticmethod
    def convertGeojsonData(rows, pointDistance, line):
        result = []
        for row in rows:
            row_as_dict = dict(row)
            result.append(row_as_dict)

        # output is the main content, rowOutput is the content from each record returned
        output = ""
        rowOutput = ""
        i = 0
        while i < len(result):

            firstCoord = (json.loads(result[i]['geometry']))
            firstHeading = (json.loads(str(result[i]['heading'])))
            hash = str(result[i]['hash'])
            imgname = str(result[i]['imgname'])

            url = f'https://cdn.mapilio.com{hash}/{imgname}'
            result1 = firstCoord['coordinates']

            try:
                secondCoord = (json.loads(result[i + int(pointDistance)]['geometry']))
                result2 = secondCoord['coordinates']
            except IndexError:
                pass

            if result[i]['geometry'] is not None:
                coordinates = [
                    result1,
                    result2
                ]

                generateCoord = json.dumps({'type': 'Point', 'coordinates': coordinates})
                # If it's the first record, don't add a comma
                comma = "," if i > 0 else ""
                rowOutput = comma + '{"type": "Feature", "geometry": ' + str(generateCoord) + ', "properties": {'
                properties = ""

                j = 0
                comma = "," if j > 0 else ""
                properties += comma + '"' + "geom" + '":"' + str(result[i]['geom']) + '"'
                # j += 1

                rowOutput += properties + ', "lines":' + str(line) + ',"heading":' + str(firstHeading) + \
                             ',"url":' + f"\"{url}\"" + '}'
                rowOutput += '}'

                output += rowOutput

            # start over
            rowOutput = ""

            i += int(pointDistance)

        # Assemble the GeoJSON
        totalOutput = '{ "type": "FeatureCollection", "features": [ ' + output + ' ]}'

        return totalOutput

    @staticmethod
    def get_geo_json(**kwargs) -> Dict:
        """
        Geo json Features format
        params kwargs |
            lat : str
            lon : str
            avg_score : int
            class_code : str
            area : float
            height: float
            width : float
            confidence : float
            matchedPoints : list
            type: str,
            feature: dict
        """
        params = Dict(kwargs)

        if params.type == "Point":
            geom_type = {
                "type": params.type,
                "coordinates": [
                    params.lon,
                    params.lat
                ]
            }
        # TODO it will be use
        if params.type == "Polygon":
            geom_type = {
                "type"          : params.type,
                "coordinates"   : params.segmentation
            }
        return Dict(
            {
                "type": "Feature",
                "properties": {
                    "average_score"     : params.avg_score,
                    "class_code"        : params.class_code,
                    "area"              : params.area,
                    "height"            : params.height,
                    "width"             : params.width,
                    "confidence"        : params.confidence,
                    "match_id"          : params.match_id,
                    "matchedPoints"     : params.matchedPoints,
                    "feature"           : params.feature
                },
                "geometry": geom_type
            })

    @staticmethod
    def convert_dict_to_geojson(params: Dict, type: str) -> json:
        for key, value in params.items():
            value = Dict(value)
            geojsonFormat = Geojson.get_geo_json(
                lat=value.lat,
                lon=value.lon,
                class_code=value.class_code,
                area=value.area,
                score=value.average_score,
                key=key,
                type=type)
            Geojson.common_json.features.append(geojsonFormat)

        return Geojson.common_json


    @staticmethod
    def create_geojson_format(input: dict) -> dict:
        geoform = []
        for key, params in input.items():
            if Dict(params).geojson:
                params = Dict(params).geojson
                geoform.append(Geojson.get_geo_json(**params))
            else:
                continue

        return geoform

    @staticmethod
    def export(points: dict, file_id: str, type: str):
        """
        Export geo json format
        """
        Geojson.common_json.features = points
        with open(os.path.join('Exports', file_id, f'{type}_detected_points.json'), 'w') as f:
            json.dump(Geojson.common_json, f, cls=JSON_ENCODER_FIX)

        return Geojson.common_json