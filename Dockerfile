FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p snapshoots
CMD ["./loopagentv4.sh"]