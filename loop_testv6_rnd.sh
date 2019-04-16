#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

while true
do
(find games -name "*.checkpoint" | grep 2019 | grep "$1" | grep  -v "_0_" | sort -r | head -50) |
while read -r file
do

  echo "---------------------"
  echo $file
  echo "---------------------"
  ls -lt $file
  sleep 1
  # python3 agenttestv2.py --episodes=1 --steps=9000 -c $line -g abadia-data  -p 4477
  python3 agentv6_ngdqn.py --episodes=10 --steps=500 -g abadia-data \
  --initmodel=models/last_model_v6.model \
  -g abadia-data -c $file
  # -s http://35.241.222.173 -p 80 # -c /tmp/check

done
done
