#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulate the "Abbey of crime" environment.

Each episode is making a single action (doing nothing is an action) .
"""

# core modules
import random
import math
import json
import time
import datetime
from pathlib import Path

# 3rd party modules
import gym
import numpy as np
from gym import spaces



# AbadIA dependencies
import requests

def get_chance(x):
    """Get probability that a banana will be sold at price x."""
    e = math.exp(1)
    return (1.0 + e) / (1. + math.exp(x + 1))


class AbadiaEnv(gym.Env):
    """
    Define a Abadia environment.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        self.__version__ = "0.0.4"
        print("AbadiaEnv - Version {}".format(self.__version__))


        self.url    = "http://localhost:4477"
        self.server = "http://localhost"
        self.port   = "4477"
        self.num_episodes   = 100
        self.num_steps      = 1500


        self.gameName       = ""
        self.actionsName    = ""
        self.checkpointName = None
        self.dump_path      = "partidas/now/"
        self.gameId = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
        self.checkpointSec  = 1
        self.eventsGame    = []
        self.eventsAction   = []


        # Define what the agent can do
        # 0 -> STEP ORI 0
        # 1 -> STEP ORI 1
        # 2 -> STEP ORI 2
        # 3 -> STEP ORI 3
        # 4 -> RIGHT
        # 5 -> LEFT
        # 6 -> DOWN
        # 7 -> NOP

        self.action_space = spaces.Discrete(7)

        # json from the dump state of the episode

        self.json_dump = {}

        self.actions_list = ("cmd/A", "cmd/A" ,"cmd/A", "cmd/A", "cmd/D", "cmd/I", "cmd/B", "cmd/N")
        self.obsequium = -1
        self.porcentaje = -1
        self.haFracasado = False
        self.prevPantalla = -1
        self.rejilla = []
        self.prev_ob = dict()
        self.estaGuillermo= False


        self.curr_step = -1
        self.is_game_done = False

        self.Personajes = {
            "Guillermo":  {},
            "Adso":       {},
            "Abad":       {},
            "Malaquias":  {},
            "Berengario": {},
            "Severino":   {},
            "Jorge":      {},
            "Bernardo":   {}
        }

        self.listaPersonajes = ("Guillermo", "Adso", "Abad", "Malaquias", "Berengario",
            "Severino", "Jorge", "Bernardo")

        self.Visited = np.zeros([512, 512])

        # Observation is the remaining time
        low = np.array([0.0,  # remaining_tries
                         ])
        high = np.array([512, ])
        self.observation_space = spaces.Box(low, high)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

    def set_url(self):
        self.url = self.server + ":" + self.port

    def sendCmd(self, url, command, type="json"):
        cmd = "{}/{}".format(url, command)
        r = requests.get(cmd)
        # print("cmd {} -> {}".format(cmd, r.text))
        # print("cmd {} -> {}".format(cmd, r.json))
        if (type == "json"):
            return r.json()
        else:
            return r.text

    def step(self, action):
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """

        ob = self.sendCmd(self.url, self.actions_list[action])
        # print("ob -> {}".format(ob)) # ['obsequium']))

        # extracting all the values from the json
        # first personajes

        self._get_personajes_info(ob)

        self.obsequium    = int(ob['obsequium'])
        self.porcentaje   = int(ob['porcentaje'])
        self.bonus        = int(ob['bonus'])
        self.numPantalla  = int(ob['numPantalla'])
        self.dia          = int(ob['dia'])
        self.momentoDia   = int(ob['momentoDia'])
        self.haFracasado  = (ob['haFracasado'] == 'True')
        self.rejilla = ob['rejilla']



        # print(self.rejilla)

        # we need to check is make sense finish it
        # if self.is_game_done or self.porcentaje == 100:
        #   raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)

        ob['jugada'] = self.curr_step
        ob['gameId'] = self.gameId

        # reward = self._get_reward()

        reward = 0
        self.eventsAction = []
        # JT we need to check, that pass to another room
        # not just stay all the time between rooms to get the reward

        if self.estaGuillermo:
            if (self.prevPantalla == -1):
                self.prevPantalla = int(ob['numPantalla'])
            else:
                if (self.prevPantalla != int(ob['numPantalla'])):
                    reward += 50
                    print("----------")
                    print("reward by screen change !!!!! {} !=  {}".format(self.prevPantalla, int(ob['numPantalla'])))
                    print("Personajes: {}".format(self.Personajes))
                    print("ob: {}".format(ob))
                    print("----------")
                    self.add_event("NewRoom", "prev {} curr {}".format(self.prevPantalla, int(ob['numPantalla'])), 50)
                    self.prevPantalla = int(ob['numPantalla'])
                    self.save_game_checkpoint()

        if len(self.prev_ob) > 0:
            # reward for incrementing the obsequium: > 0 +50 / < 0 -30
            incr_obsequium = self.obsequium - int(self.prev_ob['obsequium'])
            if incr_obsequium > 0:
                reward += (50 * incr_obsequium)
                self.add_event("IncrObsequium", "Incr {}".format(incr_obsequium), 50)

            if incr_obsequium < 0:
                reward += (-30 * incr_obsequium)
                self.add_event("DecrObsequium", "Decr {}".format(incr_obsequium), -30)

            # reward for incrementing the bonus: >0 +500
            incr_bonus = self.bonus - int(self.prev_ob['bonus'])
            if incr_bonus > 0:
                reward += (500 * incr_bonus)
                self.add_event("Bonus", "prev {} curr {}".format(self.bonus, int(self.prev_ob['bonus'])), 500)

        self.eventsGame.extend(self.eventsAction)
        # if the game is over, we just finish the game and reward is -1000
        # if we completed the game, we finish and the reward is 5000
        # the percentage must be variable to help the AI to learn
        # with variable explanatory/explotation

        if (self.haFracasado == True):
            self.game_is_done = True
            reward = -1000

        if (self.porcentaje >= 90):
            self.game_is_done = True
            reward = 5000

        if reward == 0:
            reward = -0.1

        ob['reward'] = reward

        # we make a copy for the current observation in order to calculate
        # the reward for the next state

        self.prev_ob = ob

        # JT chequear si esto está bien, no parece que este devolviendo bien el estado siguiente!!!

        return ob, reward, self.is_game_done, {}

    def _get_personajes_info(self, ob):
        # print ("ob personajes -> {} ", ob['Personajes']['Personaje'][0])
        self.estaGuillermo = False
        for persona in self.listaPersonajes[:]:
            self.Personajes[persona] = {}
        for personaje in ob['Personajes']['Personaje']:
            if (len(personaje) == 1):
                break
            persona = self.listaPersonajes[int(personaje['id'])]
            datos = self.Personajes[persona]
            for key, value in personaje.items():
                #if key != "id" or key != "fil":
                datos[key] = value
            self.Personajes[persona] = datos
            if int(personaje['id']) == 0:
                self.estaGuillermo = True

        return self.estaGuillermo


    def _take_action(self, action):
        self.action_episode_memory[self.curr_episode].append(action)

        game_is_done = (self.obsequium <= 0)

        if game_is_done:
            self.is_game_done = True

        # remaining_steps = self.TOTAL_TIME_STEPS - self.curr_step
        # time_is_over = (remaining_steps <= 0)
        # throw_away = time_is_over and not self.is_banana_sold
        # if throw_away:
            # self.is_banana_sold = False # abuse this a bit
            # self.price = 0.0

    def _get_reward(self):
        """Reward is about how complete is the game"""
        if self.is_game_done:
            return self.price - 1
        else:
            return 0.0

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.gameId      = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
        self.gameName    = "abadia_game_{}.json".format(self.gameId)
        self.actionsName = "abadia_actions_{}.json".format(self.gameId)

        self.curr_episode += 1
        self.curr_step     = 1

        self.eventsGame = []
        self.eventsAction = []

        self.action_episode_memory.append([])
        self.is_game_done = False

        self.sendCmd(self.url,"reset")
        self.init_dumps_files()
        time.sleep(5)
        return self._get_state()

    def render(self, mode='human', close=False):
        print("state info: {}\n".format(self))
        return

    def _get_state(self):
        """Get the observation."""
        # ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        print("I wil got the initial state with Guillermo")
        tooboring = 0
        while True:
            ob = self.sendCmd(self.url, "dump")
            tooboring += 1
            if self._get_personajes_info(ob):
                print("getting the characters from ob:{}".format(ob))
                print("DONE")
                break
            else:
                print("getting the characters from ob:{}".format(ob))
                print("Guillermo is not present yet, waiting")
                # self.sendCmd(self.url, "cmd/_")
                if tooboring % 10 == 0:
                    print("Getting Boring ...")
                    if tooboring <= 10:
                        self.sendCmd(self.url, "cmd/_")
                    else:
                        self.sendCmd(self.url, "fin")
                    # self.sendCmd(self.url, "cmd/B")
                    # self.sendCmd(self.url, "cmd/A")
                    time.sleep(1)
                time.sleep(2)
        return ob

    def _seed(self, seed):
        random.seed(seed)
        np.random.seed

    def add_event(self, name, des, reward):
        self.eventsAction.append({'name': name, 'des':des, 'reward': reward})
        print("events {}".format(self.eventsAction))

    def save_game(self):
        self.fdGame.write("{}{}\"gameId\":\"{}\", \"totalSteps\":{}, \"obsequium\":{}, \"porcentaje\":{}, \"bonus\":{}, "
                          .format("[", "{", self.gameId, self.curr_step, self.obsequium, self.porcentaje, self.bonus))

        self.fdGame.write("\"events\":{}"
                .format(json.dumps(self.eventsGame)))

        self.fdGame.write("{}\n".format("}]"))
        self.fdGame.flush()
        self.fdGame.close()

    def save_action(self, state, action, reward, nextstate):
        s1 = state.copy()
        s2 = nextstate.copy()
        s1.pop('rejilla')
        s2.pop('rejilla')

        self.fdActions.write("{}{}\"action\":{}\"state\":{},\"action\":{},\"reward\":{},\"nextstate\":{}{}{}\n"
                             .format("[", "{", "{", json.dumps(s1), action, reward, json.dumps(s2), "}", "}]"))
        self.fdActions.flush()

    def reset_fin_partida(self):
        ob = self.sendCmd(self.url, "cmd/_")

    def init_dumps_files(self):

        # check is directory exist, if not we will create it
        now = datetime.datetime.now()
        self.dump_path = now.strftime('partidas/%Y%m%d')
        path = Path(self.dump_path)
        path.mkdir(parents=True, exist_ok=True)

        # create the game and actions files
        self.fdGame    = open(self.dump_path + "/" + self.gameName, "w")
        self.fdActions = open(self.dump_path + "/" + self.actionsName, "w")

    def save_game_checkpoint(self):

        checkpoint = self.sendCmd(self.url, "save", type="raw")

        now = datetime.datetime.now()
        self.dump_path = now.strftime('partidas/%Y%m%d')
        path = Path(self.dump_path)
        path.mkdir(parents=True, exist_ok=True)

        # create the game and actions files
        self.checkpointTmpName  = "abadia_checkpoint_{}_{}".format(self.gameId, self.checkpointSec)
        self.checkpointSec     += 1
        self.checkpointTmpName += "_{}_{}_{}_{}_{}.checkpoint".format(self.dia, self.momentoDia,
                                                self.numPantalla, self.obsequium, np.round(self.porcentaje,2))

        self.fdCheckpoint = open(self.dump_path + "/" + self.checkpointTmpName, "w")
        self.fdCheckpoint.write(checkpoint)
        self.fdCheckpoint.flush()

    def load_game_checkpoint(self, name):
        # name = "partidas/20180425/abadia_checkpoint_18-04-25_23:13:57:264379_1_4_27_23_0.checkpoint"
        print("voy a abrir el fichero ({})".format(name))
        self.fdCheckpoint = open(name, "r")
        checkpoint = self.fdCheckpoint.read()
        requests.post(self.url+"/load", data=checkpoint[:-6 ])
        time.sleep(2)
        return self._get_state()

