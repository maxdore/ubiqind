#!/bin/bash
# usage: ./scientists.sh 3 12 circle 1000 data/output.txt

for ((i=$1;i<=$2;i++))
do
    python3 ubiqind.py $3 $i $4 -s >> $5
done
