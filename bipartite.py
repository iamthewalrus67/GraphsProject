'''
Module for checking if the graph is bipartite.
'''

from graphs import get_adjancy_matrix


def bipartite_check(graph: list) -> bool:
    """
    Return True if given graph is bipartite and False if not.
    >>> bipartite_check([(5, 1), (1, 1), (2, 1), (3, 2), (4, 5), (1, 2), (5, 5)])
    False
    >>> bipartite_check([(1, 2), (1, 4), (2, 1), (2, 3), (3, 2), (3, 4), (4, 1)])
    True
    >>> bipartite_check([(1, 2), (1, 3), (2, 1), (2, 3), (3, 2), (3, 1)]) 
    False
    >>> bipartite_check([])
    True
    """
    if graph == []:
        return True
    matrix = get_adjancy_matrix(graph)
    vertices = len(matrix)
    colors = [-1] * vertices
    colors[0] = 1
    queue = []
    queue.append(0)
    while queue:
        i = queue.pop()
        if matrix[i][i] == 1:
            return False
        for k in range(vertices):
            if matrix[i][k] == 1 and colors[k] == -1:
                colors[k] = 1 - colors[i]
                queue.append(k)
            elif matrix[i][k] == 1 and colors[k] == colors[i]:
                return False
    return True
