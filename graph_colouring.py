'''
Module for checking if graph can be coloured in 3 colours.
'''

from graphs import get_adjancy_matrix, get_vertices


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


def colour_graph(graph: list) -> dict:
    """
    Return list with tuples (vertex of graph, colour) if colouring
    in 3 colours is possible. Else return message about impossibility.
    >>> colour_graph([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'd'), ('c', 'd')])
    [('a', 1), ('b', 2), ('c', 2), ('d', 3)]
    >>> colour_graph([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')])
    'Colouring in 3 colours is impossible.'
    >>> colour_graph([(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)])
    [(1, 1), (2, 1), (3, 1), (4, 2), (5, 3)]
    >>> colour_graph([(1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (3, 4), (4, 5)])
    [(1, 1), (2, 2), (3, 1), (4, 3), (5, 2)]
    >>> colour_graph([('a', 'b')])
    'Colouring in 3 colours is impossible.'
    """
    matrix = get_adjancy_matrix(graph)
    vertices = get_vertices(graph)
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
