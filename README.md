# dataAnalyzer
python script to calculate physical quantities from data including units and uncertainty propagation

# ToDo

- Darum kümmern, dass N,I,O? als Variablen verwendet werden können
- Einheitensystem!
- SI-System implementieren, m,c,d,k,M als Vorfaktoren?, clearUnits optimieren
- Latex-Ausgabe verbessern
- Regressionen
- Performance-Verbesserungen / Calculate-Caching?
- GnuPlot-Erweiterung

# Run it

To use it, you need python3, sympy and pdflatex. On Ubuntu:

sudo apt-get install python3

sudo apt-get install python3-pip

sudo pip3 install sympy

For pdflatex, you need some latex packages, I'm not sure.


Then, run:

python3 dataAnalyser.py
