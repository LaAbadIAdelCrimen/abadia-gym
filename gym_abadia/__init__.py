import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Abadia-v0',
    entry_point='gym_abadia.envs:AbadiaEnv',
)
