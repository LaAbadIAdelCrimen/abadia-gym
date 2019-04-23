#!/bin/bash

(gsutil ls gs://abadia-data/games/$1 | grep abadia_actions
) | while read -r action
do
  echo "$action"
  gcloud pubsub topics publish pretraining --message "$action"

done

