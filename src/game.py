import numpy as np

from simplexlib.src.table import Table, V


class StrategyMatrix:
    data: np.ndarray

    def __init__(self, data: np.ndarray):
        self.data = data

    def straight(self) -> Table:
        return Table.straight(
            [1] * len(self.data[0]),
            *[V[line] <= 1 for line in self.data]
        )

    def inverse(self) -> Table:
        return Table.inverse(
            [1] * len(self.data[0]),
            *[V[line] <= 1 for line in self.data]
        )

def optimal(table: Table):
    h = 1 / table.F
    return h, table.real_b * h