#!/bin/bash
for file in `curl https://storage.googleapis.com/abadia-data/all_abadia_actions_list.txt | grep _actions_18 | grep -v ".gz"`
do
  echo "$file"
  gs=`echo $file | sed -e 's/https\:\/\/storage\.googleapis\.com/gs\:\//'`
  echo "$gs"
  curl $file | gzip - | gsutil cp - $gs.gz && gsutil rm $gs
done