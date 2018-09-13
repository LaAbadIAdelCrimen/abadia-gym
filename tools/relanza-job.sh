#!/bin/bash

kubectl delete job abadia-pubsub
kubectl create -f k8s/job-pubsub.yaml
kubectl get jobs
kubectl describe jobs/abadia-pubsub
job=`kubectl describe jobs/abadia-pubsub | grep Created | cut -d":" -f2`
kubectl logs -f $job agent
