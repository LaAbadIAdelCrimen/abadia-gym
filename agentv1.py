import gym
import gym_abadia

env = gym.make('Abadia-v0')
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render(mode="human")
        print("observation: {}\n", observation)
        action = env.action_space.sample()
        print("Next Action: {}\n".format(action))
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

