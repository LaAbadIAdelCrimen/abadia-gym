# Agent v2 a.k.a. Simple Qlearning
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

from collections import deque

from DQN import DQN


def init_env(env):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--server', help='server name')
    argparser.add_argument('-p', '--port', help='port number')
    argparser.add_argument('-c', '--checkpoint', help='checkpoint file')
    argparser.add_argument('-m', '--model', help='model file')
    argparser.add_argument('-e', '--episodes', help='number of episodes')
    argparser.add_argument('-n', '--steps', help='total steps of the episode')

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



def mainLoop():

    nameVisitedSnap = "snapshoots/current-visited"

    if os.path.exists(nameVisitedSnap) and os.path.getsize(nameVisitedSnap) > 0:
        fvisitedsnap = open(nameVisitedSnap, "rb+")
        env.Visited = np.load(fvisitedsnap)
    else:
        fvisitedsnap = open(nameVisitedSnap, "wb+")
        env.Visited = np.zeros([512, 512])
        np.save(fvisitedsnap, env.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

    rList = []
    bucle = 0

    # DQN parameters

    gamma = 0.9
    epsilon = .95

    dqn_agent = DQN(env=env)
    steps = []

    for i_episode in range(env.num_episodes):
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

            dqn_agent.remember(env.prev_vector, action, reward, env.vector, done)

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                env.save_game()
                if (env.haFracasado):
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

            print("Episode({}:{}) A({})XYOP {},{},{},{} -> {},{} r:{} tr:{} V:{}"
                .format(i_episode, t, action, x, y, ori, env.numPantalla, newX, newY, np.round(reward,2),
                np.round(rAll,2), np.round(env.predictions,3), end="\r"))

            if (t % 10 == 0 or reward > 0):
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
        dqn_agent.save_model("models/model_v1_{}_trial_{}.model".format(env.gameId, i_episode))
        dqn_agent.save_model("models/model_v1_lastest.model".format(env.gameId))

        rList.append(rAll)

        if t >= env.num_steps:
            print("Failed to complete in trial {}".format(env.num_episodes))
        # else:
        #   print("Completed in {} trials".format(i_episode))
        #   dqn_agent.save_model("models/success.model")
        #   break

        fvisitedsnap = open(nameVisitedSnap, "wb+")
        np.save(fvisitedsnap, env.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

    print("Score over time: " + str(sum(rList)/env.num_episodes))

if __name__ == '__main__':
    env = gym.make('Abadia-v0')
    init_env(env)
    mainLoop()


