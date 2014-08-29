"""
Tests for the sprockets.clients.postgresql package

"""
import mock
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from sprockets.clients import postgresql


class TestGetURI(unittest.TestCase):

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

    def test_session_invokes_queries_session(self):
        self.assertTrue(self.mock_init.called)
