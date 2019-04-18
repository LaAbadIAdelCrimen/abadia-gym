import gym
import gym_abadia
import numpy as np
import os
import argparse
import random
import json
import AbadIA.VDQN

print("creating/updating the value model v1 from the last version")
# vdqn = AbadIA.VDQN.VDQN(env=None, initModelName=None, modelName=None)
vdqn = AbadIA.VDQN.VDQN(env=None, initModelName="models/pre_last_value_v1.model", modelName="models/pre_last_model_v1.model")

print("Loading some vectors from a dir")
vdqn.load_vectors_from_a_dir("./games/20190418")

print("Training with replay_game")
[history, score] = vdqn.replay_game(epochs=10, verbose=1)
print("history loss    :", history.history['loss'])
print("history val loss:", history.history['val_loss'])
print("score           :", score)

print("Saving the updated model")
vdqn.save_model("models/pre_last_value_v1.model")
