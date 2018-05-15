#!/bin/bash

find partidas -name "*.checkpoint" | cut -d"_"  -f8 | sort -n | uniq -c
