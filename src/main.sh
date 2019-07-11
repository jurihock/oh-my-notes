#!/bin/sh

OMN=$(dirname "$(readlink -f "$0")")

python3 $OMN/main.py
