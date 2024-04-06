import networkx as nx


def kshell(graph):
    importance_dict = {}
    ks = 1
    while graph.nodes():
        temp = []
        node_degrees_dict = {}
        for i in graph.degree():
            node_degrees_dict[i[0]] = i[1]
        kks = min(node_degrees_dict.values())
        while True:
            for k, v in node_degrees_dict.items():
                if v == kks:
                    temp.append(k)
                    graph.remove_node(k)
                    node_degrees_dict = {}
                    for i in graph.degree():
                        node_degrees_dict[i[0]] = i[1]
            if kks not in node_degrees_dict.values():
                break
        importance_dict[ks] = temp
        ks += 1
    return importance_dict


if __name__ == "__main__":
    f = open("USAir.txt")
    line = f.readline()
    start = []
    to = []
    value = []
    while line:
        # print (line)
        a = line.split('	')
        start.append(int(a[0]))
        to.append(int(a[1][:-1]))
        # print(int(a[1][:-1]))
        line = f.readline()
    f.close()
    graph = nx.DiGraph()
    for i in range(len(start)):
        graph.add_edge(start[i], to[i])
    res = kshell(graph)
    print(res)
