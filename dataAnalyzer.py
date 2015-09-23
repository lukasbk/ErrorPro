from sympy import Symbol
import units
from quantities import *
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

inp.readFiles("data")
for m in inp.measurements:
	q=newMeasurement(m["name"],m["description"],m["value"],m["uncertainty"],m["unit"])
	out.addQuantity(q)

for m in inp.measurementLists:
	q=newMeasurementList(m["name"],m["description"],m["values"],m["uncertainties"],m["unit"])
	out.addQuantity(q)

for m in inp.results:
	q=newResult(m["name"],m["description"],m["value"])
	out.addQuantity(q)



#a=q.newMeasurement("s",1,0.1,"V*A")
#b=q.newResult("B","s*3")
#c=q.newMeasurementList("l",[1,2,1,2,2],[1,1,1,1,1],"Pa")
#d=q.newUnweightedMeanValue("m",c)

#latexOutput.addQuantity(q.newMeasurement("s_1",1437,13,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_2",1144100,6660,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_3",0.003,0.1,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_4",0.00007,0.000000001,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_5",14,1,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_6",41.88,2.9,"V*A"))

#latexOutput.addQuantity(q.newResult("T","sqrt((s_2-s_1)/s_3-s_2)"))

out.save("test")

