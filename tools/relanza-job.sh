#!/bin/bash

kubectl delete job abadia-pubsub
kubectl create -f k8s/job-pubsub.yaml
kubectl get jobs
kubectl describe jobs/abadia-pubsub
