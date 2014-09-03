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

from tornado import gen
from sprockets.clients import postgresql
import queries
from tornado import testing


class TestGetURI(unittest.TestCase):

    def tearDown(self):
        for key in ['HOST', 'PORT', 'DBNAME', 'USER', 'PASSWORD']:
            del os.environ['TEST1_%s' % key]

    def test_get_uri_returns_proper_values(self):

        os.environ['TEST1_HOST'] = 'test1-host'
        os.environ['TEST1_PORT'] = '5436'
        os.environ['TEST1_DBNAME'] = 'test1'
        os.environ['TEST1_USER'] = 'foo1'
        os.environ['TEST1_PASSWORD'] = 'baz1'

        self.assertEqual(postgresql._get_uri('test1'),
                         'postgresql://foo1:baz1@test1-host:5436/test1')


class TestSession(unittest.TestCase):

    @mock.patch('queries.session.Session.__init__')
    def setUp(self, mock_init):
        self.mock_init = mock_init
        os.environ['TEST2_HOST'] = 'db1'
        os.environ['TEST2_PORT'] = '5433'
        os.environ['TEST2_DBNAME'] = 'bar'
        os.environ['TEST2_USER'] = 'foo'
        os.environ['TEST2_PASSWORD'] = 'baz'
        self.session = postgresql.Session('test2')

    def tearDown(self):
        for key in ['HOST', 'PORT', 'DBNAME', 'USER', 'PASSWORD']:
            del os.environ['TEST2_%s' % key]

    def test_session_invokes_queries_session(self):
        self.assertTrue(self.mock_init.called)


class TestTornadoSession(unittest.TestCase):

    @mock.patch('queries.tornado_session.TornadoSession.__init__')
    def setUp(self, mock_init):
        self.mock_init = mock_init
        os.environ['TEST3_HOST'] = 'db1'
        os.environ['TEST3_PORT'] = '5434'
        os.environ['TEST3_DBNAME'] = 'bar'
        os.environ['TEST3_USER'] = 'foo'
        os.environ['TEST3_PASSWORD'] = 'baz'
        self.session = postgresql.TornadoSession('test3')

    def tearDown(self):
        for key in ['HOST', 'PORT', 'DBNAME', 'USER', 'PASSWORD']:
            del os.environ['TEST3_%s' % key]

    def test_session_invokes_queries_session(self):
        self.assertTrue(self.mock_init.called)


class SessionIntegrationTests(unittest.TestCase):

    def setUp(self):
        os.environ['TEST4_HOST'] = 'localhost'
        os.environ['TEST4_PORT'] = '5432'
        os.environ['TEST4_DBNAME'] = 'postgres'
        os.environ['TEST4_USER'] = 'postgres'

        try:
            self.session = postgresql.Session('test', pool_max_size=10)
        except postgresql.OperationalError as error:
            raise unittest.SkipTest(str(error).split('\n')[0])

    def tearDown(self):
        for key in ['HOST', 'PORT', 'DBNAME', 'USER']:
            del os.environ['TEST4_%s' % key]

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
        os.environ['TEST5_HOST'] = 'localhost'
        os.environ['TEST5_PORT'] = '5432'
        os.environ['TEST5_DBNAME'] = 'postgres'
        os.environ['TEST5_USER'] = 'postgres'
        self.session = postgresql.TornadoSession('test',
                                                 pool_max_size=10,
                                                 io_loop=self.io_loop)

    #def tearDown(self):
    #    for key in ['HOST', 'PORT', 'DBNAME', 'USER']:
    #        del os.environ['TEST5_%s' % key]

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
