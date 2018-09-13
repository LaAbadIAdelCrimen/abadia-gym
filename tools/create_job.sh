#!/bin/bash

# Number of jobs to create
REPLICAS=$1


CALLED=$_
if [[ $CALLED != $0 ]]; then BASEPATH=$(dirname "${BASH_SOURCE[0]}") ; else BASEPATH=$(dirname "$0"); fi

JOB_YAML="$BASEPATH/../k8s/job-pubsub.yaml"
SEARCH="abadia-pubsub"

re='^[0-9]+$'
if ! [[ $REPLICAS =~ $re ]] ; then
   echo "error: Param \$1 must be a number" >&2; exit 1
fi

RND=$(LC_CTYPE=C tr -dc 'a-z0-9'  < /dev/urandom | fold -w 4 | head -n 1)
DATE=$(date '+%Y%m%d%H%M%S')
BASE_NAME="abadia-pubsub-"${DATE}-$RND

for (( c=1; c<=$REPLICAS; c++ ))
do
   JOB_NAME=${BASE_NAME}"-$c"
   echo "Creating Job $JOB_NAME"
   sed 's/'$SEARCH'/'$JOB_NAME'/g' $JOB_YAML | kubectl create -f -
done