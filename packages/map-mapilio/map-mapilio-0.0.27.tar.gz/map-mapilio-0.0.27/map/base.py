import os

from folium import folium, plugins
from folium.plugins import MeasureControl, Draw
import folium
import re
import ast


class Map:
    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
            geojsonData
        """
        self.__dict__.update(kwargs)

        self.map = self._create()
        self._gps_point_tracer()

    def _create(self):
        self.map = folium.Map(location=[41.105645123000002, 28.790535551000001],
                              tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga', attr="google",
                              max_zoom=25,
                              control_scale=True, zoom_start=16)

        self.map.add_child(MeasureControl())
        self.map.fit_bounds(self.zoom_data, max_zoom=15)
        Draw(export=True).add_to(self.map)
        self._compass()
        return self.map

    def _compass(self):
        kw = {
            'prefix': 'fa',
            'color': 'green',
            'icon': 'arrow-up'
        }

        # angle = 180
        # icon = folium.Icon(angle=angle, **kw)
        # folium.Marker(location=[36.893651, 30.616286], icon=icon, tooltip=str(angle)).add_to(self.map)
        #
        # angle = 45
        # icon = folium.Icon(angle=angle, **kw)
        # folium.Marker(location=[36.893651, 30.616686], icon=icon, tooltip=str(angle)).add_to(self.map)

    def _gps_point_tracer(self):
        geojson = ast.literal_eval(re.search('({.+})', self.geojsonData).group(0)) # because of coming data dict in str
        outlines = folium.FeatureGroup("outlines")
        line_bg = folium.FeatureGroup("lineBg")
        bus_lines = folium.FeatureGroup("busLines")
        bus_stops = folium.FeatureGroup("busStops")

        line_weight = 6
        line_colors = ["red", "#08f", "#0c0", "#f80"]
        stops = []
        headings = []
        urls = []
        for line_segment in geojson["features"]:

            # Get every bus line coordinates
            segment_coords = [[x[1], x[0]] for x in line_segment["geometry"]["coordinates"]]
            # Get bus stops coordinates
            stops.append(segment_coords[0])
            stops.append(segment_coords[-1])
            headings.append(line_segment["properties"]["heading"])
            headings.append(line_segment["properties"]["heading"])
            urls.append(line_segment["properties"]["url"])
            urls.append(line_segment["properties"]["url"])


            # Get number of bus lines sharing the same coordinates
            lines_on_segment = line_segment["properties"]["lines"]
            # Width of segment proportional to the number of bus lines
            segment_width = len(lines_on_segment) * (line_weight + 1)
            # For the white and black outline effect
            folium.PolyLine(
                segment_coords, color="#000", weight=segment_width + 5, opacity=1
            ).add_to(outlines)
            folium.PolyLine(
                segment_coords, color="#fff", weight=segment_width + 3, opacity=1
            ).add_to(line_bg)
            # Draw parallel bus lines with different color and offset
            for j, line_number in enumerate(lines_on_segment):
                plugins.PolyLineOffset(
                    segment_coords,
                    color=line_colors[line_number],
                    weight=line_weight,
                    opacity=1,
                    offset=j * (line_weight + 1) - (segment_width / 2) + ((line_weight + 1) / 2),
                ).add_to(bus_lines)

        # Draw bus stops
        for stop, heading, url in zip(stops, headings, urls):
            kw = {
                'prefix': 'fa',
                'color': 'green',
                'icon': 'arrow-up',
            }

            angle = int(heading)
            icon = folium.Icon(angle=angle, **kw)  # TODO look after for vehicle car bearing
            # folium.Marker(location=stop, icon=icon, tooltip=str(angle)).add_to(bus_stops)

            html = "<section class="'container'" style="'width:450px'"> \
                                    <div class="'value'"> \
                                        <a href="'{imgUrl}'">Panorma Image </a> \
                                    </div> \
                                </section>".format(imgUrl=url)

            folium.Marker(
                stop,
                color="#000",
                fill_color="#ccc",
                fill_opacity=1,
                radius=10,
                weight=3,
                tooltip=2,
                opacity=1,
                icon=icon,
                popup=html
            ).add_to(bus_stops)

        # outlines.add_to(self.map)
        # line_bg.add_to(self.map)
        # bus_lines.add_to(self.map)
        bus_stops.add_to(self.map)

    def saveMap(self, file_id):
        self.map.save(os.path.join('Exports',file_id, "map.html"))
