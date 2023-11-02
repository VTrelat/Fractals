#!/bin/bash

for pic in *.ppm;
do
    echo "Converting $pic to ${pic%.*}.jpg"
    pnmtojpeg -quality=100 "/seq/$pic" > ~/Desktop/fractals/${pic%.*}.jpg
done