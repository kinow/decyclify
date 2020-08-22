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


"""
Tests for `decyclify.functions`.
"""

import networkx as nx
import pytest

from decyclify.functions import *
from collections.abc import Iterable


def test_graph_creation():
    graph = nx.DiGraph()
    graph.add_edge('a', 'b')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'b')
    graph.add_edge('c', 'd')
    # graph.add_edge('d', 'c')
    print()

    graph, cycles_removed = decyclify(graph, 'a')

    d = create_intraiteration_matrix(graph)
    print_matrix(d, graph.nodes, True)

    c = create_interiteration_matrix(graph.nodes, cycles_removed)
    print_matrix(c, graph.nodes, True)

# --- decyclify

def test_empty_graph():
    g = decyclify([])
    assert isinstance(g, Iterable)


def test_invalid_type_decyclify():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        decyclify(10)

# --- intraiteration

@pytest.mark.parametrize('n, graph_string', [
    (2, ['a b']),
    (3, ['a b', 'b c']),
    (4, ['a b', 'b c', 'c d']),
    (10, ['a b', 'b c', 'c d', 'd e', 'e f', 'f g', 'g h', 'h i', 'i j'])
])
def test_create_matrices_matrix_dimensions(n, graph_string):
    g = create_intraiteration_matrix(graph_string)
    assert len(g[0]) == n
    assert len(g[1]) == n


def test_print_matrix(capsys):
    graph = nx.DiGraph()
    graph.add_edge('a', 'd')
    graph.add_edge('d', 'b')
    graph.add_edge('d', 'c')
    graph.add_edge('b', 'd')
    graph.add_edge('c', 'a')
    intra = create_intraiteration_matrix(graph)
    print_matrix(intra, graph.nodes)
    out, _ = capsys.readouterr()
    assert '[-1 -1 -1 -1]' not in out
    assert '[0 0 0 0]' not in out # A


def test_print_intra_matrix_tabulate(capsys):
    graph = nx.DiGraph()
    graph.add_edge('a', 'd')
    graph.add_edge('d', 'b')
    graph.add_edge('d', 'c')
    graph.add_edge('b', 'd')
    graph.add_edge('c', 'a')
    intra = create_intraiteration_matrix(graph)
    print_matrix(intra, graph.nodes, tabulate=True)
    out, _ = capsys.readouterr()
    # have only one white space between letters
    out = ' '.join(out.split())
    assert '' in out

# --- interiteration
