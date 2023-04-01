#!/bin/bash
N=1000
z=0.00000000000008
x=-1.940967706102894
y=0.0010053830006
for i in $(seq 0 $N)
do
    # result=$(echo "e(-$i/20)" | bc -l);
    result=$(echo "1 - (1 - $z) / (1 + e(-10 * $i / (0.2*$N)+ $N / 100))" | bc -l);
    echo "[$i/$N, $result]";
    ./parallel -z $result -x $x -y $y -w 1920 -h 1080 -o seq/$i.ppm
done