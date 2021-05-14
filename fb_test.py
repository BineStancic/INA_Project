import collections
import networkx as nx
import matplotlib.pyplot as plt
import time
import matplotlib.dates as md
import datetime as dt
import math


def read(data):
    G = nx.DiGraph()
    with open(data) as f:
        selfposts = 0
        for line in f:
            #print(line)
            node1, node2, timestamp = line.split("\t")[:3]
            if node1 == node2:
                selfposts += 1
            #G.add_nodes_from(node1,node2)
            G.add_edge(int(node2),int(node1), timestamp = float(timestamp))
    #edges = G.edges(data = True)
    print("Number of posts on own wall: " + str(selfposts))
    #print(edges)
    #edge_list = list(edges)
    return G

def degree_dist(G):

    nodes = G.number_of_nodes()

    #degree distribution
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degree_dic = collections.Counter(degree_sequence)
    degrees, degree_count = zip(*degree_dic.items())


    #in degree distribution
    in_degree_sequence = sorted([d for n, d in G.in_degree()], reverse=True)
    in_degree_dic = collections.Counter(in_degree_sequence)
    in_degrees, in_degree_count = zip(*in_degree_dic.items())

    
    #out degree distribution
    out_degree_sequence = sorted([d for n, d in G.out_degree()], reverse=True)
    out_degree_dic = collections.Counter(out_degree_sequence)
    out_degrees, out_degree_count = zip(*out_degree_dic.items())
    ##normalise by dividing by number of total nodes
    degree_count = [i / nodes for i in degree_count]
    in_degree_count = [i / nodes for i in in_degree_count]
    out_degree_count = [i / nodes for i in out_degree_count]
    #plots
    plt.figure(figsize=(12, 8)) 
    plt.loglog(degrees, degree_count, marker = ".", linewidth = 0, color = 'b', label = "Degree distribution") 
    plt.loglog(in_degrees, in_degree_count, marker = ".", linewidth = 0, color = 'g', label = "In degree distribution") 
    plt.loglog(out_degrees, out_degree_count, marker = ".", linewidth = 0, color = 'r', label = "out degree distribution") 
    plt.xlabel('Node Degree')
    plt.ylabel('Probability')
    #plt.title(file + " degree distribution")
    plt.legend()
    plt.show()

def in_degree_out_degree(G):

    node_ids = G.nodes()

    in_deg = sorted(G.in_degree, key=lambda x: x[1], reverse=True)
    out_deg = sorted(G.out_degree, key=lambda x: x[1], reverse=True)


    in_deg_lists = [0 for i in range(max(node_ids)+1)]
    out_deg_lists = [0 for i in range(max(node_ids)+1)]


    for node in in_deg:
        #print(node)
        in_deg_lists[node[0]] = node[1]
        #out_deg_lists[node[0]] = out_deg[node]

    for node in out_deg:
        out_deg_lists[node[0]] = node[1]

    plt.figure(figsize=(12, 8)) 
    plt.scatter(in_deg_lists, out_deg_lists, marker = ".", linewidth = 0, color = 'b')
    plt.xlabel('In degree')
    plt.ylabel('Out degree')
    plt.show()


def timestamp_vs_indeg(G):
    edges = G.edges(data = True)
    edge_list = list(edges)
    timestamp_list = []
    for edge in edge_list:
        timestamp = edge[2]["timestamp"]
        timestamp_list.append(timestamp)
    #print(timestamp)


    dates=[dt.datetime.fromtimestamp(ts) for ts in timestamp_list]
    #print(dates)

    #in_deg = sorted(G.in_degree, key=lambda x: x[1], reverse=True)
    #print(in_deg)

    bins = 100
    plt.figure(figsize=(12, 8)) 
    #fig, ax = plt.subplots(figsize=(12, 8))
    plt.hist(dates,bins, color = "g")
    #ax.set(xlabel = 'Time', ylabel = 'Number of Interactions' )
    #ax=plt.gca()

    #ax=plt.gca()
    #xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    #ax.xaxis.set_major_formatter(xfmt)
    
    #plt.hist(dates,bins, color = "g")
    plt.xlabel('Dates')
    plt.ylabel('Number of Interactions')
    plt.show()



def run_powerlaw(G):
    power_law("overall degree",G.degree,1)
    power_law("in degree",G.in_degree,1)
    power_law("out_degree", G.out_degree,1)

def power_law(degtype,distribution,k_min):
    #degree sequence
    degree_sequence = list([d for n, d in distribution])
    #degree sequence above kmin
    degree_sequence_lim = [i for i in degree_sequence if i >= k_min]
    liss = []
    for i in degree_sequence_lim:
        if i >= k_min:
            liss.append(math.log(i/(k_min - 0.5)))
    gamma = 1+ len(degree_sequence_lim)* (sum(liss)**-1)
    print("gamma " + degtype + " = " +str(gamma))






if __name__ == "__main__":
    graph = read("data/facebook-wall.txt.anon")
    #degree_dist(graph)
    #in_degree_out_degree(graph)
    #timestamp_vs_indeg(graph)
    #run_powerlaw(graph)
