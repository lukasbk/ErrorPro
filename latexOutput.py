from sympy import latex
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

\end{document}
'''

def addQuantity(quantity):
	quantities.append(quantity)
	content["a"]=2
	print("1")

def test():
	content["a"]=2

def save(filename):
	print("2")
	content["results"]="aaa"
	for q in quantities:
		content["results"]=""
		content["results"]+=r'\begin{align*}'
		content["results"]+=q.name+"= ("+str(q.calculate())+"\pm "+\
							str(q.calculateUncertainty())+")"\
							+"\mathrm{"+latex(units.clearUnits(q.calculateUnit()))+"}"
		content["results"]+=r'\end{align*}'

	with open(filename+'.tex','w') as f:
		f.write(code%content)
	proc=subprocess.Popen(shlex.split('pdflatex '+filename+'.tex'))
	proc.communicate()
	os.unlink(filename+'.log')
	os.unlink(filename+'.aux')
