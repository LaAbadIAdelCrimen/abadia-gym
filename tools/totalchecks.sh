#!/bin/bash

echo "------"
echo "LOCAL"
echo "------"
echo "Last 500 checkpoints by room (not checkd)"
echo "-----------------------------------------"
find games -name "*.checkpoint" | sort -rn | head -500 | cut -d"_"  -f9 | sort -n | uniq -c
echo "All time  checkpoints"
echo "---------------------"
find games -name "*.checkpoint" | sort -rn | cut -d"_"  -f9 | sort -n | uniq -c

echo "------"
echo "REMOTE"
echo "------"
echo "Last 500 checkpoints by room (not checkd)"
echo "-----------------------------------------"
gsutil cat "gs://abadia-data/all_checkpoint_list.txt" | grep checkpoint | sed -e 's/gs:\/\/abadia-data\///g' | head -500 | cut -d"_"  -f9 | sort -n | uniq -c
echo "All time  checkpoints"
echo "---------------------"
gsutil cat "gs://abadia-data/all_checkpoint_list.txt" | grep checkpoint | sed -e 's/gs:\/\/abadia-data\///g' | cut -d"_"  -f9 | sort -n | uniq -c
