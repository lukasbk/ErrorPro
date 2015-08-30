from sympy import Symbol
import units
import quantities as q
import latexOutput

units.makeUnit("m")
units.makeUnit("s")
units.makeUnit("A")
units.makeUnit("mol")
units.makeUnit("cd")
units.makeUnit("kg")
units.makeUnit("K")
#Newton
units.makeUnit("Pa","kg/m/s**2")
units.makeUnit("J","m**2*kg/s**2")
units.makeUnit("W","m**2*kg/s**3")
units.makeUnit("C","s*A")
units.makeUnit("V","m**2*kg/s**3/A")
units.makeUnit("F","s**4*A**2/m**2/kg")
units.makeUnit("Ohm","m**2*kg/s**3/A**2")
#...


a=q.newMeasurement("s",1,0.1,"V*A")
b=q.newResult("B","s*3")
c=q.newMeasurementList("l",[1,2,1,2,2],[1,1,1,1,1],"Pa")
d=q.newUnweightedMeanValue("m",c)

latexOutput.addQuantity(q.newMeasurement("s_1",1437,13,"V*A"))
latexOutput.addQuantity(q.newMeasurement("s_2",1144100,6660,"V*A"))
latexOutput.addQuantity(q.newMeasurement("s_3",0.003,0.1,"V*A"))
latexOutput.addQuantity(q.newMeasurement("s_4",0.00007,0.000000001,"V*A"))
latexOutput.addQuantity(q.newMeasurement("s_5",14,1,"V*A"))
latexOutput.addQuantity(q.newMeasurement("s_6",41.88,2.9,"V*A"))

latexOutput.addQuantity(q.newResult("T","sqrt((s_2-s_1)/s_3-s_2)"))

latexOutput.save("test")

