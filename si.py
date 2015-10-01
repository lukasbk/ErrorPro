from sympy.physics.unitsystems.dimensions import Dimension
from units import BaseUnit,DerivedUnit

length=Dimension(length=1)
time=Dimension(time=1)
mass=Dimension(mass=1)
current=Dimension(current=1)
temperature=Dimension(temperature=1)
amount=Dimension(amount=1)
luminosity=Dimension(luminosity=1)

system={}
system["m"]=	BaseUnit("m",length)
system["s"]=	BaseUnit("s",time)
system["kg"]=	BaseUnit("kg",mass)
system["A"]=	BaseUnit("A",current)
system["K"]=	BaseUnit("K",temperature)
system["mol"]=	BaseUnit("mol",amount)
system["cd"]=	BaseUnit("cd",luminosity)

system["V"]=	DerivedUnit("V","m**2*kg/A/s**3",system)
system["Ohm"]=	DerivedUnit("Ohm","m**2*kg/s**3/A**2",system)
system["N"]=	DerivedUnit("N","kg*m/s**2",system)
system["Pa"]=	DerivedUnit("Pa","kg/m/s**2",system)
system["J"]=	DerivedUnit("J","N*m",system)
# ...

system["Hz"]=	DerivedUnit("Hz","1/s",system,standard=False)
system["min"]=	DerivedUnit("min","60*s",system,standard=False)
system["h"]=	DerivedUnit("h","3600*s",system,standard=False)

def extend_by_prefixes(unit,system):
	for prefix,factor in [("m",1/1000),("k",1000),("M",1000000)]:
		system[prefix+unit.name]=DerivedUnit(prefix+unit.name,unit*factor,system,standard=False)


systemCopy=system.copy()
for name in systemCopy:
	if not name=="kg":
		extend_by_prefixes(system[name],system)

system["mg"]=	DerivedUnit("mg","1/1000000*kg",system,standard=False)
system["g"]=	DerivedUnit("g","1/1000*kg",system,standard=False)
system["Mg"]=	DerivedUnit("Mg","1000*kg",system,standard=False)

print(system)