import collections

import networkx as nx
import matplotlib.pyplot as plt
import datetime as dt
import time

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
    return(G)

def deg_score_distr(G):

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
    plt.legend()
    plt.show()

def deg_distr(G):
    nodes = G.number_of_nodes()
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
        #print(edge)
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


#if two nodes score each other plot the scores in a scatter plot
#xax the score node 1 on node 2, yax the score of node 2 on node 1
def score_score(G):
    
    nodes = G.nodes()
    #G.out_edges(node)
    node_pairs = []
    
    # for every node check if there is a node that it grades and is graded by it
    for node in nodes:
        out_edges = (G.out_edges(node))
        in_edges = (G.in_edges(node))
        #print(in_edges)
        #for edge in in_edges:
        #    print(edge[::-1])
        for i in out_edges:
            for j in in_edges:
            #    print(j)
                if i==j[::-1]:
                    #print(i)
                    node_pairs.append(i)

    
    # remove duplicates from node pairs
    # not needed lool
    #print(len(node_pairs))
    #node_pairs = list(dict.fromkeys(node_pairs))
    #print(len(node_pairs))
    
    print(len(node_pairs))
    node_pair_scores = [] 
    edges = G.edges(data = True)
    edge_list = list(edges)
    print(len(edge_list))

    # for every pair that matchec match it to an edge in edgelist
    # so we can see the weight of the edges
    # break when an edge that matches is found
    for pair in node_pairs:
        #print("brokee")
        for edge in edge_list:
            #print(edge[0])
            #print(pair[0])
            if edge[0] == pair[0] and edge[1] == pair[1]:
                node_pair_scores.append(edge)
                #print(edge)
                #print("Hiit")
                break

    
    #print(node_pair_scores)

    # go through edges that match and for evry (a,b) and (b,a) place them in the same dict key
    # from this can calculate average score for these connections and can also plot the scores score of 
    scores = []
    score_dict = {}
    for pair in node_pair_scores:
        #score = pair[2]["weight"]
        #scores.append(score)
        if frozenset([pair[0],pair[1]]) not in score_dict.keys():
            score_dict[frozenset([pair[0], pair[1]])] = [pair[2]["weight"]]
        else:
            score_dict[frozenset([pair[0], pair[1]])].append(pair[2]["weight"])
    
    
    print(len(score_dict))
    print(score_dict)



    
    
    xaxx = []
    yaxx = []
    

    for item in score_dict.items():
        #item_lis = list(item)
        xaxx.append(item[1][0])
        yaxx.append(item[1][1])


    plt.figure(figsize=(12, 8)) 
    plt.scatter(xaxx, yaxx, marker = ".", color = 'b', label = "Degree distribution") 
    #plt.loglog(in_degrees, in_degree_count, marker = ".", linewidth = 0, color = 'g', label = "In degree distribution") 
    #plt.loglog(out_degrees, out_degree_count, marker = ".", linewidth = 0, color = 'r', label = "out degree distribution") 
    plt.xlabel('node a score')
    plt.ylabel('node b score')
    #plt.legend()
    plt.show()



    

    #plt.figure(figsize=(12, 8)) 
    #plt.loglog(degrees, degree_count, marker = ".", linewidth = 0, color = 'b', label = "Degree distribution") 
    #plt.loglog(in_degrees, in_degree_count, marker = ".", linewidth = 0, color = 'g', label = "In degree distribution") 
    #plt.loglog(out_degrees, out_degree_count, marker = ".", linewidth = 0, color = 'r', label = "out degree distribution") 
    #plt.xlabel('node a score')
    #plt.ylabel('node b score')
    #plt.legend()
    #plt.show()




if __name__ == "__main__":
    graph = read("data/soc-sign-bitcoinotc.csv")
    deg_score_distr(graph)
    deg_distr(graph)
    in_degree_out_degree(graph)
    #timestamp_vs_indeg(graph)
    #score_score(graph)
    #a = frozenset(['A','T'])
    #b= frozenset(['T','A'])
    #if a == b:
    #    print("YEEET")