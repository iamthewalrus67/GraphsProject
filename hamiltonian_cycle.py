'''
Module for finding Hamiltonian cycle in graphs.
'''

from graphs import get_adjancy_matrix, get_vertices


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


def find_hamiltonian_cycle(graph: list, directed=False) -> list:
    '''
    Return Hamiltonian cycle if it exists and empty list if it doesn't.

    >>> find_hamiltonian_cycle([(1, 2), (3, 2), (3, 1)])
    [1, 2, 3, 1]
    >>> find_hamiltonian_cycle([(1, 2), (3, 2), (3, 1)], directed=True)
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
