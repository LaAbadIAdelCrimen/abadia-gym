#!/bin/bash

cd /content/abadia-gym/datasets
#curl https://storage.googleapis.com/abadia-data/last_5000_actions_list.txt

(curl $1) |
while read -r line
do
  wget $line
done

