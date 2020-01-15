import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import math
import geopandas as gpd
from shapely.ops import cascaded_union
from os import listdir
from os.path import isfile, join

inputpath = "../Output/BufferFilesCombinedDissolved/RUTA 1.shp"
datapath = "../Input/EJExportApril10/EJIndexShapefile.shp"
outputpath = "testintersect.shp"

df = gpd.read_file(inputpath)
polygon = df['geometry'][0]
# print(polygon)

data = gpd.read_file(datapath)
count = 0
total = 0
for i in range(len(data['geometry'])):
	if polygon.intersection(data['geometry'][i]):
		# print(polygon.intersection(data['geometry'][i]))
		# count += 1
		print(data['IndexAggth'][i])
		count += 1

	total += 1

print(count)
print(total)