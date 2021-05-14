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

    trusts = []
    for edge in edge_list:
        trusts.append(edge[2]["weight"])
    #nx.draw(G)
    #plt.show()
    print("Average trust score: " + str(sum(trusts)/len(trusts)))
    

    #avg = []
    #for edge1 in edge_list:
    #    if edge1[1] == 1:
    #        avg.append(edge1[2]["weight"])
    #print(sum(avg)/len(avg))

    node_ids = G.nodes()
    #print(max(node_ids))

    trust_total = [[] for i in range(max(node_ids)+1)]
    #print(len(trust_total))
    #print(trust_total)
    for edge1 in edge_list:
        second_node = edge1[1]
        #print(second_node)
        trust = edge1[2]["weight"]
        trust_total[second_node].append(trust)
        #edge_trust = []
        #edge_trust.append()
        #if edge1[1] == 1810:
            #print(edge1[2]["weight"])
    #print(trust_35)
    #print("Trust score of node 35: " + str(sum(trust_35)/len(trust_35)))
    #print(trust_total)
    average_trust_total = [0 for i in range(max(node_ids)+1)]
    for i,trust in enumerate(trust_total):
        if len(trust) != 0:
            average_trust_total[i] = sum(trust)/len(trust)

    #print(average_trust_total)
    
    nodes = G.number_of_nodes()

    aa = sorted(G.in_degree, key=lambda x: x[1], reverse=True)
    #print(aa)
    print("10 highest in degree nodes: " +str(aa[:10]))


    #print(node_ids)
    x_axx = [0 for i in range(max(node_ids)+1)]
    y_axx = [0 for i in range(max(node_ids)+1)]

    for degrees in aa:
        #print(degrees)
        x_axx[degrees[0]] = degrees[1]
        y_axx[degrees[0]] = average_trust_total[degrees[0]]

    #print(y_axx)

    plt.figure(figsize=(12, 8)) 
    #plt.loglog(degrees, degree_count, marker = ".", linewidth = 0, color = 'b', label = "Degree distribution") 
    plt.scatter(x_axx, y_axx, marker = ".", linewidth = 0, color = 'g', label = "In degree distribution") 
    #plt.loglog(out_degrees, out_degree_count, marker = ".", linewidth = 0, color = 'r', label = "out degree distribution") 
    plt.xlabel('Node Degree')
    plt.ylabel('Average score')
    #plt.title(file + " degree distribution")
    plt.legend()
    plt.show()


    #in degree distribution
    in_degree_sequence = sorted([d for n, d in G.in_degree()], reverse=True)
    in_degree_dic = collections.Counter(in_degree_sequence)
    in_degrees, in_degree_count = zip(*in_degree_dic.items())

    indegree_tot = 0
    for i in G.out_degree():
        indegree_tot += i[1]
    print(indegree_tot/G.number_of_nodes())
    
    
    #out degree distribution
    out_degree_sequence = sorted([d for n, d in G.out_degree()], reverse=True)
    out_degree_dic = collections.Counter(out_degree_sequence)
    out_degrees, out_degree_count = zip(*out_degree_dic.items())
    ##normalise by dividing by number of total nodes
    #degree_count = [i / nodes for i in degree_count]
    in_degree_count = [i / nodes for i in in_degree_count]
    out_degree_count = [i / nodes for i in out_degree_count]
    #plots
    plt.figure(figsize=(12, 8)) 
    #plt.loglog(degrees, degree_count, marker = ".", linewidth = 0, color = 'b', label = "Degree distribution") 
    plt.loglog(in_degrees, in_degree_count, marker = ".", linewidth = 0, color = 'g', label = "In degree distribution") 
    plt.loglog(out_degrees, out_degree_count, marker = ".", linewidth = 0, color = 'r', label = "out degree distribution") 
    plt.xlabel('Node Degree')
    plt.ylabel('Probability')
    #plt.title(file + " degree distribution")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    read("data/soc-sign-bitcoinotc.csv")