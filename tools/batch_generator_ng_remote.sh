#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P
# the second argument ($2) is the agent you want to run

(gsutil cat  "gs://abadia-data/last_5000_checkpoint_list.txt" | sed -e 's/gs:\/\/abadia-data\///g'| grep $1 | grep -v "_0_0.che" | head -500) |
while read -r line
do
  case $line in
    *_0_0.c*)
      echo "look like a dead checkpoint, I don't queue it ($line)"
      ;;
    *)
      options=" $2 --episodes=5 --steps=2000 --initmodel=models/last_model_v6.model -g abadia-data -s http://localhost -p 4477 -c $line "
      echo "Queuing -> ($options) into the topic agent-batches"
      gcloud beta pubsub topics publish agent-batches --message "$options"
      ;;
  esac
done
