#!/bin/bash

echo "Creating $2  list with this query ($1)"
gsutil ls -r "gs://abadia-data/games/**" | fgrep "$1" | sort -rn | sed  "s/gs:\/\//https:\/\/storage.googleapis.com\//"> /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/datasets/$2.txt
echo "Done: list created"
echo "Getting all the files to build the $2.tgz"

rm -f /tmp/data
mkdir -p /tmp/data
cd /tmp/data
rm -f $2.tgz

cat /tmp/s1 |
while read -r line
do
  echo $line
  wget $line  2>/dev/null
done
echo "DONE: now we will pack in a tgz file"
tar cvzf $2.tgz *
ls -lt *.tgz
ls -lt *.json
echo "COPYING is to GCP"
gsutil cp $2.tgz gs://abadia-data/datasets/$2.tgz
gsutils ls -l gs://abadia-data/datasets/$2.tgz
