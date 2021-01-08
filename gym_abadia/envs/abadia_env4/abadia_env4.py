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
import time
import os
from pathlib import Path
from threading import Thread
import gzip
import shutil

# 3rd party modules
import gym
import numpy as np
from gym import spaces
from google.cloud import storage

import logging
import pathlib
import ctypes

# AbadIA2 dependencies
import requests
import ctypes as ct


# Control definitions
(P1_UP,
 P1_LEFT,
 P1_DOWN,
 P1_RIGHT,
 P1_BUTTON1,
 P1_BUTTON2,
 P2_UP,
 P2_LEFT,
 P2_DOWN,
 P2_RIGHT,
 P2_BUTTON1,
 P2_BUTTON2,
 START_1,
 START_2,
 COIN_1,
 COIN_2,
 SERVICE_1,
 SERVICE_2,
 KEYBOARD_A,
 KEYBOARD_B,
 KEYBOARD_C,
 KEYBOARD_D,
 KEYBOARD_E,
 KEYBOARD_F,
 KEYBOARD_G,
 KEYBOARD_H,
 KEYBOARD_I,
 KEYBOARD_J,
 KEYBOARD_K,
 KEYBOARD_L,
 KEYBOARD_M,
 KEYBOARD_N,
 KEYBOARD_O,
 KEYBOARD_P,
 KEYBOARD_Q,
 KEYBOARD_R,
 KEYBOARD_S,
 KEYBOARD_T,
 KEYBOARD_U,
 KEYBOARD_V,
 KEYBOARD_W,
 KEYBOARD_X,
 KEYBOARD_Y,
 KEYBOARD_Z,
 KEYBOARD_0,
 KEYBOARD_1,
 KEYBOARD_2,
 KEYBOARD_3,
 KEYBOARD_4,
 KEYBOARD_5,
 KEYBOARD_6,
 KEYBOARD_7,
 KEYBOARD_8,
 KEYBOARD_9,
 KEYBOARD_SPACE,
 KEYBOARD_INTRO,
 KEYBOARD_SUPR,
 FUNCTION_1,
 FUNCTION_2,
 FUNCTION_3,
 FUNCTION_4,
 FUNCTION_5,
 FUNCTION_6,
 FUNCTION_7,
 FUNCTION_8,
 FUNCTION_9,
 FUNCTION_10,
 FUNCTION_11,
 FUNCTION_12) = range(69)

class LibAbadIA(object):
    def __init__(self):

        logging.info("Loading LibAbadia")
        libname = pathlib.Path().absolute() / "LibAbadIA.so"
        self.lib = ct.cdll.LoadLibrary(libname)
        logging.info("loaded")

        self.lib.LibAbadIA_init()

        self.lib.LibAbadIA_step.argtypes = [ct.POINTER(ct.c_int), ct.c_char_p, ct.c_size_t]
        self.lib.LibAbadIA_step.restype = ct.c_char_p

        self.lib.LibAbadIA_step2.argtypes = [ct.c_int, ct.c_char_p]
        self.lib.LibAbadIA_step2.restype = ct.c_char_p

        self.lib.LibAbadIA_save.argtypes = [ct.c_char_p, ct.c_size_t]
        self.lib.LibAbadIA_save.restype = ct.c_char_p

        self.lib.LibAbadIA_load.argtypes = [ct.c_char_p]

