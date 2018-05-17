#!/bin/bash

echo "Last 200 checkpoints by room (not checkd)"
find partidas -name "*.checkpoint" | sort -rn | head -200 | cut -d"_"  -f9 | sort -n | uniq -c
echo "All time  checkpoints"
find partidas -name "*.checkpoint" | sort -rn | cut -d"_"  -f9 | sort -n | uniq -c
