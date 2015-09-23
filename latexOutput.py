from sympy import latex, N, Symbol
from math import log10, floor, ceil, fabs
import shlex, subprocess, os
import units
from quantities import Measurement,Result,MeasurementList,ResultList,UnweightedMeanValue

content={}
quantities=[]
q={}


code=r'''
\documentclass[a4paper,10pt]{scrbook}
\usepackage[utf8]{inputenc}
\usepackage{latexsym,exscale,stmaryrd,amssymb,amsmath}
\begin{document}

\section*{Auswertung}

\subsection*{Ergebnisse}

%(results)s

\subsection*{Fehlerformeln}

%(formulas)s

\end{document}
'''

#Größe zur Ausgabe hinzufügen
def addQuantity(quantity):
	quantities.append(quantity)

def format(quantity):
	return formatName(quantity)+" = "+formatValue(quantity)

def formatName(quantity):
	description=quantity.getDescription()
	if not description == "":
		description=r"\text{"+description+"}\,"
	return description+quantity.name

def formatValue(quantity):
	u=quantity.calculateUncertainty().evalf(6)
	uFirstDigitPos=floor(log10(u))
	uFirstDigit=floor(u*10**(-uFirstDigitPos))
	if uFirstDigit<3:
		precision=uFirstDigitPos-1
	else:
		precision=uFirstDigitPos

	vPrecise=quantity.calculate()
	vRough=fabs(vPrecise.evalf(1))

	v=vPrecise.evalf(floor(log10(vRough))-precision+5)

	uCeiled=ceil(u*10**(-precision))/10**(-precision)
	vRounded=round(v,-precision)

	number=str(vRounded)+"\pm "+str(uCeiled)
	unit="\mathrm{"+latex(units.clearUnits(quantity.calculateUnit()))+"}"

	return "("+number+")\\,"+unit


#Ausgabe in Datei speichern
def save(filename):
	content["results"]=""
	content["formulas"]=""
	for q in quantities:
		if isinstance(q, Measurement) or isinstance(q,Result):
			content["results"]+=r'\begin{align*}'+'\n'
			content["results"]+=format(q)+'\n'
			content["results"]+=r'\end{align*}'+'\n'
		elif isinstance(q,MeasurementList) or isinstance(q,ResultList):
			content["results"]+=r"\begin{table}[htb]"+'\n'
			content["results"]+=r"\centering"+'\n'
			content["results"]+=r"\begin{tabular}{|l|}"+'\n'
			content["results"]+=r"\hline"+'\n'
			content["results"]+="$"+formatName(q)+r"$  \\ \hline"+'\n'
			for item in q.getItems():
				content["results"]+="$"+formatValue(item)+'$\n'
				content["results"]+=r"\\ \hline"+'\n'
			content["results"]+=r"\end{tabular}"+'\n'
			content["results"]+=r"\end{table}"+'\n'



	for q in quantities:
		try:
			formula=q.getUncertaintyFormula()
			for var in formula.free_symbols:
				if not (var.name[:1]=="{" and var.name[-1:]=="}"):
					formula=formula.subs(var,Symbol("{"+var.name+"}"))
			content["formulas"]+=r'\begin{align*}'
			content["formulas"]+="\\sigma_{"+q.name+"}="+latex(formula)
			content["formulas"]+=r'\end{align*}'
		except AttributeError:
			pass


	with open(filename+'.tex','w') as f:
		f.write(code%content)
	proc=subprocess.Popen(shlex.split('pdflatex '+filename+'.tex'))
	proc.communicate()
	os.unlink(filename+'.log')
	os.unlink(filename+'.aux')
