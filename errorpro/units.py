from sympy import Symbol,N,S
from sympy.core import Mul,Pow
from sympy.functions import sign
from errorpro.dimensions.dimensions import Dimension
from errorpro.dimensions.simplifiers import dim_simplify
from errorpro.dimensions.solvers import subs_symbols
from errorpro.exceptions import DimensionError
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify


def parse_unit(unit,unitSystem):
	"""
	parses a unit string or unit expression and returns (factor,dimension)
	where factor is the correction factor to get to the base unit system
	"""
	if isinstance(unit,str):
		if unit=="":
			unit=S.One
		else:
			unit=parse_expr(unit,local_dict=unitSystem)

	for u in unit.free_symbols:
		if not isinstance(u,Unit):
			raise ValueError("%s is not a unit." % u.name)

	#calculate dimension
	dim=unit
	factor=unit
	for var in unit.free_symbols:
		exp=unit.as_coeff_exponent(var)[1]
		if exp==0:
			raise ValueError("%s is not a valid unit string." % unitStr)
		dim=subs_symbols(dim,{var.name:var.dim})
		factor=factor.subs(var,var.factor)

	return (factor,dim_simplify(dim),unit)


def convert_to_unit(inputDimension,unitSystem,outputUnit=None,onlyBase=False):
	"""
	function that converts dimension to unit
	With outputUnit, you can specify a unit to convert to.
	Returns factor and unit.
	"""

	if outputUnit==None:
		outputUnit=S.One
		if inputDimension.is_dimensionless:
			return (S.One,S.One)
		assert isinstance(inputDimension,Dimension)
		factor=1

		sortedComplexities=sorted(set(map(lambda x:unitSystem[x].complexity,unitSystem)), reverse=True)
		#iterates all complexities
		for complexity in sortedComplexities:
			reciprocal=S.One
			#checks first putting in normally, then putting in reciprocally
			while True:
				#iterates all units of this complexity
				for unit in unitSystem.values():
					if (not onlyBase) or isinstance(unit,BaseUnit):
						if unit.standard and unit.complexity==complexity:
							#tries to put in as often as possible
							while True:
								if fits_in(unit,inputDimension,reciprocal):
									inputDimension=dim_simplify(inputDimension/(unit.dim**reciprocal))
									outputUnit*=unit**reciprocal
									factor*=unit.factor**reciprocal
									if inputDimension.is_dimensionless:
										return (factor,outputUnit)
								else:
									break

				if reciprocal==S.One:
					reciprocal=S.NegativeOne
				else:
					break
		assert inputDimension.is_dimensionless
	else:
		factor, dim, unit=parse_unit(outputUnit,unitSystem)
		if not inputDimension==dim:
			raise DimensionError("unit %s does not fit dimension %s." % (outputUnit,inputDimension))

	return (factor,outputUnit)

#internal
def fits_in(unit,dimension,reciprocal):
	"""
	checks if unit fits in given dimension
	reciprocal: 1 or -1 to show if unit is supposed to be fitted in as reciprocal or not
	"""
	assert isinstance(unit,Unit)
	assert isinstance(dimension,Dimension)
	assert reciprocal is S.One or reciprocal is S.NegativeOne

	for lookAtThis, unitExp in unit.dim.items():
		dimExp=dimension.get(lookAtThis,0)
		if not unitExp==0:
			if not sign(unitExp)==sign(dimExp*reciprocal):
				return False
			if not abs(unitExp)<=abs(dimExp):
				return False

	return True

class Unit(Symbol):
	"""
	class for handling unit system internally.
	Output will also be given as expressions containing Unit-objects.
	Calculations must be done with Dimension objects!
	properties:
	 - dim: corresponding dimension
	 - factor: factor with respect to base unit system
	 - complexity: number summing up all exponents
	 - standard: bool if unit should appear in output
	"""
	def __new__(cls,name):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self.name=name
		return self

class BaseUnit(Unit):
	"""
	all units forming the base unit system
	"""
	def __new__(cls,name,dim):
		self = Unit.__new__(cls, name)
		self.dim=dim
		self.factor=1
		self.complexity=1
		self.standard=True
		return self

class DerivedUnit(Unit):
	"""
	all units derived from other units
	"""
	def __new__(cls,name,dependency,unitSystem,standard=True):
		self = Unit.__new__(cls, name)
		self.standard=standard
		if isinstance(dependency,str):
			self.dependency=parse_expr(dependency,local_dict=unitSystem)
			for u in self.dependency.free_symbols:
				if not isinstance(u,Unit):
					raise ValueError("%s is not a unit." % u.name)
		else:
			self.dependency=dependency

		#calculate factor
		self.factor=self.dependency
		for var in self.dependency.free_symbols:
			exponent=self.factor.as_coeff_exponent(var)[1]
			self.factor*=var.factor**exponent
			self.factor/=var**exponent
		assert self.factor.is_number

		#calculate dimension
		dim=self.dependency
		for var in self.dependency.free_symbols:
			dim=subs_symbols(dim,{var.name:var.dim})
		self.dim=dim_simplify(dim)

		#calculate complexity
		self.complexity=0
		for exponent in self.dim.values():
			self.complexity+=abs(exponent)

		return self
