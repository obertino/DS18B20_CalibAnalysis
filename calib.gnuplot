#set xdata time
#set timefmt "%d/%m/%Y %H:%M:%S"
#set format x "%M:%S"
#set format y "%3.1E"
set termoption dash
#set yrange [-5:30]
set terminal pngcairo enhanced font "arial,16" fontscale 1.0 size 1024, 768
set grid

#t(x)=a+b*exp(-x*(1/c)-x*(1/d))
#a=0.5
#b=10
#c=5
#d=30

set datafile separator ";"

#get start time from first measurement
start=system("awk -F ';' 'FNR == 1 {print $1}' calibrazione_ghiaccio.dat")

#set fit logfile

if (!exists("filename")) filename='calibrazione.dat'

#print strptime("%d/%m/%Y %H:%M:%S",start)
set table "calib.dat"
#set output "plots/temp.png"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 pi -1 ps 1.5
#fit t(x) filename using (strptime("%d/%m/%Y %H:%M:%S",strcol(1))-strptime("%d/%m/%Y %H:%M:%S",start)):3:(0.1) via a,b,c,d
#plot time in s from first measurement
plot filename using (strptime("%d/%m/%Y %H:%M:%S",strcol(1))-strptime("%d/%m/%Y %H:%M:%S",start)):3 w linespoints ls 1 t "DS18B20_1"
unset table

