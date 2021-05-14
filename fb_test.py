import collections
import networkx as nx
import matplotlib.pyplot as plt


def read(data):
    G = nx.DiGraph()
    with open(data) as f:
        for line in f:
            temp_node1, temp_node2, trust, timestamp = line.split(",")[:4]
            
            #print(weight)
            node1, node2 = int(temp_node1), int(temp_node2)
            #print(node2)
            #G.add_nodes_from(node1,node2)

            G.add_edge(node1,node2, weight = int(trust), timestamp = float(timestamp))

            #g[node1].append(node2)
            #g[node2].append(node1)
    edges = G.edges(data = True)
    edge_list = list(edges)