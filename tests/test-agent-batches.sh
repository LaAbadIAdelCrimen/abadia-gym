#!/bin/bash

# gcloud init
gcloud beta pubsub topics create agent-batches
gcloud beta pubsub subscriptions create --topic agent-batches agent-batch
gcloud beta pubsub topics publish agent-batches --message "--episodes=1 --steps=50 --model=models/model_v1_lastest.model -g abadia-data -s http://35.241.222.173 -p 80"
gcloud beta pubsub subscriptions pull --auto-ack agent-batch
