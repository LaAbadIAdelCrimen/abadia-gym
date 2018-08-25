This repository contains a PIP package which is an OpenAI environment for
simulating an environment for the AbadIA (The abbey of crime game).

Also included some agents from random to more complex ones.

## Pre-installation

We recommend use virtualenv in order to have a controlled (and tested/controlled) enviroment. 

You can create this enviroment with: 

```
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


For install AbadIA-gym just install all the dependencies from the requirements.txt file using pip3: 
 
```
pip3 install -r requirements.txt 
```


## Usage

```
import gym
import gym_abadia

env = gym.make('abadia-v0')
```

### how to launch the game engine. 

Clone the game engine project and do the usual things like read the README.md file and then launch the game engine: 

```
./VigasocoSDL abadia -input:libVigasocoFakeInputPlugin.so,FakeInputPlugin  -audio:libVigasocoNULLAudioPlugin.so,NULLAudioPlugin
```
or use our not so cool bash shell loop: 

```
./loopVigasocoSDL.sh
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


