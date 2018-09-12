#!/bin/bash
while true
do
  options=`gcloud beta pubsub subscriptions pull agent-batch --auto-ack --limit=1 --format="value(DATA)"`
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
    *_0_0.c*)
      echo "game over checkpoint"
      ;;
    *)
      python3 agentv4_dqn.py $options
      # --episodes=500 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80 # -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
      ;;
  esac
done
