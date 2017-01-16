
def true_model(G):
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
