Examples
========
The following example sets the environment variables for connecting to
PostgreSQL on localhost to the ``postgres`` database and issues a query.

.. code:: python

    import os

    from sprockets.clients import postgresql

    os.environ['PGSQL'] = 'postgresql://postgres@localhost:5432/postgres'

    session = postgresql.Session()
    result = session.query('SELECT 1')
    print(repr(result))


The following example shows how to use the :py:class:`TornadoSession <sprockets.clients.postgresql.TornadoSession>`
class in a Tornado :py:class:`RequestHandler <tornado.web.RequestHandler>`.

.. code:: python

    import os

    from tornado import gen
    from sprockets.clients import postgresql
    from tornado import web

    os.environ['PGSQL_FOO'] = 'postgresql://postgres@localhost:5432/foo'

    class RequestHandler(web.RequestHandler):

        def initialize(self):
            self.session = postgresql.TornadoSession('foo')

        @gen.coroutine
        def get(self, *args, **kwargs):
            result = yield self.session.query('SELECT 1')
            self.write(result.as_dict())
            result.free()
