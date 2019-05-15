#!/bin/bash

echo "Moving the $1 directory to the AbadIA Data cold storage"
gsutil ls "gs://abadia-data/games/$1" | while read -r line
do
  echo $line
  file=`echo $line | sed -e 's/gs\:\/\/abadia-data\///g'`
  gsutil cp $line gs://abadia-data-cold/$file
done
