import os

measurements=[]
results=[]
measurementLists=[]

def readFiles(dir):
	for dirname, dirnames, filenames in os.walk(dir):

	    for filename in filenames:

	        if filename[-4:] == ".dat":
	        	file = open(dir+"/"+filename, 'r')

	        	for line in file:
	        		if "=" in line:
	        			line=line.partition("=")
	        			#Variablenname
	        			name=line[0].strip()
	        			if not name.isalpha():
	        				raise IOError("Variablenname '"+name+"' besteht nicht nur aus Buchstaben.")

	        			if line[2].find("+-") == -1:
	        			#Result
	        				value=line[2].strip()
	        				results.append({"name":name,"value":value})
	        			else:
	        			#Measurement
	        				line2=line[2].rpartition(" ")

	        				#Einheit
	        				unit=line2[2].strip()

	        				line3=line2[0].partition("+-")
	        				#Wert
	        				value=line3[0].strip()
	        				#Fehler
	        				uncert=line3[2].strip()
	        				measurements.append({"name":name,"value":value,"uncertainty":uncert,"unit":unit})
	        elif filename[-5:] == ".list":
	        	file = open(dir+"/"+filename, 'r')
	        	
	        	qs=file.readline().split("	")
	        	measurementsHere=[]
	        	for q in qs:
	        		dict={}
	        		q=q.partition("[")
	        		#Name
	        		dict["name"]=q[0].strip()
	        		if not dict["name"].isalpha():
	        			raise IOError("Variablenname '"+dict["name"]+"' besteht nicht nur aus Buchstaben.")


	        		#Einheit
	        		dict["unit"]=q[2].strip()
	        		if not dict["unit"][-1:] == "]":
	        			raise IOError("Falsche Formatierung der ersten Zeile")
	        		dict["unit"]=dict["unit"][:-1]
	        		dict["values"]=[]
	        		dict["uncertainties"]=[]
	        		measurementsHere.append(dict)

	        	for line in file:
	        		turnForValue=True
	        		mCount=0
	        		line=line.split("	")
	        		for v in line:
	        			if turnForValue:
	        				measurementsHere[mCount]["values"].append(v)
	        				turnForValue=False
	        			else:
	        				measurementsHere[mCount]["uncertainties"].append(v)
	        				turnForValue=True
	        				mCount+=1
	        	measurementLists.extend(measurementsHere)