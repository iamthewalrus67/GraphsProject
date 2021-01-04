'''
Module for checking if two graphs are isomorphic.
'''

from graphs import get_adjancy_matrix


def num_vertices(graph1: list, graph2: list):
    """
    Checks for number of vertices
    >>> num_vertices([[1, 1], [1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    False
    >>> num_vertices([[1, 0], [0, 1]], [[0, 0], [0, 0]])
    True
    """
    if len(graph1[0]) != len(graph2[0]):
        return False
    return True


def num_edges(graph1: list, graph2: list):
    """
    Checks for number of edges
    >>> num_edges([[1, 1], [0, 1]], [[1, 1], [1, 1]])
    False
    >>> num_edges([[1, 0], [0, 1]], [[0, 1], [1, 0]])
    True
    """
    check1 = 0
    check2 = 0
    for row, _ in enumerate(graph1):
        for column, _ in enumerate(graph1[row]):
            if graph1[row][column] == 1:
                check1 += 1
            if graph2[row][column] == 1:
                check2 += 1
    return check1 == check2


def vertices_degree(graph1: list, graph2: list):
    """
    Checks for vertices' degrees
    >>> vertices_degree([[1, 0], [1, 1]], [[0, 1], [1, 0]])
    (False, [])
    >>> vertices_degree([[1, 1], [0, 1]], [[1, 0], [1, 1]])
    (True, [2, 1], [1, 2])
    """
    check1 = []
    check2 = []
    for row, _ in enumerate(graph1):
        degree1 = 0
        degree2 = 0
        for column, _ in enumerate(graph1[row]):
            if graph1[row][column] == 1:
                degree1 += 1
            if graph2[row][column] == 1:
                degree2 += 1
        check1.append(degree1)
        check2.append(degree2)
    if sorted(check1) == sorted(check2):
        return True, check1, check2
    return False, []


def permutations(graph1: list, graph2: list, degrees: tuple):
    """
    Checks if there can be bijection between two graphs
    """
    degrees1 = degrees[0]
    degrees2 = degrees[1]
    check1 = []
    check2 = []
    for index, _ in enumerate(degrees1):
        degree = degrees1[index]
        temp = []
        for vertex, _ in enumerate(graph1[index]):
            if graph1[index][vertex] == 1:
                temp.append(degrees1[vertex])
        check1.append((degree, tuple(sorted(temp))))

    for index, _ in enumerate(degrees2):
        degree = degrees2[index]
        temp = []
        for vertex in range(len(graph2[index])):
            if graph2[index][vertex] == 1:
                temp.append(degrees2[vertex])
        check2.append((degree, tuple(sorted(temp))))

    return len(set(check1 + check2)) == len(set(check1))


def check_for_isomorphism(graph1: list, graph2: list, directed=False) -> bool:
    """
    Main function for checking isomorphism
    >>> check_for_isomorphism([(1, 2), (1, 3), (1, 5),\
    (2, 4), (2, 6), (3, 1), (3, 4),\
    (4, 2), (5, 1), (5, 6), (5, 7), (6, 8), (7, 8)],\
    [(1, 2), (1, 3), (1, 5), (2, 4), (3, 1), (3, 4),\
    (3, 7), (4, 2), (5, 6), (5, 7), (6, 8), (7, 8)])
    True
    >>> check_for_isomorphism([(1, 3), (1, 5),\
    (2, 4), (2, 6), (3, 1), (3, 4),\
    (4, 2), (5, 1), (5, 6), (5, 7), (6, 8), (7, 8)],\
    [(1, 2), (1, 3), (1, 5), (2, 4), (3, 1), (3, 4),\
    (3, 7), (4, 2), (5, 6), (5, 7), (6, 8), (7, 8)])
    False
    """
    matrix1 = get_adjancy_matrix(graph1, directed)
    matrix2 = get_adjancy_matrix(graph2, directed)

    if num_vertices(matrix1, matrix2):
        if num_edges(matrix1, matrix2):
            degrees = vertices_degree(matrix1, matrix2)
            if degrees[0]:
                return permutations(matrix1, matrix2, degrees[1:])
    return False
