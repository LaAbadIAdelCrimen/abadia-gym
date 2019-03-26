#!/bin/bash

echo "Creating $2  list with this query ($1)"
gsutil ls -r "gs://abadia-data/games/**" | grep -E "$1" | sort -rn | sed  "s/gs:\/\//https:\/\/storage.googleapis.com\//"> /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/datasets/$2.txt
echo "Done: list created"
echo "Getting all the files to build the $2.tar"

rm -rf /tmp/data
mkdir -p /tmp/data
cd /tmp/data

cat /tmp/s1 |
while read -r line
do
  echo $line
  wget $line  2>/dev/null
done
echo "DONE: now we will pack in a tgz file"
tar cvzf /tmp/$2.tgz *
ls -lt /tmp/*.tar
ls -lt *.json
echo "COPYING is to GCP"
gsutil cp /tmp/$2.tgz gs://abadia-data/datasets/$2.tgz
gsutil ls -l gs://abadia-data/datasets/$2.tgz
rm /tmp/$2.tgz

