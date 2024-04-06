import matplotlib.pyplot as plt
import seaborn as sns


def plot_rewards(rewards,
                 running_rewards,
                 tag="train",
                 env='CartPole-v0',
                 algo="DQN",
                 save=True,
                 path='./'):
    sns.set()
    plt.title("average learning curve of {} for {}".format(algo, env))
    plt.xlabel('epsiodes')
    plt.plot(rewards, label='rewards')
    plt.plot(running_rewards, label='running rewards')
    plt.legend()
    if save:
        plt.savefig(path + "{}_rewards_curve".format(tag))
