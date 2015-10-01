from sympy import Symbol,N
from sympy.core import Mul,Pow
from sympy.physics.unitsystems.simplifiers import dim_simplify
from sympy.parsing.sympy_parser import parse_expr

#überprüft local_dict, ob es auch Sachen nicht gibt?
#write_as_unit muss sich um Faktoren kümmern

def parse_unit(unitStr,unitSystem):
	"""
	parses a unit string and returns (factor,dimension)
	where factor is the correction factor to get to the base unit system
	"""
	unit=parse_expr(unitStr,local_dict=unitSystem)


	factor=unit
	for var in unit.free_symbols:
		exponent=factor.as_coeff_exponent(var)[1]
		factor*=var.factor**exponent
		factor/=var**exponent
	if not factor.is_number:
		raise ValueError("%s is not a valid unit string." % unitStr)

	
	dim=unit
	for var in unit.free_symbols:
		exp=unit.as_coeff_exponent(var)[1]
		if exp==0:
			raise ValueError("%s is not a valid unit string." % unitStr)
		dim=dim.subs(var,var.dim)
	return (factor,dim_simplify(dim))


def write_as_unit(inputDimension,unitSystem):
	"""
	function that converts dimension into units
	very ugly...
	doesn't look at factors so far
	"""
	if inputDimension.is_number:
		return 1
	outputUnit=1
	sortedUnits=sorted(unitSystem.values(),key=lambda u: -u.complexity)
	for unit in sortedUnits:
		if unit.standard:
			tryAgain=True
			while(tryAgain):
				tryAgain=False

				for baseDimension,exponent in unit.dim.items():
					#checks if unit dimension fits into input dimension
					inputExponent=inputDimension.get(baseDimension,0)
					if inputExponent>0:
						if exponent<0 or exponent>inputExponent:
							#this is when dimension doesn't fit
							break
					elif inputExponent<0:
						if exponent>0 or exponent<inputExponent:
							#this is when dimension doesn't fit
							break
					else:
						if not exponent==0:
							break
				else:
					#if it fits, unit will be used and it will try to fit it in again
					outputUnit*=unit
					inputDimension=dim_simplify(inputDimension/unit.dim)
					tryAgain=True
				if isinstance(inputDimension,int) or inputDimension.is_number:
					break

			if isinstance(inputDimension,int) or inputDimension.is_number:
				break

			tryAgain=True
			while(tryAgain):
				tryAgain=False

				for baseDimension,exponent in unit.dim.items():
					#checks if unit dimension fits reciprocal into input dimension
					inputExponent=inputDimension.get(baseDimension,0)
					if inputExponent>0:
						if exponent>0 or abs(exponent)>inputExponent:
							#this is when dimension doesn't fit
							break
					elif inputExponent<0:
						if exponent<0 or exponent>abs(inputExponent):
							#this is when dimension doesn't fit
							break
					else:
						if not exponent==0:
							break
				else:
					#if it fits, unit will be used and it will try to fit it in again
					outputUnit/=unit
					inputDimension=dim_simplify(inputDimension*unit.dim)
					tryAgain=True
				if isinstance(inputDimension,int) or inputDimension.is_number:
					break


		if isinstance(inputDimension,int) or inputDimension.is_number:
			break
	assert isinstance(inputDimension,int) or inputDimension.is_number
	return outputUnit


class Unit(Symbol):
	"""
	class for handling units and output
	calculations must be done with Dimension!
	dim: corresponding dimension
	factor: factor with respect to base unit system
	complexity: number summing up all exponents
	standard: bool if unit should appear in output
	"""
	def __new__(cls,name):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self.name=name
		return self

class BaseUnit(Unit):
	def __new__(cls,name,dim,standard=True):
		self = Unit.__new__(cls, name)
		self.dim=dim
		self.factor=1
		self.complexity=1
		self.standard=standard
		return self

class DerivedUnit(Unit):
	def __new__(cls,name,dependency,unitSystem,standard=True):
		"""
		class for units that are derived from base units
		"""
		self = Unit.__new__(cls, name)
		self.standard=standard
		if isinstance(dependency,str):
			self.dependency=parse_expr(dependency,local_dict=unitSystem)
		else:
			self.dependency=dependency
		
		self.factor=self.dependency
		for var in self.dependency.free_symbols:
			exponent=self.factor.as_coeff_exponent(var)[1]
			self.factor*=var.factor**exponent
			self.factor/=var**exponent
		assert self.factor.is_number

		dim=self.dependency
		for var in self.dependency.free_symbols:
			dim=dim.subs(var,var.dim)
		self.dim=dim_simplify(dim)

		self.complexity=0
		for exponent in self.dim.values():
			self.complexity+=abs(exponent)

		return self