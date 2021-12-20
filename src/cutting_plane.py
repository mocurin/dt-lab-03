import numpy as np

from dataclasses import dataclass, field

from simplexlib.src.table import Table, Simplex, V


@dataclass
class CuttingPlaneResult:
    history: list = field(default_factory=list)
    solved: bool = False

    @property
    def result(self):
        return self.history and self.history[-1] 


def has_integer_solution(table: Table) -> bool:
    return all(np.float64.is_integer(value) for value in table.b)


class CuttingPlane:
    @classmethod
    def _infer_constraint(cls, result: Table) -> np.ndarray:
        fracs = np.modf(result.b)[0]
        idx = np.argmax(fracs)

        left = np.modf(result[idx, 1:])[0]
        left[left < 0] += 1
        return V[left].inv >= fracs[idx]

    @classmethod
    def resolve(cls, table: Table) -> CuttingPlaneResult:
        history = list()
        while summary := Simplex.resolve(table):
            if not summary.solved:
                return CuttingPlaneResult(history, False)

            history.append(summary)

            if has_integer_solution(summary.result):
                return CuttingPlaneResult(history, True)
            
            table = summary.result.add_constraint(
                cls._infer_constraint(summary.result)
            )
        
