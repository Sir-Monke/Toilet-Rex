#!/bin/sh
# Double-click in Finder to run in Terminal
printf '\033[8;56;150t'  # make the Terminal window 150x56: more cells, more detail
cd "$(dirname "$0")" && exec python3 iris_loop.py
