#!/bin/bash

# gcloud init
gcloud pubsub topics create agent-batches
gcloud pubsub subscriptions create --topic agent-batches agent-batch
gcloud pubsub topics publish myTopic --message "--episodes=1 --steps=50 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80"
gcloud pubsub subscriptions pull --auto-ack agent-batch
