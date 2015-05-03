#!/usr/bin/env python2.7
# Created by Aaron Cohen

import unittest
from mock import patch

from simple_database import Database, NoTransactionException
from db_cli import CommandLineDatabaseInterface, BadCommandException


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        db = Database()
        self.cli = CommandLineDatabaseInterface(db)

    @patch('simple_database.Database.set')
    def test_set_command(self, mock_set):
        self.cli.parse_command('SET banana rama')
        mock_set.assert_called_with('banana', 'rama')

    @patch('simple_database.Database.get')
    def test_get_command(self, mock_get):
        self.cli.parse_command('GET banana')
        mock_get.assert_called_with('banana')

    @patch('simple_database.Database.unset')
    def test_unset_command(self, mock_unset):
        self.cli.parse_command('UNSET banana')
        mock_unset.assert_called_with('banana')

    @patch('simple_database.Database.num_equal_to')
    def test_numequalto_command(self, mock_num_equal_to):
        self.cli.parse_command('NUMEQUALTO rama')
        mock_num_equal_to.assert_called_with('rama')

    def test_end_command(self):
        with self.assertRaises(EOFError):
            self.cli.parse_command('END')

    @patch('simple_database.Database.begin')
    def test_begin_transaction_command(self, mock_begin):
        self.cli.parse_command('BEGIN')
        mock_begin.assert_called_with()

    @patch('simple_database.Database.rollback')
    def test_rollback_transaction_command(self, mock_rollback):
        self.cli.parse_command('ROLLBACK')
        mock_rollback.assert_called_with()

    @patch('simple_database.Database.commit')
    def test_commit_transaction_command(self, mock_commit):
        self.cli.parse_command('COMMIT')
        mock_commit.assert_called_with()

    def test_invalid_command(self):
        with self.assertRaises(BadCommandException):
            self.cli.parse_command('BADCOMMAND')


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set(self):
        self.db.set('banana', 'rama')

    def test_get_matches_set(self):
        self.db.set('banana', 'rama')
        self.assertEqual(self.db.get('banana'), 'rama')

    def test_set_with_spaces_in_value(self):
        self.db.set('banana', 'rama rama')
        self.assertEqual(self.db.get('banana'), 'rama rama')

    def test_unset(self):
        self.db.set('banana', 'rama')
        self.db.unset('banana')
        self.assertIsNone(self.db.get('banana'))

    def test_numequalto(self):
        self.assertEqual(self.db.num_equal_to('rama'), 0)
        self.db.set('banana', 'rama')
        self.assertEqual(self.db.num_equal_to('rama'), 1)
        self.db.set('cavendish', 'rama')
        self.assertEqual(self.db.num_equal_to('rama'), 2)

    def test_begin_transaction(self):
        self.db.begin()
        self.db.set('banana', 'rama')
        self.assertEqual(self.db.get('banana'), 'rama')

    def test_rollback_transaction(self):
        self.db.begin()
        self.db.set('banana', 'rama')
        self.assertEqual(self.db.get('banana'), 'rama')
        self.db.rollback()
        self.assertIsNone(self.db.get('banana'))

    def test_commit_transaction(self):
        self.db.begin()
        self.db.set('banana', 'rama')
        self.db.commit()
        self.assertEqual(self.db.get('banana'), 'rama')

    def test_nested_rollback(self):
        self.db.begin()
        self.db.set('a', 10)
        self.assertEqual(self.db.get('a'), 10)
        self.db.begin()
        self.db.set('a', 20)
        self.assertEqual(self.db.get('a'), 20)
        self.db.rollback()
        self.assertEqual(self.db.get('a'), 10)
        self.db.rollback()
        self.assertIsNone(self.db.get('a'))

    def test_nested_commit_ends_all_transactions(self):
        self.db.begin()
        self.db.set('a', 30)
        self.db.begin()
        self.db.set('a', 40)
        self.db.commit()
        self.assertEqual(self.db.get('a'), 40)
        with self.assertRaises(NoTransactionException):
            self.db.rollback()

    def test_nested_unset_is_rolled_back(self):
        self.db.set('a', 50)
        self.db.begin()
        self.assertEqual(self.db.get('a'), 50)
        self.db.set('a', 60)
        self.db.begin()
        self.db.unset('a')
        self.assertIsNone(self.db.get('a'))
        self.db.rollback()
        self.assertEqual(self.db.get('a'), 60)
        self.db.commit()
        self.assertEqual(self.db.get('a'), 60)

    def test_nested_numequalto_is_rolled_back(self):
        self.db.set('a', 10)
        self.db.begin()
        self.assertEqual(self.db.num_equal_to(10), 1)
        self.db.begin()
        self.db.unset('a')
        self.assertEqual(self.db.num_equal_to(10), 0)
        self.db.rollback()
        self.assertEqual(self.db.num_equal_to(10), 1)
        self.db.commit()

    def test_nested_includes_previous_scope(self):
        self.db.begin()
        self.db.set('a', 10)
        self.db.begin()
        self.assertEqual(self.db.get('a'), 10)


if __name__ == '__main__':
    unittest.main()
