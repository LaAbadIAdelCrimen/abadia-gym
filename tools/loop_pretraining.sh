#!/bin/bash

echo "Creating a temporary dir"
rm -rf /tmp/pretraining
mkdir -p /tmp/pretraining

while true
do
  actions=`gcloud beta pubsub subscriptions pull pretraining --auto-ack --limit=1 --format="value(DATA)"`
  echo "data: $actions"
  case $actions in
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
      echo "pretraining ${actions}"
      gsutil ls -l $actions
      ret=$?
      case $ret in
          0)
            python3 extract_vectors_from_actions.py $actions
            ;;
          *)
            echo "Looks like there is a problem with $actions"
            ;;
      esac

      # python3 $options
      # --episodes=500 --steps=2000 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80 # -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
      ;;
  esac
done

