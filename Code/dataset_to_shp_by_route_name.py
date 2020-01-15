import csv, os
import shapefile

with open('../Input/test.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	readfile = []
	for row in reader:
		readfile += [row]

listofroutes = []
dictofids = {}
dictofnames = {}

for i in range(1, len(readfile)):
	threed = eval(readfile[i][1])["coordinates"]
	twodwithoutorder = [threed[j][:2] for j in range(len(threed))]
	twod = [threed[j][:2] + [j + 1] for j in range(len(threed))]
	listofroutes += [twod]
	dictofids[int(readfile[i][2])] = i
	if readfile[i][4] in dictofnames.keys():
		dictofnames[readfile[i][4]] += [int(readfile[i][2])]
	elif readfile[i][4] == '':
		if 'Empty' not in dictofnames.keys():
			dictofnames['Empty'] = [int(readfile[i][2])]
			os.mkdir('../Output/BusRoutesByRouteName/Empty/')
		else:
			dictofnames['Empty'] += [int(readfile[i][2])]
	else:
		dictofnames[readfile[i][4]] = [int(readfile[i][2])]
		os.mkdir('../Output/BusRoutesByRouteName/{}/'.format(readfile[i][4]))

	if readfile[i][4] == '':
		w = shapefile.Writer('../Output/BusRoutesByRouteName/Empty/{}'.format(readfile[i][2]), shapeType=3)
	else:
		w = shapefile.Writer('../Output/BusRoutesByRouteName/{}/{}'.format(readfile[i][4], readfile[i][2]), shapeType=3)
	w.field('name', 'C')
	w.record("linestring")
	w.line([twodwithoutorder])
	w.close()

for name in dictofnames.keys():
	array = dictofnames[name]
	w = shapefile.Writer('../Output/BusRoutesCombinedByRouteName/{}'.format(name))
	w.field('name', 'C')
	for i in array:
		x = eval(readfile[dictofids[i]][1])["coordinates"]
		y = [x[j][:2] for j in range(len(x))]
		w.line([y])
		w.record("linestring")
	w.close()
