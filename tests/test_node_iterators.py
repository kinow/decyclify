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


"""Tests for the node_iterators."""

import pytest
from networkx import nx

from decyclify.functions import decyclify
from decyclify.node_iterators import CycleIterator, TasksIterator


def test_cycle_iterator_type_error():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        CycleIterator(10)

def test_cycle_iterators():
    graph = nx.DiGraph()
    graph.add_edge('a', 'b')
    graph.add_edge('a', 'e')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'b')
    graph.add_edge('c', 'd')

    graph, cycles_removed = decyclify(graph, 'a')

    iterator = CycleIterator(graph)

    expected = [['a.0'], ['b.0', 'e.0'], ['c.0'], ['d.0'], ['a.1'], ['b.1', 'e.1'], ['c.1'], ['d.1']]
    iterated = []

    for index, node in enumerate(iterator):
        iterated.append(node)
        if index == 7:
            break

    assert iterated == expected

def test_tasks_iterator():
    graph = nx.DiGraph()
    graph.add_edge('a', 'b')
    graph.add_edge('a', 'e')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'b')
    graph.add_edge('c', 'd')

    graph, cycles_removed = decyclify(graph, 'a')

    iterator = TasksIterator(graph)

    expected = []
    iterated = []

    # TODO: use iterator

    assert iterated == expected
