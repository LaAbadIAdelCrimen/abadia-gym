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
        self.__version__ = "0.0.6"
        print("AbadiaEnv - Version {}".format(self.__version__))


        self.url    = "http://localhost:4477"
        self.server = "http://localhost"
        self.port   = "4477"
        self.num_episodes   = 100
        self.num_steps      = 1500


        self.gameName       = ""
        self.actionsName    = ""
        self.checkpointName = None
        self.modelName      = None
        self.dump_path      = "games/now/"
        self.gameId = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
        self.checkpointSec  = 1
        self.gsBucket       = None
        self.eventsGame     = []
        self.eventsAction   = []
        self.totalReward    = 0.0

        # Define what the agent can do
        # 0 -> STEP FORWARD
        # 1 -> RIGHT
        # 2 -> LEFT
        # 3 -> DOWN
        # 4 -> GET

        self.action_space = spaces.Discrete(5)

        # json from the dump state of the episode

        self.json_dump = {}

        self.actions_list = ("cmd/A", "cmd/D", "cmd/I", "cmd/B", "cmd/N", "cmd/_")
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

        # Observation is the position of Guillermo and the information of the room
        X = np.array([0,256])
        Y = np.array([0, 256])
        O = np.array([0,4])

        high = np.array([np.inf] * 15)  # useful range is -1 .. +1, but spikes can be higher
        self.observation_space = spaces.Box(-high, high)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

        now = datetime.datetime.now()
        self._seed(time.mktime(now.timetuple()))

    def set_url(self):
        self.url = self.server + ":" + self.port
    # TODO JT refactoring and eliminate this function
    def sendReset(self):
        return self.sendCmd(self.url, "reset")

    def sendCmd(self, url, command, type="json"):
        cmd = "{}/{}".format(url, command)
        r = requests.get(cmd)
        if (type == "json"):
            cmdDump = "{}/dump".format(url)
            r = requests.get(cmdDump)
            if r.status_code == 599:
                tmp = r.json()
                tmp['haFracasado'] = True
                return tmp
            else:
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
                    reward += 50
                    print("----------")
                    print("reward by screen change !!!!! {} !=  {}".format(self.prevPantalla, int(ob['numPantalla'])))
                    print("Personajes: {}".format(self.Personajes))
                    print("ob: {}".format(ob))
                    print("----------")
                    self.add_event("NewRoom", "prev {} curr {}".format(self.prevPantalla, int(ob['numPantalla'])), 50)
                    self.prevPantalla = int(ob['numPantalla'])
                    self.save_game_checkpoint()

        # If there is an obsequium change, it will be rewarded pos/neg
        if len(self.prev_ob) > 0 and int(self.prev_ob['obsequium']) > 0:
            # reward for incrementing the obsequium: > 0 +50 / < 0 -30
            incr_obsequium = self.obsequium - int(self.prev_ob['obsequium'])
            if incr_obsequium > 0:
                reward += (50 * incr_obsequium)
                self.add_event("IncrObsequium", "Obsequium {} Incr {}".format(self.prev_ob['obsequium'],incr_obsequium), 50*incr_obsequium)

            if incr_obsequium < 0:
                reward += (30 * incr_obsequium)
                self.add_event("DecrObsequium", "Obsequium {} Decr {}".format(self.prev_ob['obsequium'], incr_obsequium),-30*incr_obsequium)

        # reward for incrementing the bonus: >0 +500
        if len(self.prev_ob) > 0 and int(self.prev_ob['bonus']) > 0:
            incr_bonus = self.bonus - int(self.prev_ob['bonus'])
            if incr_bonus > 0:
                reward += (500 * incr_bonus)
                self.add_event("Bonus", "prev {} curr {}".format(self.bonus, int(self.prev_ob['bonus'])), 500 * incr_bonus)

        # we check if Guillermo change his position. Positive reward if yes, negative if no
        if action == 0:
            if len(self.prev_ob) > 0 and len(self.prev_ob['Personajes']) > 0:
                prev = self.dataPersonaje(self.prev_ob, "Guillermo")
                curr = self.dataPersonaje(ob, "Guillermo")
                if (prev['posX'] != curr['posX']) or (prev['posY'] != curr['posY']):
                    print("se ha movido: {},{} -> {},{}".format(prev['posX'], prev['posY'],
                                                            curr['posX'], curr['posY']))
                    reward += 0.5

        self.eventsGame.extend(self.eventsAction)
        # if the game is over, we just finish the game and reward is -1000
        # if we completed the game, we finish and the reward is 5000
        # the percentage must be variable to help the AI to learn
        # with variable explanatory/explotation

        if (self.haFracasado == True):
            print("GAME OVER")
            self.sendCmd(self.url, "start")
            # time.sleep(4)
            # self.sendCmd(self.url, "fin")
            self.game_is_done = True
            reward = -1000

        if (self.porcentaje >= 90):
            self.game_is_done = True
            print("FACKING YEAH GAME DONE")
            print("FACKING YEAH GAME DONE")
            print("FACKING YEAH GAME DONE")
            print("FACKING YEAH GAME DONE")
            print("FACKING YEAH GAME DONE")
            reward = 5000


        if reward == 0:
            reward = -0.5

        self.totalReward += reward
        ob['reward'] = reward
        ob['totalReward'] = self.totalReward
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

        print("-----> RESET the GAME")
        ob = self.sendReset()
        print("reset status {}".format(ob))
        print("-----> DONE")
        print("-----> INIT dumps files: START ...")
        self.init_dumps_files()
        print("-----> INIT dumps files: DONE")
        # time.sleep(5)
        if self._get_personajes_info(ob):
            print("Esta Guillermo")
        return ob

    def render(self, mode='human', close=False):
        print("state info: {}\n".format(self))
        return

    def _get_state(self):
        """Get the observation."""
        # ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        print("--------> I wil got the initial state with Guillermo")
        tooboring = 0
        while True:
            ob = self.sendCmd(self.url, "dump")
            print("{}".format(ob))
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

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)

        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def add_event(self, name, des, reward):
        data = {'name': name, 'des': des, 'reward': reward, 'totalReward': self.totalReward}
        data.update(self.get_commons())

        self.eventsAction.append(data)
        print("events {}".format(self.eventsAction))

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
            print("Uploading Game: {} to GCP".format(self.dump_path + "/" + self.gameName))
            self.upload_blob(self.gsBucket, self.dump_path + "/" + self.gameName,
                             self.dump_path + "/" + self.gameName)
            print("Uploading Actions: {} to GCP".format(self.dump_path + "/" + self.actionsName))
            self.upload_blob(self.gsBucket, self.dump_path + "/" + self.actionsName,
                             self.dump_path + "/" + self.actionsName)

    def save_action(self, state, action, reward, nextstate):
        s1 = state.copy()
        s2 = nextstate.copy()
        # s1.pop('Rejilla')
        # s2.pop('Rejilla')

        self.fdActions.write("{}{}\"action\":{}\"state\":{},\"action\":{},\"reward\":{},\"nextstate\":{}{}{}\n"
                             .format("[", "{", "{", json.dumps(s1), action, reward, json.dumps(s2), "}", "}]"))
        self.fdActions.flush()


    def visited_snap_load(self):
        nameVisitedSnap = "snapshoots/current-visited"
        if (self.gsBucket != None):
            print("Downloading Visited from GCP")
            try:
                self.download_blob(self.gsBucket, nameVisitedSnap, nameVisitedSnap)
            except:
                print("File {} not exist at bucket {}".format(nameVisitedSnap, self.gsBucket))

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
                print("Uploading to GCP")
                self.upload_blob(self.gsBucket, nameVisitedSnap, nameVisitedSnap)

    def visited_snap_save(self):
        nameVisitedSnap = "snapshoots/current-visited"

        fvisitedsnap = open(nameVisitedSnap, "wb+")
        np.save(fvisitedsnap, self.Visited)
        fvisitedsnap.flush()
        fvisitedsnap.close()

        if (self.gsBucket != None):
            print("Uploading visited to GCP")
            self.upload_blob(self.gsBucket, nameVisitedSnap, nameVisitedSnap)


    def reset_fin_partida(self):
        ob = self.sendCmd(self.url, "start")

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

        checkpoint = self.sendCmd(self.url, "save", type="raw")

        now = datetime.datetime.now()
        self.dump_path = now.strftime('games/%Y%m%d')
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

        if (self.gsBucket != None):
            print("Uploading {} to GCP".format(self.dump_path + '/' + self.checkpointTmpName))
            self.upload_blob(self.gsBucket, self.dump_path + '/' + self.checkpointTmpName,
                             self.dump_path + '/' + self.checkpointTmpName)

    def load_game_checkpoint(self, name):
        # name = "games/20180425/abadia_checkpoint_18-04-25_23:13:57:264379_1_4_27_23_0.checkpoint"
        print("voy a abrir el fichero ({})".format(name))
        self.fdCheckpoint = open(name, "r")
        checkpoint = self.fdCheckpoint.read()
        requests.post(self.url+"/load", data=checkpoint) # [:-6 ])
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

        print("Guillermo {},{} Adso {},{}".format(x, y, adsoX, adsoY))
        print("+---+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")
        for yy in range(y - h, y + h):
            print("|%3d|" % yy, end="")
            for xx in range(x - w, x + w):
                if (xx == x and yy == y):
                    if ori == 0:
                        print(">", end="")
                    if ori == 3:
                        print("V", end="")
                    if ori == 1:
                        print("^", end="")
                    if ori == 2:
                        print("<", end="")
                else:
                    if (xx == adsoX and yy == adsoY):
                        print("a", end="")
                    else:
                        if (self.Visited[xx, yy] == 0):
                            print("·", end="")
                        else:
                            if (self.Visited[xx, yy] > 0):
                                print(" ", end="")
                            else:
                                print("#", end="")

            print("|", end="")
            if yRejilla < 24:
                for xx in range(0, 24):
                    if (self.rejilla[yRejilla][xx] == 0):
                        print(" ", end="")
                    else:
                        if (self.rejilla[yRejilla][xx] >= 16):
                            print("P", end="")
                        else:
                            print("#", end="")

            print("|", end="")
            if yRejilla < 24:
                for xx in range(0, 24):
                    if (self.rejilla[yRejilla][xx] == 0):
                        print("  ", end="")
                    else:
                        print("{}".format(format(self.rejilla[yRejilla][xx], '2x')), end="")
            yRejilla += 1
            print("|")

        print("+" + "-" * (w * 2) + "+" + "-" * 24 + "+" + "-" * 48 + "+")


