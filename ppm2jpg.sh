#!/bin/bash

for pic in seq/*.ppm;
do
    echo "Converting $pic to ${pic%.*}.jpg"
    pnmtojpeg -quality=60 "$pic" > ${pic%.*}.jpg
done