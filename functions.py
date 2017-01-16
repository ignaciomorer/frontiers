
def real_distance(G,node1,node2):
    from math import sin, cos, radians, asin, sqrt
    lon0=G.node[node1]['longitude']
    lat0=G.node[node1]['latitude']
    lon1=G.node[node2]['longitude']
    lat1=G.node[node2]['latitude']
    lon0, lat0, lon1, lat1 = map(radians, [lon0, lat0, lon1, lat1])
    # haversine formula
    dlon = lon1 - lon0
    dlat = lat1 - lat0
    a = sin(dlat/2)**2 + cos(lat0) * cos(lat1) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # 6367 is the radius of the Earth
    km = 6367 * c
    return km

def distance_matrix(G):
    D = []
    for i in range(len(G.nodes())):
        D+=[[]]
        for j in range(len(G.nodes())):
            if i==j:
                d= 0
            else:
                d = real_distance(G,G.nodes()[i],G.nodes()[j])
            D[i]+=[(d,j)]
            #D[i]+=[d]
    return D

def min_distances_tree(G):
    import networkx as nx
    Gm=G.copy()
    Gm.remove_edges_from(G.edges())
    D=distance_matrix(Gm)
    D_list=[]
    for i in range(len(D)):
        j = 0
        while j < i:
            dist=D[i][j]
            D_list +=[(dist,i,j)]
            j += 1

    D_list=sorted(D_list)
    i=0
    edge_count=0
    ncc=nx.number_connected_components(Gm)
    while not ncc==1:
        node1=Gm.nodes()[D_list[i][1]]
        node2=Gm.nodes()[D_list[i][2]]
        if not nx.has_path(Gm,node1,node2):
            d=D_list[i][0][0]
            edge_count+=1
            Gm.add_edge(node1,node2,weight=d,time=edge_count)
            ncc=nx.number_connected_components(Gm)
        i+=1

    return Gm

def global_efficiency(G):
    import networkx as nx
    # Matriz de distancias ordenadas segun lista G.nodes()
    distances=[]
    N=len(G.nodes())
    for i in range(N):
        distances+=[[]]
        for j in range(N):
            node1=G.nodes()[i]
            node2=G.nodes()[j]
            d=real_distance(G,node1,node2)
            distances[i]+=[d]

    # Calculo eficiencia global
    total_global=0
    for i in range(N):
        for j in range(N):
            node1=G.nodes()[i]
            node2=G.nodes()[j]
            if i != j and nx.has_path(G,node1,node2):
                path=float(nx.shortest_path_length(G,node1,node2,weight='weight'))
                total_global+=(distances[i][j])/path
    global_eff= round(total_global/float(N*(N-1)),5)
    return global_eff


def local_efficiency(G):
    import networkx as nx
    # Matriz de distancias ordenadas segun lista G.nodes()
    distances=[]
    N=len(G.nodes())
    for i in range(N):
        distances+=[[]]
        for j in range(N):
            node1=G.nodes()[i]
            node2=G.nodes()[j]
            d=real_distance(G,node1,node2)
            distances[i]+=[d]
    # Calculo eficiencia local
    total_local=0
    for i in range(N):
        # Copia del grafo sin nodo i
        G2 = G.copy()
        G2.remove_node(G.nodes()[i])
        subtotal=0
        # Set de vecinos
        neighbors=nx.neighbors(G,G.nodes()[i])
        deg=len(neighbors)
        # Grado <= 1 no contribuye a la eficiencia -> saltar step
        if deg <=1:
            continue
        for j in range(deg):
            node1=neighbors[j]
            index1=G.nodes().index(node1)
            k=deg-1
            while k != j:
                node2=neighbors[k]
                index2=G.nodes().index(node2)
                #print node1, node2
                # Solo contribuye a la eficiencia si hay camino
                if nx.has_path(G2,node1,node2):
                    distance=distances[index1][index2]
                    path=float(nx.shortest_path_length(G2,node1,node2,weight='weight'))
                    #print distance/path
                    subtotal+= distance/path
                k-=1
        # Se divide por parejas de vecinos

        total_local+=subtotal*2/(deg*(deg-1))

    local_eff=round(total_local/float(N),5)
    return local_eff
