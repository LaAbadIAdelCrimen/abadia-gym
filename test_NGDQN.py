import gym
import gym_abadia
import numpy as np
import os
import argparse
import random
import AbadIA.NGDQN
AbadIA.NGDQN
# env = gym.make('Abadia-v2')
dqn_agent = AbadIA.NGDQN.NGDQN(env=None)

print("Creating a new model")
dqn_agent.create_model()

