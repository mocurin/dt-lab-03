import numpy as np

from simplexlib.src.table import Table, Simplex, V

from .tree import Node, Edge


class BranchAndBound:
    @classmethod
    def resolve(cls, table: Table, prev: np.float64 = None) -> Node:
        summary = Simplex.resolve(table)

        if not summary.fixed or not summary.solved:
            return Node(summary, True)

        result: Table = summary.result
        source: Table = summary.source

        if prev is not None and result.F == prev:
            return Node(summary, True)

        node = Node(summary)

        for idx, (value, label) in enumerate(zip(result.b, result.vlabels)):
            if np.float64.is_integer(value):
                continue

            condition = np.zeros(len(result.c))
            condition[idx] = 1
            left, right = np.floor(value), np.ceil(value)
            ltable = source.add_constraint(
                V[condition] <= left
            )
            rtable = source.add_constraint(
                V[condition].inv >= right
            )

            node.left = Edge(
                [label, "≤", left],
                node,
                cls.resolve(ltable, result.F),
            )

            node.right = Edge(
                [label, "≥", right],
                node,
                cls.resolve(rtable, result.F),
            )

            return node

        return node
