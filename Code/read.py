import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import math
import geopandas as gpd
from shapely.ops import cascaded_union
from os import listdir
from os.path import isfile, join

inputpath = "../Output/elevation.shp"
inputdf = gpd.read_file(inputpath)
print(inputdf)