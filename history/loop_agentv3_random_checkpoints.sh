#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

(find partidas -name "*.checkpoint" | sort -r | grep $1 | head -500) |
while read -r line
do
  python3 agentv3_qlearning.py --episodes=50 --steps=350  -c $line
done
