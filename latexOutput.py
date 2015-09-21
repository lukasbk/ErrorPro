from sympy import latex, N
from math import log10, floor, ceil
import shlex, subprocess, os
import units

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
	u=quantity.calculateUncertainty().evalf(6)

	uFirstDigitPos=floor(log10(u))
	uFirstDigit=floor(u*10**(-uFirstDigitPos))
	if uFirstDigit<3:
		precision=uFirstDigitPos-1
	else:
		precision=uFirstDigitPos

	vPrecise=quantity.calculate()
	vRough=vPrecise.evalf(1)
	v=vPrecise.evalf(floor(log10(vRough))-precision+5)

	uCeiled=ceil(u*10**(-precision))/10**(-precision)
	vRounded=round(v,-precision)

	number=str(vRounded)+"\pm "+str(uCeiled)
	unit="\mathrm{"+latex(units.clearUnits(quantity.calculateUnit()))+"}"

	return quantity.name+" = ("+number+")\\,"+unit



#Ausgabe in Datei speichern
def save(filename):
	content["results"]=""
	content["formulas"]=""
	for q in quantities:
		content["results"]+=r'\begin{align*}'
		content["results"]+=format(q)
		content["results"]+=r'\end{align*}'

	for q in quantities:
		try:
			formula=q.getUncertaintyFormula()
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
