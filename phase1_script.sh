#!/bin/bash

rm -f terms.txt
rm -f tweets.txt
rm -f dates.txt

cat $1 | python3 phase1.py
