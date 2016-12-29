


def global_efficiency(G):
    import networkx as nx
    from utilities import real_distance
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
