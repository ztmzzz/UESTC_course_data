import numpy as np
import pandas as pd


def get_train():
    x = pd.read_csv('train/data.csv', header=None)
    y = x[:][[2]]
    x = x[:][[0, 1]]
    x = np.array(x)
    y = np.array(y)
    return x, y


def get_test():
    x = pd.read_csv('test/data.csv', header=None)
    y = x[:][[2]]
    x = x[:][[0, 1]]
    x = np.array(x)
    y = np.array(y)
    return x, y


def spitdata():
    df = pd.read_csv('data.csv', names=['school', 'province', 'batch', 'wenli', '2017', '2018', '2019', '2020'])
    x = df[['2017', '2018', '2019', '2020']]

    def process(x):
        if (x['2018'] == 0) | (x['2017'] == 0) | (x['2019'] == 0) | (x['2020'] == 0):
            return 0, 0, 0, 0
        else:
            return x['2017'], x['2018'], x['2019'], x['2020']

    # -40~+40
    def process1(x):
        x1 = (x[1] - x[0])
        x2 = (x[2] - x[1])
        x3 = (x[3] - x[2])+40
        if (x3 >= 80):
            x3 = 80
        elif (x3 <= 0):
            x3 = 0;
        return x1, x2, x3

    x = x.apply(process, axis=1, result_type="expand")
    x = x.drop(x[(x[0] == 0) & (x[1] == 0) & (x[2] == 0) & (x[3] == 0)].index)
    x = x.apply(process1, axis=1, result_type="expand")
    x = x.sample(frac=1)
    print(len(x))
    # print(x)
    t = int(len(x) / 4 * 3)
    x_train = x[0:t][:]
    print(len(x_train))
    x_train.to_csv("train/data.csv", header=False, index=False)
    x_test = x[t + 1:][:]
    x_test.to_csv("test/data.csv", header=False, index=False)


if __name__ == "__main__":
    spitdata()
