#!/bin/bash

echo "Creating the mega abadia-data list"
gsutil ls -r "gs://abadia-data/games/**" | sort -rn | sed  "s/gs:\/\//https:\/\/storage.googleapis.com\//"> /tmp/all
gsutil cp /tmp/all gs://abadia-data/all_abadia_data_info.txt

for group in "abadia_actions" "abadia_game" "abadia_value_vector" "abadia_vectors" "checkpoint"
do
    echo "Creating all $group list gs://abadia-data/all_${group}_list.txt"
    grep $group /tmp/all | gsutil cp - gs://abadia-data/all_${group}_list.txt

    echo "Creating Last 5000 ${group} list"
    grep $group /tmp/all | head -5000 | gsutil cp - gs://abadia-data/last_5000_${group}_list.txt

    echo "Creating Last 1000 ${group} list"
    grep $group /tmp/all | head -1000 | gsutil cp - gs://abadia-data/last_1000_${group}_list.txt
done

