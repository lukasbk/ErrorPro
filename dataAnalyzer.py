from sympy import Symbol
import units
from quantities import *
import gnuplot
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

#TODO Dateien und Abhängigkeit der Größen auf groups der Ausgabe weiterleiten

inp.readFiles("data")
for m in inp.measurements:
	q=newMeasurement(m["name"],m["description"],m["value"],m["uncertainty"],m["unit"])
	out.addQuantity(q)

for m in inp.measurementLists:
	q=newMeasurementList(m["name"],m["description"],m["values"],m["uncertainties"],m["unit"])
	out.addQuantity(q)

for m in inp.results:
	q=newResult(m["name"],m["description"],m["value"])
	out.addQuantity(q,"extra")

m=newFitParameter("m","")
b=newFitParameter("b","")
gnuplot.fit(parse_expr("L"),parse_expr("m*P+b"))
out.addQuantity(m)
out.addQuantity(b)

out.save("test")

