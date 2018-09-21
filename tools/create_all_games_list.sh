#!/bin/bash

gsutil ls -r "gs://abadia-data/games/**" | grep "abadia_game" > /tmp/s1
gsutil cp /tmp/s1 gs://abadia-data/all_game_list.txt

