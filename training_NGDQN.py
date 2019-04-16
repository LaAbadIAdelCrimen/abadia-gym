import gym
import gym_abadia
import numpy as np
import os
import argparse
import random
import json
import AbadIA.NGDQN
AbadIA.NGDQN

print("Creating the Model v6 from the last version")
dqn_agent = AbadIA.NGDQN.NGDQN(env=None, iniModelName="models/testv6.model", modelName="models/last_v6.model")

print("Loading some actions")
dqn_agent.load_actions_from_a_file("/tmp/actions.json")
print("Training with replay_game")
history = dqn_agent.replay_game(epochs=30, verbose=1)
print("Saving the updated model")
dqn_agent.save_model(dqn_agent.modelName)
