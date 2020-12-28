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

"""Function to iterate graph nodes. Implements functions that can be
used to implement the experiments of the Sandnes and Sinnen paper."""

from typing import Union

import numpy as np
from networkx import DiGraph

from decyclify.functions import create_intraiteration_matrix, create_interiteration_matrix


class CycleIterator:
    """An iterator that will iterate over all the nodes in a cycle,
    before moving to the next cycles."""

    def __init__(self, graph: DiGraph, cycles=2, include_cycle=True):
        if not isinstance(graph, DiGraph):
            raise TypeError('graph must be a non-empty DiGraph')
        if not isinstance(cycles, int):
            raise TypeError('cycles must be an integer')
        if cycles <= 0:
            raise ValueError('cycles value must be greater than zero')
        self.graph = graph
        self.cycles = cycles
        self.intraiteration_matrix = create_intraiteration_matrix(graph)
        self.matrix = np.array(self.intraiteration_matrix, copy=True)
        self.current_cycle = 0
        self.current_column = -1
        self.nodes = [node for node in self.graph.nodes]
        self.count_nodes = len(self.nodes)
        self.include_cycle = include_cycle

    def __iter__(self):
        return self

    def _get_node_text(self, node):
        if not self.include_cycle:
            return node
        return f'{node}.{self.current_cycle}'


    def __next__(self):
        # if we have completed a cycle, we must reset the indexes
        if self.current_column == self.count_nodes - 1:
            self.current_cycle += 1
            if (self.current_cycle >= self.cycles):
                raise StopIteration
            self.current_column = -1
        nodes = []
        # if this is the first column, we know this task won't have any
        # dependency
        if self.current_column == -1:
            node = self.nodes[self.current_column + 1]
            nodes.append(self._get_node_text(node))
        else:
            while True:
                empty_column = True
                for row_index in range(0, self.count_nodes):
                    if self.matrix[row_index, self.current_column] == 1:
                        node = self.nodes[row_index]
                        nodes.append(self._get_node_text(node))
                        empty_column = False
                if not empty_column:
                    break
                self.current_column += 1
        self.current_column += 1
        return nodes


class Cycle:

    def __init__(
            self,
            cycle_number:int=1,
            graph:DiGraph=None,
            nodes:[]=None,
            interiteration_matrix:np.ndarray=None
    ):
        self.cycle_number = cycle_number
        self.nodes: Union[None, list] = nodes
        self.current_nodes = [node for node in nodes]
        # one-cycle iteration (i.e. intra-iteration)
        self.intraiteration_nodes = [node for node in CycleIterator(graph, cycles=1, include_cycle=False)]
        self.interiteration_matrix = interiteration_matrix

        self.previous: Union[Cycle, None] = None
        self.next = None

    def iterate(self, new_nodes_in_this_cycle) -> list:
        new_nodes = []
        if self._is_first():
            intraiteration_nodes = self._pop_next()
            if intraiteration_nodes:
                new_nodes.extend(intraiteration_nodes)
            else:
                # we have iterated through all possible nodes in the current cycle
                raise RemoveCycle()
        else:
            # for the next cycle, we can only add; the next cycle later becomes current cycle,
            # and is then later removed
            new_nodes.extend(self._pop_next_interiteration(new_nodes_in_this_cycle))
        return new_nodes

    def _get_node_text(self, node):
        return f'{node}.{self.cycle_number}'

    def _next_nodes(self):
        if not self.intraiteration_nodes:
            return []
        return [self._get_node_text(node) for node in self.intraiteration_nodes[0].copy()]

    def _remove_nodes(self, nodes):
        for (key, intraiteration_node) in enumerate(self.intraiteration_nodes):
            for node in intraiteration_node.copy():
                if node in nodes:
                    intraiteration_node.remove(node)
                    self.current_nodes.remove(node)
            if not intraiteration_node:
                self.intraiteration_nodes.pop(key)

    def _pop_next(self) -> []:
        nodes = self._next_nodes()
        self._remove_nodes([node.split('.', 1)[0] for node in nodes])
        return nodes

    def _is_first(self) -> bool:
        return self.previous is None

    def _is_last(self) -> bool:
        return self.next is None

    def _pop_next_interiteration(self, new_nodes_in_this_cycle):
        nodes = []
        new_nodes_in_this_cycle = [node.split('.', 1)[0] for node in new_nodes_in_this_cycle]
        if not self._is_first():
            next_intraiteration_nodes = self._next_nodes()
            for next_intraiteration_node in next_intraiteration_nodes:
                # given an intraiteration node, let's find its upstream nodes,
                # from the previous cycle
                node = next_intraiteration_node.split('.', 1)[0]
                if node in self.previous.current_nodes or node in new_nodes_in_this_cycle:
                    continue
                row_index = self.nodes.index(node)
                row = self.interiteration_matrix[row_index]

                # these are the nodes triggering the `next_intraiteration_node` from the
                # previous cycle
                interiteration_trigger_nodes = [value for (key, value) in enumerate(row) if value == 1]
                if not interiteration_trigger_nodes:
                    # node has no intercycle dependency, fine to return it
                    nodes.append(next_intraiteration_node)
                    self._remove_nodes([node])
                if interiteration_trigger_nodes:
                    for interiteration_trigger_node in interiteration_trigger_nodes:
                        # if this is True, it means the node in the previous cycle has been
                        # returned, so we are good to return this downstream dependency
                        if interiteration_trigger_node not in self.previous.current_nodes:
                            nodes.append(next_intraiteration_node)
                            self._remove_nodes([node])
        return nodes


class RemoveCycle(BaseException):
    ...


class TasksIterator:
    """An iterator that will iterate over all the nodes in a cycle,
    starting a new cycle as soon as a task has a interiteration
    dependency (IOW, if a task c.1 has a back-edge to a.2, once
    c.1 is found, it will start the cycle 2 and iterate over a.2,
    even if the cycle 1 is still being processed."""

    def __init__(self, graph: DiGraph, cycles_removed: Union[None, list], cycles=2):
        if not isinstance(graph, DiGraph):
            raise TypeError('graph must be a non-empty DiGraph')
        if not isinstance(cycles, int):
            raise TypeError('cycles must be an integer')
        if cycles <= 0:
            raise ValueError('cycles value must be greater than zero')
        self.graph = graph
        self.nodes = [node for node in self.graph.nodes]
        self.intraiteration_matrix = np.array(create_intraiteration_matrix(graph), copy=True)
        self.interiteration_matrix = np.array(create_interiteration_matrix(list(graph.nodes), cycles_removed), copy=True)

        # here we create a linked-list of cycles; where each cycle knows its previous
        # cycle and the next cycle (if available).
        self.cycles = []
        for cycle_number in range(0, cycles):
            cycle = Cycle(
                cycle_number=cycle_number,
                graph=self.graph,
                nodes=self.nodes,
                interiteration_matrix=self.interiteration_matrix
            )
            if self.cycles:
                cycle.previous = self.cycles[-1]
                self.cycles[-1].next = cycle
            self.cycles.append(cycle)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.cycles:
            raise StopIteration

        # collect tasks/nodes ready to execute in each cycle
        new_nodes_in_this_cycle = []
        for cycle in self.cycles.copy():
            try:
                new_nodes_in_this_cycle.extend(cycle.iterate(new_nodes_in_this_cycle))
            except RemoveCycle:
                self.cycles.remove(cycle)

        # no more nodes, stop iterating
        if not new_nodes_in_this_cycle:
            raise StopIteration

        return new_nodes_in_this_cycle
