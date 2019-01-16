import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Abadia-v2',
    entry_point='gym_abadia.envs:AbadiaEnv2',

