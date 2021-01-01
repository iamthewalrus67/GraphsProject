'''
Module for working with graphs.

Functions:
read_graph_from_file: get graph edges from file.
get_adjancy_matrix: get adjancy matrix for given graph.
bipartite_check: checks whether graph is bipartite.
'''

from typing import List, Tuple


def read_graph_from_file(path: str) -> List[Tuple[str, str]]:
    '''
    Read graph from csv file and return list of its edges.
    '''
    edges = []
    with open(path, 'r') as vertices:
        for vertex in vertices:
            edge = vertex.strip().split(',')
            edges.append(tuple(edge))
    return edges


def get_adjancy_matrix(graph: List[Tuple[object, object]], directed=False) -> List[List[int]]:
    '''
    Return adjancy matrix for given graph.

    >>> get_adjancy_matrix([(5,1), (1,1), (2,1), (3,2), (4,5), (1,2), (5,5)])
    [[1, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [1, 0, 0, 1, 1]]
    >>> get_adjancy_matrix([(5,1), (1,1), (2,1), (3,2), (4,5), (1,2), (5,5)], True)
    [[1, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 1]]
    '''
    # Find unique vertices in graph
    vertices = []
    for edge in graph:
        for vertex in edge:
            if vertex not in vertices:
                vertices.append(vertex)

    vertices.sort()

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


def bipartite_check(matrix: list) -> bool:
    """
    Return True if given graph is bipartite and False if not.

    >>> bipartite_check([[1, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0],\
 [0, 0, 0, 0, 1], [1, 0, 0, 0, 1]])
    False
    >>> bipartite_check([[0, 1, 0, 0, 1], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1],\
 [0, 1, 0, 0, 1], [1, 0, 1, 0, 0]])
    True
    >>> bipartite_check([])
    True
    """

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
