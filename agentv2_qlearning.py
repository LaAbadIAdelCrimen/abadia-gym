# Agent v2 a.k.a. Simple Qlearning
# this agent is a very simple agent using Qlearning

import gym
import gym_abadia
import numpy as np
import os

def pintaRejilla():
    print("")
    print("+---------------------+")
    for yy in range(y-10, y+10):
        print("|", end="")
        for xx in range(x-10, x+10):
            if (xx == x and yy == y):
                print("G", end="")
            else:
                if (xx == adsoX and yy == adsoY):
                    print("A", end="")
                else:
                    if (Visited[xx,yy] == 0):
                        print("·", end="")
                    else:
                        if (Visited[xx,yy] > 0):
                            print(" ", end="")
                        else:
                            print("#", end="")

        print("|")
    print("+---------------------+")

env = gym.make('Abadia-v0')

#Initialize Q-table with all zeros
# Q = np.zeros([env.observation_space.n, env.action_space.n])

nameSnap = "snapshoots/current-qtable"
fsnap = open(nameSnap, "a+")

if os.path.exists(nameSnap) and os.path.getsize(nameSnap) > 0:
    Q = np.load(fsnap)
else:
    Q = np.zeros([512, 512, env.action_space.n])

# Set learning parameters
lr = .8
yy = .95

rList = []

for i_episode in range(50):

    state = env.reset()
    # Reset environment and get first new state
    rAll = 0
    done = False
    Visited = np.zeros([512,512])

    for t in range(5000):
        x = int(env.Personajes['Guillermo']['posX'])
        y = int(env.Personajes['Guillermo']['posY'])

        adsoX = int(env.Personajes['Adso']['posX'])
        adsoY = int(env.Personajes['Adso']['posY'])

        ori = int(env.Personajes['Guillermo']['orientacion'])
        # env.render(mode="human")

        # Choose an action by greedily (with noise) picking from Q table
        noise = np.random.randn(1, env.action_space.n) * (1. / (t + 1))
        action = np.argmax(Q[x, y, :] + noise)
        # print ("noise {}".format(noise))
        # Get new state and reward from environment
        newState, reward, done, info = env.step(action)

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

        newX = int(env.Personajes['Guillermo']['posX'])
        newY = int(env.Personajes['Guillermo']['posY'])

        if (action <= 3):
            if (x != newX or y != newY):
                if (Visited[newX, newY] == 0):
                    reward += 0.05
                if (Visited[newX, newY] % 10 == 0):
                    reward -= 0.05
                Visited[newX, newY] += 1
                print("-------------------------------------------------------")
                print("({},{}) Ori {} inc X {} inc Y {} Visited {}".format(
                    x, y, ori, newX - x, newY -y, Visited[newX, newY]))
                print("-------------------------------------------------------")
            if (x == newX and y == newY):
                if (ori == 0):
                    Visited[x+1, y] += -0.01
                if (ori == 1):
                    Visited[x, y-1] += -0.01
                if (ori == 2):
                    Visited[x-1, y] += -0.01
                if (ori == 3):
                    Visited[x, y+1] += -0.01
                reward -= 0.5
                print("-------------------------------------------------------")
                print("({},{}) Ori {} inc X {} inc Y {} y el puto Adso esta en {},{} Visited {}".format(
                    x, y, ori, newX - x, newY -y, adsoX, adsoY, Visited[newX, newY]))
                print("-------------------------------------------------------")

        if (action == 4 or action == 5):
            if (x == newX and y == newY):
                reward -= 0.2

        if (action == 6 or action == 7):
            if (x == newX and y == newY):
                reward -= 0.5

        # Update Q-Table with new knowledge
        Q[x, y, action] = Q[x, y, action] + lr * (reward + yy * np.max(Q[newX, newY, :]) - Q[x, y, action])
        print("Episode({}:{}) A({}) XYO {},{},{} -> {},{} r:{} tr:{} Q(s,a)= {}".format(
                i_episode, t, action, x, y, ori, newX, newY, reward, rAll, Q[x,y]), end="\r")

        if (t % 20 == 0):
            pintaRejilla()

        rAll += reward
        state = newState
        if done == True:
            break

    # jList.append(j)
    rList.append(rAll)
    np.save(fsnap, Q)

print("Score over time: " + str(sum(rList)/100))

print("Final Q-Table Values")
print(Q)

