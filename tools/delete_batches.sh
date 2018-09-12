#!/bin/bash

while true
do
gcloud beta pubsub subscriptions pull agent-batch --auto-ack --limit=1000 --format="value(DATA)"
done
