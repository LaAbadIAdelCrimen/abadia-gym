#!/bin/bash

gsutil cp gs://abadia-data/models/pre_last_model_v6.model models/last_model_v6.model
cp models/last_model_v6.model models/pre_last_model_v6.model

while true
do
  options=`gcloud beta pubsub subscriptions pull training --auto-ack --limit=50 --format="value(DATA)"`
  # options=`gcloud beta pubsub subscriptions pull training --limit=300 --format="value(DATA)"`
  echo "I will pick a few vectors ---> $options"
  case $options in
    "exit")
      echo "OK I will exit now"
      exit 0
      ;;
    "")
      echo "updatig the pre_last_model_v6.model"
      gsutil cp models/pre_last_model_v6.model gs://abadia-data/models/pre_last_model_v6.model
      gsutil cp models/pre_last_model_v6.model gs://abadia-data/models/pre_last_model_v6_`date +'%y%m%d-%H'`.model
      echo "No more batches, no more fun ..."
      exit 0
      ;;
    *)
      rm -rf /tmp/vectors
      mkdir /tmp/vectors
      (
        echo $options
      ) | while read -r line
      do
        echo $line
        cd /tmp/vectors && wget $line
      done
      pwd
      echo "ready to training these vectors files"
      ls -lt /tmp/vectors
      echo "training"
      python3 ./training_NGDQN.py /tmp/vectors
      echo "cleaning the temporary dir"
      sleep 5
      echo "uploading the updated model"
      gsutil cp models/pre_last_model_v6.model gs://abadia-data/models/last_model_v6.model
      gsutil cp models/pre_last_model_v6.model gs://abadia-data/models/pre_last_model_v6.model
      ;;
  esac
done
