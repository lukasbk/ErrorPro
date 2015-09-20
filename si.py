from sympy.physics.unitsystems.dimensions import Dimension, DimensionSystem
from sympy.physics.unitsystems.units import Unit, UnitSystem, Constant
from sympy.physics.unitsystems.prefixes import PREFIXES, prefix_unit
from sympy.physics.unitsystems.simplifiers import qsimplify



# base dimensions
length = Dimension(name="length", symbol="L", length=1)
mass = Dimension(name="mass", symbol="M", mass=1)
time = Dimension(name="time", symbol="T", time=1)
current = Dimension(name='current', symbol='I', current=1)
temperature = Dimension(name='temperature', symbol='Teta', temperature=1)
amount = Dimension(name='amount', symbol='N', amount=1)
luminosity = Dimension(name='luminosity', symbol='J', luminosity=1)

# derived dimensions
velocity = Dimension(name="velocity", length=1, time=-1)
acceleration = Dimension(name="acceleration", length=1, time=-2)
momentum = Dimension(name="momentum", mass=1, length=1, time=-1)
force = Dimension(name="force", symbol="F", mass=1, length=1, time=-2)
energy = Dimension(name="energy", symbol="E", mass=1, length=2, time=-2)
power = Dimension(name="power", length=2, mass=1, time=-3)
pressure = Dimension(name="pressure", mass=1, length=-1, time=-2)
frequency = Dimension(name="frequency", symbol="f", time=-1)
action = Dimension(name="action", symbol="A", length=2, mass=1, time=-1)

voltage = Dimension(name='voltage', symbol='U', mass=1, length=2, current=-1,
                    time=-3)
impedance = Dimension(name='impedance', symbol='Z', mass=1, length=2,
                      current=-2, time=-3)
conductance = Dimension(name='conductance', symbol='G', mass=-1, length=-2,
                      current=2, time=3)
capacitance = Dimension(name='capacitance', mass=-1, length=-2, current=2,
                        time=4)
inductance = Dimension(name='inductance', mass=1, length=2, current=-2, time=-2)
charge = Dimension(name='charge', symbol='Q', current=1, time=1)
magnetic_density = Dimension(name='charge', symbol='B', mass=1, current=-1,
                             time=-2)
magnetic_flux = Dimension(name='charge', length=2, mass=1, current=-1, time=-2)

dims = (velocity, acceleration, momentum, force, energy, power, pressure,
        frequency, action, voltage, impedance, conductance, capacitance, inductance, charge,
        magnetic_density, magnetic_flux)

# dimension system
si_dim = DimensionSystem(base=(length, mass, time, current, temperature, amount, luminosity), dims=dims, name="SI")

# base units
m = Unit(length, abbrev="m")
kg = Unit(mass, abbrev="g", prefix=PREFIXES["k"])
s = Unit(time, abbrev="s")
A = Unit(current, abbrev='A')
K = Unit(temperature, abbrev='K')
mol = Unit(amount, abbrev='mol')
cd = Unit(luminosity, abbrev='cd')

# gram; used to define its prefixed units
g = Unit(mass, abbrev="g")


# derived units
J = Unit(energy, factor=10**3, abbrev="J")
N = Unit(force, factor=10**3, abbrev="N")
W = Unit(power, factor=10**3, abbrev="W")
Pa = Unit(pressure, factor=10**3, abbrev="Pa")
Hz = Unit(frequency, abbrev="Hz")

V = Unit(voltage, factor=10**3, abbrev='V')
ohm = Unit(impedance, factor=10**3, abbrev='ohm')
# siemens
S = Unit(conductance, factor=10**-3, abbrev='S')
# farad
F = Unit(capacitance, factor=10**-3, abbrev='F')
# henry
H = Unit(inductance, factor=10**3, abbrev='H')
# coulomb
C = Unit(charge, abbrev='C')
# tesla
T = Unit(magnetic_density, abbrev='T')
# weber
Wb = Unit(magnetic_flux, abbrev='Wb')

# constants
# Newton constant
G = Constant(qsimplify(m**3*kg**-1*s**-2).as_unit, factor=6.67384e-11, abbrev="G")
# speed of light
c = Constant(velocity, factor=299792458, abbrev="c")

units = [m, g, s, A, K, mol, cd, J, N, W, Pa, Hz, V, ohm, S, F, H, C, T, Wb]
all_units = []
all_units.extend(units)
for u in units:
    all_units.extend(prefix_unit(u, PREFIXES))
all_units.extend([G, c])


# unit system
system = UnitSystem(base=(m, kg, s, A, K, mol, cd), units=all_units, name="SI")