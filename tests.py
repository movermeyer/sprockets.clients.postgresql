"""
Tests for the sprockets.clients.postgresql package

"""
import datetime
import mock
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from sprockets.clients import postgresql
import queries.pool
import queries.tornado_session
from tornado import testing


class TestGetURI(unittest.TestCase):

    def test_get_uri_returns_proper_values(self):
        os.environ['PGSQL_TEST1'] = \
            'postgresql://foo1:baz1@test1-host:5436/test1'

        self.assertEqual(postgresql._get_uri('test1'),
                         'postgresql://foo1:baz1@test1-host:5436/test1')


class TestSession(unittest.TestCase):

    @mock.patch('queries.session.Session.__init__')
    def test_session_invokes_queries_session(self, mock_init):
        os.environ['PGSQL_TEST2'] = 'postgresql://foo:baz@db1:5433/bar'
        self.session = postgresql.Session('test2')
        self.assertTrue(mock_init.called)

    @mock.patch('queries.session.Session.__init__')
    def test_session_invokes_queries_session_with_url(self, mock_init):
        self.session = postgresql.Session('test6',
                                          db_url='postgresql://localhost/b')
        mock_init.assert_called_once_with(
            'postgresql://localhost/b', queries.RealDictCursor,
            queries.pool.DEFAULT_IDLE_TTL, queries.pool.DEFAULT_MAX_SIZE,
        )


class TestTornadoSession(unittest.TestCase):

    @mock.patch('queries.tornado_session.TornadoSession.__init__')
    def test_session_invokes_queries_session(self, mock_init):
        os.environ['PGSQL_TEST3'] = 'postgresql://foo:baz@db1:5434/bar'
        self.session = postgresql.TornadoSession('test3')
        self.assertTrue(mock_init.called)

    @mock.patch('queries.tornado_session.TornadoSession.__init__')
    def test_session_invokes_queries_session_with_url(self, mock_init):
        self.session = postgresql.TornadoSession(
            'test7', db_url='postgresql://localhost/b')
        mock_init.assert_called_once_with(
            'postgresql://localhost/b', queries.RealDictCursor,
            queries.pool.DEFAULT_IDLE_TTL,
            queries.tornado_session.DEFAULT_MAX_POOL_SIZE, None,
        )


class SessionIntegrationTests(unittest.TestCase):

    def setUp(self):
        os.environ['PGSQL_TEST4'] = \
            'postgresql://postgres@localhost:5432/postgres'
        try:
            self.session = postgresql.Session('test4', pool_max_size=10)
        except postgresql.OperationalError as error:
            raise unittest.SkipTest(str(error).split('\n')[0])

    def test_query_returns_results_object(self):
        self.assertIsInstance(self.session.query('SELECT 1 AS value'),
                              queries.Results)

    def test_query_result_value(self):
        result = self.session.query('SELECT 1 AS value')
        self.assertDictEqual(result.as_dict(), {'value': 1})

    def test_query_multirow_result_has_at_least_three_rows(self):
        result = self.session.query('SELECT * FROM pg_stat_database')
        self.assertGreaterEqual(result.count(), 3)

    def test_callproc_returns_results_object(self):
        timestamp = int(datetime.datetime.now().strftime('%s'))
        self.assertIsInstance(self.session.callproc('to_timestamp',
                                                    [timestamp]),
                              queries.Results)

    def test_callproc_mod_result_value(self):
        result = self.session.callproc('mod', [6, 4])
        self.assertEqual(6 % 4, result[0]['mod'])


class TornadoSessionIntegrationTests(testing.AsyncTestCase):

    def setUp(self):
        super(TornadoSessionIntegrationTests, self).setUp()
        os.environ['PGSQL_TEST5'] = \
            'postgresql://postgres@localhost:5432/postgres'
        self.session = postgresql.TornadoSession('test5',
                                                 pool_max_size=10,
                                                 io_loop=self.io_loop)

    @testing.gen_test
    def test_query_returns_results_object(self):
        try:
            result = yield self.session.query('SELECT 1 AS value')
        except postgresql.OperationalError:
            raise unittest.SkipTest('PostgreSQL is not running')
        self.assertIsInstance(result, queries.Results)
        result.free()

    @testing.gen_test
    def test_query_result_value(self):
        try:
            result = yield self.session.query('SELECT 1 AS value')
        except postgresql.OperationalError:
            raise unittest.SkipTest('PostgreSQL is not running')
        self.assertDictEqual(result.as_dict(), {'value': 1})
        result.free()

    @testing.gen_test
    def test_query_multirow_result_has_at_least_three_rows(self):
        try:
            result = yield self.session.query('SELECT * FROM pg_stat_database')
        except postgresql.OperationalError:
            raise unittest.SkipTest('PostgreSQL is not running')
        self.assertGreaterEqual(result.count(), 3)
        result.free()

    @testing.gen_test
    def test_callproc_returns_results_object(self):
        timestamp = int(datetime.datetime.now().strftime('%s'))
        try:
            result = yield self.session.callproc('to_timestamp', [timestamp])
        except postgresql.OperationalError:
            raise unittest.SkipTest('PostgreSQL is not running')
        self.assertIsInstance(result, queries.Results)
        result.free()

    @testing.gen_test
    def test_callproc_mod_result_value(self):
        try:
            result = yield self.session.callproc('mod', [6, 4])
        except postgresql.OperationalError:
            raise unittest.SkipTest('PostgreSQL is not running')
        self.assertEqual(6 % 4, result[0]['mod'])
        result.free()
