# Copyright 2020 Bruno P. Kinoshita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import Iterable
from typing import List, Tuple, Union

import numpy as np
from networkx import DiGraph
from networkx.algorithms.cycles import simple_cycles
from networkx.readwrite.edgelist import parse_edgelist
from tabulate import tabulate as tabulate_fn


def _cycle_exists(cycles: List, from_node: object, to_node: object):
    for cycle in cycles:
        # is the to_node at the end of the cycle (target)?, and,
        # is the other node one of the source nodes?
        if cycles[-1] == to_node and from_node in cycle:
            return True
    return False


def _dfs_visit(graph, node):
    graph.nodes[node]['color'] = 'gray'
    for vertex in graph.adj.copy().get(node):
        vertex_color = graph.nodes[vertex]['color']
        if vertex_color == 'white':
            # recursive call
            _dfs_visit(graph, vertex)
        elif vertex_color == 'gray':
            # remove back link
            graph.remove_edge(node, vertex)
    graph.nodes[node]['color'] = 'black'

def decyclify(graph: Union[List, DiGraph], start_node: object=None, number_of_cycles: int=1):
    """
    Remove cycle edges from a graph.

    :param graph: a networkx object representing the input graph
    :type graph: Union[List, DiGraph]
    :param start_node: start node
    :type start_node: object
    :param number_of_cycles: number of cycles to be generated
    :type number_of_cycles: int
    :return: a DCG that is iterable and contains multiple cycles, each cycle with a single DAG
    :rtype: Tuple[np.ndarray, np.ndarray]
    """
    if not isinstance(graph, DiGraph) and not isinstance(graph, List):
        raise TypeError(f"Graph must be a List or a networkx.DiGraph, but '{type(graph)}' given")
    if not isinstance(number_of_cycles, int):
        raise TypeError(f"Number of cycles must be an integer, but '{type(number_of_cycles)}' given")
    if number_of_cycles < 1:
        raise ValueError(f"Number of cycles must be at least '1', but '{number_of_cycles}' given")

    if isinstance(graph, List):
        graph = parse_edgelist(graph, create_using=DiGraph)

    graph = graph.copy()

    nodes = graph.nodes
    # color as vertices white
    for node in nodes:
        graph.nodes[node]['color'] = 'white'

    if start_node is None:
        # TODO: handle empty graph
        start_node = list(nodes.keys())[0]

    print(*graph.nodes.items())
    print(graph.edges)
    _dfs_visit(graph, start_node)
    print(*graph.nodes.items())
    print(graph.edges)

    number_of_nodes = len(nodes)
    cycles: list = list(simple_cycles(graph))

    # create matrix filled with -1's
    matrix_intraiteration = np.full((number_of_nodes, number_of_nodes), 0)
    matrix_interiteration = np.full((number_of_nodes, number_of_nodes), 0)

    for i, node_1 in enumerate(nodes):
        for j, node_2 in enumerate(nodes):
            # ignore diagonal (same node)
            if i == j:
                continue
            node_2_adjacent_nodes = graph.adj.get(node_2)
            if node_1 in node_2_adjacent_nodes:
                # here we have two adjacent nodes, they could be either
                # cyclic or acyclic; the only way to tell which one we
                # have, is by looking at the list of simple cycles
                #
                # note that the original paper had its own algorithm
                # for coloring nodes and removing back-edges, but it
                # was simpler to use networkx for now
                if _cycle_exists(cycles, from_node=node_2, to_node=node_1):
                    # add to matrix C
                    matrix_interiteration.itemset((i, j), 1)
                else:
                    # add to matrix D
                    matrix_intraiteration.itemset((i, j), 1)

    return matrix_intraiteration, matrix_interiteration

def create_matrices(graph: Union[DiGraph, List]):
    if not isinstance(graph, DiGraph) and not isinstance(graph, List):
        raise TypeError(f"Graph must be a List or a networkx.DiGraph, but '{type(graph)}' given")

    if isinstance(graph, List):
        graph = parse_edgelist(graph, create_using=DiGraph)

    nodes = graph.nodes
    number_of_nodes = len(nodes)
    adjacent_nodes: dict = graph.adj
    cycles: list = list(simple_cycles(graph))

    # create matrix filled with -1's
    matrix_intraiteration = np.full((number_of_nodes, number_of_nodes), 0)
    matrix_interiteration = np.full((number_of_nodes, number_of_nodes), 0)

    for i, node_1 in enumerate(nodes):
        for j, node_2 in enumerate(nodes):
            # ignore diagonal (same node)
            if i == j:
                continue
            node_2_adjacent_nodes = adjacent_nodes.get(node_2)
            if node_1 in node_2_adjacent_nodes:
                # here we have two adjacent nodes, they could be either
                # cyclic or acyclic; the only way to tell which one we
                # have, is by looking at the list of simple cycles
                #
                # note that the original paper had its own algorithm
                # for coloring nodes and removing back-edges, but it
                # was simpler to use networkx for now
                if _cycle_exists(cycles, from_node=node_2, to_node=node_1):
                    # add to matrix C
                    matrix_interiteration.itemset((i, j), 1)
                else:
                    # add to matrix D
                    matrix_intraiteration.itemset((i, j), 1)

    return matrix_intraiteration, matrix_interiteration

def print_matrix(matrix: np.ndarray, nodes: Iterable, tabulate: bool = False) -> None:
    """
    Print the matrix tabulated.
    :param matrix:
    :param nodes:
    :param tabulate:
    """
    if tabulate:
        # copy the original data
        # change type to object so we can prepend columns with strings
        matrix_copy = np.array(matrix, copy=True).astype(dtype=object)

        # add a header row with the nodes
        matrix_copy = np.vstack((nodes, matrix_copy))

        # add a header column with the nodes (compensate for new header row with an empty space)
        matrix_copy = np.insert(matrix_copy, 0, np.concatenate(([' '], nodes)), axis=1)

        print(tabulate_fn(matrix_copy))
    else:
        print(matrix)
