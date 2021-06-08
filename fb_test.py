import collections
from collections import Counter
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
            #here these are flipped because user 2 posted on user 1 wall
            G.add_edge(int(node2),int(node1), timestamp = float(timestamp))
    #could remove this
    print("Number of posts on own wall: " + str(selfposts))
    #print(edges)
    #edge_list = list(edges)'
    #print(G.number_of_nodes())
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





# for each node find what date it hs most in degrees
# then to make sense of it modulo it 365 and see if they match
def date_most_posts(G):
    nodes = G.nodes()
    edges = G.edges(data = True)
    edge_list = list(edges)
    timestamp_list = []
    for edge in edge_list:
        timestamp = edge[2]["timestamp"]
        timestamp_list.append(timestamp)
    #print(edge_list[10])

    dates=[dt.datetime.fromtimestamp(ts) for ts in timestamp_list]
    #print(dates[0].month)
    #print(dates[0].day)
    # replace the unix time with datetime
    for i,edge in enumerate(edge_list):
        edge[2]["timestamp"] = dates[i]
    
    #convert edgelist to dict for linear lookup
    # note if an edge between the nodes already exists append to list the second date
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Frozenset.... dont we lose the information weather we are looking at indegree vs outdegree
    edge_dict = {}
    for edge in edge_list:
        #print(edge[0])
        if frozenset([edge[0],edge[1]]) not in edge_dict.keys():
            edge_dict[frozenset([edge[0],edge[1]])] = [(edge[2]["timestamp"].day, edge[2]["timestamp"].month)]
        else:
            edge_dict[frozenset([edge[0],edge[1]])].append((edge[2]["timestamp"].day, edge[2]["timestamp"].month))

    #print(len(edge_dict))
    # dictionary with each node as key
    # then for every node count the number of in degree for every date of year
    # only considering month and day, find the largest one and 
    # NOTEEEE!!!!!!!!!!
    # this is only dist with node as key and then list of dates that people posted on wall
    # LOOK AT THE LENGTH OF each list to see how many people posted on the wall??
    dates_dict = {}
    for node in nodes:
        in_edges = (G.in_edges(node))
        for in_edge in in_edges:
            #print(edge_dict[frozenset(in_edge)])
            if node not in dates_dict.keys():
                dates_dict[node] = list([edge_dict[frozenset(in_edge)]])      # here had ot add brackets because otherwise the first entry want read into a tuple but just the items
            else:
                dates_dict[node].append(edge_dict[frozenset(in_edge)])

    #print(dates_dict)

    # go through dates dict find most popular date for each node print it
    # then convert it to 365?
    #assumed_bdays = []
    #for date in dates_dict:
    #    dates_lis = dates_dict[date]
    #    flat_list = [item for sublist in dates_lis for item in sublist]
    #    most_freq = most_frequent(flat_list)
    #    assumed_bdays.append(most_freq[1])




    """


    ############################################################################
    ### SAME BUT for out deg.note we still expect this to be highest in birth months 
    out_dates_dict = {}
    for node in nodes:
        out_edges = (G.out_edges(node))
        for out_edge in out_edges:
            #print(edge_dict[frozenset(in_edge)])
            if node not in out_dates_dict.keys():
                out_dates_dict[node] = list([edge_dict[frozenset(out_edge)]])      # here had ot add brackets because otherwise the first entry want read into a tuple but just the items
            else:
                out_dates_dict[node].append(edge_dict[frozenset(out_edge)])

    #print(dates_dict)

    # go through dates dict find most popular date for each node print it
    # then convert it to 365?
    normalization = []
    for date in out_dates_dict:
        dates_lis = out_dates_dict[date]
        flat_list = [item for sublist in dates_lis for item in sublist]
        most_freq = most_frequent(flat_list)
        normalization.append(most_freq[1])
    """






    
    #in days
    assumed_bdays = []
    for date in dates_dict:
        dates_lis = dates_dict[date]
        flat_list = [item for sublist in dates_lis for item in sublist]
        most_freq = most_frequent(flat_list)
        assumed_bdays.append(int((most_freq[1]-1)*30.4 + most_freq[0]))

    #print(min(assumed_bdays))
    """
    plt.figure(figsize=(12, 8)) 
    #fig, ax = plt.subplots(figsize=(12, 8))
    plt.hist(assumed_bdays,365, color = "g", histtype='bar', ec='black')
    plt.xlabel('Day of the year')
    plt.ylabel('Number of nodes with highest in degree on this month')
    plt.show()
    """
    return(assumed_bdays)



