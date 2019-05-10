#!/bin/bash

(
gsutil cat "gs://abadia-data/all_abadia_vectors_list.txt" | head -6000
) | while read -r line
do
  echo $line
  gcloud pubsub topics publish training --message "${line}"
done
