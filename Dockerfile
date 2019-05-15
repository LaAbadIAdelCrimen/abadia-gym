FROM python:3.6

WORKDIR /usr/src/app

ENV PATH $PATH:/root/google-cloud-sdk/bin
RUN curl -sSL https://sdk.cloud.google.com | bash

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p snapshoots
RUN mkdir -p models


CMD ["./loop_testv6_rnd.sh > /dev/nul"]
