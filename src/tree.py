from __future__ import annotations

import graphviz as gv

from dataclasses import dataclass
from typing import Optional


@dataclass
class Edge:
    """Generic directed edge"""

    label: str
    source: Node = None
    target: Node = None

    def register(self, dot: gv.Digraph):
        """Register edge in graphviz.Digraph"""
        dot.edge(self.source, self.target, self.label)

        self.target.register(dot)


@dataclass
class Node:
    """Generic graph node"""

    label: str
    left: Optional[Edge] = None
    right: Optional[Edge] = None

    def register(self, dot: gv.Digraph):
        """Register node in graphviz.Digraph"""
        dot.node(self.name, self.label)

        if left := self.left:
            left.register(dot)

        if right := self.right:
            right.register(dot)

    def visualize(self, *args, **kwargs):
        """Create graphviz repr of a graphn with start in a current Node"""
        dot = gv.Digraph(*args, **kwargs)

        self.register(dot)

        return dot

    @property
    def name(self):
        """
        Generates unique Node-identifier
        !Usage of id() means that Nodes should never be reused in the same graph!
        """
        return str(id(self))
