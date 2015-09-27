from sympy import Symbol
import units
from quantities import *
import gnuplot
import numpy as np
import latexOutput as out
import fileInput as inp


units.makeUnit("m")
units.makeUnit("s")
units.makeUnit("A")
units.makeUnit("mol")
units.makeUnit("cd")
units.makeUnit("kg")
units.makeUnit("K")

units.makeUnit("mA","A/1000")
units.makeUnit("mm","m/1000")
units.makeUnit("Hz","1/s")
#Newton
units.makeUnit("Pa","kg/m/s**2")
units.makeUnit("J","m**2*kg/s**2")
units.makeUnit("W","m**2*kg/s**3")
units.makeUnit("C","s*A")
units.makeUnit("V","m**2*kg/s**3/A")
units.makeUnit("F","s**4*A**2/m**2/kg")
units.makeUnit("ohm","m**2*kg/s**3/A**2")
#...

data={}
data["m"]=Measurement("m","",np.array([123421.124556,4.0,14]),np.array([0.0145,1.3,3]),units.parse_expr("kg"))
data["b"]=Result("b","",parse_expr("m*2",data))

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

