import numpy as np

from typing import Tuple


def add_condition(
    constraints: Tuple[np.ndarray, np.ndarray],
    to_add: Tuple[np.ndarray, int],
) -> Tuple[np.ndarray, np.ndarray]:
    A, b = constraints
    A, b = A.copy(), b.copy()

    a, B = to_add
    return np.vstack((A, a)), np.hstack((b, B))
