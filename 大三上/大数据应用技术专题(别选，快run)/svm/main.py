import copy
import networkx as nx


def compare(truedict, testdict):
    sorted_test = sorted(testdict.items(), key=lambda x: x[1], reverse=True)
    print("排序后结果")
    print(sorted_test)
    result = []
    for item in sorted_test:
        key = item[0]
        truevalue = truedict[key]
        result.append((truevalue, item[1]))
    return result


def gettao(true_test_list):
    n = len(true_test_list)
    n_true = 0
    n_false = 0
    for i in range(n):
        v1 = true_test_list[i][0]
        v2 = true_test_list[i][1]
        for j in range(n - i - 1):
            t1 = true_test_list[j + 1][0]
            t2 = true_test_list[j + 1][1]
            if (v1 >= t1 and v2 >= t2) or (v1 <= t1 and v2 <= t2):
                n_true += 1
            else:
                n_false += 1
    tao = 2 * (n_true - n_false) / n / (n - 1)
    return n, n_true, n_false, tao


def printresult(testdict):
    true_test_list = compare(guimo, testdict)
    print("对比列表")
    print(true_test_list)
    (n, n_true, n_false, tao) = gettao(true_test_list)
    print("总数:" + str(n))
    print("n+:" + str(n_true))
    print("n-:" + str(n_false))
    print("结果:" + str(tao))


f = open("USAir.txt")
line = f.readline()
start = []
to = []
while line:
    a = line.split('	')
    start.append(int(a[0]))
    to.append(int(a[1][:-1]))
    line = f.readline()
f.close()
# 有向图
# G = nx.DiGraph()
# 无向图
G = nx.Graph()
for i in range(len(start)):
    G.add_edge(start[i], to[i])

nodes = G.nodes()
print("结点数")
print(nodes)
guimo = {}
for node in nodes:
    infected = [node]
    for i in range(3):
        for t in infected:
            neighbors = list(G.neighbors(t))
            # 全感染
            infected = neighbors + infected

            # 概率感染
            # for neighbo in neighbors:
            #     a = random.randint(1, 10)
            #     if a <= 5:
            #         infected.append(neighbo)

            infected = list(set(infected))

    guimo[node] = len(infected)
print("节点对应传播规模")
print(guimo)

# 度为排序
print("以度为排序")
degree = {}
for i in G.degree():
    degree[i[0]] = i[1]
print("度数")
print(degree)
printresult(degree)
# kshell为排序
print("以kshell为排序")
tempG = copy.deepcopy(G)
kshelldict = {}
ks = 1
while tempG.nodes():
    tempdegree = {}
    for i in tempG.degree():
        tempdegree[i[0]] = i[1]
    kks = min(tempdegree.values())
    while True:
        for k, v in tempdegree.items():
            if v == kks:
                kshelldict[k] = ks
                tempG.remove_node(k)
                tempdegree = {}
                for i in tempG.degree():
                    tempdegree[i[0]] = i[1]
        if kks not in tempdegree.values():
            break
    ks += 1
print("kshell")
print(kshelldict)
printresult(kshelldict)
# closeness为排序
print("closeness")
CC = {}
for node in G.nodes():
    sum = -1
    shortest_path = nx.shortest_path(G, node)
    # print(shortest_path)
    for nodes in G.nodes:
        try:
            sum += 1 / len(shortest_path[nodes])
        except KeyError:
            # print("没有key:" + str(nodes))
            pass
    CC[node] = sum
print(CC)
printresult(CC)

# LeaderRank为排序
print("LeaderRank")
tempG = copy.deepcopy(G)
nodes = tempG.nodes()
num_nodes = len(nodes)
# 在网络中增加节点g并且与所有节点进行连接
tempG.add_node(999)
for node in nodes:
    tempG.add_edge(999, node)
    tempG.add_edge(node, 999)
# LR值初始化
LR = dict.fromkeys(nodes, 1.0)
LR[999] = 0.0
# 迭代从而满足停止条件
i = 0
while True:
    tempLR = {}
    for node1 in tempG.nodes():
        s = 0
        for node2 in tempG.nodes():
            if node1 in list(tempG.neighbors(node2)):
                s += 1.0 / len(list(tempG.neighbors(node2))) * LR[node2]
        tempLR[node1] = s
    # 终止条件:LR值不在变化
    error = 0.0
    for n in tempLR.keys():
        error += abs(tempLR[n] - LR[n])
    if error <= 0.1:
        break
    LR = tempLR
# 节点g的LR值平均分给其它的N个节点并且删除节点
avg = LR[999] / num_nodes
LR.pop(999)
for k in LR.keys():
    LR[k] += avg
print(LR)
printresult(LR)
