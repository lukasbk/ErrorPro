from sympy import Symbol
import units
import quantities as q

units.makeUnit("m")
units.makeUnit("s")
units.makeUnit("A")
units.makeUnit("mol")
units.makeUnit("cd")
units.makeUnit("kg")
units.makeUnit("K")
units.makeUnit("C","A*s")
units.makeUnit("n","kg*m/s**2")


q.newMeasurement("s",1,1,"C")
q.newMeasurementList("R",[1,2,3,4],[0.1,0.2,0.1,0.2],"A*s")
r=q.newResultList("L","R*2-s",4)
print(r.getItem(1).calculateUnit())

