#!/usr/bin/env python2.7
# Created by Aaron Cohen


class Database(object):
    """
    This is the heart of the database. It stores data in dicts, which generally have O(n) behavior for most operations.
    It keeps an ordered list of transactions, which are stored as shallow copies of the original data or the previous
    scope.

    This approach will break down if used with more than one user or thread. A model where transactions have parent
    transactions and are then merged is the better approach for any sort of production system using something other
    than a command line interface. That seemed to exceed the requirements somewhat, though.

    That said, this was designed to be modular enough that a network-based descendent of AbstractDatabaseInterface
    could be implemented without much refactoring.
    """

    def __init__(self):
        self._data = {}
        self._transactions = []

    def set(self, name, value):
        if len(self._transactions):
            self._transactions[-1][name] = value
        else:
            self._data[name] = value

    def get(self, name, default=None):
        if len(self._transactions):
            return self._transactions[-1].get(name, default)
        else:
            return self._data.get(name, default)

    def unset(self, name):
        if len(self._transactions):
            del self._transactions[-1][name]
        else:
            del self._data[name]

    def num_equal_to(self, value):
        if len(self._transactions):
            return self._transactions[-1].values().count(value)
        else:
            return self._data.values().count(value)

    def begin(self):
        if len(self._transactions):
            self._transactions.append(self._transactions[-1].copy())  # shallow copy
        else:
            self._transactions.append(self._data.copy())  # shallow copy

    def rollback(self):
        if len(self._transactions):
            del self._transactions[-1]
        else:
            raise NoTransactionException()

    def commit(self):
        if len(self._transactions):
            self._data = self._transactions[-1]
            self._transactions = []
        else:
            raise NoTransactionException()


class NoTransactionException(Exception):
        pass


class AbstractDatabaseInterface(object):
    def __init__(self, database):
        self._database = database

    def run(self):
        raise NotImplementedError()

    def parse_command(self, command_string):
        raise NotImplementedError()


if __name__ == '__main__':
    exit("Please run db_cli.py to get a commandline interface.")
