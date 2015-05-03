# aaroncohen-simple-database
An implementation of the simple database described in the [Thumbtack engineering challenge](https://www.thumbtack.com/challenges/simple-database).

### Requires:
* Python 2.7
* pip install mock  (only used for unittests)

### To Run:
`python db_cli.py`

### To Test:
`python tests.py`


The heart of the database is in [simple_database.py](simple_database.py). It stores data in dicts, which generally have 
[O(n) behavior for most operations](https://wiki.python.org/moin/TimeComplexity). It keeps an ordered list of transactions, which are stored as shallow copies of the 
original data or the previous scope. When a transaction is committed, that transaction replaces the main data dict.

This approach will break down if used with more than one user or thread. A model where transactions have parent
transactions and are then merged is the better approach for any sort of production system using something other
than a command line interface. That seemed to exceed the requirements, though.

That said, this was designed to be modular enough that a network-based descendent of AbstractDatabaseInterface
could be implemented without much refactoring.

The command line interface lives in [db_cli.py](db_cli.py).

The tests in [tests.py](tests.py) cover both the CLI and the database itself.

