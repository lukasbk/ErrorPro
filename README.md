# dataAnalyzer
python script to calculate physical quantities from data including units and uncertainty propagation

# ToDo

- Messdaten aus Dateien lesen (Einzelmessungen, Konstanten, Messreihen, abhängige Größen)
- SI-System implementieren, m,c,d,k,M als Vorfaktoren?, clearUnits optimieren
- Formschöne Ausgabe von Zahlen (Einheiten gut formatiert, Wert und Fehler in der Form "(5 +- 1)")
- Latex-Ausgabe der Fehlerformel
- Mittelwertberechnung einer Liste (gewichtet/nicht gewichtet?)
- Regressionen?
- Performance-Verbesserungen?
- GnuPlot-Erweiterung?

# Run it

To use it, you need python3 and sympy. In Ubuntu:

sudo apt-get install python3

sudo apt-get install python3-pip

sudo pip3 install sympy


Then, run:

python3 dataAnalyser.py
