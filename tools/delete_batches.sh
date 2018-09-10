#!/bin/bash

gcloud beta pubsub subscriptions pull agent-batch --auto-ack --limit=10000 --format="value(DATA)"
