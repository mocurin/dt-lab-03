from __future__ import annotations

import graphviz as gv
from simplexlib.src.table import SimplexResult, Format, pretty_value

from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class Edge:
    """Generic directed edge"""

    data: List
    source: Node = None
    target: Node = None

    def register(self, dot: gv.Digraph, formatter: Format):
        """Register edge in graphviz.Digraph"""
        dot.edge(self.source.name, self.target.name, self.label(formatter))

        self.target.register(dot, formatter)

    def label(self, formatter: Format = None, pretty: bool = False):
        formatter = formatter or Format(None)

        label, sign, value = self.data

        s = f"{formatter.default_var_sym}{'_' if pretty else ''}{label}{sign}{pretty_value(value, formatter.default_precision)}"

        return f"${s}$" if pretty else s


@dataclass
class Node:
    """Generic graph node"""

    data: Any
    invalid: bool = False
    left: Optional[Edge] = None
    right: Optional[Edge] = None

    def register(self, dot: gv.Digraph, formatter: Format):
        """Register node in graphviz.Digraph"""
        dot.node(self.name, self.label(formatter))

        if left := self.left:
            left.register(dot, formatter)

        if right := self.right:
            right.register(dot, formatter)

    def visualize(self, formatter: Format = None, *args, **kwargs):
        """Create graphviz repr of a graphn with start in a current Node"""
        dot = gv.Digraph(*args, **kwargs)
        formatter = formatter or Format(None)

        self.register(dot, formatter)

        return dot

    def label(self, formatter: Format = None, pretty: bool = False):
        formatter = formatter or Format(None)

        if self.invalid:
            return "No solution"

        base = ", ".join(
            f"{formatter.default_var_sym}{'_' if pretty else ''}{label}={pretty_value(value, formatter.default_precision)}"
            for label, value in zip(
                self.data.result.vlabels,
                self.data.result.b
            )
        )

        splitter = ', ' if pretty else '\\n'
        s = f"{formatter.default_tgt_sym}={pretty_value(self.data.result.F, formatter.default_precision)}{splitter}{base}"

        return f"${s}$" if pretty else s

    @property
    def name(self):
        """
        Generates unique Node-identifier
        !Usage of id() means that Nodes should never be reused in the same graph!
        """
        return str(id(self))

    @property
    def leaves(self):
        leaves = list()

        if self.left:
            leaves.extend(self.left.target.leaves)
        
        if self.right:
            leaves.extend(self.right.target.leaves)

        if not self.left and not self.right:
            leaves.append(self)

        return leaves
