import torch
import torch.nn as nn
import torch.utils.data as data
from other.getData import *


def train():
    model.train()
    for epoch in range(1, num_epochs + 1):
        loss_sum = 0.0
        for step, (x, y) in enumerate(train_loader):
            x = x.to(device)
            y = y.to(device)
            y_pred = model(x)
            y = y.squeeze()  # 修正标签格式
            loss = LOSS_FUNC(y_pred, y)
            loss_sum += loss
            OPTIMIZER.zero_grad()
            loss.backward()
            OPTIMIZER.step()
        if epoch % 200 == 0:
            print("epoch: %d, loss: %f" % (epoch, loss_sum / batch_size))
            test()
            # torch.save(model.state_dict(), 'model')


def test():
    model.eval()
    with torch.no_grad():
        acc_sum = 0.0
        count = 0
        fuck_sum = 0
        for step, (x, y) in enumerate(test_loader):
            x = x.to(device)
            y = y.to(device)
            acc_sum += abs((model(x).argmax(dim=1) - y.squeeze())).sum()
            count += len(y)
            # fuck_sum += abs((x[[0], [1]] - y.squeeze())).sum()
        print("误差: %f" % (acc_sum / count))
        # print("fuck: %f" % (fuck_sum / count))
        global bad
        if bad > (acc_sum / count):
            torch.save(model.state_dict(), 'model')
            bad = (acc_sum / count)


def result():
    df = pd.read_csv('data.csv', names=['school', 'province', 'batch', 'wenli', '2017', '2018', '2019', '2020'])
    x = df[['school', 'province', 'wenli', '2018', '2019', '2020']]

    def process(x):
        if (x['2018'] == 0) | (x['2019'] == 0) | (x['2020'] == 0):
            return x['school'], x['province'], 0, 0, 0
        else:
            z = [x['2019'] - x['2018'], x['2020'] - x['2019']]
            # print(z)
            # print(type(z))
            z = np.array(z)
            z = torch.from_numpy(z).type(torch.FloatTensor)
            z = z.to(device)
            y = model(z)
            # print(y.data)
            y = y.argmax() - 40
            # print(y)
            y = y.cpu().item()

            return x['school'], x['province'], x['wenli'], x['2020'], y

    def process1(x):
        y = x[4] + x[3]
        return x[0], x[1], 2021, x[2], y

    x = x.apply(process, axis=1, result_type="expand")
    x = x.drop(x[(x[3] == 0)].index)
    x = x.apply(process1, axis=1, result_type="expand")

    x.to_csv("resultData.csv", header=False, index=False)


if __name__ == '__main__':
    bad = 999
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # device = 'cpu'
    torch.cuda.empty_cache()
    num_epochs = 40000
    batch_size = 100
    learning_rate = 0.00001
    x_train, y_train = get_train()
    x_test, y_test = get_test()
    x_train = torch.from_numpy(x_train).type(torch.FloatTensor)
    y_train = torch.from_numpy(y_train).type(torch.LongTensor)
    train_set = data.TensorDataset(x_train, y_train)

    train_loader = data.DataLoader(
        dataset=train_set,
        batch_size=batch_size,
        shuffle=True
    )
    x_test = torch.from_numpy(x_test).type(torch.FloatTensor)
    y_test = torch.from_numpy(y_test).type(torch.LongTensor)
    test_set = data.TensorDataset(x_test, y_test)

    test_loader = data.DataLoader(
        dataset=test_set,
        batch_size=batch_size,
        shuffle=True
    )

    model = nn.Sequential(
        nn.Linear(2, 60),
        nn.ReLU(),
        nn.Linear(60, 300),
        nn.ReLU(),
        nn.Linear(300, 81),
    )
    LOSS_FUNC = nn.CrossEntropyLoss()
    OPTIMIZER = torch.optim.Adam(model.parameters(), lr=learning_rate)
    model.load_state_dict(torch.load('model'))
    model.eval()
    model.to(device)
    # train()
    # test()
    result()
