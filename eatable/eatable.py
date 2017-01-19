
import csv
from typing import Iterable, Any, Union

class Table:
    """
    A simple in-memory database.
    """
    @staticmethod
    def from_csv_file(filename: str, header: Iterable[str] = None) -> 'Table':
        """
        Create a Table object using data from the file at the given path.

        If `header` is not provided, the first row is used as header.
        """
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            table = Table(next(reader) if header is None else tuple(header))
            table.append_many(reader)
        return table

    def __init__(self, header: Iterable[str]) -> None:
        self.header = tuple(header)
        self.width = len(self.header)
        self.data = [] # type: list[tuple]
        self.column_index = dict(zip(self.header, range(self.width)))

    def __len__(self):
        return len(self.data)

    def get_column(self, name: str) -> int:
        """
        Get the index of the column with the given name.

        This is for internal uses.
        """
        index = self.column_index.get(name)
        if index is None:
            raise KeyError("The table has no column named '{}'".format(name))
        return index

    def append(self, data: Iterable):
        """
        Append a new row to the table.
        """
        actual_data = tuple(data)
        assert len(actual_data) == self.width
        self.data.append(actual_data)

    def append_many(self, iterable: Iterable[Iterable]) -> None:
        for row in iterable:
            self.append(row)


class Row:
    """
    A proxy for rows in Table
    """
    def __init__(self, table: Table, index: int) -> None:
        self.table = table
        self.index = index

    def __getitem__(self, key: int) -> Any:
        return self.table.data[self.index][key]
