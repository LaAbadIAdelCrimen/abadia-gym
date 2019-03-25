#!/bin/bash

echo "Creating Last 5000 actions list"
gsutil ls -r "gs://abadia-data/games/**" | grep "actions" | sort -rn | head -10000 > /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/last_5000_actions_list.txt

echo "Creating a all games list gs://abadia-data/all_game_list.txt"
gsutil ls -r "gs://abadia-data/games/**" | grep "abadia_game" > /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/all_game_list.txt

