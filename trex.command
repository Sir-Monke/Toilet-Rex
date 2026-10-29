#!/bin/sh
# Double-click in Finder to run in Terminal
printf '\033[8;50;100t'  # make the Terminal window 100x50
cd "$(dirname "$0")" && exec python3 trex_art.py
