#!/bin/bash

cd /content/abadia-gym/datasets
#curl https://storage.googleapis.com/abadia-data/last_5000_actions_list.txt

rm -f $line.json
(curl $1) |
while read -r line
do
  wget $line >> file.json 2>/dev/null
done

