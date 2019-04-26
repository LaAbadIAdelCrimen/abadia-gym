#!/bin/bash
while true
do
  options=`gcloud beta pubsub subscriptions pull training --auto-ack --limit=23 --format="value(DATA)"`
  echo "I will pick a few vectors ---> $options"
  case $options in
    "exit")
      echo "OK I will exit now"
      exit 0
      ;;
    "")
      echo "No more batches, no more fun ..."
      curl http://$SERVERIP:$PORT/fin
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
      # --episodes=500 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80 # -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
      ;;
  esac
done
