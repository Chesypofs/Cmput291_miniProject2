#!/bin/bash

rm -f da.idx
rm -f tw.idx
rm -f te.idx

sort -u -o tweets.txt tweets.txt
sort -u -o terms.txt terms.txt
sort -u -o dates.txt dates.txt

python3 phase2.py
