# decyclify

![CI](https://github.com/kinow/decyclify/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/kinow/decyclify/branch/master/graph/badge.svg)](https://codecov.io/gh/kinow/decyclify)

Graph decyclify algorithm implementation as in Sandnes &amp; Sinnen paper (2004) in Python.

"A new strategy for multiprocessor scheduling of cyclic task graphs", link to [article in Research Gate](https://www.researchgate.net/publication/220298826_A_new_strategy_for_multiprocessor_scheduling_of_cyclic_task_graphs).

See open issues for current status of the project.

## decyclify algorithm

The algorithm uses two matrices, `D` and `C`.

`D` is the **intraiteration dependencies** matrix. It represents the dependencies
in the graph within a cycle.

`C` is the **interiteration dependencies** matrix. It represents the dependencies
in the graph between cycles.

## Changelog

**0.1 (2020-??-??)**

- [#2](https://github.com/kinow/decyclify/issues/2) Graph input
- [#1](https://github.com/kinow/decyclify/issues/1) Build and packaging

## License

Licensed under the Apache License. See `LICENSE` for more.

