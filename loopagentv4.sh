#!/bin/bash
while true
do
  python3 agentv4_dqn.py --episodes=5 --steps=250 --model=models/model_v1_lastest.model # -c partidas/20180429/abadia_checkpoint_18-04-29_19:53:02:726983_1_4_34_13_0.checkpoint
done