class AbadiaEnv4(gym.Env):
    """
    Define a Abadia4 environment. LibAbadia version

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        self.__version__ = "0.0.8"
        # print("AbadiaEnv4 - Version {}".format(self.__version__))
        logging.basicConfig(format='%(asctime)s:[%(filename)s:%(funcName)s:%(lineno)s]:%(levelname)s:%(message)s',
                            datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
        self.libAbadIA = LibAbadIA()
        self.num_episodes   = 100
        self.num_steps      = 1500
        self.gsBucket       = None

        self.gameName       = ""
        self.actionsName    = ""
        self.actionsCheckpointName    = None
        self.actionsCheckpointStep    = 1
        self.modelName      = None
        self.valueModelName = None
        self.initValueModelName = None
        self.dump_path      = "games/now/"
        self.gameId = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
        self.checkpointSec  = 1
        self.storage_client = None
        self.eventsGame     = []
        self.eventsAction   = []
        self.totalReward    = 0.0
        self.verbose        = 0
        self.playing        = False
        self.minimunObsequium = 29
        self.speedtest      = False
        self.speedtestcount = 100

        self.action_space = spaces.Discrete(14)

        # json from the dump state of the episode

        self.json_dump = {}

        self.action_mode = 1
        # TODO JT we will include SPACE and QR in the available actions
        self.actions_list = ('UP-2', 'UP-10', 'UP-20', 'UP-40', 'UP-60', 'NOP-1', 'NOP-5', 'NOP-25', 'NOP-50',
                             'RIGHT', 'LEFT', 'DOWN', 'SPACE', 'QR')

        self.obsequium = -1
        self.reward = 0
        self.porcentaje = -1
        self.haFracasado = False
        self.prevPantalla = -1
        self.rejilla = []
        self.prev_ob = dict()
        self.estaGuillermo= False
        self.room = np.zeros([20,20,3], np.int)

        self.curr_step = 1
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

        # TODO JT: check all this initializations

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

        # self.logger.info("AbadiaEnv just initialized")
        # helper to normalize paths to positions
        #   1
        # 2   0
        #   3

    def check2dict(self, line):

        pre = "core_"
        output = {}
        # self.logger.info(type(line))
        for line in line.split('\n'):
            # print(line)
            res = line.split("// ")

            if (len(res) == 2):
                value = res[0]
                key = res[1]
                if (value == ""):
                    pre = key.replace(" ", "_") + "_"
                else:
                    output[pre + key] = int(value)

            # print("value ({}) key ({})".format(value, pre + key))
        # print(json.dumps(output))
        # self.logger.info(output)
        return output

    # TODO JT we need a Dict to Checkpoint to recover from actions check dictionary

    def dict2check(self):
        pass

    def sendCmd(self, action):
        command = self.actions_list[action]
        if "-" in command:
            cmd = command.split("-")[0]
            num = int (command.split("-")[1])
        else:
            cmd = command
            num = 1
        self.logger.info(f"action {action} {command}: cmd ---> {cmd} {num} times")

        # ('UP-2', 'UP-10', 'UP-20', 'UP-40', 'UP-60', 'NOP-1', 'NOP-5', 'NOP-25', 'NOP-50',
        # 'RIGHT', 'LEFT', 'DOWN', 'SPACE', 'QR')
        if (cmd == 'UP'):
            ob = self.libstep(P1_UP)
        if (cmd == 'NOP'):
            ob = self.libstep(-1)
        if (cmd == 'RIGHT'):
            ob = self.libstep(P1_RIGHT)
        if (cmd == 'LEFT'):
            ob = self.libstep(P1_LEFT)
        if (cmd == 'DOWN'):
            ob = self.libstep(P1_DOWN)
        if (cmd == 'SPACE'):
            ob = self.libstep(KEYBOARD_SPACE)
        if (cmd == 'QR'):
            ob = self.libstep(KEYBOARD_Q)
            # TODO implementar en el lado del libAbaIA.so
            # self.libAbadIA.controles[self.libAbadIA.KEYBOARD_R] = 1
        dump =self.getGameDump().decode()
        # self.logger.info(dump)
        core = self.check2dict(dump)
        ob['core'] = core
        return ob

    def libstep(self, control):
        result = ct.create_string_buffer(10000)
        # self.logger.info("Voy a ejecutar el control ---> {}".format(control))
        tmp = self.libAbadIA.lib.LibAbadIA_step2(ct.c_int(control), ct.cast(result, ct.c_char_p))
        # self.logger.info(type(result.value))
        # self.logger.info("step2 result: {}".format(tmp))
        return json.loads(tmp)

    def step(self, action):
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        ------
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
        self.logger.info(f"action: {action}")
        ob = self.sendCmd(action)
        self._get_personajes_info(ob)
        self._get_general_info(ob)

        self.curr_step += 1
        self._take_action(action)

        ob['jugada'] = self.curr_step
        ob['gameId'] = self.gameId
        ob['action_meta'] = self.actions_list[action]
        ob['action'] = action

        reward = 0
        self.eventsAction = []

        if (self.obsequium < self.minimunObsequium):
            self.logger.info("GAME OVER by lack of Obsequium {}        ".format(self.obsequium))
            # self.reset_game()
            self.game_is_done = True
            self.haFracasado = True
            reward = -1

        if (self.haFracasado == True):
            self.logger.info("GAME OVER")
            # self.reset_game()
            self.game_is_done = True
            self.haFracasado = True
            reward = -1

        if (self.porcentaje >= 90):
            self.game_is_done = True
            self.logger.info("FUCKING YEAH GAME ALMOST DONE")
            self.logger.info("FUCKING YEAH GAME ALMOST DONE")
            self.logger.info("FUCKING YEAH GAME ALMOST DONE")
            self.logger.info("FUCKING YEAH GAME ALMOST DONE")
            self.logger.info("FUCKING YEAH GAME ALMOST DONE")
            reward = 1

        # TODO JT we need to parametize the reward function

        reward = float(((self.porcentaje + 1) / 100)) * float (self.curr_step * 0.00001)

        # TODO JT: deprecated now only need to check for UP and objects actions

        if (self.wallMovs[action] == 1):
            self.logger.info("***** Invalid move against Wall, penalizing it")
            reward = -0.00091

        if (self.perMovs[action] == 1):
            self.logger.info("***** Invalid move against a Character, penalizing it")
            reward = -0.00092

        self.reward       = reward
        self.totalReward += reward
        ob['reward']      = reward
        ob['totalReward'] = self.totalReward
        self.logger.info("reward: {} tr: {} action: {} ".format(reward, self.totalReward, action))

        # adding more information for debugging: valid moves, vectors, predictions, etc.
        ob['valMovs']            = self.valMovs.tolist()
        ob['wallMovs']           = self.wallMovs.tolist()
        ob['wallMovs']           = self.wallMovs.tolist()
        ob['perMovs']            = self.perMovs.tolist()
        ob['predictions']        = self.calculated_predictions
        ob['final']              = self.final_predictions
        ob['vector']             = self.vector_predictions
        ob['action_predictions'] = self.action_predictions
        ob['action_type']        = self.action_type

        # we make a copy for the current observation in order to calculate
        # the reward for the next state

        self.ob = ob
        self.prev_ob = ob

        # TODO JT chequear si esto está bien, no parece que este devolviendo bien el estado siguiente!!!

        return ob, reward, self.game_is_done, {}

    def _get_personajes_info(self, ob):
        # print ("ob personajes -> {} ", ob['Personajes'][0])
        self.estaGuillermo = False
        for persona in self.listaPersonajes[:]:
            self.Personajes[persona] = {}
        for personaje in ob['Personajes']:
            if (len(personaje) == 1):
                break
            # persona = self.listaPersonajes[int(personaje['id'])]
            # datos = self.Personajes[persona]
            # for key, value in personaje.items():
                #if key != "id" or key != "fil":
                # datos[key] = value
            self.Personajes[personaje['nombre']] = personaje

            if int(personaje['id']) == 0:
                self.estaGuillermo = True

        return self.estaGuillermo


    def _get_general_info(self, ob):
        self.obsequium = int(ob['obsequium'])
        self.porcentaje = int(ob['porcentaje'])
        self.bonus = int(ob['bonus'])
        self.numPantalla = int(ob['numPantalla'])
        self.dia = int(ob['dia'])
        self.momentoDia = int(ob['momentoDia'])
        self.haFracasado = ob['haFracasado']
        self.rejilla = ob['Rejilla']

        return

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
        # self.logger.info("append {} {}".format(self.curr_episode, action))
        self.action_episode_memory[self.curr_episode].append(action)

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
        self.game_is_done = False

        # self.logger.info('-----> RESET the GAME 1 SP')

        ob = self.libstep(KEYBOARD_E)
        # self.logger.info('reset status {}'.format(ob))
        # self.logger.info('-----> DONE')

        self.logger.info('-----> INIT dumps files: START ...')
        self.init_dumps_files()
        self.logger.info('-----> INIT dumps files: DONE')
        if self._get_personajes_info(ob):
            self.logger.info('Esta Guillermo')
        ob['jugada'] = self.curr_step
        return ob

    # TODO JT check if we use this function

    def render(self, mode='human', close=False):
        self.logger.info('state info: {}'.format(self))
        return

    def _get_state(self):
        """Get the observation."""

        self.logger.info("--------> I wil got the initial state with Guillermo")
        tooboring = 0
        while True:
            ob = self.sendCmd(self.url, "/abadIA/current/game", mode='GET', type='json')
            self.logger.info("current game status {}".format(ob))
            tooboring += 1
            if self._get_personajes_info(ob):
                self.logger.info("getting the characters from Dump")
                break
            else:
                self.logger.info("getting the characters from ob") # :{}".format(ob))
                self.logger.info("Guillermo is not present yet, waiting")
                if tooboring % 10 == 0:
                    self.logger.info("Getting Boring ...")
                    if tooboring <= 10:
                        self.sendCmd(self.url, "start")
                    else:
                        self.sendCmd(self.url, "fin")
                    time.sleep(1)
                time.sleep(2)
        ob['jugada'] = self.curr_step
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

        self.logger.info('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))

    def upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        blob = self.google_storage_bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        self.logger.info('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def add_event(self, name, des, reward):
        data = {'name': name, 'des': des, 'reward': reward, 'totalReward': self.totalReward, 'version': 1}
        data.update(self.get_commons())

        self.eventsAction.append(data)
        self.logger.info("events {}".format(self.eventsAction))

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

        if (not self.fdActions.closed):
            self.logger.info("flushing and closing {} before exit".format(self.actionsName))
            self.fdActions.flush()
            self.fdActions.close()

        if (self.gsBucket != None):
            self.logger.info("Uploading Game: {} to GCP".format(self.dump_path + "/" + self.gameName))
            t = Thread(target=self.upload_blob, args=(self.dump_path + "/" + self.gameName,
                                                      self.dump_path + "/" + self.gameName))
            t.start()

            # compressing the file
            self.logger.info("Gziping ---> {}".format(self.dump_path + "/" + self.actionsName))
            with open(self.dump_path + "/" + self.actionsName, 'rb') as f_in, gzip.open(self.dump_path + "/" + self.actionsName + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

            self.logger.info("Uploading Actions: {} to GCP".format(self.dump_path + "/" + self.actionsName + ".gz"))
            t = Thread(target=self.upload_blob, args=(self.dump_path + "/" + self.actionsName + ".gz",
                             self.dump_path + "/" + self.actionsName + ".gz"))
            t.start()
            self.logger.info("Deleting ---> {}".format(self.dump_path + "/" + self.actionsName))
            os.remove(self.dump_path + "/" + self.actionsName)

    def save_action(self, state, action, reward, nextstate):
        s1 = state.copy()
        s2 = nextstate.copy()
        if s1["haFracasado"] == False:
            s1["haFracasado"] = 0
        else:
            s1["haFracasado"] = 1

        if s2["haFracasado"] == False:
            s2["haFracasado"] = 0
        else:
            s2["haFracasado"] = 1

        if s1["investigacionCompleta"] == False:
            s1["investigacionCompleta"] = 0
        else:
            s1["investigacionCompleta"] = 1

        if s2["investigacionCompleta"] == False:
            s2["investigacionCompleta"] = 0
        else:
            s2["investigacionCompleta"] = 1

        str1 = json.dumps(json.loads(str(s1).replace("'","\"")))
        str2 = json.dumps(json.loads(str(s2).replace("'","\"")))

        string = "{}\"action\":{}\"state\":{},\"action\":{},\"reward\":{},\"nextstate\":{}{}{}\n".format("[{", "{",
                str1, action, reward, str2, "}", "}]")
        self.fdActions.write(string)
        self.fdActions.flush()

    def visited_snap_load(self):
        nameVisitedSnap = "snapshots/current-visited"

        # for speed up the games if the visited  exist locally
        # we download an updated version just a 10% of the time

        if self.gsBucket != None and np.random.randint(10) <= 1 and not os.path.exists(nameVisitedSnap):
            self.logger.info("Downloading Visited from GCP")
            try:
                self.download_blob(nameVisitedSnap, nameVisitedSnap)
            except:
                self.logger.info("File {} not exist at bucket {}".format(nameVisitedSnap, self.gsBucket))

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
                self.logger.info("Uploading to GCP")
                self.upload_blob(nameVisitedSnap, nameVisitedSnap)

    def visited_snap_save(self):
        nameVisitedSnap = "snapshots/current-visited"

        fvisitedsnap = open(nameVisitedSnap, "wb+")
        np.save(fvisitedsnap, self.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

        if (self.gsBucket != None):
            self.logger.info("Uploading visited to GCP")
            t = Thread(target=self.upload_blob, args=(nameVisitedSnap, nameVisitedSnap))
            t.start()

    def reset_fin_partida(self):
        self.sendCmd(self.actions_list.index("SPACE"))
        self.libstep(KEYBOARD_E)

    def init_dumps_files(self):

        # check is directory exist, if not we will create it
        now = datetime.datetime.now()
        self.dump_path = now.strftime('games/%Y%m%d')
        path = Path(self.dump_path)
        path.mkdir(parents=True, exist_ok=True)

        # create the game and actions files
        self.fdGame    = open(self.dump_path + "/" + self.gameName, "w")
        self.fdActions = open(self.dump_path + "/" + self.actionsName, "w")

    # TODO JT now every action included a checkpoint so we don't need this function. Check it.

    def save_game_checkpoint(self):

        checkpoint = self.sendCmd(self.url, "/abadIA/game/current", mode='GET', type="raw")
        if (checkpoint is None):
            self.logger.error("I cannot save the checkpoint game file. Probably because I cannot connect with the game server ")
            return
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
            self.logger.info("Uploading {} to GCP".format(self.dump_path + '/' + self.checkpointTmpName))
            t = Thread(target=self.upload_blob, args=(self.dump_path + '/' + self.checkpointTmpName,
                             self.dump_path + '/' + self.checkpointTmpName))
            t.start()
        # else:
            # self.logger.error("Not saving it to the local filesystem")

    def dict2check(self, check):
        """
        this function convert the dict with the checkpoint to the format expected by the engine
        :return:
        """
        ant = ""
        result = ""
        for key in check.keys():
            # print("key: {} value: {}".format(key, file2[key]))
            elements = key.split("_")
            pre = "NaN"
            name = "NaN"

            if (elements[0] == "core"):
                pre = ""
                name = elements[1]
            else:
                if (len(elements) == 3):
                    pre = "{} {}".format(elements[0], elements[1])
                    name = elements[2]
                else:
                    pre = elements[0]
                    name = elements[1]

                if (ant != pre):
                    ant = pre
                    result += "// {}\n".format(pre)

            result += "{}// {}\n".format(check[key], name)
        return result

    # TODO JT We need to refactoring this function
    # Now we will pass the actions file and which step we wants to reload

    def load_actions_checkpoint(self, name, step):
        self.logger.info("Opening the local actions file ({}) step ({})".format(name, step))

        if (self.gsBucket != None):
            self.logger.info("Downloading Actions Checkpoint {} from GCP".format(name))
            try:
                self.download_blob(name, name)
            except:
                self.logger.error("*** ErrorFile: {} not exist at bucket {}".format(name, self.gsBucket))

        with open(name) as fdActionsCheckpoint:
            for cnt, action in enumerate(fdActionsCheckpoint):
                st = json.loads(action)[0]
                if "jugada" in st['action']['state'] and int(st['action']['state']['jugada']) == step:
                    env.logger.info("I will load the {} step into the engine".format(st['action']['state']['jugada']))
                    #    TODO JT now we read the json object, get the checkpoint dict and convert it to Abbey format
                    env.logger.info(st['action']['state']['core'])
                    checkpoint = self.dict2check(st['action']['state']['core'])
                    self.logger.info("Restoring the saved game")
                    response = requests.put(self.url+"/abadIA/game/current", data=checkpoint)
                    self.logger.info("Done status: {}".format(response))
                    self.curr_step = step
        fdActionsCheckpoint.close()

        # TODO JT check if we can delete this delay.
        # time.sleep(2)
        return self._get_state()

    def personajeByName(self, name):
        # TODO JT: we need to check that there are values for this personaje
        if (name in self.Personajes) and ('posX' in self.Personajes[name]):
            return int(self.Personajes[name]['posX']), int(self.Personajes[name]['posY']), int(self.Personajes[name]['orientacion'])
        else:
            # self.logger.info("No hay {}: {}".format(name, self.Personajes))
            return 0, 0, 0

    def dataPersonaje(self, ob, name):
        notfound = {}
        for persona in ob['Personajes']:
            if (persona['nombre'] == name):
                return persona
        return notfound

    # TODO JT we need to included as a valid mov the doors even it is closed

    def checkValidMovs(self, orientation=0):

        actions_dim = len(self.actions_list)
        self.valMovs = np.zeros(actions_dim, np.int)
        self.wallMovs = np.zeros(actions_dim, np.int)
        self.perMovs = np.zeros(actions_dim, np.int)

        if (self.rejilla == []):
            for ii in range(0, actions_dim):
                self.valMovs[ii] = 1
            return self.valMovs

        room = np.zeros([24, 24, 2], np.int)
        chkM2 = [
            [ # 0 EAST
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 0]
            ],[ # 1 NORTH
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],[ # 2 WEST
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, 0]
            ],[ # 3 SOUTH
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 1, 0]
            ],
        ]

        chkM = np.array([
            [0, 0, 0, -1, 0],
            [0, 0, 1, -1, 0],
            [1, 0, 0, -1, 0],
            [1, 0, -1, -1, 0],
            [1, 0, 0, 0, -1],
            [2, 0, 1, 0, 2],
            [2, 1, 1, 1, 2],
            [3, 1, 0, 2, 0],
            [3, 1, -1, 2, -1],
            [4, 1, 0, 2, 0],
            [4, 1, -1, 2, -1],
            [5, 0, -1, 0, -2],
            [5, 1, -1, 1, -2],
            [5, 1, -1, 2, -1],
            [6, 0, -1, 0, -2],
            [6, 1, -1, 1, -2],
            [7, 0, 0, -1, 0],
            [7, 0, -1, -1, -1],
            [7, 0, -1, 0, -2]],
            np.int)

        yPos = -1
        xPos = -1

        for yy in range(0, 24):
            for xx in range(0, 24):
                per = int(self.rejilla[yy][xx]) >> 4
                alt = self.rejilla[yy][xx] % 16
                # print(per)
                # we found Guillermo
                if (per == 1 and xPos == -1 and yPos == -1):
                    yPos = yy
                    xPos = xx

                room[yy, xx, 0] = per
                room[yy, xx, 1] = alt

        self.valMovs2 = np.zeros(14, np.int)
        self.wallMovs = np.zeros(14, np.int)
        self.perMovs  = np.zeros(14, np.int)

        self.valMovs[range(0,14)] = 1
        self.valMovs2[range(0,14)] = 1

        if (self.verbose >= 1):
            print(f"checking orientation {orientation} room at ({yPos},{xPos})   ")
            print("*-----*-----*---*-----*")
            print("*chkM2*Room0*---*Room1*")
            print("*-----*-----*---*-----*")
            for yy in range(0, 4):
                for xx in range(0, 4):
                    print("{}".format(chkM2[orientation][yy][xx]), end="")
                print("|".format(yy), end="")
                for xx in range(0, 4):
                    print("{}".format(room[yPos + yy - 1][xPos + xx - 1, 0]), end="")
                print("|%3d|" % (yPos + yy - 1), end="")
                for xx in range(0, 4):
                    print("{}".format(room[yPos + yy - 1][xPos + xx - 1, 1]), end="")
                print("| {}".format(yPos + yy - 1))
        for yy in range(0, 4):
            for xx in range(0, 4):
                if (chkM2[orientation][yy][xx] == 1):
                    diff = room[yPos + yy - 1, xPos + xx - 1, 1] - room[yPos, xPos, 1]
                    if self.verbose > 1:
                        print("I will check wall at {},{} diff {} pers {}   ".format(yy, xx, diff, room[yPos + yy - 1, xPos + xx - 1, 0]))
                    if (not (diff >= -1 and diff <= 1)):
                        self.wallMovs[range(0,5)] = 1
                        self.valMovs2[range(0,5)] = 0
                        if self.verbose > 1:
                            print("Wall Blocks G {},{} ".format(yy, xx))
                    if room[yPos + yy - 1, xPos + xx - 1, 0] != 0:
                        if (self.verbose > 1):
                            print("Adso/* block {},{} ".format(yy, xx))
                        self.valMovs2[range(0,5)] = 0
                        self.perMovs[range(0,5)] = 1

        self.valMovs = self.valMovs2
        if (self.verbose > 1):
            self.logger.info ("new valMovs2: {}".format(self.valMovs2))
            self.logger.info ("wallMovs: {}".format(self.wallMovs))
            self.logger.info ("perMovs: {}".format(self.perMovs))

        return self.valMovs

    def getGameDump(self):
        result = ct.create_string_buffer(10000)
        return bytearray(self.libAbadIA.lib.LibAbadIA_save(ct.cast(result, ct.c_char_p), 10000))

    def speed_test(self, count=100):
        # test one: how many count context switches the engine could do

        print("Resetting the game engine")
        ob = self.reset()
        print (f"ob {ob['core']}")
        checkpoint = self.dict2check(ob['core'])

        print(f"Test 1: counts {count}")

        # TODO JT build a little decorated wrapper

        start_time = time.time()
        for ii in range(0, count):
            response = requests.put(self.url + "/abadIA/game/current", data=checkpoint)
            # self.logger.info("Done status: {}".format(response))
        elapsed_time = time.time() - start_time
        secs = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"finished test1 in {secs}")

    def update_visited_cells(self, x, y, ori):

        newX, newY, _ = self.personajeByName('Guillermo')

        if (x != newX or y != newY):
            self.Visited[newX, newY] += 1

        if (x == newX and y == newY):
            if (ori == 0):
                self.Visited[x + 1, y] += -0.01
            if (ori == 1):
                self.Visited[x, y - 1] += -0.01
            if (ori == 2):
                self.Visited[x - 1, y] += -0.01
            if (ori == 3):
                self.Visited[x, y + 1] += -0.01

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
        abadX, abadY, abadO = self.personajeByName('Abad')

        self.logger.info("\x1b[HGuillermo {},{} Adso {},{} Abad {},{} Obsequium:{} Porcentaje:{} Reward:{} TR:{} V:{}".format(x, y, adsoX, adsoY,
                             abadX, abadY, self.obsequium, self.porcentaje, np.round(self.reward, 6), np.round(self.totalReward, 6), np.round(self.predictions, 4)))

        self.logger.info("+---+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")

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
                    character = False
                    if (xx == adsoX and yy == adsoY):
                        ss += "a"
                        character = True
                    if (xx == abadX and yy == abadY):
                        ss += "A"
                        character = True

                    if not character:
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
            self.logger.info(ss)

        self.logger.info("+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")
