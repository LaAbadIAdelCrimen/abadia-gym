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
dqn_agent = AbadIA.NGDQN.NGDQN(env=None, initModelName="models/last_v6.model", modelName="models/last_version_v6.model")

print("Transforming some actions to vectors and saving it into a dir")
dqn_agent.load_actions_from_a_dir_and_save_to_vectors("./games/20190417")

print("Loading the vectors from a dir")
# dqn_agent.load_vectors_from_a_dir("./games/20190416")





