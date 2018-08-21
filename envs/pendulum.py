import sys
sys.path.insert(0, '../libs')
from monitor import train, watch
from dqn_agent import Agent
from environment import Environment


environment = Environment('Pendulum-v0', 'gym', max_steps=1000, action_bins=(10,))
agent = Agent(state_size=3, action_size=9, fc1_units=32, fc2_units=32, seed=0)
train(environment, agent, n_episodes=4000, max_t=1000)