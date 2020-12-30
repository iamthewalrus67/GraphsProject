def read_graph_from_file(path):
    edges = []
    with open(path, 'r') as vertices:
        for vertex in vertices:
            edge = vertex.strip().split(',')
            edges.append(tuple(edge))
    return edges
