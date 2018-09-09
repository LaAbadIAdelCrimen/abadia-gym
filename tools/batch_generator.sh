#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

(find games -name "*.checkpoint" | sort -r | grep $1 | head -500) |
while read -r line
do
  gcloud beta pubsub topics publish agent-batches "--episodes=1 --steps=200 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80 -c $line "
done

