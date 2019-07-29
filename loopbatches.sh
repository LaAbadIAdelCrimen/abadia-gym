#!/bin/bash
while true
do
  options=`gcloud beta pubsub subscriptions pull agent-batches --auto-ack --limit=1 --format="value(DATA)"`
  echo "I will execute $options"
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
    *_2[23]_[0-9]_0.c*)
      echo "*************************************** tired of doing this for now $options"
      echo "*************************************** tired of doing this for now $options"
      echo "*************************************** tired of doing this for now $options"
      ;;
    *_2[23]_[0-9][0-9]_0.c*)
      echo "*************************************** tired of doing this for now $options"
      echo "*************************************** tired of doing this for now $options"
      echo "*************************************** tired of doing this for now $options"
      ;;
    *_0_0.c*)
      echo "game over checkpoint"
      ;;
    *)

      python3 $options   --obsequium=31 # --learning=False --episodes=1 --steps=200 --obsequium=31
      # --episodes=500 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80 # -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
      ;;
  esac
done
