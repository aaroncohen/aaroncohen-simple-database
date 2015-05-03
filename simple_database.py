#!/usr/bin/env python2.7
# Created by Aaron Cohen


class Database(object):
    """
    This is the heart of the database. It stores data in dicts, which have O(n) behavior for most operations.
    It keeps an ordered list of transactions, which are stored as dicts as well. When nested transactions are created,
    a shallow copy of the previous transaction is used, which saves us the work of iterating over all of the
    transactions to coalesce them on commit. As transactions are never going to be shared between multiple
    connections/users/threads, there shouldn't be problems with lower tier transactions being modified underneath.

    In order to make this database usable in a production environment, it would need to be modified to have a connection
    pool of some sort. Transactions would exist on a per-connection basis, and any uncommitted transactions would be
    cleaned up upon the closing of the connection.
    """

    def __init__(self):
        self._data = {}  # the main data-store
        self._transactions = []  # if a connection pool were implemented, transactions would be per-connection

    def set(self, name, value):
        if len(self._transactions):
            self._transactions[-1][name] = value
        else:
            self._data[name] = value

    def get(self, name, default=None):
        if len(self._transactions):
            # We create a temporary copy here in order to simulate the transaction having been committed already,
            # as users expect to be able to query both changed keys and unchanged keys that don't exist in the
            # transaction.
            temp_merged_data = self._data.copy()  # shallow copy
            temp_merged_data.update(self._transactions[-1])
            return temp_merged_data.get(name, default)
        else:
            return self._data.get(name, default)

    def unset(self, name):
        if len(self._transactions):
            # Keys with the value None are treated the same as keys that don't exist, though the key's name pollutes the
            # db a little. Cleaning these out of the database at commit time might give an undesirable perf hit, so a
            # periodic garbage collection mechansim or some other means of tagging for deletion might make sense.
            self._transactions[-1][name] = None
        else:
            del self._data[name]

    def num_equal_to(self, value):
        if len(self._transactions):
            temp_merged_data = self._data.copy()  # shallow copy
            temp_merged_data.update(self._transactions[-1])
            return temp_merged_data.values().count(value)
        else:
            return self._data.values().count(value)

    def begin(self):
        if len(self._transactions):
            # We make a shallow copy here to avoid the pain of progressively merging any nested transactions
            self._transactions.append(self._transactions[-1].copy())  # shallow copy
        else:
            self._transactions.append({})

    def rollback(self):
        if len(self._transactions):
            del self._transactions[-1]
        else:
            raise NoTransactionException()

    def commit(self):
        if len(self._transactions):
            self._data.update(self._transactions[-1])
            self._transactions = []
        else:
            raise NoTransactionException()


class NoTransactionException(Exception):
        pass


if __name__ == '__main__':
    exit("Please run db_cli.py to get a commandline interface.")
