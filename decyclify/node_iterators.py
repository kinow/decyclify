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

from decyclify.functions import create_intraiteration_matrix, create_interiteration_matrix, decyclify
from networkx import DiGraph
import numpy as np


class CycleIterator:
    """An iterator that will iterate over all the nodes in a cycle,
    before moving to the next cycles."""

    def __init__(self, graph: DiGraph):
        if not isinstance(graph, DiGraph):
            raise TypeError('graph must be a non-empty DiGraph')
        self.graph = graph
        self.intraiteration_matrix = create_intraiteration_matrix(graph)
        self.matrix = np.array(self.intraiteration_matrix, copy=True)
        self.current_cycle = 0
        self.current_column = -1
        self.nodes = [node for node in self.graph.nodes]
        self.count_nodes = len(self.nodes)

    def __iter__(self):
        return self

    def __next__(self):
        # if we have completed a cycle, we must reset the indexes
        if self.current_column == self.count_nodes - 1:
            self.current_cycle += 1
            self.current_column = -1
        nodes = []
        # if this is the first column, we know this task won't have any
        # dependency
        if self.current_column == -1:
            node = self.nodes[self.current_column + 1]
            nodes.append(f'{node}.{self.current_cycle}')
        else:
            while True:
                empty_column = True
                for row_index in range(0, self.count_nodes):
                    if self.matrix[row_index, self.current_column] == 1:
                        node = self.nodes[row_index]
                        nodes.append(f'{node}.{self.current_cycle}')
                        empty_column = False
                if not empty_column:
                    break
                self.current_column += 1
        self.current_column += 1
        return nodes


class TasksIterator:
    """An iterator that will iterate over all the nodes in a cycle,
    starting a new cycle as soon as a task has a interiteration
    dependency (IOW, if a task c.1 has a back-edge to a.2, once
    c.1 is found, it will start the cycle 2 and iterate over a.2,
    even if the cycle 1 is still being processed."""

    def __init__(self, graph: DiGraph):
        if not isinstance(graph, DiGraph):
            raise TypeError('graph must be a non-empty DiGraph')
        graph, cycles_removed = decyclify(graph)
        self.graph = graph
        self.cycles_removed = cycles_removed

        self.intraiteration_matrix = create_intraiteration_matrix(graph)

        self.interiteration_matrix = create_interiteration_matrix(graph.nodes, cycles_removed)

    def __iter__(self):
        return self

    def __next__(self):
        # WIP
        raise StopIteration
