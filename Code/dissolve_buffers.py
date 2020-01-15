import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import math
import geopandas as gpd
from shapely.ops import cascaded_union
from os import listdir
from os.path import isfile, join

inputpath = "../Output/BufferFilesCombined/"
onlyshpfiles = [f for f in listdir(inputpath) if '.shp' in f]
outputpath = "../Output/BufferFilesCombinedDissolved/"

for f in onlyshpfiles:
    df = gpd.read_file(join(inputpath, f))
    polygons = df['geometry']
    boundary = gpd.GeoSeries(cascaded_union(polygons))
    boundary.to_file(filename=join(outputpath,f),driver='ESRI Shapefile')