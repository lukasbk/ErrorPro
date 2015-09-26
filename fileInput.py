import os
import re

measurements=[]
results=[]
fitParameters=[]
fits=[]
measurementLists=[]

rDescription=r"[\w ,]+"
rName=r"[\w\{\}\\]+"
rUnit=r"[\w\*\/\°]+"
rNumber=r"[\d\.\-]+"
rTerm=r"[\w\{\}\\*/\+\-\(\) ]+"
rS="\s+"
rW="\s*"

def readFiles(dir):
	for dirname, dirnames, filenames in os.walk(dir):

	    for filename in filenames:

	        if filename[-4:] == ".dat":
	        	file = open(dir+"/"+filename, 'r')
	        	lineNo=0
	        	for line in file:
	        		lineNo+=1
	        		#Kommentar oder Leerzeile
	        		match=re.match("^"+rW+"#",line)
	        		if line.strip()=="" or not match == None:
	        			continue
	        		#Measurement
	        		match=re.match(r"^"+rW+"(?:("+rDescription+")"+rS+")?("+rName+")"+rW+"="+rW+"("+rNumber+")[\s(?:\+\-)]+("+rNumber+")"+rW+"("+rUnit+")?"+rW+"$",line)
	        		if not match == None:
	        			description=match.group(1)
	        			if description == None:
	        				description=""
	        			else:
	        				description=description.strip()
	        			name=match.group(2)
	        			value=match.group(3)
	        			uncert=match.group(4)
	        			unit=match.group(5)
	        			if unit == None:
	        				unit="1"
	        			measurements.append({"name":name,"description":description,"value":value,"uncertainty":uncert,"unit":unit,"file":filename})
	        			continue
	        		#Result
	        		match=re.match("^"+rW+"(?:("+rDescription+")"+rS+")?("+rName+")"+rW+"="+rW+"("+rTerm+")"+rW+"$",line)
	        		if not match == None:
	        			description=match.group(1)
	        			if description == None:
	        				description=""
	        			else:
	        				description=description.strip()
	        			name=match.group(2)
	        			term=match.group(3)
	        			results.append({"name":name,"description":description,"value":term,"file":filename})
	        			continue
	        		#FitParameter
	        		match=re.match("^"+rW+"(?:("+rDescription+")"+rS+")?("+rName+")"+rW+"(?:\[("+rUnit+")\])?"+rW+"$",line)
	        		if not match == None:
	        			description=match.group(1)
	        			if description == None:
	        				description=""
	        			else:
	        				description=description.strip()
	        			name=match.group(2)
	        			unit=match.group(3)
	        			if unit == None:
	        				unit="1"
	        			fitParameters.append({"name":name,"description":description,"unit":unit,"file":filename})
	        			continue
	        		#gnuplot fit
	        		match=re.match("^"+rW+"[fF]it"+rW+r"\("+rW+"("+rName+")"+rW+","+rW+"("+rTerm+")"+rW+r"\)"+rW+"$",line)
	        		if not match == None:
	        			yData=match.group(1)
	        			fitFunction=match.group(2)
	        			fits.append({"yData":yData,"fitFunction":fitFunction,"file":filename})
	        			continue

	        		raise SyntaxError("Falsche Syntax in '"+filename+"', Zeile "+str(lineNo)+".")
	        elif filename[-5:] == ".list":
	        	file = open(dir+"/"+filename, 'r')
	        	
	        	quantitiesStr=file.readline().split("	")
	        	measurementsHere=[]
	        	#Erste Zeile
	        	quantityAmount=0
	        	for quantityStr in quantitiesStr:
	        		dict={}
	        		match=re.match("^"+rW+"(?:("+rDescription+")"+rS+")?("+rName+")"+rW+"(?:\(("+rNumber+")\))?"+rW+"(?:\[("+rUnit+")\])?"+rW,quantityStr)
	        		if match == None:
	        			raise SyntaxError("Erste Zeile von "+filename+" hat falsches Format.")
	        		description=match.group(1)
	        		if description == None:
        				description=""
        			else:
        				description=description.strip()
	        		dict["description"]=description
	        		dict["name"]=match.group(2)
	        		dict["uncertainty"]=match.group(3)
	        		unit=match.group(4)
	        		if unit == None:
	        			unit="1"
	        		dict["unit"]=unit
	        		dict["file"]=filename
	        		dict["values"]=[]
	        		dict["uncertainties"]=[]
	        		measurementsHere.append(dict)
	        		quantityAmount+=1

	        	#Rest
	        	number=re.compile("^"+rNumber+"$")
	        	lineCount=2
	        	for line in file:
	        		turnForValue=True
	        		count=0
	        		line=line.split("	")
	        		for value in line:
	        			if number.match(value) == None:
	        				raise SyntaxError("Werte von "+filename+" sind falsch formatiert.")

	        			if turnForValue:
	        				measurementsHere[count]["values"].append(value)
	        				if measurementsHere[count]["uncertainty"] == None:
	        					turnForValue=False
	        					print(filename)
	        				else:
	        					measurementsHere[count]["uncertainties"].append(measurementsHere[count]["uncertainty"])
	        					count+=1
	        			else:
	        				measurementsHere[count]["uncertainties"].append(value)
	        				turnForValue=True
	        				count+=1
	        		if not count == quantityAmount:
	        			raise SyntaxError("Anzahl der Werte ("+str(count)+") in "+filename+", Zeile "+str(lineCount)+" entspricht nicht der der definierten Größen ("+str(quantityAmount)+").")
	        		lineCount+=1
	        	measurementLists.extend(measurementsHere)