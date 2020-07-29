import random
import numpy as np
import logging
import json
import gzip

from math import hypot
from math import atan2
import pickle
import os
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from collections import deque

# VALUE MODEL FOR any: Guillermo X,Y/Day/Hour/Height

class VDQN:
    def __init__(self, env=None, modelName=None, initModelName=None, gsBucket=None):
        self.env     = env
        self.memory  = deque(maxlen=10000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01 # previously 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125
        self.initModelName = None
        self.modelName = None
        self.gsBucket = None

        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%m-%y %H:%M:%S',
                            level=logging.INFO)

        self.logging = logging

        # TODO JT: we need to implement this when goes to production
        if env != None:
            if env.initModelName != None:
                self.initModelName = env.initValueModelName
            if env.modelName != None:
                self.ModelName = env.valueModelName

        if modelName != None:
            self.modelName = modelName

        if initModelName != None:
            self.initModelName = initModelName

        self.model        = self.create_model()
        self.target_model = self.create_model()

        if (self.initModelName is not None):
            fileName = self.initModelName
        else:
            fileName = self.modelName

        if self.env != None:
            # TODO JT: we need to implement this when goes to production
            if (env.gsBucket != None):
                self.env.download_blob(fileName, fileName)
                self.logging.info("Downloading the value model from Bucket: {} file: {}".format(self.gsBucket, fileName))

        if not (env == None and initModelName == None and modelName == None):
            self.model        = self.load_model(fileName)
            self.target_model = self.load_model(fileName)

    def create_model(self, input_dim=5, output_dim=1):
        self.logging.info("Creating a new a Value model v1")
        model   = Sequential()

        # TODO JT we need to redesign the internal lawyers

        model.add(Dense(8, input_shape=(1,5), activation="relu"))
        model.add(Dense(16, activation="relu"))
        model.add(Dense(output_dim))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate),
            metrics=['accuracy'])
        return model

    def load_model(self, name):
        self.logging.info("Loading a local value model from: ({})".format(name))
        # we're calling the load_model method imported from keras
        # and return the model loaded (h5 format)
        return load_model(name)

    def create_empty(self, name="models/empty_value_model_v6.model"):
        model = self.create_model()
        self.save_model(name)
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if (self.env == None):
            return act_prediction(state)
        else:
            return self.act_env(state)

    def act_prediction(self, vector):

        # self.env.vector = vector

        predictions = self.model.predict(vector)[0]
        # self.env.predictions = predictions
        # TODO JT: how to get the action_space
        # final = np.zeros(self.env.action_space.n)

        action = np.argmax(final)
        # self.logging.info("vector:      {}              ".format(vector))
        self.logging.info("predictions: {}              ".format(predictions))
        self.logging.info("final:       {}              ".format(final))
        self.logging.info("Action:      {} Prediction: {}    ".format(action, final[action]))

        return action

    def act_env(self, state):

        # vector = self.env.stateVector()
        vector = self.state2vector(state)
        self.env.vector = vector

        if (self.env.playing is False) and (np.random.random() < self.epsilon):
            action = self.env.action_space.sample()
            self.env.logging.info("e-greedy: {}  epsilon: {}<----               ".format(action, self.epsilon))
            actionType = "E"
            self.env.calculated_predictions = []
            self.env.final_predictions = []
        else:
            predictions = self.model.predict(vector.reshape(1,1,71)).reshape(9)
            logging.info(predictions)
            self.env.predictions = predictions
            final = np.zeros(self.env.action_space.n)

            for ii in range(0,self.env.action_space.n):
                if (self.env.valMovs[ii] >= 1):
                    final[ii] = predictions[ii]
                else:
                    final[ii] = -99 # predictions[ii]*0.9

            action = np.argmax(final)
            # self.env.logging.info("vector:      {}              ".format(vector))
            # self.env.logging.info("predictions: {}              ".format(predictions))
            # self.env.logging.info("final:       {}              ".format(final))
            self.env.logging.info("Action:      {} Prediction: {}    ".format(action, final[action]))
            for ii in range(9):
                self.env.logging.info("%3s %d:%d:%d -> %.8f %.8f" % ( self.env.actions_list[ii],
                                                                     self.env.valMovs[ii],
                                                                     self.env.wallMovs[ii],
                                                                     self.env.perMovs[ii],
                                                                     predictions[ii],
                                                                     final[ii]))
            actionType = "P"

            self.env.calculated_predictions = predictions.tolist()
            self.env.final_predictions = final.tolist()


        self.env.vector_predictions = vector.tolist()
        self.env.action_predictions = int(action)
        self.env.action_type = actionType

        return action

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done, 0])

    def replay_game(self, epochs=4, verbose=0):
        batch_size = 32
        logging.info("We have {} samples for training".format(len(self.memory)))

        temp = self.memory

        states  = []
        rewards = []
        for sample in temp:
            state, action, reward, new_state, done, future_reward = sample

            states.append(state)
            rewards.append(reward)

        X_data = np.array(states).reshape(len(states), 1, 5)
        y_data = np.array(rewards).reshape(len(rewards), 1, 1)

        size = int(len(states)*77/100)
        X_training = X_data[:size]
        y_training = y_data[:size]

        X_test = X_data[size:]
        y_test = y_data[size:]

        history = self.model.fit(X_training, y_training, validation_data=(X_test, y_test), \
                                epochs=epochs, batch_size=32, verbose=verbose)

        print("loss:", history.history["loss"], "\n")

        score = self.model.evaluate(X_test, y_test, verbose=verbose)
        print("score:", score)
        return history, score

    def target_train(self):
        self.env.logging.info("training target ..")
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.logging.info("Saving the value model to the local file: {}".format(fn))
        self.model.save(fn)

    def load_actions_from_a_dir_and_save_to_vectors(self, dirName):
        files = []
        for entry in os.scandir(dirName):
            if entry.is_file() and 'actions_' in entry.path:
                self.load_actions_from_a_file(entry.path)
                tmpName = entry.path.replace("actions", "value_vectors")
                print("Processing: {} -> {}".format(entry.path, tmpName))
                self.save_actions_as_vectors(tmpName)
                files.append(tmpName)
        return files

    def load_vectors_from_a_dir(self, dirName):
        self.memory = deque()
        for entry in os.scandir(dirName):
            if entry.is_file() and 'value_vectors_' in entry.path:
                logging.info("Loading: {} ".format(entry.path))
                tmp = self.load_vectors_into_actions(entry.path)
                for action in tmp:
                    self.memory.append(action)
                logging.info("Actions: {} total {}".format(len(tmp), len(self.memory)))

    def load_actions_from_a_file(self, fileName):
        self.memory = deque(maxlen=10000)

        if ".gz" in fileName:
            json_data = gzip.open(fileName, 'rb')
        else:
            json_data = open(fileName)

        lines = json_data.readlines()
        if lines:
            for line in lines:
                # if (len(line) > 0 and line.startswith("[")):
                try:
                    state = json.loads(line)[0]
                    # print("{}".format(state))

                    current_state = self.state2vector(state['action']['state'])
                    new_state = self.state2vector(state['action']['state'])
                    action = state['action']['action']
                    reward = state['action']['reward']
                    self.remember(current_state, action, reward, new_state, False)
                except:
                    print("json line read error")

    def save_actions_as_vectors(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.memory, f)

    def load_vectors_into_actions(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def state2vector(self, state):

        chars  = state['Personajes']
        # print(chars)
        vChars = np.zeros([2], np.float)
        vChars[0] = float(chars[0]['posX']/256)
        vChars[1] = float(chars[0]['posY']/256)

        # vEnv vector with the environment data
        vEnv = np.zeros([3], np.float)
        vEnv[0] = float(state['dia']/7)
        vEnv[1] = float(state['momentoDia']/10)
        vEnv[2] = float(state['planta']/3)

        vector = np.append(vChars, vEnv)
        # print(vector)
        return vector.reshape(1,5)

