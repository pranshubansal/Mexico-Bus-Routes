from shapely.geometry import LineString
from math import radians, cos, sin, asin, sqrt
import csv

# Calculates distance between 2 GPS coordinates
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1.60934

with open('../Input/test.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	readfile = []
	for row in reader:
		readfile += [row]

listofroutes = []
listofids = []
dictofids = {}
dictofnames = {}

for i in range(1, len(readfile)):
	threed = eval(readfile[i][1])["coordinates"]
	twodwithoutorder = [threed[j][:2] for j in range(len(threed))]
	listofroutes += [twodwithoutorder]
	dictofids[int(readfile[i][2])] = i
	listofids += [readfile[i][2]]
	if readfile[i][4] in dictofnames.keys():
		dictofnames[readfile[i][4]] += [readfile[i][2]]
	elif readfile[i][4] == '':
		if 'Empty' not in dictofnames.keys():
			dictofnames['Empty'] = [readfile[i][2]]
		else:
			dictofnames['Empty'] += [readfile[i][2]]
	else:
		dictofnames[readfile[i][4]] = [readfile[i][2]]

listofdistbyids = []
for route in listofroutes:
	total = 0
	for i in range(len(route) - 1):
		total += haversine(route[i][1], route[i][0], route[i+1][1], route[i+1][0])
	listofdistbyids.append(total)

dictofdistancesbyid = {}
for i in range(len(listofids)):
	dictofdistancesbyid[listofids[i]] = listofdistbyids[i]

dictofdistancesbyroutename = {}
for name in dictofnames.keys():
	dictofdistancesbyroutename[name] = sum([dictofdistancesbyid[id] for id in dictofnames[name]])

print(dictofdistancesbyid)
print(dictofdistancesbyroutename)