#!/bin/bash
while true
do
  python3 agentv5_dqn.py --episodes=1 --steps=5000 --model=models/model_v2_lastest.model -g abadia-data # -s http://35.241.222.173 -p 80 # -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
done
