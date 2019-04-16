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
import os
from pathlib import Path

# 3rd party modules
import gym
import numpy as np
from gym import spaces
from google.cloud import storage

import logging

# AbadIA2 dependencies
import requests

def get_chance(x):
    """Get probability that a banana will be sold at price x."""
    e = math.exp(1)
    return (1.0 + e) / (1. + math.exp(x + 1))


class AbadiaEnv2(gym.Env):
    """
    Define a Abadia2 environment.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        self.__version__ = "0.0.7"
        print("AbadiaEnv2 - Version {}".format(self.__version__))


        self.url    = "http://localhost:4477"
        self.server = "http://localhost"
        self.port   = "4477"
        self.num_episodes   = 100
        self.num_steps      = 1500
        self.gsBucket       = None


        self.gameName       = ""
        self.actionsName    = ""
        self.checkpointName = None
        self.modelName      = None
        self.dump_path      = "games/now/"
        self.gameId = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
        self.checkpointSec  = 1
        self.storage_client = None
        self.storage_client = None
        self.eventsGame     = []
        self.eventsAction   = []
        self.totalReward    = 0.0
        self.verbose        = 0
        self.playing        = False


        # Define what the agent can do
        # 0 -> STEP FORWARD
        # 1 -> RIGHT
        # 2 -> LEFT
        # 3 -> DOWN
        # 4 -> GET

        self.action_space = spaces.Discrete(9)

        # json from the dump state of the episode

        self.json_dump = {}

        self.action_mode = 1

        self.actions_list_2 = ("abadIA/game/current/actions/UP",
                             "abadIA/game/current/actions/RIGHT",
                             "abadIA/game/current/actions/LEFT",
                             "abadIA/game/current/actions/DOWN",
                             "cmd/N",
                             "cmd/_"
                             )
        self.actions_list = ("N", "NE", "E", "SE", "S", "SW", "W", "NW", "NOP")

        self.obsequium = -1
        self.porcentaje = -1
        self.haFracasado = False
        self.prevPantalla = -1
        self.rejilla = []
        self.prev_ob = dict()
        self.estaGuillermo= False
        self.room = np.zeros([20,20,3], np.int)


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

        # Observation is the position of Guillermo and the information of the room
        X = np.array([0, 256])
        Y = np.array([0, 256])
        O = np.array([0,   4])

        high = np.array([np.inf] * 15)  # useful range is -1 .. +1, but spikes can be higher
        self.observation_space = spaces.Box(-high, high)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

        now = datetime.datetime.now()
        self._seed(time.mktime(now.timetuple()))
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%m-%y %H:%M:%S',
                            level=logging.INFO)

        # helper to normalize paths to positions
        #   1
        # 2   0
        #   3

        self.path2Pos = {
            "0N": "LEFT:UP:UP",
            "1N": "UP:UP",
            "2N": "RIGHT:UP:UP",
            "3N": "RIGHT:RIGHT:UP:UP",

            "0NE": "UP:UP:LEFT:UP:UP",
            "1NE": "UP:UP:RIGHT:UP:UP",
            "2NE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "3NE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",

            "0E": "UP:UP",
            "1E": "RIGHT:UP:UP",
            "2E": "RIGHT:RIGHT:UP:UP",
            "3E": "LEFT:UP:UP",

            "0SE": "UP:UP:RIGHT:UP:UP",
            "1SE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "2SE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "3SE": "UP:UP:LEFT:UP:UP",

            "0S": "RIGHT:UP:UP",
            "1S": "RIGHT:RIGHT:UP:UP",
            "2S": "LEFT:UP:UP",
            "3S": "UP:UP",

            "0SW": "RIGHT:UP:UP:RIGHT:UP:UP",
            "1SW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "2SW": "UP:UP:LEFT:UP:UP",
            "3SW": "UP:UP:RIGHT:UP:UP",

            "0W": "RIGHT:RIGHT:UP:UP",
            "1W": "LEFT:UP:UP",
            "2W": "UP:UP",
            "3W": "RIGHT:UP:UP",

            "0NW": "LEFT:UP:UP:LEFT:UP:UP",
            "1NW": "UP:UP:LEFT:UP:UP",
            "2NW": "UP:UP:RIGHT:UP:UP",
            "3NW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP"

        }

    def set_url(self):
        self.url = self.server + ":" + self.port
    # TODO JT refactoring and eliminate this function
    def sendReset(self):
        self.sendCmd(self.url, "abadIA/game/current/actions/SPACE", mode='POST')
        # sleep(1)
        self.sendCmd(self.url, "abadIA/game/current/actions/SPACE", mode='POST')
        return self.sendCmd(self.url, "abadIA/game", mode="POST")

    def sendCmd(self, url, command, type="json", mode="GET"):
        cmd = "{}/{}".format(url, command)
        if mode == "GET":
            r = requests.get(cmd)
        if mode == "POST":
            r = requests.post(cmd)
        if (type == "json"):
            headers = {'accept': 'application/json'}
        else:
            headers = {'accept': 'text/x.abadIA+plain'}

        cmdDump = "{}/abadIA/game/current".format(url)
        r = requests.get(cmdDump, headers= headers)
        if r.status_code == 599:
            tmp = r.json()
            tmp['haFracasado'] = True
            return tmp

        if (type == "json"):
            return r.json()
        else:
            return r.text

    def sendMultiCmd(self, path):
        logging.info("Path: %s Cmds: %s" % (path,  self.path2Pos[path]))
        cmds = self.path2Pos[path].split(":")
        for step in cmds:
            self.sendCmd(self.url, "abadIA/game/current/actions/{}".format(step), mode='POST')

        headers = {'accept': 'application/json'}
        cmdDump = "{}/abadIA/game/current".format(self.url)
        r = requests.get(cmdDump, headers=headers)
        if r.status_code == 599:
            tmp = r.json()
            tmp['haFracasado'] = True
            return tmp

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

        if (action >=8 ):
            ob = self.sendCmd(self.url, self.actions_list[action], mode="POST")
        else:
            ori = str(self.Personajes['Guillermo']['orientacion'])
            ob = self.sendMultiCmd(ori + self.actions_list[action])

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
        self.haFracasado  = ob['haFracasado']
        self.rejilla      = ob['Rejilla']


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
                    reward += 0.03
                    logging.info("----------")
                    logging.info("reward by screen change !!!!! {} !=  {}".format(self.prevPantalla, int(ob['numPantalla'])))
                    logging.info("Personajes: {}".format(self.Personajes))
                    logging.info("ob: {}".format(ob))
                    logging.info("----------")
                    self.add_event("NewRoom", "prev {} curr {}".format(self.prevPantalla, int(ob['numPantalla'])), 0.001)
                    self.prevPantalla = int(ob['numPantalla'])
                    self.save_game_checkpoint()

        # If there is an obsequium change, it will be rewarded pos/neg
        if len(self.prev_ob) > 0 and int(self.prev_ob['obsequium']) > 0:
            # reward for incrementing the obsequium: > 0 +50 / < 0 -30
            incr_obsequium = self.obsequium - int(self.prev_ob['obsequium'])
            if incr_obsequium > 0:
                reward += (50 * incr_obsequium) / 10000
                self.add_event("IncrObsequium", "Obsequium {} Incr {}".format(self.prev_ob['obsequium'],incr_obsequium), (50 * incr_obsequium) / 10000)

            if incr_obsequium < 0:
                reward += (30 * incr_obsequium) / 10000
                self.add_event("DecrObsequium", "Obsequium {} Decr {}".format(self.prev_ob['obsequium'], incr_obsequium),(30 * incr_obsequium) / 10000)

        # reward for incrementing the bonus: >0 +500
        if len(self.prev_ob) > 0 and int(self.prev_ob['bonus']) > 0:
            incr_bonus = self.bonus - int(self.prev_ob['bonus'])
            if incr_bonus > 0:
                reward += (500 * incr_bonus) / 10000
                self.add_event("Bonus", "prev {} curr {}".format(self.bonus, int(self.prev_ob['bonus'])), (500 * incr_bonus) / 10000)

        # we check if Guillermo change his position. Positive reward if yes, negative if no
        # if action == 0:
        if len(self.prev_ob) > 0 and len(self.prev_ob['Personajes']) > 0:
            prev = self.dataPersonaje(self.prev_ob, "Guillermo")
            curr = self.dataPersonaje(ob, "Guillermo")
            if (prev['posX'] != curr['posX']) or (prev['posY'] != curr['posY']):
                logging.info("se ha movido: {},{} -> {},{}".format(prev['posX'], prev['posY'],
                                                        curr['posX'], curr['posY']))
                reward += 0.001

        # TODO: check this self.eventsGame.extend(self.eventsAction)
        # if the game is over, we just finish the game and reward is -1000
        # if we completed the game, we finish and the reward is 5000
        # the percentage must be variable to help the AI to learn
        # with variable explanatory/explotation

        if (self.haFracasado == True):
            logging.info("GAME OVER")
            self.sendCmd(self.url, "/abadIA/game", mode='POST', type='raw')

            self.game_is_done = True
            reward = -1

        if (self.porcentaje >= 90):
            self.game_is_done = True
            logging.info("FUCKING YEAH GAME ALMOST DONE")
            logging.info("FUCKING YEAH GAME ALMOST DONE")
            logging.info("FUCKING YEAH GAME ALMOST DONE")
            logging.info("FUCKING YEAH GAME ALMOST DONE")
            logging.info("FUCKING YEAH GAME ALMOST DONE")
            reward = 1

        # if no reward we penalized it
        if reward == 0:
            logging.info("***** No reward, penalizing it")
            reward = -0.005

        if self.obsequium > 0:
            reward = reward * float((self.obsequium / self.obsequium)*0.5)
        if self.porcentaje > 0:
            reward = reward * float(((self.porcentaje * 0.5) / self.porcentaje)+1)

        if (self.wallMovs[action] == 1):
            logging.info("***** Invalid move against Wall, penalizing it")
            reward = -0.0901

        if (self.perMovs[action] == 1):
            logging.info("***** Invalid move against a Character, penalizing it")
            reward = -0.0902

        self.totalReward += reward
        ob['reward'] = reward
        ob['totalReward'] = self.totalReward
        logging.info("reward: {} tr: {} action: {} ".format(reward, self.totalReward, action))

        # adding more information for debugging: valid moves, vectors, predictions, etc.
        ob['valMovs'] = self.valMovs.tolist()
        ob['wallMovs'] = self.wallMovs.tolist()
        ob['perMovs'] = self.perMovs.tolist()
        ob['predictions'] = self.calculated_predictions
        ob['final'] = self.final_predictions
        ob['vector'] = self.vector_predictions
        ob['action_predictions'] = self.action_predictions
        ob['action_type'] = self.action_type

        # we make a copy for the current observation in order to calculate
        # the reward for the next state

        self.ob = ob
        self.prev_ob = ob

        # JT chequear si esto está bien, no parece que este devolviendo bien el estado siguiente!!!

        return ob, reward, self.game_is_done, {}

    def _get_personajes_info(self, ob):
        # print ("ob personajes -> {} ", ob['Personajes']['Personaje'][0])
        self.estaGuillermo = False
        for persona in self.listaPersonajes[:]:
            self.Personajes[persona] = {}
        for personaje in ob['Personajes']:
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

    # check is make sense do it for special state

    def normalizaVisited(self, x, y):
        bordes = []
        for X in range(x-1, x+2):
            for Y in range(y-1, y+2):
                if (self.Visited[X,Y] < 0):
                    bordes.append(1)
                else:
                    bordes.append(0)
        # print("bordes {}".format(bordes))
        return bordes

    def stateVector(self):
        x, y, ori    = self.personajeByName('Guillermo')
        ax, ay, aori = self.personajeByName('Adso')

        vector = np.append([x, y, ori, ax, ay, aori],self.normalizaVisited(x,y))
        # print("vector {}".format(vector))
        return vector.reshape(1,15)

    def _take_action(self, action):
        self.action_episode_memory[self.curr_episode].append(action)

        game_is_done = (self.obsequium <= 0)

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

        self.eventsGame   = []
        self.eventsAction = []
        self.totalReward  = 0.0
        self.predictions  = []

        self.action_episode_memory.append([])
        # self.is_game_done = False
        self.game_is_done = False

        logging.info('-----> RESET the GAME')
        ob = self.sendReset()
        logging.info('reset status {}'.format(ob))
        logging.info('-----> DONE')
        logging.info('-----> INIT dumps files: START ...')
        self.init_dumps_files()
        logging.info('-----> INIT dumps files: DONE')
        # time.sleep(5)
        if self._get_personajes_info(ob):
            logging.info('Esta Guillermo')
        return ob

    def render(self, mode='human', close=False):
        logging.info('state info: {}'.format(self))
        return

    def _get_state(self):
        """Get the observation."""
        # ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        logging.info("--------> I wil got the initial state with Guillermo")
        tooboring = 0
        while True:
            ob = self.sendCmd(self.url, "/abadIA/current/game", mode='GET', type='json')
            logging.info("{}".format(ob))
            tooboring += 1
            if self._get_personajes_info(ob):
                logging.info("getting the characters from ob:{}".format(ob))
                logging.info("DONE")
                break
            else:
                logging.info("getting the characters from ob:{}".format(ob))
                logging.info("Guillermo is not present yet, waiting")
                if tooboring % 10 == 0:
                    logging.info("Getting Boring ...")
                    if tooboring <= 10:
                        self.sendCmd(self.url, "start")
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

    # "planta": "0", "sonidos": ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], "frases": [], "Personajes": {"Personaje": [{"id": "0", "nombre": "Guillermo", "posX": "137", "posY": "168", "altura": "0", "orientacion": "0", "objetos": "32"}, {"id": "1", "nombre": "Adso", "posX": "134", "posY": "168", "altura": "0", "orientacion": "1", "objetos": "32"}]}, "Objetos": {"ListaObjetos": []}
    def get_commons(self):
        commons = dict()
        commons.update({'timestamp': "{}".format(datetime.datetime.now()), 'numDia': int(self.ob['dia'])})
        commons.update({'momentoDia': int(self.ob['momentoDia']), 'obsequium': int(self.ob['obsequium'])})
        x = int(self.Personajes['Guillermo']['posX'])
        y = int(self.Personajes['Guillermo']['posY'])
        pantallaHex = "%1X%1X" % (x >> 4, y >> 4)
        commons.update({'numPantalla': int(self.ob['numPantalla']), 'pantallaHex': pantallaHex})
        commons.update({'planta': int(self.ob['planta']), 'guillermoPosX': x, 'guillermoPosY': y})
        commons.update({'bonus': int(self.ob['bonus']), 'porcentaje': int(self.ob['porcentaje'])})
        return commons

    def init_google_store_bucket(self):
        storage_client = storage.Client()
        self.google_storage_bucket = storage_client.get_bucket(self.gsBucket)

    def download_blob(self, source_blob_name, destination_file_name):
        blob = self.google_storage_bucket.blob(source_blob_name)
        directory = os.path.dirname(destination_file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        blob.download_to_filename(destination_file_name)

        logging.info('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))

    def upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        blob = self.google_storage_bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        logging.info('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def add_event(self, name, des, reward):
        data = {'name': name, 'des': des, 'reward': reward, 'totalReward': self.totalReward, 'version': 1}
        data.update(self.get_commons())

        self.eventsAction.append(data)
        logging.info("events {}".format(self.eventsAction))

    def save_game(self):
        self.fdGame.write("{}{}\"gameId\":\"{}\", \"totalSteps\":{}, \"obsequium\":{}, \"porcentaje\":{}, \"bonus\":{}, "
                          .format("[", "{", self.gameId, self.curr_step, self.obsequium, self.porcentaje, self.bonus))

        self.fdGame.write("\"totalReward\": \"{}\", "
                          .format("%.4f" % self.totalReward))

        self.fdGame.write("\"events\":{}"
                .format(json.dumps(self.eventsGame)))

        self.fdGame.write("{}\n".format("}]"))
        self.fdGame.flush()
        # self.fdGame.close()
        if (self.gsBucket != None):
            logging.info("Uploading Game: {} to GCP".format(self.dump_path + "/" + self.gameName))
            self.upload_blob(self.dump_path + "/" + self.gameName,
                             self.dump_path + "/" + self.gameName)
            logging.info("Uploading Actions: {} to GCP".format(self.dump_path + "/" + self.actionsName))
            self.upload_blob(self.dump_path + "/" + self.actionsName,
                             self.dump_path + "/" + self.actionsName)

    def save_action(self, state, action, reward, nextstate):
        s1 = state.copy()
        s2 = nextstate.copy()

        self.fdActions.write("{}{}\"action\":{}\"state\":{},\"action\":{},\"reward\":{},\"nextstate\":{}{}{}\n"
                             .format("[", "{", "{", json.dumps(s1), action, reward, json.dumps(s2), "}", "}]"))
        self.fdActions.flush()


    def visited_snap_load(self):
        nameVisitedSnap = "snapshoots/current-visited"
        if (self.gsBucket != None):
            logging.info("Downloading Visited from GCP")
            try:
                self.download_blob(nameVisitedSnap, nameVisitedSnap)
            except:
                logging.info("File {} not exist at bucket {}".format(nameVisitedSnap, self.gsBucket))

        if os.path.exists(nameVisitedSnap) and os.path.getsize(nameVisitedSnap) > 0:
            fvisitedsnap = open(nameVisitedSnap, "rb+")
            self.Visited = np.load(fvisitedsnap)
        else:
            fvisitedsnap = open(nameVisitedSnap, "wb+")
            self.Visited = np.zeros([512, 512])
            np.save(fvisitedsnap, self.Visited)
            fvisitedsnap.flush()
            fvisitedsnap.close()

            if (self.gsBucket != None):
                logging.info("Uploading to GCP")
                self.upload_blob(nameVisitedSnap, nameVisitedSnap)

    def visited_snap_save(self):
        nameVisitedSnap = "snapshoots/current-visited"

        fvisitedsnap = open(nameVisitedSnap, "wb+")
        np.save(fvisitedsnap, self.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

        if (self.gsBucket != None):
            logging.info("Uploading visited to GCP")
            self.upload_blob(nameVisitedSnap, nameVisitedSnap)


    def reset_fin_partida(self):
        self.sendCmd(self.url, "abadIA/game/current/actions/SPACE", mode='POST')
        ob = self.sendCmd(self.url, "abadIA/game", mode="POST")

    def init_dumps_files(self):

        # check is directory exist, if not we will create it
        now = datetime.datetime.now()
        self.dump_path = now.strftime('games/%Y%m%d')
        path = Path(self.dump_path)
        path.mkdir(parents=True, exist_ok=True)

        # create the game and actions files
        self.fdGame    = open(self.dump_path + "/" + self.gameName, "w")
        self.fdActions = open(self.dump_path + "/" + self.actionsName, "w")

    def save_game_checkpoint(self):

        checkpoint = self.sendCmd(self.url, "/abadIA/game/current", mode='GET', type="raw")

        now = datetime.datetime.now()
        self.dump_path = now.strftime('games/%Y%m%d')
        path = Path(self.dump_path)
        path.mkdir(parents=True, exist_ok=True)

        # create the checkpoint file
        self.checkpointTmpName  = "abadia_checkpoint_{}_{}".format(self.gameId, self.checkpointSec)
        self.checkpointSec     += 1
        self.checkpointTmpName += "_{}_{}_{}_{}_{}.checkpoint".format(self.dia, self.momentoDia,
                                                self.numPantalla, self.obsequium, np.round(self.porcentaje,2))

        self.fdCheckpoint = open(self.dump_path + "/" + self.checkpointTmpName, "w")
        self.fdCheckpoint.write(checkpoint)
        self.fdCheckpoint.flush()

        if (self.gsBucket != None):
            logging.info("Uploading {} to GCP".format(self.dump_path + '/' + self.checkpointTmpName))
            self.upload_blob(self.dump_path + '/' + self.checkpointTmpName,
                             self.dump_path + '/' + self.checkpointTmpName)
        else:
            logging.error("Not saving it to the local filesystem")

    def load_game_checkpoint(self, name):
        logging.info("voy a abrir el fichero ({})".format(name))

        if (self.gsBucket != None):
            logging.info("Downloading Checkpoint {} from GCP".format(name))
            try:
                self.download_blob(name, name)
                self.fdCheckpoint = open(name, "r")
                checkpoint = self.fdCheckpoint.read()
                requests.put(self.url+"/abadIA/game/current", data=checkpoint)
            except:
                logging.error("*** ErrorFile: {} not exist at bucket {}".format(name, self.gsBucket))
        else:
            logging.error("Not Loading {} from local filesystem.".format(name))

        time.sleep(2)
        return self._get_state()

    def personajeByName(self, name):
        # TODO JT: we need to check that there are values for this personaje
        return int(self.Personajes[name]['posX']), int(self.Personajes[name]['posY']), int(self.Personajes[name]['orientacion'])

    def dataPersonaje(self, ob, name):
        notfound = {}
        for persona in ob['Personajes']:
            if (persona['nombre'] == name):
                return persona
        return notfound

    def pintaRejilla(self, width, height):
        w = int(width / 2)
        h = int(height / 2)
        yRejilla = 0
        xRejilla = 0


        # TODO: to display all the characters, now only Guillermo and Adso
        # pers = {}
        # for per in env.Personajes:
        #    datos = {'x': per['posX'], 'y': per['posY']}
        #   pers.update(per['id']:datos)
        #

        x, y, ori           = self.personajeByName('Guillermo')
        adsoX, adsoY, adsoO = self.personajeByName('Adso')

        logging.info("\x1b[HGuillermo {},{} Adso {},{}".format(x, y, adsoX, adsoY))
        logging.info("+---+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")

        for yy in range(y - h, y + h):
            ss = "|%3d|" % yy
            for xx in range(x - w, x + w):
                if (xx == x and yy == y):
                    if ori == 0:
                        ss += ">"
                    if ori == 3:
                        ss += "V"
                    if ori == 1:
                        ss += "^"
                    if ori == 2:
                        ss += "<"
                else:
                    if (xx == adsoX and yy == adsoY):
                        ss += "a"
                    else:
                        if (self.Visited[xx, yy] == 0):
                            ss += "·"
                        else:
                            if (self.Visited[xx, yy] > 0):
                                ss += " "
                            else:
                                ss += "#"

            ss += "|"
            if yRejilla < 24:
                for xx in range(0, 24):
                    if (self.rejilla[yRejilla][xx] == 0):
                        ss += " "
                    else:
                        if (self.rejilla[yRejilla][xx] >= 16):
                            ss += "P"
                        else:
                            ss += "#"

            ss += "|"
            if yRejilla < 24:
                for xx in range(0, 24):
                    if (self.rejilla[yRejilla][xx] == 0):
                        ss += "  "
                    else:
                        ss += "{}".format(format(self.rejilla[yRejilla][xx], '2x'))
            yRejilla += 1
            ss += "|"
            logging.info(ss)

        logging.info("+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")

