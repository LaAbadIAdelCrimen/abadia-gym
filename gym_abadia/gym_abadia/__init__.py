import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Abadia-v0',
    entry_point='gym_abadia.envs:AbadiaEnv'
)

register(
    id='Abadia-v2',
    entry_point='gym_abadia.envs:AbadiaEnv2'
)

register(
    id='Abadia-v3',
    entry_point='gym_abadia.envs:AbadiaEnv3'
)
