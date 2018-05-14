This repository contains a PIP package which is an OpenAI environment for
simulating an environment for the AbadIA (The abbey of crime game).


## Installation

Install the [OpenAI gym](https://gym.openai.com/docs/).

Then install this package via

```
pip install -e .
```

## Usage

```
import gym
import gym_abadia

env = gym.make('abadia-v0')
```

how to test with a dumb agent. 
Launch the game engine: 

```
./VigasocoSDL abadia -input:libVigasocoFakeInputPlugin.so,FakeInputPlugin  -audio:libVigasocoNULLAudioPlugin.so,NULLAudioPlugin

```

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


