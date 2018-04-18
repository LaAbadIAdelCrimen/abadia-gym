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

## The Environment

Imagine you are selling bananas. One at a time. And the bananas get bad pretty
quickly. Let's say in 3 days. The probability that I will sell the banana
is given by

$$p(x) = (1+e)/(1. + e^(x+1))$$

where x-1 is my profit. This x-1 is my reward. If I don't sell the
banana, the agent gets a reward of -1 (the price of the banana).
