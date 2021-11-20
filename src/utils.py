import numpy as np

from simplexlib.src.simplex import Table


def copy_table(tbl: Table) -> Table:
    return Table(
        # Copy table's underlying matrix
        tbl.table.copy(),
        # Create new list of h-labels
        # (labels are same, but are `str`, hence immutable)
        list(tbl.h_labels),
        # Create new list of v-labels
        list(tbl.v_labels),
    )


def add_condition(tbl: Table, a, b):
    tbl.table = np.insert(
        # Destination
        tbl.table,
        # Insertion index
        -1,
        # [B, A0, A1, ..., AN], following simple table structure
        [b, *a],
        # Inserting as row
        axis=0,
    )
