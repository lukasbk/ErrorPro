from sympy import Symbol
import units
import quantities as q
import latexOutput
from sympy.physics.unitsystems.simplifiers import qsimplify

a=q.newMeasurement("s",1,0.1,"V*A")
e=q.newMeasurement("e",1,0.1,"V*A")
b=q.newResult("B","s+e")
c=q.newMeasurementList("l",[1,2,1,2,2],[1,1,1,1,1],"Pa")
d=q.newUnweightedMeanValue("m",c)

#latexOutput.addQuantity(q.newMeasurement("s_1",1437,13,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_2",1144100,6660,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_3",0.003,0.1,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_4",0.00007,0.000000001,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_5",14,1,"V*A"))
#latexOutput.addQuantity(q.newMeasurement("s_6",41.88,2.9,"V*A"))

#latexOutput.addQuantity(q.newResult("T","sqrt((s_2-s_1)/s_3-s_2)"))

#latexOutput.save("test")

