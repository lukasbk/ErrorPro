import units
from quantities import *
import gnuplot
import numpy as np
import latexOutput as out
import fileInput as inp


data={}
data["m"]=Measurement("m","",np.array([123421.124556,4.0,14]),np.array([0.0145,1.3,3]),units.parse_expr("V"))
data["n"]=Measurement("n","",np.array([123421.124556,4.0,14]),np.array([0.0145,1.3,3]),units.parse_expr("A"))
data["b"]=Result("b","",parse_expr("2*m/n",data))

out.addQuantity(data["m"])
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

