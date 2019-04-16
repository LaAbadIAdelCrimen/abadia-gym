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
dqn_agent = AbadIA.NGDQN.NGDQN(env=None, initModelName="models/last_v6.model", modelName="models/last_v6.model")

print("Loading some actions")
dqn_agent.load_actions_from_a_file("/tmp/actions.json")

print("Loading some actions from a dir")
dqn_agent.load_actions_from_a_dir("./games/20190416")

print("Saving as vector format")
dqn_agent.save_actions_as_vectors("/tmp/vectors.json")


