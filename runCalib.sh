#!/bin/bash

#script takes 2 arguments
#./runCalib.sh <dat file> <nsensors>

mkdir -p data
mkdir -p plots

#clean data from strange measurements
awk -F ';' 'NF>2{ if ($3<70 && $3>-50) {print $0;}}' $1 > data/temp.dat
mv -f data/temp.dat $1

gnuplot -e "filename='$1'" -e "nsensors='$2'" calib.gnuplot
python calib.py $2
