"""
Training loop.
"""

#import glob
#import os
import torch
import libs.statistics


def train(environment, agent, n_episodes=2000, max_t=1000,
          render=False,
          solve_score=100000.0,
          graph_when_done=False):
    """ Run training loop for DQN.

    Params
    ======
        environment: environment object
        agent: agent object
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        render (bool): whether to render the agent
        solve_score (float): criteria for considering the environment solved
        graph_when_done (bool): whether to show matplotlib graphs of the training run
    """

    stats = libs.statistics.DeepDeterministicPolicyGradientStats()

    # remove checkpoints from prior run
    #prior_checkpoints = glob.glob('checkpoints/last_run/episode*.pth')
    #for checkpoint in prior_checkpoints:
    #    os.remove(checkpoint)

    for i_episode in range(1, n_episodes+1):
        rewards = []
        state = environment.reset()

        # loop over steps
        for t in range(max_t):
            if render:  # optionally render agent
                environment.render()

            # select an action
            action = agent.act(state)
            # take action in environment
            next_state, reward, done = environment.step(action)
            # update agent with returned information
            agent.step(state, action, reward, next_state, done)
            state = next_state
            rewards.append(reward)
            if done:
                break

        # every episode
        buffer_len = len(agent.memory)
        stats.update(t, rewards, i_episode)
        stats.print_episode(i_episode, agent.alpha, buffer_len, t)

        # every epoch (100 episodes)
        if i_episode % 100 == 0:
            stats.print_epoch(i_episode, agent.alpha, buffer_len)
            save_name = 'checkpoints/last_run/episode.{}'.format(i_episode)
            torch.save(agent.actor_local.state_dict(), save_name + '.actor.pth')
            torch.save(agent.critic_local.state_dict(), save_name + '.critic.pth')

        # if solved
        if stats.is_solved(i_episode, solve_score):
            stats.print_solve(i_episode, agent.alpha, buffer_len)
            torch.save(agent.actor_local.state_dict(), 'checkpoints/last_run/solved.actor.pth')
            torch.save(agent.critic_local.state_dict(), 'checkpoints/last_run/solved.critic.pth')
            break

    # training finished
    if graph_when_done:
        stats.plot(agent.loss_list)