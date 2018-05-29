#!/bin/bash
while true
do
  python3 agentv4_dqn.py --episodes=100 --steps=250  # -c partidas/20180429/abadia_checkpoint_18-04-29_19:53:02:726983_1_4_34_13_0.checkpoint
done
