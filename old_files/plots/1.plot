
reset
set term pngcairo enhanced
set fit errorvariables
set output 'plots/1.png'
#set xlabel 
#set ylabel 
p0=1
p1=1

f(x)=p0 + p1*x

fit f(x) 'plots/1.dat' u 1:2:3 via p0, p1
plot 'plots/1.dat' u 1:2:3 w e, f(x)
set print 'plots/params_1.dat'
print p0,p0_err
print p1,p1_err

