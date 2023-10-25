#!/bin/bash
N=40000
z=0.00000000001
x=-1.255615900225
y=0.03497725995
result=1.0
alpha=$(echo "e(-l($z)/$N)" | bc -l);
for i in $(seq 4520 16 $N)
do
    # result=$(echo "e(-$i/20)" | bc -l);
    # result=$(echo "1 - (1 - $z) / (1 + e(-1 * $i / (0.2*$N)+ $N / 10))" | bc -l);q
    
    n1=$i;
    n2=$(echo "$i+1" | bc -l);
    n3=$(echo "$i+2" | bc -l);
    n4=$(echo "$i+3" | bc -l);
    n5=$(echo "$i+4" | bc -l);
    n6=$(echo "$i+5" | bc -l);
    n7=$(echo "$i+6" | bc -l);
    n8=$(echo "$i+7" | bc -l);
    n9=$(echo "$i+8" | bc -l);
    n10=$(echo "$i+9" | bc -l);
    n11=$(echo "$i+10" | bc -l);
    n12=$(echo "$i+11" | bc -l);
    n13=$(echo "$i+12" | bc -l);
    n14=$(echo "$i+13" | bc -l);
    n15=$(echo "$i+14" | bc -l);
    n16=$(echo "$i+15" | bc -l);


    z1=$(echo "e(-($n1)*l($alpha))" | bc -l);
    z2=$(echo "e(-($n2)*l($alpha))" | bc -l);
    z3=$(echo "e(-($n3)*l($alpha))" | bc -l);
    z4=$(echo "e(-($n4)*l($alpha))" | bc -l);
    z5=$(echo "e(-($n5)*l($alpha))" | bc -l);
    z6=$(echo "e(-($n6)*l($alpha))" | bc -l);
    z7=$(echo "e(-($n7)*l($alpha))" | bc -l);
    z8=$(echo "e(-($n8)*l($alpha))" | bc -l);
    z9=$(echo "e(-($n9)*l($alpha))" | bc -l);
    z10=$(echo "e(-($n10)*l($alpha))" | bc -l);
    z11=$(echo "e(-($n11)*l($alpha))" | bc -l);
    z12=$(echo "e(-($n12)*l($alpha))" | bc -l);
    z13=$(echo "e(-($n13)*l($alpha))" | bc -l);
    z14=$(echo "e(-($n14)*l($alpha))" | bc -l);
    z15=$(echo "e(-($n15)*l($alpha))" | bc -l);
    z16=$(echo "e(-($n16)*l($alpha))" | bc -l);

    echo "[$i/$N, $z1]" ;

    ./parallel -z $z1 -x $x -y $y -w 3840 -h 2160 -o seq/$n1.ppm &
    ./parallel -z $z2 -x $x -y $y -w 3840 -h 2160 -o seq/$n2.ppm &
    ./parallel -z $z3 -x $x -y $y -w 3840 -h 2160 -o seq/$n3.ppm &
    ./parallel -z $z4 -x $x -y $y -w 3840 -h 2160 -o seq/$n4.ppm &
    ./parallel -z $z5 -x $x -y $y -w 3840 -h 2160 -o seq/$n5.ppm &
    ./parallel -z $z6 -x $x -y $y -w 3840 -h 2160 -o seq/$n6.ppm &
    ./parallel -z $z7 -x $x -y $y -w 3840 -h 2160 -o seq/$n7.ppm &
    ./parallel -z $z8 -x $x -y $y -w 3840 -h 2160 -o seq/$n8.ppm &
    ./parallel -z $z9 -x $x -y $y -w 3840 -h 2160 -o seq/$n9.ppm &
    ./parallel -z $z10 -x $x -y $y -w 3840 -h 2160 -o seq/$n10.ppm &
    ./parallel -z $z11 -x $x -y $y -w 3840 -h 2160 -o seq/$n11.ppm &
    ./parallel -z $z12 -x $x -y $y -w 3840 -h 2160 -o seq/$n12.ppm &
    ./parallel -z $z13 -x $x -y $y -w 3840 -h 2160 -o seq/$n13.ppm &
    ./parallel -z $z14 -x $x -y $y -w 3840 -h 2160 -o seq/$n14.ppm &
    ./parallel -z $z15 -x $x -y $y -w 3840 -h 2160 -o seq/$n15.ppm &
    ./parallel -z $z16 -x $x -y $y -w 3840 -h 2160 -o seq/$n16.ppm ;
done

# ffmpeg -framerate 240 -pattern_type glob -i '*.jpeg' -c:v libx264 -r 240 output.mov