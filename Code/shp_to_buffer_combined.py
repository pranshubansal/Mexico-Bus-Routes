import shapefile, shapely, shapely.geometry
from shapely.geometry import shape
import csv, os, math

#in meters
distance = 500 
city_lat = 19.4326
city_lon = 99.1332
m_per_deg_lat = 111132.954 - 559.822 * math.cos(2*city_lat) + 1.175 * math.cos(4*city_lat);
m_per_deg_lon = 111132.954 * math.cos(city_lat);
avg_m = (m_per_deg_lon + m_per_deg_lat)/2
degrees = distance/avg_m

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
        else:
            dictofnames['Empty'] += [int(readfile[i][2])]
    else:
        dictofnames[readfile[i][4]] = [int(readfile[i][2])]

for i in dictofnames.keys():
    

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

    # WRITE TO SHAPEFILE USING PYSHP
    shapewriter = shapefile.Writer("../Output/BufferFilesCombined/{}.shp".format(i))
    shapewriter.field("field1")
    
    for name in dictofnames[i]:
        # Reading Shapefile
        sampleshape = shapefile.Reader("../Output/ShapefilesPolyLine/{}.shp".format(name))

        # Reading its records
        feature = sampleshape.shapeRecords()[0]

        # Converting it into GeoJSON
        first = feature.shape.__geo_interface__  

        # Converting it into a shapely object
        sampleshapely = shape(first)

        # Creating a buffer
        shapebuffer = sampleshapely.buffer(degrees)
        # step1: convert shapely to pyshp using the function above
        converted_shape = shapely_to_pyshp(shapebuffer)

        # step2: tell the writer to add the converted shape
        shapewriter.shape(converted_shape)
        # add a list of attributes to go along with the shape
        shapewriter.record(["empty record"])
    shapewriter.close()