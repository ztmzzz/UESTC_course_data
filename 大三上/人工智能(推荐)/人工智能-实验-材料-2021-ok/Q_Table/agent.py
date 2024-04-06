import math

import numpy as np


class QLearning(object):
    def __init__(self, state_dim, action_dim, cfg):
        self.action_dim = action_dim  # dimension of acgtion
        self.lr = cfg.lr  # learning rate
        self.gamma = cfg.gamma  # 衰减系数
        self.epsilon = 0
        self.sample_count = 0
        self.Q_table = np.zeros((state_dim, action_dim))  # Q表格

    def choose_action(self, state):
        self.sample_count += 1
        self.epsilon = 0.2 + 0.8 * math.exp(-1.0 * self.sample_count / 500)
        if np.random.uniform(0, 1) > self.epsilon:
            action = self.predict(state)
        else:
            action = np.random.choice(self.action_dim)  # 随机探索选取一个动作
        return action

    def update(self, state, action, reward, next_state, done):
        self.Q_table[state, action] += self.lr * (
                reward + self.gamma * np.max(self.Q_table[next_state]) - self.Q_table[state, action])
        if done:
            self.Q_table[state, action] = reward

    def predict(self, state):
        max_num = np.max(self.Q_table[state])
        action = np.where(self.Q_table[state] == max_num)[0]
        action = np.random.choice(action)
        return action

    def save(self, path):
        np.save(path + "Q_table.npy", self.Q_table)

    def load(self, path):
        self.Q_table = np.load(path + "Q_table.npy")
