'''
Module for working with graphs.

Functions:
read_graph_from_file: get graph edges from file.
get_adjancy_matrix: get adjancy matrix for given graph.
bipartite_check: checks whether graph is bipartite.
hamiltonian_cycle: find Hamiltonian cycle in graph. 
'''


def read_graph_from_file(path: str) -> list:
    '''
    Read graph from csv file and return list of its edges.
    '''
    edges = []
    with open(path, 'r') as vertices:
        for vertex in vertices:
            edge = vertex.strip().split(',')
            edges.append(tuple(edge))
    return edges


def get_adjancy_matrix(graph: list, directed=False) -> list:
    '''
    Return adjancy matrix for given graph.

    >>> get_adjancy_matrix([(5,1), (1,1), (2,1), (3,2), (4,5), (1,2), (5,5)])
    [[1, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [1, 0, 0, 1, 1]]
    >>> get_adjancy_matrix([(5,1), (1,1), (2,1), (3,2), (4,5), (1,2), (5,5)], True)
    [[1, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 1]]
    '''
    # Find unique vertices in graph
    vertices = get_vertices(graph)

    # Create empty matrix
    matrix = [[0] * len(vertices) for _ in vertices]

    # Fill in matrix
    for edge in graph:
        pos1 = vertices.index(edge[0])
        pos2 = vertices.index(edge[1])
        if directed:
            matrix[pos1][pos2] = 1
        else:
            matrix[pos1][pos2] = 1
            matrix[pos2][pos1] = 1

    return matrix


def get_vertices(graph: list) -> list:
    '''
    Return unique vertices of graph.

    >>> get_vertices([(1, 2), (2, 1), (3, 1)])
    [1, 2, 3]
    >>> get_vertices([])
    []
    '''
    vertices = []
    for edge in graph:
        for vertex in edge:
            if vertex not in vertices:
                vertices.append(vertex)

    return sorted(vertices)


def is_vertex_valid(vertex, position: int, path: list, matrix: list, vertices: list) -> bool:
    '''
    Check if vertex can be placed in path.
    '''
    # Check if vertex is already in path
    if vertex in path:
        return False

    # Check if edge exists
    if matrix[vertices.index(path[position-1])][vertices.index(vertex)] == 0:
        return False

    return True


def hamiltonian_util(position: int, path: list, matrix: list, vertices: list) -> list:
    '''
    Recursive utility function for finding Hamiltonian cycle.
    Return Hamiltonian cycle if it exists and [] if it doesn't.
    '''
    # Check if all vertices are in path
    if position == len(vertices):
        if matrix[vertices.index(path[position-1])][vertices.index(path[0])] == 1:
            return True
        return False

    for vertex in vertices:
        if is_vertex_valid(vertex, position, path, matrix, vertices):
            path[position] = vertex

            if hamiltonian_util(position+1, path, matrix, vertices):
                return path + [path[0]]

            # Remove current vertex if it didn't lead to result
            path[position] = -1

    return False


def hamiltonian_cycle(graph: list, directed=False) -> list:
    '''
    Return Hamiltonian cycle if it exists and empty list if it doesn't.

    >>> hamiltonian_cycle([(1, 2), (3, 2), (3, 1)])
    [1, 2, 3, 1]
    >>> hamiltonian_cycle([(1, 2), (3, 2), (3, 1)], directed=True)
    []
    '''
    vertices = get_vertices(graph)
    adjancy_matrix = get_adjancy_matrix(graph, directed)

    path = [-1] * len(vertices)
    path[0] = vertices[0]

    cycle = hamiltonian_util(1, path, adjancy_matrix, vertices)
    if not cycle:
        return []

    return cycle


def bipartite_check(graph: list) -> bool:
    """
    Return True if given graph is bipartite and False if not.

    >>> bipartite_check([(1, 2), (3, 2), (4, 2), (1, 5), (3, 5), (4, 2)])
    False
    >>> bipartite_check([(1, 4), (2, 3), (1, 2), (3, 4)])
    True
    >>> bipartite_check([])
    True
    """
    matrix = get_adjancy_matrix(graph)
    vertices = len(matrix)

    for i in range(vertices):
        # checking diagonals not to contain self-loops
        if matrix[i][i] == 1:
            return False

        edges_amount = 0

        for k in range(vertices):
            # counting amount of edges
            if matrix[i][k] == 1:
                edges_amount = edges_amount + 1
        # checking number of edges and returning False if it is odd
        if edges_amount % 2 != 0:
            return False
    return True
