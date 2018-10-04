"""
NOTE: Download pre-built Unity Bannana.app from: https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher
"""

agent_type='ddpg'
env_class='UnityMLVector'
model_class='LowDim2x'

environment = {
    'name': 'cfg/compiled_unity_environments/Reacher_Linux/Reacher.x86_64',
    'seed': 1
}

model = {
    'state_size': 33,
    'action_size': 4,
}

agent = {
    'action_size': 4,
    'update_every': 1,
}

train = {
    'n_episodes': 1000,
    'solve_score': 30.0,
    'max_t': 1000
}