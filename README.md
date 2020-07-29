This repository contains a PIP package which is an OpenAI environment for
simulating an environment for the AbadIA (The abbey of crime game).

Also included some agents from random to more complex ones.

### How to launch the game engine.

```
git clone https://github.com/LaAbadIAdelCrimen/VigasocoSDL-AI.git

cd VigasocoSDL-AI/extra/Docker/vnc/

docker build -t vigasoco .

docker run -p 4477:4477 -p 5900:5900 vigasoco
```

## Installation pyhton3

We recommend use virtualenv in order to have a controlled (and tested/controlled) enviroment. 

You can create this enviroment with: 

```
git clone https://github.com/LaAbadIAdelCrimen/abadia-gym.git
cd abadia-gym/
apt install virtualenv
apt install python3-pip
virtualenv -p python3 python3
```

We're using python version 3 and the name of the directory with the enviroment will be python3. In this case it's created at the current directory.

The second step is invoke this enviroment with: 

```
source ./python3/bin/activate
```

Note: that I created previuosly at the current directory this enviroment directory (python3) but you could create this wherever you wish. 

Note2: you don't need to do that if you have python3 and you are not worried of messing with your current (and global) python enviroment.  


## Installation


For install AbadIA-gym  install all the dependencies from the requirements.txt file using pip3 and 2 last models agent: 
 
```
pip3 install -r requirements.txt 
mkdir -p snapshots
mkdir -p models
cd models/
wget https://storage.googleapis.com/abadia-data/models/last_model_v6.model
wget https://storage.googleapis.com/abadia-data/models/last_value_v1.model
cd ..
```


## Usage

```
import gym
import gym_abadia

env = gym.make('abadia-v0')
```

### How to run the agent v6
```
python3 agentv6_ngdqn.py --learning=false --episodes=5 --steps=2000 --initmodel=models/last_model_v6.model
```
You can run it in a loop: 
```
./loopagentv6.sh
```

### How to run the agent v4

run the version 4 agent QTables implementation and a few options to control the enviroment.

```
python3 agentv4_dqn.py --episodes=5 --steps=300 # --model=models/model_v1_lastest.model -c /tmp/check # -c partidas/20180602/abadia_checkpoint_180602_214255_980367_2_1_4_21_25_0.checkpoint
```

You can run it in a loop: 

```
./loopagentv4.sh
```


### Older versions of the agent

run the version 3 agent QTables implementation and a few options to control the enviroment.

```
python3 agentv3_qlearning.py --episodes=100 --steps=250 # -c partidas/20180429/abadia_checkpoint_18-04-29_19:53:02:726983_1_4_34_13_0.checkpoint
```

You can run it in a loop: 

```
./loopagentv3.sh
```

** Note: You can expects lot of log info and some ascii art **

run the dumb agent: 

```
(python3) ~/proyectos/abadia-gym (master ✘)✹✭ ᐅ python3 agentv1.py
```

run the version 2 agent a simple QTables implementation

```
(python3) ~/proyectos/abadia-gym (master ✘)✹✭ ᐅ python3 agentv2_qlearning.py
```


