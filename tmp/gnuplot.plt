
reset
set term pngcairo enhanced
set output 'tmp/gnuplot.png'
set xlabel ' [s]'
set ylabel ' [ms]'

f0(x) = 3000.0*x

plot f0(x) title '3*x', 'tmp/data0' with xerrorbars title 'y'
