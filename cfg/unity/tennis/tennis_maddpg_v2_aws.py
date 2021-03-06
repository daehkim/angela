algorithm='maddpg_v2'
env_class='UnityMLVectorMultiAgent'
model_class='LowDim2x'

environment = {
    'name': 'compiled_unity_environments/Tennis_Linux/Tennis.x86_64',
}

model = {
    'state_size': 24,
    'action_size': 2,
}

agent = {
    'action_size': 2,
    'update_every': 2,
    'n_agents': 2,
    #'evaluation_only': True
}

train = {
    'n_episodes': 100000,
    'solve_score': 0.5,
}
