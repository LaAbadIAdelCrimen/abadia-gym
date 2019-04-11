import gym
import gym_abadia
import numpy as np
import os
import argparse
import random
import json
import AbadIA.NGDQN
AbadIA.NGDQN
# env = gym.make('Abadia-v2')
dqn_agent = AbadIA.NGDQN.NGDQN(env=None, modelName="models/testv5.model")

print("Creating a new model")
dqn_agent.model = dqn_agent.create_model()
dqn_agent.target_model = dqn_agent.create_model()

state1 = ['{"action":{"action":5,"nextstate":{"Objetos":[],"Personajes":[{"altura":0,"id":0,"nombre":"Guillermo","objetos":32,"orientacion":2,"posX":133,"posY":160},{"altura":0,"id":1,"nombre":"Adso","objetos":0,"orientacion":3,"posX":136,"posY":160}],"Rejilla":[[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,16,16,0,32,32,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,14,14,14,14,16,16,0,32,32,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,15,0,0,0,0,0,0,0,0,15,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,15,0,0,0,0,0,0,0,0,15,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,15,0,0,0,0,0,0,0,0,15,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],"action_predictions":5,"action_type":"E","bonus":0,"dia":1,"final":[],"frases":[],"gameId":"190331_164106_711419","haFracasado":false,"investigacionCompleta":false,"jugada":2,"momentoDia":4,"numPantalla":23,"numeroRomano":0,"obsequium":31,"planta":0,"porcentaje":0,"predictions":[],"reward":-0.005,"sonidos":[0,0,0,0,0,0,0,0,0,0,0,0],"totalReward":-0.005,"valMovs":[1,1,1,1,1,1,1,1,1],"vector":[[134,159,1,137,159,1,0,0,0,0,0,0,0,0,0]]},"reward":-0.005,"state":{"Objetos":[],"Personajes":[{"altura":0,"id":0,"nombre":"Guillermo","objetos":32,"orientacion":1,"posX":134,"posY":159},{"altura":0,"id":1,"nombre":"Adso","objetos":0,"orientacion":1,"posX":137,"posY":159}],"Rejilla":[[0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0],[0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0],[14,14,14,14,14,14,14,14,2,2,2,2,2,2,2,2,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,1,1,1,1,1,1,1,1,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,16,16,0,32,32,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,0,0,0,0,0,16,16,0,32,32,0,0,0,0,0,0,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14],[14,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,14]],"bonus":0,"dia":1,"frases":[],"haFracasado":false,"investigacionCompleta":false,"momentoDia":4,"numPantalla":22,"numeroRomano":0,"obsequium":31,"planta":0,"porcentaje":0,"sonidos":[0,0,0,0,0,0,0,0,0,0,0,0]}}}']
state = json.loads(state1[0])
print(state['action']['action'])
print(state['action']['nextstate'])
dqn_agent.state2vector(state['action']['state'])


for t in range(33):
    current_state = dqn_agent.state2vector(state['action']['state'])
    new_state = dqn_agent.state2vector(state['action']['state'])
    action = state['action']['action']
    reward = state['action']['reward']

    dqn_agent.remember(current_state, action, reward, new_state, False)
#    if (t % 32 == 0):

print("trainig it")
print(current_state.shape[0])
print(current_state.shape[1])
print(current_state)

dqn_agent.replay()

print("get some predictions -------------------")
print("new_state: {}".format(current_state))
print("----------------------")
prediction = dqn_agent.target_model.predict(current_state)
print("prediction: {}".format(prediction))

print("trainig it a game at time")
print(current_state.shape[0])
print(current_state.shape[1])
print(current_state)

history = dqn_agent.replay_game(verbose=1)
dqn_agent.save_model(dqn_agent.modelName)
dqn_agent.load_actions_from_a_file("/tmp/actions.json")

# with open("/tmp/actions.json") as json_data:
#    lines = json_data.readlines()
#    if lines:
#        rejilla = np.empty([24, 24])
#        for line in lines:
#            # print("line:"+line)
#            # if (len(line) > 0 and line.startswith("[")):
#            state = json.loads(line)[0]
#            print("{}".format(state))

#            current_state = dqn_agent.state2vector(state['action']['state'])
#            new_state = dqn_agent.state2vector(state['action']['state'])
#            action = state['action']['action']
#            reward = state['action']['reward']

#            dqn_agent.remember(current_state, action, reward, new_state, False)

history = dqn_agent.replay_game(epochs=30, verbose=1)
dqn_agent.save_model(dqn_agent.modelName)
