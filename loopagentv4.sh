#!/bin/bash
while true
do
  python3 agentv4_dqn.py --episodes=5 --steps=500 --model=models/model_v1_lastest.model -c /tmp/check  # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
done
