'''
Module for printing Eulerian circuit.
'''

from graphs import get_adjancy_matrix


def to_edge_dict(edge_list: list) -> dict:
    """
    Converts a graph from tuples of edges to dictionary of vertices.

    >>> to_edge_dict([(1,2), (3,4), (1,5), (2,4)])
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


def dfs(vertex1, graph, visited_edge, path=None):
    """
    Uses dfs for finding eulerian path traversal.
    """
    if path is None:
        path = []

    path = path + [vertex1]
    for vertex2 in graph[vertex1]:
        if visited_edge[vertex1][vertex2] is False:
            visited_edge[vertex1][vertex2], visited_edge[vertex2][vertex1] = True, True
            path = dfs(vertex2, graph, visited_edge, path)
    return path


def check_euler(graph, max_node=10):
    """
    Prints the Eulerian circuit or the message about its absence.

    >>> check_euler([(1, 2), (1, 3), (1, 4), (2, 3), (4, 5)])
    graph doesn't have an Eulerian circuit
    >>> check_euler([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (4, 5)])
    [1, 2, 3, 1, 4, 5, 1]
    >>> check_euler([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 5)])
    graph doesn't have an Eulerian circuit
    >>> check_euler([(1, 2), (1, 3), (2, 3)])
    [1, 2, 3, 1]
    """
    graph = to_edge_dict(graph)
    visited_edge = [[False for _ in range(max_node + 1)]
                    for _ in range(max_node + 1)]
    odd_degree_nodes = 0
    start_node = 1
    for i in range(max_node):
        if i not in graph.keys():
            continue
        if len(graph[i]) % 2 == 1:
            odd_degree_nodes += 1
    if odd_degree_nodes == 0:
        path = dfs(start_node, graph, visited_edge)
        print(path)
    else:
        print("graph doesn't have an Eulerian circuit")
