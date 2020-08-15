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


def test_graph_creation():
    graph = nx.DiGraph()
    graph.add_edge('a', 'b')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'b')
    graph.add_edge('c', 'd')
    print()
    g = decyclify_networkx(graph)
    print_matrix(g, graph.nodes, True)
    print(graph.adj)


@pytest.mark.parametrize('exc, args', [
    (TypeError, ['string', 1]),
    (TypeError, [["a b"], 'string']),
    (TypeError, [None, 1]),
    (TypeError, [["a b"], None]),
    (ValueError, [["a b"], 0])
])
def test_decyclify_invalid_args(exc, args):
    with pytest.raises(exc):
        decyclify(*args)


@pytest.mark.parametrize('exc, args', [
    (TypeError, ['string', 1]),
    (TypeError, [nx.DiGraph({'a': {'b': {}}}), 'string']),
    (TypeError, [None, 1]),
    (TypeError, [nx.DiGraph({'a': {'b': {}}}), None]),
    (ValueError, [nx.DiGraph({'a': {'b': {}}}), 0])
])
def test_decyclify_networkx_invalid_args(exc, args):
    with pytest.raises(exc):
        decyclify_networkx(*args)


def test_empty_graph():
    g = decyclify([])
    assert isinstance(g, Iterable)


@pytest.mark.parametrize('n, graph_string', [
    (2, ['a b']),
    (3, ['a b', 'b c']),
    (4, ['a b', 'b c', 'c d']),
    (10, ['a b', 'b c', 'c d', 'd e', 'e f', 'f g', 'g h', 'h i', 'i j'])
])
def test_decyclify_matrix_dimensions(n, graph_string):
    g = decyclify(graph_string)
    assert len(g[0]) == n
    assert len(g[1]) == n


def test_print_matrix(capsys):
    graph = nx.DiGraph()
    graph.add_edge('a', 'd')
    graph.add_edge('d', 'b')
    graph.add_edge('d', 'c')
    graph.add_edge('b', 'd')
    graph.add_edge('c', 'a')
    g = decyclify_networkx(graph)
    print_matrix(g, graph.nodes)
    out, _ = capsys.readouterr()
    assert '[-1 -1 -1 -1]' in out


def test_print_matrix_tabulate(capsys):
    graph = nx.DiGraph()
    graph.add_edge('a', 'd')
    graph.add_edge('d', 'b')
    graph.add_edge('d', 'c')
    graph.add_edge('b', 'd')
    graph.add_edge('c', 'a')
    g = decyclify_networkx(graph)
    print_matrix(g, graph.nodes, tabulate=True)
    out, _ = capsys.readouterr()
    assert 'a   d   b   c' in out
