# Agent v1 a.k.a. DoNothing
# this agent is a very simple agent to test abadia gym


import gym
import gym_abadia
import numpy as np

board_visited = (300, 300)

env = gym.make('Abadia-v0')
for i_episode in range(20):
    observation = env.reset()
    np.zeros(board_visited)
    for t in range(100):
        print("observation: {}\n".format(observation['Guillermo']))
        x = int(observation['Guillermo']['posX'])
        y = int(observation['Guillermo']['posY'])
        ori = int(observation['Guillermo']['orientacion'])
        print ("X,Y -> {},{} ori {}".format(x, y, ori))
        # board_visited[x][y] += 1
        env.render(mode="human")
        action = env.action_space.sample()

        print("Next Action: {}\n".format(action))
        observation, reward, done, info = env.step(action)

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

