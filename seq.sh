#!/bin/bash
N=800
z=8e-16
for i in $(seq 0 $N)
do
    # result=$(echo "e(-$i/20)" | bc -l);
    result=$(echo "1 - (1 - $z) / (1 + e(-10 * $i / (.2*$N)+.2*$N/10))" | bc -l);
    echo "[$i/$N, $result]";
    ./parallel -z $result -x -0.2262670179899671 -y 1.1161743290644637 -w 1920 -h 1080 -o seq/$i.ppm
done