from imports import *


def dqn():
    SEED = 42
    #SEED = random.randint(0, 2 ** 30)
    #print('SEED: {}'.format(SEED))

    environment = GymEnvironment('Carnival-ram-v0', seed=SEED, normalize=True)

    model = DuelingQNet(state_size=128, action_size=6, fc1_units=256, fc2_units=128, seed=SEED)

    agent = DQNAgent(model, action_size=6, seed=SEED,
              use_double_dqn=True,
              use_prioritized_experience_replay=False,
              buffer_size=100000)

    #load(model, 'best/carnival_ram_256x128.pth')
    train_dqn(environment, agent, n_episodes=30000, max_t=10000,
              eps_start=1,
              eps_end=0.1,
              eps_decay=0.9999,
              graph_when_done=True,
              render_every=10000000)


def hc():
    #SEED = random.randint(0, 2 ** 30)
    #print('SEED: {}'.format(SEED))

    environment = GymEnvironment('Carnival-ram-v0', seed=SEED, normalize=True)

    agent = HillClimbingAgent(state_size=128, action_size=6, seed=SEED,
                              policy='deterministic')

    train_hc(environment, agent, seed=SEED, n_episodes=4000, max_t=2000,
             use_adaptive_noise=True,
             npop=10,
             print_every=100,
             graph_when_done=True)


### main ###
dqn()
#hc()