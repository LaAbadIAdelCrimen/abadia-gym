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
            # action gs://abadia-data/games/20190504/abadia_actions_190504_053720_134598.json.gz
            # games/20190504/abadia_values_vectors_190504_053720_134598.data
            # line = https://storage.googleapis.com/abadia-data/
            line=`echo $actions | sed -e 's/gs:\/\//https\:\/\/storage.googleapis.com\//g' \
            | sed -e 's/abadia_actions/abadia_vectors/g' \
            | sed -e 's/json\.gz/data/g'`
            gcloud pubsub topics publish training --message "${line}"
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

