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
system["ohm"]=	DerivedUnit("ohm","m**2*kg/s**3/A**2",system)