# Agent v2 a.k.a. Simple Qlearning
# this agent is a very simple agent using Qlearning

import gym
import gym_abadia
import numpy as np
import os
import argparse

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


def pintaRejilla(Visited, width, height):
    w = int(width/2)
    h = int(height/2)
    yRejilla = 0
    xRejilla = 0

    # TODO: to display all the characters, now only Guillermo and Adso
    # pers = {}
    # for per in env.Personajes:
    #    datos = {'x': per['posX'], 'y': per['posY']}
    #   pers.update(per['id']:datos)
    #

    x     = int(env.Personajes['Guillermo']['posX'])
    y     = int(env.Personajes['Guillermo']['posY'])
    adsoX = int(env.Personajes['Adso']['posX'])
    adsoY = int(env.Personajes['Adso']['posY'])

    print("Guillermo {},{} Adso {},{}".format(x, y, adsoX, adsoY))
    print("+" + "-"*(w*2) + "+" + "-"*24 + "+")
    for yy in range(y-h, y+h):
        print("|", end="")
        for xx in range(x-w, x+w):
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

        print("|", end="")
        if yRejilla < 24:
            for xx in range(0, 23):
                if (env.rejilla[yRejilla][xx] == 0):
                    print (" ", end="")
                else:
                    if (env.rejilla[yRejilla][xx] >= 16):
                        print ("P", end="")
                    else:
                        print ("#", end="")

        print("|", end="")
        if yRejilla < 24:
            for xx in range(0, 23):
                if (env.rejilla[yRejilla][xx] == 0):
                    print ("  ", end="")
                else:
                    print ("{}".format(format(env.rejilla[yRejilla][xx], '2x')), end="")
        yRejilla += 1
        print("|")

    print("+" + "-"*(w*2) + "+")

def mainLoop():


    # Initialize Q-table with all zeros
    # Q = np.zeros([env.observation_space.n, env.action_space.n])

    nameQtableSnap = "snapshoots/current-qtable"

    if os.path.exists(nameQtableSnap) and os.path.getsize(nameQtableSnap) > 0:
        fqtablesnap = open(nameQtableSnap, "rb+")
        Q = np.load(fqtablesnap)
    else:
        fqtablesnap = open(nameQtableSnap, "wb+")
        Q = np.zeros([512, 512, env.action_space.n])
        np.save(fqtablesnap, Q)
        fqtablesnap.flush()
        fqtablesnap.close()

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

    # Set learning parameters
    # lr = .4
    # yy = .98
    lr = .8
    yy = .95

    rList = []
    bucle = 0

    for i_episode in range(env.num_episodes):
        state = env.reset()
        if(env.checkpointName != None):
            # state = env.load_game_checkpoint("partidas/20180425/abadia_checkpoint_18-04-25_23:13:57:264379_1_4_27_23_0.checkpoint")
            state = env.load_game_checkpoint(env.checkpointName)
        # print("reseteado:{}".format(env.Personajes))
        # Reset environment and get first new state
        rAll = 0
        done = False

        for t in range(env.num_steps):
            x = int(env.Personajes['Guillermo']['posX'])
            y = int(env.Personajes['Guillermo']['posY'])

            adsoX = int(env.Personajes['Adso']['posX'])
            adsoY = int(env.Personajes['Adso']['posY'])

            ori = int(env.Personajes['Guillermo']['orientacion'])
            # env.render(mode="human")

            # Choose an action by greedily (with noise) picking from Q table
            noise = np.random.randn(1, env.action_space.n) * (1. / (t + 1))
            action = np.argmax(Q[x, y, :] + noise)

            # Get new state and reward from environment and check if
            # in the state of the game is Guillermo

            while True:
                newState, reward, done, info = env.step(action)
                # we also save the non Guillermo status because there is a lot
                # of clues like monks location, objects, etc
                env.save_action(state, action, reward, newState)
                if env.estaGuillermo:
                    break
                # else:
                    # print("Skipping a screen without Guillermo!!!!")

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                env.save_game()
                if (env.haFracasado):
                    env.reset_fin_partida()
                    break

            newX = int(env.Personajes['Guillermo']['posX'])
            newY = int(env.Personajes['Guillermo']['posY'])

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

            # Update Q-Table with new knowledge
            Q[x, y, action] = \
                Q[x, y, action] + lr * (reward + yy * np.max(Q[newX, newY, :]) - Q[x, y, action])

            print("Episode({}:{}) A({})XYOP {},{},{},{} -> {},{} r:{} tr:{} Q(s,a)= {}".format(
                i_episode, t, action, x, y, ori, env.numPantalla, newX, newY, np.round(reward,2),
                np.round(rAll,2), np.round(Q[x,y],2)), end="\r")

            if (t % 10 == 0 or reward > 0):
                pintaRejilla(env.Visited, 40, 20)

            rAll += reward
            state = newState
            if done == True:
                env.save_game()
                break

        # jList.append(j)
        env.save_game()
        rList.append(rAll)

        fqtablesnap = open(nameQtableSnap, "wb+")
        np.save(fqtablesnap, Q)
        fqtablesnap.flush()
        fqtablesnap.close()

        fvisitedsnap = open(nameVisitedSnap, "wb+")
        np.save(fvisitedsnap, env.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

    print("Score over time: " + str(sum(rList)/env.num_episodes))

    print("Final Q-Table Values")
    print(Q)

if __name__ == '__main__':
    env = gym.make('Abadia-v0')
    init_env(env)
    mainLoop()


