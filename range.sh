#!/bin/bash
# usage: ./range.sh complete-wheel-circle .499,.5-.499,.499,.5 3 12 1000 data/output.txt

export IFS="-"
for network in $1; do
    for ops in $2; do
        for ((i=$3;i<=$4;i++))
        do
            op=${ops//,/\ }
            python3 ubiqind.py $network $i $5 $op -s >> $6
        done
    done
done
