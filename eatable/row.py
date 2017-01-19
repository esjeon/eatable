
from typing import Any, Union
from .table import Table

class Row:
    """
    A wrapper class which binds row data to a Table instance.
    """
    def __init__(self, table: Table, index: int, data: tuple) -> None:
        assert table.width == len(data)
        self.table = table
        self.index = index
        self.data = data

    def __getitem__(self, key: Union[str, int]) -> Any:
        if isinstance(key, str):
            return self.data[self.table.get_column_index(key)]
        return self.data[key]
