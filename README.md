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

./VigasocoSDL abadia -input:libVigasocoFakeInputPlugin.so,FakeInputPlugin  -audio:libVigasocoNULLAudioPlugin.so,NULLAudioPlugin

run the dumb agent: 

(python3) ~/proyectos/abadia-gym (master ✘)✹✭ ᐅ python3 agentv1.py

run the version 2 agent a simple QTables implementation

(python3) ~/proyectos/abadia-gym (master ✘)✹✭ ᐅ python3 agentv2_qlearning.py


