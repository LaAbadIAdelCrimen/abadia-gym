import gym

def register(id, entry_point, force=True):
    env_specs = gym.envs.registry.env_specs
    if id in env_specs.keys():
        if not force:
            return
        del env_specs[id]
    gym.register(
        id=id,
        entry_point=entry_point,
    )

# Register modified versions of existing environments

register(id='Abadia-v3', entry_point='envs.abadia_env3:AbadiaEnv3')
register(id='Abadia-v4', entry_point='envs.abadia_env4:AbadiaEnv4')
#register(id='Abadia-v3', entry_point='gym_abadia.envs.abadia_env3:AbadiaEnv3')
# register(id='Abadia-v4', entry_point='gym_abadia.envs.abadia_env4:AbadiaEnv4')
