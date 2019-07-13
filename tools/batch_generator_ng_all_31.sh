#!/bin/bash

gsutil cp gs://abadia-data/all_checkpoint_list.txt /tmp/acl.txt
grep "_31_0.check" /tmp/acl.txt | grep -v "_2[23]_31_0.c" > /tmp/o31

cut -d"_"  -f9,10 < /tmp/o31 | cut -d"_" -f1 | sort -n | uniq -c  | \
 sort -n | sed -e 's/^  //g'  | sed -e 's/^  //g'  | sed -e 's/^ //g' | sed -e 's/^ //g' | cut -d" " -f2  | head -10 > /tmp/rooms
echo "Selected rooms with 31 obsequium and total visits"
cut -d"_"  -f9,10 < /tmp/o31 | cut -d"_" -f1 | sort -n | uniq -c | sort -n
echo "I will look for the this rooms:"
echo "------------"
cat /tmp/rooms
echo "------------"
echo "I will look for the room: (21)"
(cat /tmp/o31 | sort -n | sed -e 's/https:\/\/storage.googleapis.com\/abadia-data\///g' | egrep "_21_31_0.che") |
while read -r line
do
  case $line in
    *_0_0.c*)
      echo "look like a dead checkpoint, I don't queue it ($line)"
      ;;
    *)
      options=" $2 --episodes=1 --steps=2000 --initmodel=models/last_model_v6.model -g abadia-data -s http://localhost -p 4477 -c $line "
      echo "Queuing ($room) -> ($options) into the topic agent-batches"
      gcloud beta pubsub topics publish agent-batches --message "$options"
      ;;
  esac
done

