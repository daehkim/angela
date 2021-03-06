"""
Vanilla Policy Gradient agent.
"""

import numpy as np
import torch
import torch.optim as optim
from torch.distributions import Categorical

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Agent():
    def __init__(self, model, seed=0, load_file=None, lr=1e-2, action_map=None):
        """
        Params
        ======
            model: model object
            seed (int): Random seed
            load_file (str): path of checkpoint file to load
            lr (float): learning rate
            action_map (dict): how to map action indexes from model output to gym environment
        """
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

        self.model = model.to(device)
        if load_file:
            # self.model.load_state_dict(torch.load(load_file))
            self.model.load_state_dict(torch.load(load_file, map_location='cpu'))  # load from GPU to CPU
            print('Loaded: {}'.format(load_file))
        self.action_map = action_map
        self.optimizer = optim.Adam(model.parameters(), lr=lr)


    def _discount(self, rewards, gamma, normal):
        """
        Calulate discounted future (and optionally normalized) rewards.
        From https://github.com/wagonhelm/Deep-Policy-Gradient
        """

        discounted_rewards = np.zeros_like(rewards)
        G = 0.0
        for i in reversed(range(0, len(rewards))):
            G = G * gamma + rewards[i]
            discounted_rewards[i] = G
        # normalize rewards
        if normal:
            mean = np.mean(discounted_rewards)
            std = np.std(discounted_rewards)
            std = max(1e-8, std) # avoid divide by zero if rewards = 0.0
            discounted_rewards = (discounted_rewards - mean) / (std)
        return discounted_rewards


    def act(self, state):
        """Given a state, determine the next action."""

        if len(state.shape) == 1:   # reshape 1-D states into 2-D (as expected by the model)
            state = np.expand_dims(state, axis=0)
        state = torch.from_numpy(state).float().to(device)
        probs = self.model.forward(state).cpu()
        m = Categorical(probs)
        action = m.sample()
        # use action_map if it exists
        if self.action_map:
            return self.action_map[action.item()], m.log_prob(action)
        else:
            return action.item(), m.log_prob(action)


    def learn(self, rewards, saved_log_probs, gamma):
        """Update model weights."""

        # calculate discounted rewards for each step and normalize them
        discounted_rewards = self._discount(rewards, gamma, True)

        policy_loss = []
        for i, log_prob in enumerate(saved_log_probs):
            policy_loss.append(-log_prob * discounted_rewards[i])
        policy_loss = torch.cat(policy_loss).sum()

        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()
