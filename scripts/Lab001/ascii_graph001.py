from ascii_graph import Pyasciigraph
from ascii_graph import colors

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

data = [('A', 15, colors.BCya), ('B', 13, colors.BRed), ('C', 7, colors.Gre), ('D', 10, colors.BYel), ('E', 18, colors.BBlu)]

graph = Pyasciigraph()
for line in graph.graph('test graph', data):
    print(line)

