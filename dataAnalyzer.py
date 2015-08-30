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
latexOutput.addQuantity(a)
latexOutput.addQuantity(b)
latexOutput.test()
latexOutput.save("test")

