from units import parse_unit
from quantities import *
import gnuplot
import numpy as np
import latexOutput as out
import fileInput as inp


data={}
data["m"]=Measurement("m","",np.float64(34),np.float64(1),"V")
data["n"]=Measurement("n","",np.float64(23),np.float64(2),"A")
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

