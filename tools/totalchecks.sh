#!/bin/bash

echo "Last 500 checkpoints by room (not checkd)"
find games -name "*.checkpoint" | sort -rn | head -500 | cut -d"_"  -f9 | sort -n | uniq -c
echo "All time  checkpoints"
find games -name "*.checkpoint" | sort -rn | cut -d"_"  -f9 | sort -n | uniq -c
