from __future__ import division
import math, random, re
from collections import defaultdict

class Table:
    
    def __init__(self, columns):
        self.columns = columns
        self.rows = []

    @property
    def get_rows(self):
        return self.rows

    @property
    def get_columns(self):
        return self.columns

    def __repr__(self):
        return str(self.columns) + "\n" + "\n".join(map(str, self.rows))

    def insert(self, row_values):
        if len(row_values) != len(self.columns):
            raise TypeError("wrong number of elements")
        row_dict = dict(zip(self.columns, row_values))
        self.rows.append(row_dict)

    def select(self, keep_columns=None, additional_columns=None):
        if keep_columns is None:
            keep_columns = self.columns

        if additional_columns is None:
            additional_columns = {}

        result_table = Table(keep_columns + list(additional_columns.keys()))

        for row in self.rows:
            new_row = [row[column] for column in keep_columns]
            for column_name, calculation in additional_columns.items():
                new_row.append(calculation(row))
            result_table.insert(new_row)

        return result_table

    def where(self, predicate=lambda row: True):
        where_table = Table(self.columns)
        where_table.rows = filter(predicate, self.rows)
        
        return where_table

    def limit(self, num_rows=None):
        limit_table = Table(self.columns)
        limit_table.rows = (self.rows[:num_rows]
                            if num_rows is not None
                            else self.rows)
        return limit_table

    def join(self, other_table, left_join=False):
        join_on_columns = [c for c in self.columns if c in other_table.columns]

        additional_columns = [c for c in other_table.columns if c not in join_on_columns]

        join_table = Table(self.columns + additional_columns)

        for row in self.rows:
            def is_join(other_row):
                return all(other_row[c] == row[c] for c in join_on_columns)

            other_rows = other_table.where(is_join).rows

            for other_row in other_rows:
                join_table.insert([row[c] for c in self.columns] + [other_row[c] for c in additional_columns])

            if left_join and not other_rows:
                join_table.insert([row[c] for c in self.columns] + [None for c in additional_columns])

        return join_table