
import csv
from typing import Iterable, Any, Union, Dict, Callable

ColumnRef = Union[str, int]
RowData = Iterable
RowIndex = int
SelectFilter = Callable[["Row"], bool]

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

    def __getitem__(self, index: RowIndex) -> "Row":
        return self.get_row(index)

    def __iter__(self) -> "TableIterator":
        return TableIterator(self)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, index: RowIndex, data: Iterable) -> None:
        self.set_row(index, data)

    def append(self, data: Iterable):
        """
        Append a new row to the table.
        """
        actual_data = tuple(data)
        assert len(actual_data) == self.width
        self.data.append(actual_data)

    def append_many(self, iterable: Iterable[Iterable]) -> None:
        """
        Append a number of rows at the same time.
        """
        # TODO: check length of each iterable in advance
        for row in iterable:
            self.append(row)

    def get_column_index(self, ref: ColumnRef) -> int:
        """
        Get the index of the column with the given name.abs

        If `int` is given, its value willbe checked and returned if it's a valid index.
        If any invalid value is given, an exception will be raised.
        """
        if isinstance(ref, int):
            if 0 <= ref < self.width:
                return ref
            raise IndexError("Index({}) out of range([0, {}])".format(0, self.width))
        elif isinstance(ref, str):
            index = self.column_index.get(ref)
            if index is not None:
                return index
            raise KeyError("Column('{}') not found".format(ref))
        raise TypeError("ref must be str or int")

    def get_row(self, index: RowIndex) -> "Row":
        if not 0 <= index < self.__len__():
            raise IndexError("index out of range: {}", format(index))
        return Row(self, index)

    def get_row_data(self, index:RowIndex) -> tuple:
        return self.data[index]

    def select(
            self,
            *columns: ColumnRef,
            where: SelectFilter = None
    ) -> "Table":
        if where is None:
            where = lambda _: True
        column_indexes = tuple(
            range(self.width) if len(columns) == 0
            else map(self.get_column_index, columns))
        table = Table(self.header[index] for index in column_indexes)
        table.append_many([
            row.select(*column_indexes)
            for row in self.__iter__() # type: ignore
            if where(row) is True
        ])
        return table

    def set_row(self, index: RowIndex, data: Iterable):
        if not 0 <= index < self.__len__():
            raise IndexError("index out of range: {}", format(index))
        actual_data = tuple(data)
        if len(actual_data) != self.width:
            raise TypeError("width mismatch")
        self.data[index] = actual_data

    def translate(self, column: ColumnRef, translator: Callable) -> None:
        index = self.get_column_index(column)
        for row in self: # type: ignore
            row[index] = translator(row[index])

    def update(
            self,
            columns: Iterable[ColumnRef] = None,
            values: Dict[RowIndex, Iterable] = None
    ) -> None:
        """
        update multiple rows and columns.
        """
        column_indexes = tuple(
            range(self.width) if columns is None
            else map(self.get_column_index, columns))
        for row_index, row_values in values.items():
            row = self.get_row(row_index)
            row.update(indexes=column_indexes, values=row_values)

class Row:
    """
    A proxy for a row in Table
    """

    def __init__(self, table: Table, index: RowIndex) -> None:
        self.table = table
        self.index = index

    def __getitem__(self, ref: ColumnRef) -> Any:
        return self.get_data()[self.table.get_column_index(ref)]

    def __iter__(self):
        return iter(zip(self.table.header, self.get_data()))

    def __setitem__(self, ref: ColumnRef, value: Any) -> None:
        data = self.get_data()
        new_data = list(data)
        new_data[self.table.get_column_index(ref)] = value
        self.table.set_row(self.index, new_data)

    def get_data(self) -> tuple:
        return self.table.get_row_data(self.index)

    def select(self, *columns: ColumnRef):
        data = self.get_data()
        indexes = map(self.table.get_column_index, columns)
        return tuple(data[index] for index in indexes)

    def update(
            self,
            columns: Iterable[ColumnRef] = None,
            indexes: Iterable[int] = None,
            values: Iterable = None
    ) -> None:
        """
        update multiple values in the row.
        """
        if indexes is None:
            indexes = tuple(
                range(self.table.width)if columns is None
                else map(self.table.get_column_index, columns))
        data = list(self.get_data())
        for index, value in zip(indexes, values):
            data[index] = value
        self.table.set_row(self.index, data)


class TableIterator:
    def __init__(self, table: Table) -> None:
        self.table = table
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self) -> Row:
        self.index += 1
        if not 0 <= self.index < self.table.width:
            raise StopIteration()
        return self.table.get_row(self.index)
