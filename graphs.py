'''
Module for working with graphs.

Functions:
read_graph_from_file: get graph edges from file.
get_adjancy_matrix: get adjancy matrix for given graph.
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
