# Agent v7 a.k.a. will use MCTS with gym_abadia version 3

import gym
import gym_abadia
import numpy as np
import argparse
from threading import Thread
import logging
import sys

from AbadIA.NGDQN import NGDQN as NGDQN

def init_env(env):

    logging.basicConfig(format='%(asctime)s:[%(filename)s:%(funcName)s:%(lineno)s]:%(levelname)s:%(message)s', datefmt='%d-%m-%y %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)

    env.logger = logger
    logger.info("Logging subsystem start")

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--server', help='server name')
    argparser.add_argument('-p', '--port', help='port number')
    argparser.add_argument('-a', '--actions', help='actions file with the checkpoint')
    argparser.add_argument('-w', '--actionsstep', help='actions step to be checkpointed')
    argparser.add_argument('-m', '--model', help='model file')
    argparser.add_argument('-i', '--initmodel', help='init model file')
    argparser.add_argument('-e', '--episodes', help='number of episodes')
    argparser.add_argument('-n', '--steps', help='total steps of the episode')
    argparser.add_argument('-g', '--gcs', help='Google storage bucket')
    argparser.add_argument('-l', '--learning', help='Learning mode (True/False)')
    argparser.add_argument('-o', '--obsequium', help='Minimun Obsequium before considering you are dead')
    argparser.add_argument('-v', '--verbose', help='Verbose output')
    argparser.add_argument('-1', '--speedtest', help='Speed Tests')

    args = argparser.parse_args()
    logging.info("args {}".format(args))

    if args.server != None:
        env.server = args.server
        env.set_url()

    if args.port != None:
        env.port = args.port
        env.set_url()

    if args.actions != None:
        env.actionsCheckpointName = args.actions

    if args.actionsstep != None:
        env.actionsCheckpointStep = int(args.actionsstep)

    if args.model != None:
        env.modelName = args.model
    else:
        env.modelName = None

    if args.initmodel != None:
        env.initModelName = args.initmodel
    else:
        env.initModelName = None

    if args.episodes != None:
        env.num_episodes = int(args.episodes)

    if args.steps != None:
        env.num_steps = int(args.steps)

    if args.gcs != None:
        env.gsBucket = args.gcs
        env.init_google_store_bucket()

    if args.learning != None:
        if (args.learning == "True"):
            env.playing = False
        else:
            env.playing = True

    if args.obsequium != None:
        env.minimunObsequium = int(args.obsequium)


    if args.verbose != None:
        env.verbose = int(args.verbose)

    if args.speedtest != None:
        env.speedtest = True


def mainLoop():
    env.logger.info("Ready to Start")
    # TODO: revisar cual es la máxima velocidad
    if (env.speedtest):
        env.speed_test(100)
        exit(0)

    env.logger.info("loading visited spap file")
    env.visited_snap_load()
    env.logger.info("Done")

    rList = []
    bucle = 0

    gamma = 0.9
    epsilon = .95
    env.logger.info("Loading default model last_model_v7.model")
    ngdqn_agent = NGDQN(env=env, initModelName="models/last_model_v7.model")
    env.logger.info("DONE")
    steps = []

    for i_episode in range(env.num_episodes):
        env.logger.info(f'runnig {i_episode} episode')
        state = env.reset()

        if(env.actionsCheckpointName != None):
            state = env.load_actions_checkpoint(env.actionsCheckpointName, env.actionsCheckpointStep)
            if state['obsequium'] < env.minimunObsequium:
                loggin.info("Obsequium {} is less than the minimun required {} so we exit now".format(state['obsequium'], env.minimunObsequium))
                break
            else:
                env.logger.info("Restarting the game from {} step {}".format(env.actionsName, env.actionsCheckpointStep))

        rAll = 0
        done = False

        for t in range(env.num_steps):

            x, y, ori       = env.personajeByName('Guillermo')
            adsoX, adsoY, _ = env.personajeByName('Adso')

            # Get new state and reward from environment and check if
            # in the state of the game is Guillermo
            env.checkValidMovs(ori)

            # TODO JT: just checking how to implement a repeat action in the loop
            # if we're playing not exploring and training we don't want to do this.
            # repeat = random.randint(5)+1
            # TODO v7 quitar el repeat
            action, repeat = ngdqn_agent.act(state)
            env.prev_vector = env.vector

            env.logger.info(f"action {action} repeat {repeat} vector {env.vector}")

            for rep in range(repeat):
                while True:
                    env.logger.info(f"action {action} repeat {rep}/{repeat}")
                    newState, reward, done, info = env.step(action)
                    # we also save the non Guillermo status because there is a lot
                    # of clues like monks location, objects, etc
                    # TODO JT as show at the perfect solution, sometimes Guillermo is not at the screen
                    # that happens when stay NOP for a time for example
                    # so we need to test it eliminate this loop

                    env.save_action(state, action, reward, newState)
                    if env.estaGuillermo:
                        break

                ngdqn_agent.remember(env.prev_vector, action, reward, env.vector, done)

                if done:
                    env.logger.info(f'Episode finished after {t+1} steps')
                    if (env.haFracasado):
                        env.logger.info(f'Episode finished with a FAIL')
                        env.reset_fin_partida()
                        break
                env.update_visited_cells(x, y, ori)

                # TODO JT: we need to create an option for this
                newX, newY, newO = env.personajeByName('Guillermo')
                env.pintaRejilla(40, 20)
                env.logger.info("E{}:curr_step {} {}-{} X:{} Y:{},{},{}->{},{} O{} %{} reward:{} tr:{} V:{}"
                             .format(i_episode, env.curr_step, action, env.actions_list[action], x, y, ori, env.numPantalla,
                                     newX, newY, env.obsequium, env.porcentaje, np.round(reward,8),
                                     np.round(rAll,8), np.round(env.predictions,4)))

                env.checkValidMovs(newO)
                x, y, ori = env.personajeByName('Guillermo')
                rAll += reward
                state = newState
                if done == True:
                    env.logger.info("DONE is True, exit and dont save the game")
                    break
                if env.valMovs[action] == 0:
                    env.logger.info("Invalid Action: Leaving the loop of the repeat")
                    break

            if env.playing == False and (t % 100) == 1:
                ngdqn_agent.replay()        # internally iterates default (prediction) model
                ngdqn_agent.target_train()


        env.save_game()

        # TODO JT: refactoring this: the way we storage models and add info to game json
        # TODO JT: check if this make sense
        nameModel = "models/model_v7_{}_trial_{}.model".format(env.gameId, i_episode)

        ngdqn_agent.save_model(nameModel)

        if (env.gsBucket != None and np.random.randint(10) <= 1):
            env.logger.info("Uploading model to GCP")
            thread = Thread(target=env.upload_blob, args=(nameModel, nameModel))
            thread.start()

        rList.append(rAll)

        if t >= env.num_steps:
            env.logger.info("Failed to complete in trial {}".format(env.num_episodes))

        if (np.random.randint(10) <= 1):
            env.visited_snap_save()

    # TODO JT, we need to save all the info available (model version, total reward, etc)
    #  so we can analyze the games
    env.logger.info("Score over time: " + str(sum(rList)/env.num_episodes))

if __name__ == '__main__':
    print("Creating Abadia v4 gym and customized env")
    env = gym.make('Abadia-v4')
    init_env(env)
    env.logger.info("Created Abadia v4 gym and customized env")
    mainLoop()