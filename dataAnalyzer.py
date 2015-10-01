from units import parse_unit
from quantities import *
import gnuplot
import numpy as np
import latexOutput as out
import fileInput as inp


data={}
data["m"]=Measurement("m","",10,1,"km/h")
data["n"]=Measurement("n","",12,1,"m/s")
data["b"]=Result("b","",parse_expr("m+n",data))

out.addQuantity(data["m"])
out.addQuantity(data["n"])
out.addQuantity(data["b"])

#inp.readFiles("data")
#for m in inp.measurements:
#	q=newMeasurement(m["name"],m["description"],m["value"],m["uncertainty"],m["unit"])
	#out.addQuantity(q)

#for m in inp.measurementLists:
#	q=newMeasurementList(m["name"],m["description"],m["values"],m["uncertainties"],m["unit"])
	#out.addQuantity(q)

#for m in inp.results:
#	q=newResult(m["name"],m["description"],m["value"])
#	out.addQuantity(q,"extra")

#for m in inp.fitParameters:
#	q=newFitParameter(m["name"],m["description"],m["unit"])
#	out.addQuantity(q)

#for m in inp.fits:
#	gnuplot.fit(parse_expr(m["yData"]),parse_expr(m["fitFunction"]))

out.save("test")

