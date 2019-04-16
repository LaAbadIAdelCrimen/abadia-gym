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
dqn_agent = AbadIA.NGDQN.NGDQN(env=None, initModelName="models/last_model_v6.model", modelName="models/last_model_v6.model")

print("Loading some vectors from a dir")
dqn_agent.load_vectors_from_a_dir("./games/20190415")

print("Training with replay_game")
[history, score] = dqn_agent.replay_game(epochs=20, verbose=1)
print("history:", history)
print("score:", score)

print("Saving the updated model")
dqn_agent.save_model(dqn_agent.modelName)
