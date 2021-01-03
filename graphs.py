'''
Module for working with graphs.

Functions:
read_graph_from_file: get graph edges from file.
get_adjancy_matrix: get adjancy matrix for given graph.
get_vertices: get unique vertices from graph.
hamiltonian_cycle: find Hamiltonian cycle in graph.
bipartite_check: checks whether graph is bipartite.
colour_graph: find colours of vertices if colouring of graph in 3 colours is possible.
check_euler: print Eularian circuit if it exists.
check_for_isomorphism: check if two graphs are isomorphic.
'''


def read_graph_from_file(path: str) -> list:
    '''
    Read graph from csv file and return list of its edges.
    '''
    edges = []
    with open(path, 'r') as vertices:
        for vertex in vertices:
            edge = vertex.strip().split(' ')
            edge = [int(i) for i in edge]
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


# Functions for finding Hamiltonian cycle in graph

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


# Function for checking if graph is bipartite

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


# Functions for graph colouring

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


# Functions for printing eulerian circuit

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


# Functions for checking if two graphs are isomorphic

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
