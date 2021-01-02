'''
Module for working with graphs.

Functions:
read_graph_from_file: get graph edges from file.
get_adjancy_matrix: get adjancy matrix for given graph.
bipartite_check: checks whether graph is bipartite.
hamiltonian_cycle: find Hamiltonian cycle in graph.
colour_graph: find colours of vertices if colouring of graph in 3 colours is possible.
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
    colorArr = [-1] * vertices
    colorArr[0] = 1
    queue = []
    queue.append(0)
    while queue:
        u = queue.pop()
        if matrix[u][u] == 1:
            return False
        for v in range(vertices):
            if matrix[u][v] == 1 and colorArr[v] == -1:
                colorArr[v] = 1 - colorArr[u]
                queue.append(v)
            elif matrix[u][v] == 1 and colorArr[v] == colorArr[u]:
                return False
    return True


def check_colour_of_vertex(matrix: list, vertex: int, list_colours: list,
                           colour: int, number_of_vertices: int) -> bool:
    """
    Return True if vertex can be coloured in colour. Else return False.
    >>> check_colour_of_vertex([[0, 1, 1, 1], [1, 0, 0, 1],\
        [1, 0, 0, 1], [1, 1, 1, 0]], 3, [1, 2, 2, 0], 2, 4)
    False
    >>> check_colour_of_vertex([[0, 1, 1, 1], [1, 0, 0, 1],\
        [1, 0, 0, 1], [1, 1, 1, 0]], 3, [1, 2, 2, 0], 3, 4)
    True
    """
    for second_vertex in range(number_of_vertices):
        if matrix[vertex][second_vertex] == 1 and colour == list_colours[second_vertex]:
            return False
    return True


def colour_vertex(matrix: list, number_of_colours: int, list_colours: list,
                  vertex: int, number_of_vertices: int) -> bool:
    """
    Return True if colouring in number_of_colours colours is possible. Else return False.
    >>> colour_vertex([[0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1],\
        [1, 1, 1, 0]], 3, [0, 0, 0, 0], 0, 4)
    True
    >>> colour_vertex([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1],\
        [1, 1, 1, 0]], 3, [0, 0, 0, 0], 0, 4)
    False
    """
    if vertex == number_of_vertices:
        return True
    for colour in range(1, number_of_colours+1):
        if check_colour_of_vertex(matrix, vertex, list_colours, colour, number_of_vertices):
            list_colours[vertex] = colour
            if colour_vertex(matrix, number_of_colours, list_colours, vertex+1, number_of_vertices):
                return True
            list_colours[vertex] = 0
    return False


def colour_graph(matrix: list, vertices: list) -> dict:
    """
    Return list with tuples (vertex of graph, colour) if colouring
    in 3 colours is possible. Else return message about impossibility.
    >>> colour_graph([[0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0]], ['a', 'b', 'c', 'd'])
    [('a', 1), ('b', 2), ('c', 2), ('d', 3)]
    >>> colour_graph([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], ['a', 'b', 'c', 'd'])
    'Colouring in 3 colours is impossible.'
    >>> colour_graph([[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1],\
        [1, 1, 1, 0, 0], [1, 1, 1, 0, 0]], [1, 2, 3, 4, 5])
    [(1, 1), (2, 1), (3, 1), (4, 2), (5, 3)]
    >>> colour_graph([[0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [0, 1, 0, 1, 0],\
        [1, 1, 0, 1, 1], [1, 0, 0, 1, 0]], [1, 2, 3, 4, 5])
    [(1, 1), (2, 2), (3, 1), (4, 3), (5, 2)]
    >>> colour_graph([\
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],\
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],\
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],\
        [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],\
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],\
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],\
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],\
        [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0],\
        [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],\
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],\
        [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]\
    ], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    [(1, 1), (2, 1), (3, 2), (4, 2), (5, 1), (6, 3),\
 (7, 3), (8, 3), (9, 1), (10, 3), (11, 2), (12, 2)]
    >>> colour_graph([[0, 1], [1, 0]], ['a', 'b'])
    'Colouring in 3 colours is impossible.'
    """
    number_of_colours = 3
    number_of_vertices = len(matrix)
    if number_of_vertices < 3:
        return "Colouring in 3 colours is impossible."
    list_colours = [0] * number_of_vertices
    if not colour_vertex(matrix, number_of_colours, list_colours, 0, number_of_vertices):
        return "Colouring in 3 colours is impossible."
    check_used_colours = len(set(list_colours))
    if check_used_colours == 2:
        list_colours[-1] = 3
    list_vertex_colour = [(name_of_vertex, list_colours[index])
                          for index, name_of_vertex in enumerate(vertices)]
    return list_vertex_colour
