import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import math
import geopandas as gpd
from shapely.ops import cascaded_union
from os import listdir
from os.path import isfile, join
import csv

with open('../Input/test.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	readfile = []
	for row in reader:
		readfile += [row]

listofroutes = []
dictofrowsids = {}
dictofrowsnames = {}

for i in range(1, len(readfile)):
	threed = eval(readfile[i][1])["coordinates"]
	twodwithoutorder = [threed[j][:2] for j in range(len(threed))]
	listofroutes += [twodwithoutorder]
	dictofrowsids[i] = int(readfile[i][2])
	if readfile[i][4]:
		dictofrowsnames[i] = readfile[i][4]
	else:
		dictofrowsnames[i] = 'Empty'

shapewriter = shapefile.Writer("../Output/elevation.shp")
shapewriter.field("ID Number")
shapewriter.field("Ruta Corredor")
for i in range(len(listofroutes)):
	route = listofroutes[i]
	name = dictofrowsnames[i + 1]
	idnumber = dictofrowsids[i + 1]

	for j in range(len(route) - 1):
		shapewriter.line([[route[j], route[j+1]]])
		shapewriter.record(dictofrowsids[i + 1], dictofrowsnames[i + 1])
shapewriter.close()
