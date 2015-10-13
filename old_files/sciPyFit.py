from quantities import *
import numpy as np
from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
from sympy import N

# Funktioniert irgendwie noch nicht richtig

def fit(yData,fitFunction):
	if not isinstance(yData, QuantityList):
		raise TypeError("y-Daten müssen vom Typ QuantityList sein.")
	xData=None
	parameters=[]
	for var in fitFunction.free_symbols:
		if not isinstance(var,FitParameter):
			if xData==None and isinstance(var,QuantityList):
				xData=var
			else:
				raise ValueError("Fit-Funktion enthält mehr als eine Liste.")
		else:
			parameters.append(var)
	if xData==None:
		raise ValueError("Fit-Funktion enthält keine Liste.")
	if not xData.getLength()==yData.getLength():
		raise ValueError("Listen haben nicht die gleiche Länge.")

	list=[xData]
	list.extend(parameters)
	func=lambdify(tuple(list),fitFunction,"numpy")

	xnumbers=[]
	for item in xData.getItems():
		xnumbers.append(float(N(item.calculate())))

	ynumbers=[]
	for item in yData.getItems():
		ynumbers.append(float(N(item.calculate())))

	sigma=[]
	for item in yData.getItems():
		sigma.append(float(N(item.calculateUncertainty())))

	print(xnumbers,ynumbers,sigma)

	popt, pcov = curve_fit(func,xnumbers,ynumbers,sigma=sigma)
	#perr = np.sqrt(np.diag(pcov))

	print(popt)


