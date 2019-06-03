#!/bin/bash

# use the $1 to grep some pattern from the last checkpoints that was autosaved
# example: _21_ would select the room 21 or not ;-P
# the second argument ($2) is the agent you want to run

# egrep "_$1_[0-9]_0.c|_$1_[0-9][0-9]_0.c" | grep -v "_0_0.che"
# (gsutil cat  "gs://abadia-data/all_checkpoint_list.txt" | sed -e 's/https:\/\/storage.googleapis.com\/abadia-data\///g'| egrep "_$1_[2-3][0-9]_0.c" | grep -v "_0_0.che" | grep -v "_2[123]_[0-9]_0.c" | grep -v "_2[123]_[0-9][0-9]_0.c" | head -100) |
# egrep "_31_0.check|_30_0.check|_29_0.check|_28_0.check|_27_0.check" /tmp/acl.txt | grep -v "_2[23]_[0-9]_0.c" | grep -v "_2[23]_[0-9][0-9]_0.c" > /tmp/o31

gsutil cp gs://abadia-data/all_checkpoint_list.txt /tmp/acl.txt

egrep "_31_0.check|_29_0.check" /tmp/acl.txt | grep -v "_2[23]_[0-9]_0.c" | grep -v "_2[23]_[0-9][0-9]_0.c" > /tmp/o31

cut -d"_"  -f9,10 < /tmp/o31 | cut -d"_" -f1 | sort -n | uniq -c  | \
 sort -n | sed -e 's/^  //g'  | sed -e 's/^  //g'  | sed -e 's/^ //g' | sed -e 's/^ //g' | cut -d" " -f2  | head -10 > /tmp/rooms
echo "Selected rooms and total visits"
cut -d"_"  -f9,10 < /tmp/o31 | cut -d"_" -f1 | sort -n | uniq -c | sort -n
echo "I will look for the this rooms:"
echo "------------"
cat /tmp/rooms
echo "------------"
(cat /tmp/rooms) |
while read -r room
do
echo "I will look for the room: ($room)"
(cat /tmp/o31 | sed -e 's/https:\/\/storage.googleapis.com\/abadia-data\///g' | egrep "_${room}_31_0.che|_${room}_2[79]_0.che" | head -50) |
while read -r line
do
  case $line in
    *_0_0.c*)
      echo "look like a dead checkpoint, I don't queue it ($line)"
      ;;
    *)
      options=" $2 --episodes=5 --steps=2000 --initmodel=models/last_model_v6.model -g abadia-data -s http://localhost -p 4477 -c $line "
      echo "Queuing ($room) -> ($options) into the topic agent-batches"
      gcloud beta pubsub topics publish agent-batches --message "$options"
      ;;
  esac
done

done
