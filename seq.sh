#!/bin/bash
N=320
for i in $(seq 0 $N)
do
    result=$(echo "e(-$i/20)" | bc -l);
    echo "[$i/$N]";
    ./parallel -z $result -x -1.768778833 -y -0.00173891 -w 1920 -h 1080 -o seq/$i.ppm
done