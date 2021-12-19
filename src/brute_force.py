import numpy as np

from dataclasses import dataclass, field
from itertools import product
from simplexlib.src.table import Table


@dataclass
class BruteforceResult:
    result: dict = field(default_factory=dict)

    @property
    def maximum(self):
        return max(self.result)

    @property
    def minimum(self):
        return min(self.result)
    
    @property
    def maxset(self):
        return self.result[self.maximum]
    
    @property
    def minset(self):
        return self.result[self.minimum]

class BruteForce:
    @classmethod
    def resolve(self, table: Table, opt: np.float64):
        A, b, c = table.A, table.b, table.c
        maxval = opt / np.min(c[c > 0])
        maxval = np.ceil(maxval).astype(int)

        result = {
            np.sum(c * vec): vec
            for vec in product(
                range(maxval),
                repeat=len(b),
            )
            if np.sum(
                np.sum(table.A[idx] * vec) <= elem
                for idx, elem in enumerate(b)
            ) == len(b)
        }

        return BruteforceResult(result)

        # return (max(res), res[max(res)]) if (
        #     res := {
        #         np.sum(table.c * vec): vec
        #         for vec in product(
        #             range(
        #                 np.ceil(
        #                     opt / np.min(table.c[table.c > 0])
        #                 ).astype(int)
        #             ),
        #             repeat=len(table.b),
        #         )
        #         if np.sum(
        #             table.A[idx] * vec <= elem
        #             for idx, elem in enumerate(table.b)
        #         ) == len(table.b)
        #     }
        # ) else None