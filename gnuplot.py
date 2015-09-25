from quantities import *
import shlex, subprocess, os

fitCount=1

def fit(yData,fitFunction):
	global fitCount
	dataFile="plots/"+str(fitCount)+".dat"
	gpFile="plots/"+str(fitCount)+".plot"
	outputFile="plots/"+str(fitCount)+".png"
	paramsFile="plots/params_"+str(fitCount)+".dat"

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

	code=r'''
reset
set term pngcairo enhanced
set fit errorvariables
set output '%(output)s'
#set xlabel 
#set ylabel 
%(varDef)s
%(function)s
%(fit)s
%(plot)s
%(printParams)s
'''

	content={}
	content["output"]=outputFile
	content["varDef"]=""
	content["fit"]="fit f(x) '"+dataFile+"' u 1:2:3 via "
	content["printParams"]="set print '"+paramsFile+"'\n"
	i=0
	gpFunction=fitFunction.subs(xData,Symbol("x"))
	first=True
	for p in parameters:
		pname="p"+str(i)
		content["varDef"]+=pname+"=1\n"
		if not first:
			content["fit"]+=", "
		content["fit"]+=pname
		gpFunction=gpFunction.subs(p,Symbol(pname))
		content["printParams"]+="print "+pname+","+pname+"_err\n"
		i+=1
		first=False
	content["function"]="f(x)="+str(gpFunction)+"\n"
	content["plot"]="plot '"+dataFile+"' u 1:2:3 w e, f(x)"

	data=""
	for i in range(0,xData.getLength()):
		data+=str(xData.getItem(i).calculate())+"	"
		data+=str(yData.getItem(i).calculate())+"	"
		data+=str(yData.getItem(i).calculateUncertainty())+"\n"
	with open(dataFile,'w') as f:
		f.write(data)
	with open(gpFile,'w') as f:
		f.write(code%content)


	proc=subprocess.Popen(shlex.split('gnuplot '+gpFile))
	proc.communicate()

	fitCount+=1