import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import math
import geopandas as gpd
from shapely.ops import cascaded_union
from os import listdir
from os.path import isfile, join

def shapely_to_pyshp(shapelygeom):
    # first convert shapely to geojson
    try:
        shapelytogeojson = shapely.geometry.mapping
    except:
        import shapely.geometry
        shapelytogeojson = shapely.geometry.mapping
    geoj = shapelytogeojson(shapelygeom)
    # create empty pyshp shape
    record = shapefile.Shape()
    # set shapetype
    if geoj["type"] == "Null":
        pyshptype = 0
    elif geoj["type"] == "Point":
        pyshptype = 1
    elif geoj["type"] == "LineString":
        pyshptype = 3
    elif geoj["type"] == "Polygon":
        pyshptype = 5
    elif geoj["type"] == "MultiPoint":
        pyshptype = 8
    elif geoj["type"] == "MultiLineString":
        pyshptype = 3
    elif geoj["type"] == "MultiPolygon":
        pyshptype = 5
    record.shapeType = pyshptype
    # set points and parts
    if geoj["type"] == "Point":
        record.points = geoj["coordinates"]
        record.parts = [0]
    elif geoj["type"] in ("MultiPoint","Linestring"):
        record.points = geoj["coordinates"]
        record.parts = [0]
    elif geoj["type"] in ("Polygon"):
        record.points = geoj["coordinates"][0]
        record.parts = [0]
    elif geoj["type"] in ("MultiPolygon","MultiLineString"):
        index = 0
        points = []
        parts = []
        for eachmulti in geoj["coordinates"]:
            points.extend(eachmulti[0])
            parts.append(index)
            index += len(eachmulti[0])
        record.points = points
        record.parts = parts
    return record


idinputpath = "../Output/BufferShapefiles/"
routeinputpath = "../Output/BufferFilesCombinedDissolved/"

idshpfiles = [f for f in listdir(idinputpath) if '.shp' in f]
routeshpfiles = [f for f in listdir(routeinputpath) if '.shp' in f]

datapath = "../Input/EJExportApril10/EJIndexShapefile.shp"
idoutputpath = "../Output/IntersectID/"
routeoutputpath = "../Output/IntersectRoute/"

def intersect(inputpath, outputpath):
    inputdf = gpd.read_file(inputpath)
    inputpolygon = inputdf['geometry'][0]
    data = gpd.read_file(datapath)

    shapewriter = shapefile.Writer(outputpath)
    shapewriter.field("IndexAggth")
    for i in range(len(data['geometry'])):
    	if inputpolygon.intersection(data['geometry'][i]):
    		converted_shape = shapely_to_pyshp(inputpolygon.intersection(data['geometry'][i]))
    		shapewriter.shape(converted_shape)
    		shapewriter.record(data["IndexAggth"][i])
    shapewriter.close()

for idfile in idshpfiles:
    intersect(idinputpath + idfile, idoutputpath + idfile)

for routefile in routeshpfiles:
    intersect(routeinputpath + routefile, routeoutputpath + routefile)
