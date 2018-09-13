#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P

(find games -name "*.checkpoint" | sort -r | grep $1 | grep -v "*_0_0.*" | head -500) |
while read -r line
do
  options="--episodes=1 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://localhost -p 4477 -c $line "
  echo "Queuing -> ($options) into the topic agent-batches"
  gcloud beta pubsub topics publish agent-batches "$options"
done

