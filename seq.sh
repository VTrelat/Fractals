#!/bin/bash
N=40000
z=0.00000000001
x=-1.255615900225
y=0.03497725995
result=1.0
alpha=$(echo "e(-l($z)/$N)" | bc -l);
for i in $(seq 0 $N)
do
    # result=$(echo "e(-$i/20)" | bc -l);
    result=$(echo "$result / $alpha" | bc -l);
    # result=$(echo "1 - (1 - $z) / (1 + e(-1 * $i / (0.2*$N)+ $N / 10))" | bc -l);
    echo "[$i/$N, $result]";
    ./parallel -z $result -x $x -y $y -w 3840 -h 2160 -o seq/$i.ppm
done