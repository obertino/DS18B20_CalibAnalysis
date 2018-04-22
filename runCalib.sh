#!/bin/bash

mkdir -p data
mkdir -p plots
gnuplot -e "filename='$1'" calib.gnuplot
python calib.py
