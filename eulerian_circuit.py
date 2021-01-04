'''
Module for printing Eulerian circuit.
'''

from graphs import get_adjancy_matrix


def convert_to_dict(edge_list: list) -> dict:
    """
    Converts a graph from tuples of edges to dictionary of vertices.

    >>> convert_to_dict([(1,2), (3,4), (1,5), (2,4)])
    {1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}
    """
    result = {}
    for each in edge_list:
        if each[0] not in result:
            result[each[0]] = [each[1]]
        else:
            result[each[0]].append(each[1])
        if each[1] not in result:
            result[each[1]] = [each[0]]
        else:
            result[each[1]].append(each[0])

    for key in result:
        result[key].sort()

    return result


def deep_first_search(vertex1, graph, visited_edge, path=None):
    """
    Uses deep first search for finding eulerian path traversal.
    """
    if path is None:
        path = []

    path = path + [vertex1]
    for vertex2 in graph[vertex1]:
        if not visited_edge[vertex1][vertex2]:
            graph[vertex1].remove(vertex2)
            graph[vertex2].remove(vertex1)
            visited_edge[vertex1][vertex2], visited_edge[vertex2][vertex1] = True, True
            path = deep_first_search(vertex2, graph, visited_edge, path)
    return path


def print_euler_circuit(graph):
    """
    Prints the Eulerian circuit or the message about its absence.
    >>> print_euler_circuit([(1, 2), (1, 3), (1, 4), (2, 3), (4, 5)])
    graph doesn't have an Eulerian circuit
    >>> print_euler_circuit([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (4, 5)])
    [1, 2, 3, 1, 4, 5, 1]
    >>> print_euler_circuit([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 5)])
    graph doesn't have an Eulerian circuit
    >>> print_euler_circuit([(1, 2), (1, 3), (2, 3)])
    [1, 2, 3, 1]
    """
    graph = convert_to_dict(graph)
    count_vertices = len(graph)
    visited_edge = [[False for _ in range(count_vertices + 1)]
                    for _ in range(count_vertices + 1)]

    starting_node = 1
    for i in graph:
        if len(graph[i]) % 2 == 1:
            print("graph doesn't have an Eulerian circuit")
            return

    path = deep_first_search(starting_node, graph, visited_edge)
    print(path)
    return
