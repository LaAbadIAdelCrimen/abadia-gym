# Agent v2 a.k.a. Simple Qlearning
# this agent is a very simple agent using Qlearning

import gym
import gym_abadia
import numpy as np
import os
import argparse
import random

# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.optimizers import Adam
# from google.cloud import storage
#from collections import deque

import logging

from DQN import DQN

def init_env(env):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--server', help='server name')
    argparser.add_argument('-p', '--port', help='port number')
    argparser.add_argument('-c', '--checkpoint', help='checkpoint file')
    argparser.add_argument('-m', '--model', help='model file')
    argparser.add_argument('-e', '--episodes', help='number of episodes')
    argparser.add_argument('-n', '--steps', help='total steps of the episode')
    argparser.add_argument('-g', '--gcs', help='Google storage bucket')

    args = argparser.parse_args()
    print("args {}".format(args))

    if args.server != None:
        env.server = args.server
        env.set_url()

    if args.port != None:
        env.port = args.port
        env.set_url()

    if args.checkpoint != None:
        env.checkpointName = args.checkpoint

    if args.model != None:
        env.modelName = args.model

    if args.episodes != None:
        env.num_episodes = int(args.episodes)

    if args.steps != None:
        env.num_steps = int(args.steps)

    if args.gcs != None:
        env.gsBucket = args.gcs
        env.init_google_store_bucket()

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%m-%y %H:%M:%S',
                        level=logging.INFO)

def mainLoop():

    rList = []
    bucle = 0
    steps = []

    for i_episode in range(env.num_episodes):
        logging.info(f'Runnig {i_episode} episode')
        logging.info("RESET: starting")
        state = env.reset()
        logging.info("RESET: done")
        if(env.checkpointName != None):
            state = env.load_game_checkpoint(env.checkpointName)

        rAll = 0
        done = False

        for t in range(env.num_steps):

            action = np.random.randint(0, 3) # dqn_agent.act(state)
            # env.prev_vector = env.vector
            while True:
                newState, reward, done, info = env.step(action)
                # we also save the non Guillermo status because there is a lot
                # of clues like monks location, objects, etc
                env.save_action(state, action, reward, newState)
                if env.estaGuillermo:
                    break
            #  dqn_agent.remember(env.prev_vector, action, reward, env.vector, done)

            if done:
                # logging.info(f'Episode finished after {t+1} steps')
                env.save_game()
                if (env.haFracasado):
                    # logging.info(f'Episode finished with a FAIL')
                    env.reset_fin_partida()
                    break

            # TODO JT: we need to create an option for this
            # if (t % 10 == 0 or reward > 0):
            env.pintaRejilla(40, 20)

            x, y, ori = env.personajeByName('Guillermo')
            rAll += reward
            state = newState
            if done == True:
                env.save_game()
                break

        if rAll > 0:
            env.save_game_checkpoint()

        env.save_game()

        if (env.gsBucket != None):
            logging.info("Uploading model to GCP")
            env.upload_blob(nameModel, nameModel)

        rList.append(rAll)

        if t >= env.num_steps:
            logging.info("Failed to complete in trial {}".format(env.num_episodes))
        # else:
        #   print("Completed in {} trials".format(i_episode))
        #   dqn_agent.save_model("models/success.model")
        #   break

        env.visited_snap_save()

    logging.info("Score over time: " + str(sum(rList)/env.num_episodes))

if __name__ == '__main__':
    env = gym.make('Abadia-v2')
    init_env(env)
    mainLoop()


