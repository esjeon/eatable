
from typing import Any
from .table import Table

class Row:
    """
    A wrapper class which binds row data to a Table instance.
    """
    def __init__(self, table: Table, data: tuple) -> None:
        assert table.width == len(data)
        self.table = table
        self.data = data

    def __getitem__(self, key: str) -> Any:
        return self.data[self.table.get_column_index(key)]
