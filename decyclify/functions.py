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

from typing import List, Iterable

from networkx import DiGraph
from networkx.readwrite.edgelist import parse_edgelist


def decyclify(graph: List, number_of_cycles: int=1):
    """
    Decyclify a directed cyclic graph (DCG) into a directed acyclic graph (DAG) with cycles.

    :param graph: the graph
    :type graph: List
    :param number_of_cycles: number of cycles to be generated
    :type number_of_cycles: int
    :return: a DCG that is iterable and contains multiple cycles, each cycle with a single DAG
    :rtype: Iterable
    """
    if not isinstance(graph, list):
        raise TypeError(f"Graph must be a List, but '{type(graph)}' given")
    g = parse_edgelist(graph, create_using=DiGraph)
    return decyclify_networkx(g, number_of_cycles)

def decyclify_networkx(graph: DiGraph, number_of_cycles: int=1):
    """
    Sibling function of `decyclify`, that takes as argument a networkx
    object.

    :param graph: a networkx object representing the input graph
    :rtype graph: DiGraph
    :param number_of_cycles: number of cycles to be generated
    :type number_of_cycles: int
    :return: a DCG that is iterable and contains multiple cycles, each cycle with a single DAG
    :rtype: Iterable
    """
    if not isinstance(graph, DiGraph):
        raise TypeError(f"Graph must be a networkx.DiGraph, but '{type(graph)}' given")
    if not isinstance(number_of_cycles, int):
        raise TypeError(f"Number of cycles must be an integer, but '{type(number_of_cycles)}' given")
    if number_of_cycles < 1:
        raise ValueError(f"Number of cycles must be at least '1', but '{number_of_cycles}' given")
    return []
