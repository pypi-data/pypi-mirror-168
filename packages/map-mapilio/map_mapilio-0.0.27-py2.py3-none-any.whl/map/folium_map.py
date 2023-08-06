import os.path
import folium


class FoliumMap:

    @staticmethod
    def create_map(file_id: str, type: str):
        m = folium.Map(location=[37, 0],
                       zoom_start=2.5,
                       tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                       attr='My Data Attribution')

        geojson = os.path.join('Exports', file_id, f'{type}_detected_points.json')

        g = folium.GeoJson(
            geojson,
            name='geojson'
        ).add_to(m)

        folium.GeoJsonTooltip(fields=["average_score", "class_code", "confidence"]).add_to(g)

        m.save(os.path.join('Exports', file_id, f'{type}_index.html'))
