import os
from addict import Dict
from folium import folium, features
import folium


class ShapeOperations:
    """
    Shape Operatings
    Draw Line
    Add Point
    """

    def __init__(self, map):
        self.map = map

    def addPoint(self, kwargs: Dict,
                 area: float = None,
                 color: str = 'darkgreen',
                 type: str = 'point'):
        """
        Add point
        """
        if type == 'point':
            params = Dict(kwargs)
            objectImage_1 = os.path.join(os.getcwd(), params.detectedPath_1)  #
            objectImage_2 = os.path.join(os.getcwd(), params.detectedPath_2)

            area = '{:.3f}'.format(area)
            html = "<section class="'container'" style="'width:450px'"> \
                        <div class="'value'"> \
                            <b>MatchId = </b> {id1}  <br>  <b>Area = </b> {area} square meter </br>\
                            <b>Classname = </b> {classname} </br>\
                            <b>ObjectId 1 = </b> {objectId_1} </br>\
                            <b>ObjectId 2 = </b> {objectId_2} </br>\
                            <img src={detectedObjectPath_1} style="'width:auto;height:80px;'"> \
                            <img src={detectedObjectPath_2} style="'width:auto;height:80px;'"> \
                            <a href="'{imgUrl_1}'">Panorma Url - 1 </a> \
                            <a href="'{imgUrl_2}'">Panorma Url - 2 </a> \
                        </div> \
                    </section>".format(id1=str(params.match_id), area=area,
                                       detectedObjectPath_1=objectImage_1,
                                       detectedObjectPath_2=objectImage_2,
                                       imgUrl_1=params.imgUrl_1,
                                       imgUrl_2=params.imgUrl_2,
                                       classname=params.classname,
                                       objectId_1=params.objId_1,
                                       objectId_2=params.objId_2)

            svg_icon_path = os.path.join(os.getcwd(), 'Config', 'icon', params.classname + '.svg')
            icon = folium.DivIcon(html=f"""
                        <div>
                        <img src = "{svg_icon_path}" width="30px" "/>
                        </div>""")

            mk = features.Marker([params.Lat_center, params.Lon_center],
                                 popup=html, icon=icon)

            mk_p = folium.Circle([params.Lat_center, params.Lon_center], # noqa
                                 radius=2,
                                 fill=True,
                                 fill_color="yellow",
                                 color="yellow",
                                 fill_opacity=0.4)

            self.map.add_child(mk)
            self.map.add_child(mk_p)

        if type == 'paired':
            for point in kwargs:
                mk = features.Marker(point,
                                     popup=None, icon=folium.Icon(color=color, icon_color='#FFFF00'))

                self.map.add_child(mk)

    def addPolyline(self, des, classname, obj, color):
        """
        Poly line drawing
        """
        folium.PolyLine(
            locations=des,
            color=color,
            opacity=4,
            tooltip=classname + "-" + str(obj),
            weight=4
        ).add_to(self.map)
        pass

    def triggerMapOperations(self, mapDrawPoint):
        """
        processing coming point data
        """

        for key, params in mapDrawPoint.items():
            params = Dict(params)
            if params.mapOp == "polyline":
                self.addPolyline(des=params.desPoint, classname=params.classname, obj=key, color=params.color)
            elif params.mapOp == "point":
                self.addPoint(kwargs=params.point, area=params.object['area'], color="red", type=params.mapOp)
            elif params.mapOp == "paired":
                pass
                # self.addPoint(kwargs=params.pairedPoint, area=None, color="gray", type=params.mapOp)
            else:
                continue
