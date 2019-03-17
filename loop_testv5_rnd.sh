#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

while true
do
(find games -name "*.checkpoint" | grep 2019 | grep _28_ | sort -r | head -50) |
while read -r line
do

  echo "---------------------"
  echo $line
  echo "---------------------"
  ls -lt $line
  sleep 1
  # python3 agenttestv2.py --episodes=1 --steps=9000 -c $line -g abadia-data  -p 4477
  python3 agentv5_dqn.py --episodes=1 --steps=1000 --model=models/model_v2_lastest.model -g abadia-data  -c $line
  # -s http://35.241.222.173 -p 80 # -c /tmp/check

done
done
