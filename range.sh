#!/bin/bash
# usage: ./range.sh complete-wheel-circle 3 12 1000 data/output.txt

export IFS="-"
for word in $1; do
    for ((i=$2;i<=$3;i++))
    do
        python3 ubiqind.py $word $i $4 -s >> $5
    done
done
