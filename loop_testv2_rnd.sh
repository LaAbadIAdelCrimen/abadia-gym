#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

while true
do
(find partidas -name "*.checkpoint" | sort -r | head -50) |
while read -r line
do

  echo "---------------------"
  echo $line
  echo "---------------------"
  ls -lt $line
  sleep 1
  python3 agenttestv2.py --episodes=1 --steps=20 -c $line -g abadia-data  -p 4477

done
done
