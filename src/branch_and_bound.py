import numpy as np

from simplexlib.src.simplex import Table, Simplex

from .tree import Node, Edge
from .utils import add_condition


class BranchAndBound:
    @classmethod
    def solve(cls, c: np.ndarray, A: np.ndarray, b: np.ndarray) -> Node:
        table = Table.create(c, A, b)

        solved = Simplex.solve(table)

        if not solved:
            return Node("No solution")

        *x, F = table.table[:, 0]

        label = f"F = {F:.2f}, " + ", ".join(
            f"{label} = {value:.2f}" for label, value in zip(table.v_labels, x)
        )

        node = Node(label)

        print(label)

        for idx, value in enumerate(x):
            if np.float64.is_integer(value):
                continue

            condition = np.zeros(table.table.shape[1] - 1)
            condition[idx] = 1
            left, right = np.floor(value), np.ceil(value)
            lA, lb = add_condition((A, b), (condition, left))
            rA, rb = add_condition((A, b), (condition, -right))
            val_label = table.v_labels[idx]

            node.left = Edge(
                f"{val_label}≤{left}",
                node,
                cls.solve(c, lA, lb),
            )

            node.right = Edge(
                f"{val_label}≥{right}",
                node,
                cls.solve(c, rA, rb),
            )

            return node

        return node
