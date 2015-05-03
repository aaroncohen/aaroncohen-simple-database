# aaroncohen-simple-database
An implementation of the simple database described in the [Thumbtack engineering challenge](https://www.thumbtack.com/challenges/simple-database).

### Requires:
* Python 2.7
* pip install mock  (only used for unittests)

### To Run:
`python db_cli.py`

### To Test:
`python tests.py`


The heart of the database is in [simple_database.py](simple_database.py). It stores data in dicts, which have 
[O(n) behavior for most operations](https://wiki.python.org/moin/TimeComplexity). It keeps an ordered list of 
transactions, which are stored as dicts as well. When nested transactions are created, a shallow copy of the previous 
transaction is used, which saves us the work of iterating over all of the transactions to coalesce them on commit. 
As transactions are never going to be shared between multiple connections/users/threads, there shouldn't be problems 
with lower tier transactions being modified underneath.

In order to make this database usable in a production environment, it would need to be modified to have a connection
pool of some sort. Transactions would exist on a per-connection basis, and any uncommitted transactions would be
cleaned up upon the closing of the connection.

The command line interface lives in [db_cli.py](db_cli.py).

The tests in [tests.py](tests.py) cover both the CLI and the database itself.

