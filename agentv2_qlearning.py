# Agent v2 a.k.a. Simple Qlearning
# this agent is a very simple agent using Qlearning

import gym
import gym_abadia
import numpy as np

env = gym.make('Abadia-v0')

#Initialize table with all zeros
# Q = np.zeros([env.observation_space.n, env.action_space.n])
Q = np.zeros([512, 512, env.action_space.n])
# Set learning parameters
lr = .8
yy = .95

rList = []

for i_episode in range(100):

    state = env.reset()
    # Reset environment and get first new state
    rAll = 0
    done = False

    for t in range(200):
        x = int(state['Guillermo']['posX'])
        y = int(state['Guillermo']['posY'])
        ori = int(state['Guillermo']['orientacion'])
        # env.render(mode="human")

        # Choose an action by greedily (with noise) picking from Q table
        action = np.argmax(Q[x, y, :] + np.random.randn(1, env.action_space.n) * (1. / (i_episode + 1)))

        # Get new state and reward from environment
        newState, reward, done, info = env.step(action)

        print ("Episode:{}:{} X,Y->{},{},{} A({}) r:{} tr:{}".format(i_episode, t, x, y, ori, action, reward, rAll))

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

        # Update Q-Table with new knowledge
        newX = int(newState['Guillermo']['posX'])
        newY = int(newState['Guillermo']['posY'])
        Q[x, y, action] = Q[x, y, action] + lr * (reward + yy * np.max(Q[newX, newY, :]) - Q[x, y, action])
        rAll += reward
        state = newState
        if done == True:
            break

    # jList.append(j)
    rList.append(rAll)

print("Score over time: " + str(sum(rList)/100))

print("Final Q-Table Values")
print(Q)