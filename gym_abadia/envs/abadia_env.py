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
        self.__version__ = "0.0.2"
        print("AbadiaEnv - Version {}".format(self.__version__))


        self.url    = "http://localhost:4477"
        self.server = "http://localhost"
        self.port   = "4477"

        self.gameName    = ""
        self.actionsName = ""
        self.dump_path  = "partidas/now/"

        # Define what the agent can do
        # 0 -> STEP ORI 0
        # 1 -> STEP ORI 1
        # 2 -> STEP ORI 2
        # 3 -> STEP ORI 3
        # 4 -> RIGHT
        # 5 -> LEFT
        # 6 -> NOP
        # 7 -> DOWN

        self.action_space = spaces.Discrete(8)

        # json from the dump state of the episode

        self.json_dump = {}

        self.actions_list = ("cmd/A", "cmd/A" ,"cmd/A", "cmd/A", "cmd/D", "cmd/I", "cmd/N", "cmd/B")
        self.obsequium = -1
        self.porcentaje = -1
        self.haFracasado = False
        self.prevPantalla = -1
        self.rejilla = []


        # TODO: JT: check what variables we need.
        # General variables defining the environment
        self.MAX_PRICE = 2.0
        self.TOTAL_TIME_STEPS = 2

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

        # Observation is the remaining time
        low = np.array([0.0,  # remaining_tries
                         ])
        high = np.array([self.TOTAL_TIME_STEPS,  # remaining_tries
                         ])
        self.observation_space = spaces.Box(low, high)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

    def sendCmd(self, url, command):
        cmd = "{}/{}".format(url, command)
        r = requests.get(cmd)
        # print("cmd {} -> {}".format(cmd, r.text))
        # print("cmd {} -> {}".format(cmd, r.json))
        return r.json()

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
        self.haFracasado =  (ob['haFracasado'] == 'True')

        self.rejilla = ob['rejilla']
        # print(self.rejilla)

        if (self.haFracasado == True):
            self.game_is_gone = True

        # we need to check is make sense finish it
        # if self.is_game_done or self.porcentaje == 100:
        #   raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)

        # reward = self._get_reward()

        reward = 0

        if (self.prevPantalla == -1):
            self.prevPantalla = int(ob['numPantalla'])
        else:
            if (self.prevPantalla != int(ob['numPantalla'])):
                reward += 0.1
                self.prevPantalla = int(ob['numPantalla'])

        reward += (self.porcentaje) / 33

        reward += (self.obsequium / 300)

        # reward = self._get_reward()

        return ob, reward, self.is_game_done, {}

    def _get_personajes_info(self, ob):
        # print ("ob personajes -> {} ", ob['Personajes']['Personaje'][0])

        for persona in self.listaPersonajes[:]:
            datos = self.Personajes[persona]
            datos = {}
        for personaje in ob['Personajes']['Personaje']:
            if (len(personaje) == 1):
                break
            persona = self.listaPersonajes[int(personaje['id'])]
            datos = self.Personajes[persona]
            for key, value in personaje.items():
                #if key != "id" or key != "fil":
                datos[key] = value
            self.Personajes[persona] = datos
            # print ("{} personaje: {}", persona, datos)


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
        now = datetime.datetime.now()
        self.gameName    = now.strftime('abadia_game_%y-%m-%d_%H:%M:%S:%f.json')
        self.actionsName = now.strftime('abadia_actions_%y-%m-%d_%H:%M:%S:%f.json')

        self.curr_episode += 1
        self.action_episode_memory.append([])
        self.is_game_done = False

        self.sendCmd(self.url,"reset")
        self.init_dumps_files()
        time.sleep(2)
        return self._get_state()

    def render(self, mode='human', close=False):
        print("state info: {}\n".format(self))
        return

    def _get_state(self):
        """Get the observation."""
        # ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        ob = self.sendCmd(self.url, "dump")
        self._get_personajes_info(ob)
        return ob

    def _seed(self, seed):
        random.seed(seed)
        np.random.seed


    def graba_partida(self):
        pass

    def save_action(self, state, action, reward, nextstate):
        s1 = state.copy()
        s2 = nextstate.copy()
        s1.pop('rejilla')
        s2.pop('rejilla')

        self.fdActions.write("action: {} state: {}, action:{}, reward:{}, nextstate{} {}\n"
                             .format("{", s1, action, reward, s2, "}"))

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


