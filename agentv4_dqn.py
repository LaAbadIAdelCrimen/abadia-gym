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

class DQN:
    def __init__(self, env):
        self.env     = env
        self.memory  = deque(maxlen=2000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        state_shape  = self.env.observation_space.shape
        model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

        vector = self.env.stateVector()
        self.env.vector = vector

        if np.random.random() < self.epsilon:
            action = self.env.action_space.sample()
            print("e-greedy: {}".format(action))
        else:
            predictions = self.model.predict(vector)[0]
            action = np.argmax(predictions)
            print("vector: {} predictions: {} action: {}".format(vector, predictions, action))

        return action

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

def init_env(env):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--server', help='server name')
    argparser.add_argument('-p', '--port', help='port number')
    argparser.add_argument('-c', '--checkpoint', help='checkpoint file')
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
                # else:
                    # print("Skipping a screen without Guillermo!!!!")

            dqn_agent.remember(env.prev_vector, action, reward, env.vector, done)

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                env.save_game()
                if (env.haFracasado):
                    env.reset_fin_partida()
                    break

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

            print("Episode({}:{}) A({})XYOP {},{},{},{} -> {},{} r:{} tr:{}  "
                .format(i_episode, t, action, x, y, ori, env.numPantalla, newX, newY, np.round(reward,2),
                np.round(rAll,2), end="\r"))

            if (t % 10 == 0 or reward > 0):
                env.pintaRejilla(40, 20)

            rAll += reward
            state = newState
            if done == True:
                env.save_game()
                break

        if rAll > 0:
            env.save_game_checkpoint()

        env.save_game()

        rList.append(rAll)

        if t >= env.num_steps:
            print("Failed to complete in trial {}".format(env.num_episodes))
            if t % 10 == 0:
                dqn_agent.save_model("models/{}_trial_{}.model".format(env.gameId, i_episode))
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


