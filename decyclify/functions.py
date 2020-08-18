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

from collections.abc import Iterable
from typing import List, Union, Tuple

import numpy as np
from networkx import DiGraph
from networkx.readwrite.edgelist import parse_edgelist
from tabulate import tabulate as tabulate_fn


def _dfs_visit(graph, cycles_detected: List[Tuple[str, str]], start_node: str) -> None:
    """
    DFS-Visit as implemented in the paper. Some extra parameters are passed here to use convenient functions from
    networkx.

    Will start visiting the ``start_node``, changing its color from 'white' to 'gray'.

    Then will iterate over the ``start_node`` adjacent nodes. For each node, if its color is
    'white', it recurse passing the new node as ``start_node``.

    Otherwise, if the node in the iteration is `gray`, it means that the node has already been
    visited, then we must have a back link from ``start_node`` to the new node.

    Back links are removed, removing any cycles, so the graph is decyclified.

    The final step is to change the color of each node visited to 'black', indicating the end of the function.

    :param graph: a directed cyclic or acyclic graph
    :type graph: DiGraph
    :param cycles_detected: initially empty list, populated by this function with each back edge removed
    :type cycles_detected: List[Tuple[str, str]]
    :param start_node: start node
    :type start_node: str
    """
    graph.nodes[start_node]['color'] = 'gray'
    for vertex in graph.adj.copy().get(start_node):
        vertex_color = graph.nodes[vertex]['color']
        if vertex_color == 'white':
            # recursive call
            _dfs_visit(graph, cycles_detected, vertex)
        elif vertex_color == 'gray':
            # remove back link
            cycles_detected.append((start_node, vertex))
            graph.remove_edge(start_node, vertex)
    graph.nodes[start_node]['color'] = 'black'

def decyclify(graph: Union[List, DiGraph], start_node: object=None):
    """
    Remove cycle edges from a graph.

    :param graph: a networkx object representing the input graph
    :type graph: Union[List, DiGraph]
    :param start_node: start node
    :type start_node: object
    :return: a copy of the given graph, but without cycles (i.e. decyclified)
    :rtype: DiGraph
    """
    if not isinstance(graph, DiGraph) and not isinstance(graph, List):
        raise TypeError(f"Graph must be a List or a networkx.DiGraph, but '{type(graph)}' given")

    if isinstance(graph, List):
        graph: DiGraph = parse_edgelist(graph, create_using=DiGraph)

    cycles_detected = []
    graph = graph.copy()

    # empty graph
    if len(graph.nodes) == 0:
        return graph

    nodes = graph.nodes
    # color as vertices white
    for node in nodes:
        graph.nodes[node]['color'] = 'white'

    if start_node is None:
        start_node = list(nodes.keys())[0]

    # start
    _dfs_visit(graph, cycles_detected, start_node)

    # remove edges crossing the iteration frontier
    for edge in graph.edges:
        source = edge[0]
        target = edge[1]
        if graph.nodes[source]['color'] == 'white' and graph.nodes[target]['color'] == 'black':
            graph.remove_edge(source, target)

    # check for uncovered vertices
    for vertex in graph.nodes:
        if graph.nodes[vertex]['color'] == 'white':
            _dfs_visit(graph, cycles_detected, vertex)

    return graph, cycles_detected

def create_intraiteration_matrix(graph: Union[DiGraph, List]):
    """
    :param graph: a DAG
    :return:
    """
    if not isinstance(graph, DiGraph) and not isinstance(graph, List):
        raise TypeError(f"Graph must be a List or a networkx.DiGraph, but '{type(graph)}' given")

    if isinstance(graph, List):
        graph = parse_edgelist(graph, create_using=DiGraph)

    nodes = graph.nodes
    number_of_nodes = len(nodes)
    adjacent_nodes: dict = graph.adj

    # create matrix filled with -1's
    matrix_intraiteration = np.full((number_of_nodes, number_of_nodes), 0)

    for i, node_1 in enumerate(nodes):
        for j, node_2 in enumerate(nodes):
            # ignore diagonal (same node)
            if i == j:
                continue
            node_2_adjacent_nodes = adjacent_nodes.get(node_2)
            if node_1 in node_2_adjacent_nodes:
                # add to matrix D
                matrix_intraiteration.itemset((i, j), 1)

    return matrix_intraiteration

def create_interiteration_matrix(nodes, cycles):
    if not cycles:
        return np.empty([])

    number_of_nodes = len(nodes)

    # create matrix filled with -1's
    matrix_interiteration = np.full((number_of_nodes, number_of_nodes), 0)

    nodes_indices_in_matrix = {
        node: index for index, node in enumerate(nodes)
    }

    for cycle in cycles:
        source = cycle[0]
        target = cycle[1]
        source_index = nodes_indices_in_matrix.get(source)
        target_index = nodes_indices_in_matrix.get(target)
        matrix_interiteration.itemset((target_index, source_index), 1)

    return matrix_interiteration

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

__all__ = [
    'decyclify',
    'create_intraiteration_matrix',
    'create_interiteration_matrix',
    'print_matrix'
]
