
def model_1(G):
    
    SD=sort_distance_matrix(G)
    edges_limit=0
    for edge in G.edges():
        edges_limit+=G.edge[edge[0]][edge[1]]['weight']
    print 2*edges_limit/float(len(G.nodes()))
    n=len(G.nodes())
    Gm=G.copy()
    Gm.remove_edges_from(G.edges())
    total_length =0
    check=0
    edge_count=0
    while check==0:
        i=randint(0,n-1)
        node1=Gm.nodes()[i]
        node2=SD[node1][1][1]

        distance=SD[node1][1][0]
        if abs((total_length+distance)-edges_limit) < abs(total_length-edges_limit):
            edge_count+=1
            Gm.add_edge(node1,node2,weight=distance,time=edge_count)
            SD[node1].remove(SD[node1][1])
            j=0
            while SD[node2][j][1] != node1:
                j+=1
            SD[node2].remove(SD[node2][j])
            total_length+=distance
        else:
            check=1

    print 2*total_length/float(len(G.nodes())), 2*len(Gm.edges())/float(len(Gm.nodes()))
    error= (edges_limit-total_length)/edges_limit
    print 'error =', error
    return Gm

def model_2(G):

    SD=sort_distance_matrix(G)
    for node in SD.keys():
        SD[node].remove(SD[node][0])
    edges_limit=0
    for edge in G.edges():
        edges_limit+=G.edge[edge[0]][edge[1]]['weight']
    #print 2*edges_limit/float(len(G.nodes()))
    n=len(G.nodes())
    #Gm=G.copy()
    #Gm.remove_edges_from(G.edges())
    total_length=0
    edge_count=0

    Gm = min_distances_tree(G)
    for edge in Gm.edges():
        total_length+=Gm.edge[edge[0]][edge[1]]['weight']
        edge_count+=1

    check=0
    while check==0:
        i=randint(0,n-1)
        node1=Gm.nodes()[i]
        ratio = 2
        for item in SD[node1]:
            #print item[0],item[1]
            dist = float(item[0])
            node2 = item[1]
            path = nx.shortest_path_length(Gm, node1, node2, weight='weight')
            if (dist / float(path)) < ratio:
                ratio = dist / float(path)
                next_edge = (dist, ratio, node1, node2)
        if abs((total_length+next_edge[0])-edges_limit) < abs(total_length-edges_limit):
            edge_count+=1
            node2=next_edge[3]
            Gm.add_edge(node1, node2, weight=next_edge[0],time=edge_count)
            j=0
            while SD[node2][j][1] != node1:
                j+=1
            SD[node2].remove(SD[node2][j])
            total_length+=next_edge[0]
        else:
            check=1

    print 2*total_length/float(len(G.nodes())), 2*len(Gm.edges())/float(len(Gm.nodes()))
    error= (edges_limit-total_length)/edges_limit
    print 'error =', error
    return Gm

def model_3(G):
    
    # starting: tree creation
    Gm = min_distances_tree(G)

    #sorted distances list creation
    D_list = []
    for i in range(len(Gm)):
        for j in range(i):
            dist = real_distance(Gm, Gm.nodes()[i], Gm.nodes()[j])
            D_list += [(dist, i, j)]
    #D_list=sorted(D_list)

    #total link length of G
    edges_limit = 0
    for edge in G.edges():
        edges_limit += G.edge[edge[0]][edge[1]]['weight']

    #total link length of Gm
    total_length = 0
    for edge in Gm.edges():
        total_length += Gm.edge[edge[0]][edge[1]]['weight']

    print total_length, edges_limit

    #stop when adding a new links increases the difference between the total link length of G and Gm
    check = 0
    edge_count=len(Gm.edges())
    while check == 0:
        #look for the next link (the one with the minimum ratio)
        ratio = 2
        for item in D_list:
            dist = float(item[0])
            node1 = Gm.nodes()[item[1]]
            node2 = Gm.nodes()[item[2]]
            path = nx.shortest_path_length(Gm, node1, node2, weight='weight')
            if (dist / float(path)) < ratio:
                ratio = dist / float(path)
                next_edge = (dist, ratio, node1, node2)
        #check if it has to add a new link
        if abs((total_length + next_edge[0]) - edges_limit) < abs(total_length - edges_limit):
            edge_count+=1
            Gm.add_edge(next_edge[2], next_edge[3], weight=next_edge[0])
            Gm[next_edge[2]][next_edge[3]]['time']=edge_count
            total_length += next_edge[0]
            print next_edge[1]
        else:
            check = 1

    return Gm

def model_3pa(G, a):

    #starting: tree creation
    Gm = min_distances_tree(G)

    #sorted distances list creation
    D_list = []
    for n1 in Gm.nodes():
        for n2 in Gm.nodes():
            if n1 != n2:
                dist = real_distance(Gm, n1, n2)
                D_list += [(dist, n1, n2)]
    #D_list=sorted(D_list)

    #total link length of G
    edges_limit = 0
    for edge in G.edges():
        edges_limit += G.edge[edge[0]][edge[1]]['weight']

    #total link length of Gm
    total_length = 0
    for edge in Gm.edges():
        total_length += Gm.edge[edge[0]][edge[1]]['weight']

    print total_length, edges_limit

    #stop when adding a new links increases the difference between the total link length of G and Gm
    check = 0
    while check == 0:
        #look for the next link (the one with the minimum ratio)
        ratio = 2000000
        for item in D_list:
            dist = float(item[0])
            node1 = item[1]
            node2 = item[2]
            path = nx.shortest_path_length(Gm, node1, node2, weight='weight')
            par = dist / (float(path) * Gm.degree(node1, weight='weight') ** a)
            if par < ratio:
                ratio = par
                next_edge = (dist, ratio, node1, node2)
        if node1 in Gm.neighbors(node2):
            print "ALARM!", next_edge
        #check if it has to add a new link
        if abs((total_length + next_edge[0]) - edges_limit) < abs(total_length - edges_limit):
            Gm.add_edge(next_edge[2], next_edge[3], weight=next_edge[0])
            total_length += next_edge[0]
            #print next_edge, total_length, edges_limit
        else:
            check = 1

    return Gm
