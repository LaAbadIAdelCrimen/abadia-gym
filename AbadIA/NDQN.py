import random
import numpy as np

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from collections import deque

class DQN:
    def __init__(self, env):
        self.env     = env
        self.memory  = deque(maxlen=2000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.0001 # previously 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        if env.modelName == None:
            self.model        = self.create_model()
            self.target_model = self.create_model()
        else:
            if (env.gsBucket != None):
                print("I will download from {} the file {}".format(env.gsBucket, env.modelName))
                env.download_blob(env.modelName, env.modelName)

            self.model        = self.load_model(env.modelName)
            self.target_model = self.load_model(env.modelName)

    def create_model(self):
        print("Creating a new model")
        model   = Sequential()
        state_shape  = self.env.observation_space.shape
        model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))
        return model

    def load_model(self, name):
        print("Loading a model from: ({})".format(name))
        return load_model(name)

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

        vector = self.env.stateVector()
        self.env.vector = vector

        if np.random.random() < self.epsilon:
            action = self.env.action_space.sample()
            print("e-greedy: {}  epsilon: {}<----               ".format(action, self.epsilon))
        else:
            predictions = self.model.predict(vector)[0]
            self.env.predictions = predictions
            final = np.zeros(9)
            for ii in range(0,9):
                if (self.env.valMovs[ii] >= 1):
                    final[ii] = predictions[ii]*1.5
                else:
                    final[ii] = predictions[ii]*0.5

            action = np.argmax(final)
            print("vector: {}                   ".format(vector))
            print("predictions: {}              ".format(predictions))
            print("action: {}                   ".format(action))

        return action

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            history = self.model.fit(state, target, epochs=1, verbose=0)
            # print("loss:", history.history["loss"], "\n")

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

