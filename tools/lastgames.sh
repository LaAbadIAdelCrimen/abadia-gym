#!/bin/bash

# display the formatted JSON from the last games
# you need to pass a pattern to filter
# need to have jq installed

find . -name "*_game_*" | sort -rn | xargs grep -h $1 | jq . -C | less -r
