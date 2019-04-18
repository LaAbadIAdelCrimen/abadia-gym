#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P
# the second argument ($2) is the agent you want to run

(gsutil ls -r "gs://abadia-data/games/**" | grep checkpoint | sed -e 's/gs:\/\/abadia-data\///g'| grep $1 | grep -v "_0_0.che" | head -500) |
while read -r line
do
  case $line in
    *_0_0.c*)
      echo "look like a dead checkpoint, I don't queue it ($line)"
      ;;
    *)
      options=" $2 --episodes=10 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://localhost -p 4477 -c $line "
      echo "Queuing -> ($options) into the topic agent-batches"
      gcloud beta pubsub topics publish agent-batches --message "$options"
      ;;
  esac
done

