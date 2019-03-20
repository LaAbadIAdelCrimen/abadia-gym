# Agent v5 a.k.a. Simple Qlearning with v2 gym_abadia
# this agent is a very simple agent using Qlearning

import gym
import gym_abadia
import numpy as np
import os
import argparse
import random

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from google.cloud import storage
from collections import deque

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

def checkValidMovs(env):
    env.valMovs = np.zeros(9, np.int)
    room = np.zeros([24, 24, 2], np.int)
    chkM = np.array([
        [0, 0, 0, -1, 0],
        [0, 0, 1, -1, 0],
        [1, 0, 0, -1, 0],
        [1, 0,-1, -1, 0],
        [1, 0, 0, 0, -1],
        [2, 0, 1, 0, 2],
        [2, 1, 1, 1, 2],
        [3, 1, 0, 2, 0],
        [3, 1,-1, 2,-1],
        [4, 1, 0, 2, 0],
        [4, 1,-1, 2,-1],
        [5, 0,-1, 0,-2],
        [5, 1,-1, 1,-2],
        [5, 1,-1, 2,-1],
        [6, 0,-1, 0,-2],
        [6, 1,-1, 1,-2],
        [7, 0, 0,-1, 0],
        [7, 0,-1,-1,-1],
        [7, 0,-1, 0,-2]],
        np.int)


    yPos = -1
    xPos = -1

    for yy in range(0, 24):
        for xx in range(0, 24):
            per = int(env.rejilla[yy][xx]) >> 4
            alt = env.rejilla[yy][xx] % 16
            # print(per)

            # we found Guillermo
            if (per == 1 and xPos == -1 and yPos == -1):
                yPos = yy
                xPos = xx

            room[yy, xx, 0] = per
            room[yy, xx, 1] = alt

    for ii in range(0,len(chkM)):
        y1 = yPos+chkM[ii, 1]
        x1 = xPos+chkM[ii, 2]
        y2 = yPos+chkM[ii, 3]
        x2 = xPos+chkM[ii, 4]
        if ((y1 >= 0 and y1 <= 23) and (x1 >= 0 and x1 <= 23) and (y2 >= 0 and y2 <= 23) and (x2 >= 0 and x2 <= 23)):
            diff = room[y1, x1, 1] - room[y2, x2, 1]
            if (diff >= -1 and diff <= 1):
                print("Wall Blocks G {} ".format(ii), end="")
                env.valMovs[chkM[ii, 0]] += 1
            if (room[y1, x1, 0] != room[y2, x2, 0] and room[y2, x2, 0] != 0):
                print("Adso/* block G {}".format(ii), end="")
                env.valMovs[chkM[ii, 0]] = 0
    env.valMovs[8] = 1
    print("\nValid Movements:", end="")
    for ii in range(9):
        print("%s:%s " % (env.actions_list[ii], env.valMovs[ii]) , end="")
    print("<--                                                            ")

    return env.valMovs

def mainLoop():

    logging.info("loading visited spap file")
    env.visited_snap_load()

    rList = []
    bucle = 0

    # DQN parameters

    gamma = 0.9
    epsilon = .95

    dqn_agent = DQN(env=env)
    steps = []

    for i_episode in range(env.num_episodes):
        logging.info(f'runnig {i_episode} episode')
        state = env.reset()
        if(env.checkpointName != None):
            state = env.load_game_checkpoint(env.checkpointName)

        rAll = 0
        done = False

        for t in range(env.num_steps):

            # TODO JT, crear dos funciones: una para sacar la posición de un personsaje y
            # y otra para sacar un array con todas las posiciones

            x, y, ori       = env.personajeByName('Guillermo')
            adsoX, adsoY, _ = env.personajeByName('Adso')

            # Get new state and reward from environment and check if
            # in the state of the game is Guillermo

            action = dqn_agent.act(state)



            env.prev_vector = env.vector
            while True:
                newState, reward, done, info = env.step(action)
                # we also save the non Guillermo status because there is a lot
                # of clues like monks location, objects, etc
                env.save_action(state, action, reward, newState)
                if env.estaGuillermo:
                    break
                    # test valid movements


            dqn_agent.remember(env.prev_vector, action, reward, env.vector, done)

            if done:
                logging.info(f'Episode finished after {t+1} steps')
                env.save_game()
                if (env.haFracasado):
                    logging.info(f'Episode finished with a FAIL')
                    env.reset_fin_partida()
                    break

            # TODO JT must be refactorized like updateRejilla/Grid
            newX, newY, _ = env.personajeByName('Guillermo')

            if (x != newX or y != newY):
                env.Visited[newX, newY] += 1

            if (x == newX and y == newY):
                if (ori == 0):
                    env.Visited[x + 1, y] += -0.01
                if (ori == 1):
                    env.Visited[x, y - 1] += -0.01
                if (ori == 2):
                    env.Visited[x - 1, y] += -0.01
                if (ori == 3):
                    env.Visited[x, y + 1] += -0.01

            dqn_agent.replay()        # internally iterates default (prediction) model
            dqn_agent.target_train()  # iterates target model

            # print("Episode({}:{}) A({})XYOP {},{},{},{} -> {},{} r:{} tr:{} Q(s,a)= {}"
            #      .format(i_episode, t, action, x, y, ori, env.numPantalla, newX, newY, np.round(reward,2),
            #              np.round(rAll,2), np.round(Q[x,y],2)), end="\r")

            logging.info("E {}:{} {}-{}:XYOP {},{},{},{} -> {},{} r:{} tr:{} V:{}"
                .format(i_episode, t, action, env.actions_list[action], x, y, ori, env.numPantalla, newX, newY, np.round(reward,2),
                np.round(rAll,2), np.round(env.predictions,3)))

            # TODO JT: we need to create an option for this
            # if (t % 10 == 0 or reward > 0):
            env.pintaRejilla(40, 20)

            checkValidMovs(env)
            x, y, ori = env.personajeByName('Guillermo')
            rAll += reward
            state = newState
            if done == True:
                env.save_game()
                break

        if rAll > 0:
            env.save_game_checkpoint()

        env.save_game()

        # TODO JT: refactoring this: the way we storage models and add info to game json

        nameModel = "models/model_v2_{}_trial_{}.model".format(env.gameId, i_episode)

        dqn_agent.save_model(nameModel)

        if (env.gsBucket != None):
            logging.info("Uploading model to GCP")
            env.upload_blob(nameModel, nameModel)

        nameModel ="models/model_v2_lastest.model".format(env.gameId)
        dqn_agent.save_model(nameModel)
        if (env.gsBucket != None):
            logging.info("Uploading lastest model to GCP")
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


