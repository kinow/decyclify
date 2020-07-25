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

from collections import Iterable

import networkx as nx
import pytest

from decyclify.functions import decyclify, decyclify_networkx


def test_graph_creation():
    graph = nx.DiGraph()
    graph.add_edge('a', 'd')
    graph.add_edge('d', 'b')
    graph.add_edge('d', 'c')
    graph.add_edge('b', 'd')
    graph.add_edge('c', 'a')
    print()
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
