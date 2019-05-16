#!/bin/bash

echo "Creating $2 actions database with this query ($1)"
gsutil ls -r "gs://abadia-data/games/$1" | grep "abadia_actions" | sort -rn > /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/datasets/$2.txt
echo "Done: list created"

rm -rf /tmp/data
mkdir -p /tmp/data
cd /tmp/data

cat /tmp/s1 |
while read -r line
do
  echo $line
  gsutil cp $line /tmp/temp_file.gz
  gzunzip /tmp/temp_file
  cat /tmp/temp_file >> /tmp/data/$2.json
done
echo "DONE: now we will gzip the file"
gzip /tmp/data/$2.json

echo "COPYING is to GCP"
gsutil cp /tmp/$2.json.gz gs://abadia-data/datasets/$2.json.gz
gsutil ls -l gs://abadia-data/datasets/$2.tgz
rm /tmp/data/$2.json.gz