def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def normalise(G):
    nodes = G.nodes()
    edges = G.edges(data = True)
    edge_list = list(edges)

    interactions_dict = {}
    # dict with every node as key and timestamp of every interaction... indeg/outdeg doesnt matter 
    for edge in edge_list:
        #print(edge)
        if edge[0] not in interactions_dict.keys():
            interactions_dict[edge[0]] = [edge[2]["timestamp"]]

        if edge[1] not in interactions_dict.keys():
            interactions_dict[edge[1]] = [edge[2]["timestamp"]]

        if edge[0] in interactions_dict.keys():
            interactions_dict[edge[0]].append(edge[2]["timestamp"])


        if edge[0] in interactions_dict.keys():
            interactions_dict[edge[1]].append(edge[2]["timestamp"])
    
    #print(interactions_dict)
    # for every node take the timestamp of the earliest interaction 
    # list of lists with list being a list of months containing the nodes that first interracted on that date.
    # from which we then take the number of nodes which we will use to normalise.
    # 
    normalise = []
    for key in interactions_dict.keys():
        timestamps = interactions_dict[key]
        min_timestamp = min(timestamps)
        #print(min_timestamp)
        interactions_dict[key] = min_timestamp
        #months[interactions_dict[key].month - 1].append(key)
        month = interactions_dict[key].month
        day = interactions_dict[key].day
        normalise.append(int((month - 1)*30.4 + day))

    #print(max(normalise))

    # want to start sum on 23rd day and finish on 22nd
    day_count = [ [0] for _ in range(max(normalise)) ]
    for i in normalise:
        day_count[i-1][0] += 1
    day_count = [item for sublist in day_count for item in sublist]

    #print(day_count)

    # start with 23rd day and end with 22nd day of the year
    day_count = day_count[21:] + day_count[:21]
    #print(day_count)
    
    count = 0    
    for i,j in enumerate(day_count):
        count += j
        day_count[i] = count
    #print(day_count)

    #print(day_count)
    
    day_count = day_count[-21:] + day_count[:344]
    
    return(day_count)
        

    #print(interactions_dict)
 
    #print(months)
    #print(len(months[0])+ len(months[1]) +len(months[2]) + len(months[3])+len(months[4])+len(months[5])+len(months[6])+len(months[7])+len(months[8])+len(months[9])+len(months[10])+len(months[11]))
    '''
    month_count = []
    for month in months:
        month_count.append(len(month))
    # might have to be cumulative starting Feb, endjing january.... might have to do it in days
    #print(month_count)


    '''
    #return(normalise)
        



def bday_plot(assumed_bdays,norm):

    
    
    bdays_count = [ [0] for _ in range(max(assumed_bdays)) ]
    #print(month_count)
    #print(bdays_count)
    for i in assumed_bdays:
        bdays_count[i -1][0] +=1 
    #print(assumed_bdays)
    bdays_count = [item for sublist in bdays_count for item in sublist]
    print(bdays_count)

    """
    norm_count = [ [0] for _ in range(12) ]
    #print(month_count)
    #print(bdays_count)
    for i in norm:
        norm_count[i -1][0] +=1 
    print(assumed_bdays)
    norm_count = [item for sublist in norm_count for item in sublist]

    print(bdays_count)
    print(norm)
    
    """
    bananasplit = [b / m for b,m in zip(bdays_count, norm)]
    print(bananasplit)
    

    #bins = 100
    plt.figure(figsize=(12, 8)) 
    #plt.hist(assumed_bdays, 365, color = "b", histtype='bar', ec='black')
    plt.plot(bananasplit)
    plt.xlabel('day of the year')
    #plt.ylabel('Number of nodes with highest in degree on this month')
    plt.show()
    


# want to compare the average clustering of the overall graph with that of the subragphs formed starting from the nodes with 0 indegree.
def spam(G):
    print(nx.average_clustering(G))
    node_ids = G.nodes()

    in_deg = sorted(G.in_degree, key=lambda x: x[1], reverse=True)
    out_deg = sorted(G.out_degree, key=lambda x: x[1], reverse=True)
    #print(out_deg[:10])


    # look at the ratio of outdeg vs indeg for every node
    # possibly just remove all nodes with 0 indeg
    in_out_ratio = {}
    for node in out_deg:
        in_out_ratio[node[0]] = [node[1]]
        
    for node in in_deg:
        if node[1] == 0:
            in_out_ratio[node[0]][0] /= 0.01
        else:
            in_out_ratio[node[0]][0] /= node[1]


    for node in in_out_ratio:
        in_out_ratio[node].append(nx.clustering(G, node))


    aa = list(in_out_ratio.values())
    in_out, clustering = zip(*aa)
    




    
    plt.figure(figsize=(12, 8)) 
    plt.scatter(in_out, clustering, marker = ".", linewidth = 0, color = 'b')
    plt.xlabel('In_out_degree ratio')
    plt.ylabel('Clustering')
    plt.show()


    #print(nx.clustering(G, 133))
    #print(nx.clustering(G, 3727))
    #print(nx.clustering(G, 5423))
    #14416






if __name__ == "__main__":
    graph = read("data/facebook-wall.txt.anon")
    #degree_dist(graph)
    #in_degree_out_degree(graph)
    spam(graph)
    #timestamp_vs_indeg(graph)
    #run_powerlaw(graph)
    #assumed_bdays = date_most_posts(graph)
    #print(assumed_bdays)
    #norm = normalise(graph)
    #bday_plot(assumed_bdays, norm)
