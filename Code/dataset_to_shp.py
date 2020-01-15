import csv
from shape import shapefile

with open('../Input/test.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	readfile = []
	for row in reader:
		readfile += [row]

listofroutes = []
listofnames = []
for i in range(1, len(readfile)):
	threed = eval(readfile[i][1])["coordinates"]
	twodwithoutorder = [threed[j][:2] for j in range(len(threed))]
	twod = [threed[j][:2] + [j + 1] for j in range(len(threed))]
	listofroutes += [twod]
	listofnames += [readfile[i][2]]

	# with open("{}".format(listofnames[i-1]) + ".csv", "w") as f:
	# 	writer = csv.writer(f)
	# 	writer.writerows(listofroutes[i-1])

	# w = shapefile.Writer('{}'.format(listofnames[i-1]), shapeType=8)
	# w.field('name', 'C')
	# w.record("multipoint")
	# w.multipoint(twodwithoutorder)
	# w.close()
	w = shapefile.Writer('{}'.format(listofnames[i-1]), shapeType=3)
	w.field('name', 'C')
	w.record("linestring")
	w.line([twodwithoutorder])
	w.close()
