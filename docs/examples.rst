Examples
========
The following example sets the environment variables for connecting to
PostgreSQL on localhost to the ``postgres`` database and issues a query.

.. code:: python

    import os

    from sprockets.clients import postgresql

    os.environ['POSTGRES_HOST'] = 'localhost'
    os.environ['POSTGRES_USER'] = 'postgres'
    os.environ['POSTGRES_PORT'] = 5432
    os.environ['POSTGRES_DBNAME'] = 'postgres'

    session = postgresql.Session('postgres')
    result = session.query('SELECT 1')
    print(repr(result))
