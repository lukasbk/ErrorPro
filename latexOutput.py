from sympy import latex, N, Symbol
from math import log10, floor, ceil, fabs
import shlex, subprocess, os
import units
from quantities import *

content={}
quantities={}
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
def addQuantity(quantity,group="default"):
	if not group in quantities:
		quantities[group]=[]
	quantities[group].append(quantity)

def format(quantity):
	return formatName(quantity)+" = "+formatValue(*quantity.getResult())

def formatName(quantity):
	longname=quantity.getLongname()
	if not longname == "":
		longname=r"\text{"+longname+"}\,"
	return longname+quantity.name

# TODO
# Ausgabe der Floats ohne 10er-Potenzen oder unnötigen Nullen
# bzw. mit 10er-Potenzen, wenn gewollt
# Benutzen des Latex-Pakets siunitx
def formatValue(value,uncertainty,unit):

	uFirstDigitPos=floor(log10(uncertainty))
	uFirstDigit=floor(uncertainty*10**(-uFirstDigitPos))
	if uFirstDigit<3:
		precision=uFirstDigitPos-1
	else:
		precision=uFirstDigitPos

	uCeiled=ceil(uncertainty*10**(-precision))/10**(-precision)
	vRounded=round(value,-precision)

	if precision>=0:
		viewPrecision="0"
	else:
		viewPrecision=str(-precision)
	number=("{v:."+viewPrecision+"f}\pm {u:."+viewPrecision+"f}").format(v=vRounded,u=uCeiled)
	unit="\mathrm{"+latex(unit)+"}"

	return "("+number+")\\,"+unit


#Ausgabe in Datei speichern
def save(filename):
	content["results"]=""
	content["formulas"]=""
	for group in quantities:
		tables={}
		for q in quantities[group]:
			if q.getLength()==1:
				content["results"]+=r'\begin{align*}'+'\n'
				content["results"]+=format(q)+'\n'
				content["results"]+=r'\end{align*}'+'\n'
			else:
				if not q.getLength() in tables:
					tables[q.getLength()]=[]
				tables[q.getLength()].append(q)
		for length in tables:
			amount=len(tables[length])
			content["results"]+=r"\begin{table}[htb]"+'\n'
			content["results"]+=r"\centering"+'\n'
			content["results"]+=r"\begin{tabular}{|"+("l|"*amount)+"}"+'\n'
			content["results"]+=r"\hline"+'\n'
			first=True
			for q in tables[length]:
				if not first:
					content["results"]+=" & "
				content["results"]+="$"+formatName(q)+"$"
				first=False
			content["results"]+=r"  \\ \hline"+'\n'
			
			values=[]
			uncerts=[]
			units=[]
			for q in tables[length]:
				value,uncert,unit=q.getResult()
				values.append(value)
				uncerts.append(uncert)
				units.append(unit)
			for valueKey in range(0,length):
				first=True
				for quantityKey in range(0,len(tables[length])):
					if not first:
						content["results"]+=" & "
					content["results"]+="$"+formatValue(values[quantityKey][valueKey],uncerts[quantityKey][valueKey],units[quantityKey])+"$"
					first=False
				content["results"]+=r"\\ \hline"+'\n'
			content["results"]+=r"\end{tabular}"+'\n'
			content["results"]+=r"\end{table}"+'\n'


	for group in quantities:
		for q in quantities[group]:
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
