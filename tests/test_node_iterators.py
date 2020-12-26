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

from decyclify.functions import decyclify
from decyclify.node_iterators import CycleIterator, TasksIterator

from networkx import DiGraph


@pytest.mark.parametrize('graph,cycles,error', [
    (DiGraph(), None, TypeError),
    (10, 1, TypeError),
    (DiGraph(), -1, ValueError)
])
def test_cycle_iterator_validation_error(graph, cycles, error):
    with pytest.raises(error):
        # noinspection PyTypeChecker
        CycleIterator(graph, cycles)

def test_cycle_iterators(sample_graph):
    graph, cycles_removed = decyclify(sample_graph, 'a')

    iterator = CycleIterator(graph, cycles=2)

    expected = [['a.0'], ['b.0', 'e.0'], ['c.0'], ['d.0'], ['a.1'], ['b.1', 'e.1'], ['c.1'], ['d.1']]
    iterated = []

    for index, node in enumerate(iterator):
        iterated.append(node)
        if index > len(expected):
            pytest.fail('iterator iterations exceeded length of expected values!')

    assert iterated == expected

@pytest.mark.parametrize('graph,cycles,error', [
    (DiGraph(), None, TypeError),
    (10, 1, TypeError),
    (DiGraph(), -1, ValueError)
])
def test_tasks_iterator_validation_error(graph, cycles, error):
    with pytest.raises(error):
        # noinspection PyTypeChecker
        TasksIterator(graph, cycles)

def test_tasks_iterator(sample_graph):
    graph, cycles_removed = decyclify(sample_graph, 'a')

    iterator = TasksIterator(graph, cycles=2)

    expected = [['a.0'], ['b.0', 'e.0', 'a.1'], ['c.0', 'b.1'], ['d.0', 'c.1'], ['d.1']]
    iterated = []

    for index, node in enumerate(iterator):
        iterated.append(node)
        if index > len(expected):
            pytest.fail('iterator iterations exceeded length of expected values!')

    assert iterated == expected
