#!/bin/bash

rm -f terms.txt
rm -f tweets.txt
rm -f dates.txt
rm -f da.idx
rm -f tw.idx
rm -f te.idx

cat $1 | python3 phase1.py

sort -u -o tweets.txt tweets.txt
sort -u -o terms.txt terms.txt
sort -u -o dates.txt dates.txt

python3 phase2.py
python3 phase3.py
