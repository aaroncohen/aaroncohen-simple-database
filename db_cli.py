#!/usr/bin/env python2.7
# Created by Aaron Cohen
import sys
from simple_database import NoTransactionException, Database


class CommandLineDatabaseInterface(object):
    def __init__(self, database):
        self._database = database

    def run(self):
        while True:
            try:
                self.parse_command(raw_input().strip())
            except BadCommandException as e:
                print e
            except EOFError:
                sys.exit()
            except KeyboardInterrupt:
                sys.exit()

    def parse_command(self, command_string):
        if not command_string:
            raise BadCommandException('Invalid command')

        split_command = command_string.split(' ')
        command, args = split_command[0], split_command[1:]

        if command == 'SET':
            if not len(args) >= 2:
                raise BadCommandException('Not enough arguments for SET command')

            self._database.set(args[0], ' '.join(args[1:]))

        elif command == 'GET':
            if not len(args) == 1:
                raise BadCommandException('Invalid arguments for GET command')

            print self._database.get(args[0]) or 'NULL'

        elif command == 'UNSET':
            if not len(args) == 1:
                raise BadCommandException('Invalid arguments for UNSET command')

            self._database.unset(args[0])

        elif command == 'NUMEQUALTO':
            if not len(args) == 1:
                raise BadCommandException('Invalid arguments for NUMEQUALTO command')

            print self._database.num_equal_to(args[0])

        elif command == 'END':
            raise EOFError()

        elif command == 'BEGIN':
            self._database.begin()

        elif command == 'ROLLBACK':
            try:
                self._database.rollback()
            except NoTransactionException:
                raise BadCommandException('NO TRANSACTION')

        elif command == 'COMMIT':
            self._database.commit()

        else:
            raise BadCommandException('Unknown command')


class BadCommandException(Exception):
        pass

if __name__ == '__main__':
    test_database = Database()
    cli = CommandLineDatabaseInterface(test_database)
    cli.run()
