import gym
import gym_abadia
import numpy as np
import os
import argparse
import random
import json
import AbadIA.VDQN
AbadIA.VDQN

# vdqn.create_empty("models/last_vdqn_v1-model")

print("Creating the Value Model v1")
vdqn = AbadIA.VDQN.VDQN(env=None, initModelName=None, modelName=None)

print("Transforming some actions to vectors and saving it into a dir")
vdqn.load_actions_from_a_dir_and_save_to_vectors("./games/20190418")

print("Loading the vectors from a dir")
# dqn_agent.load_vectors_from_a_dir("./games/20190416")





