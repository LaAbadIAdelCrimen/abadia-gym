#!/bin/bash

echo "Creating $2 actions database with this query ($1)"
gsutil ls -r "gs://abadia-data/games/$1" | grep "abadia_actions" | sort | head -10 > /tmp/lavl
gsutil cp /tmp/lavl gs://abadia-data/datasets/$2.txt
echo "Done: list created"

rm -rf /tmp/datavl
mkdir -p /tmp/datavl
cd /tmp/datavl

cat /tmp/lavl |
while read -r line
do
  echo $line
  gsutil cat $line | zcat >> /tmp/datavl/$2.json
done
echo "DONE: now we will gzip the file"

echo "COPYING is to GCP"
cat /tmp/datavl/$2.json | grep -v null | sort -u > /tmp/$2.json
gsutil cp /tmp/$2.json gs://abadia-data/datasets/$2.json
gsutil cp gs://abadia-data/datasets/all_valid_moves.json /tmp/all_valid_moves.json
cat /tmp/all_valid_moves.json /tmp/$2.json | grep -v null | sort -u > /tmp/new_all_valid_moves.json
gsutil cp /tmp/new_all_valid_moves.json gs://abadia-data/datasets/all_valid_moves.json

gsutil ls -l gs://abadia-data/datasets/$2.json
gsutil ls -l gs://abadia-data/datasets/all_valid_moves.json

rm /tmp/data/$2.json
