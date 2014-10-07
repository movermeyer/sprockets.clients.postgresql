sprockets.clients.postgresql
============================
The ``sprockets.clients.postgresql`` package wraps the
`queries <http://queries.readthedocs.org>`_ package providing environment
variable based configuration for connecting to PostgreSQL.

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
sprockets.clients.postgresql is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.clients.postgresql>`_
and can be installed via ``pip`` or ``easy_install``:

.. code:: bash

    pip install sprockets.clients.postgresql

Documentation
-------------
https://sprocketsclientspostgresql.readthedocs.org

Requirements
------------
-  `queries`_

Example
-------
The following example sets the environment variable for connecting to
PostgreSQL on localhost to the ``production`` database and issues a query.

.. code:: python

    import os

    from sprockets.clients import postgresql

    os.environ['PGSQL_PROD'] = 'postgresql://postgres@localhost:5432/production'

    session = postgresql.Session('prod')
    result = session.query('SELECT 1')
    print(repr(result))

Version History
---------------
Available at https://sprocketsclientspostgresql.readthedocs.org/en/latest/history.html

.. |Version| image:: https://badge.fury.io/py/sprockets.clients.postgresql.svg?
   :target: http://badge.fury.io/py/sprockets.clients.postgresql

.. |Status| image:: https://travis-ci.org/sprockets/sprockets.clients.postgresql.svg?branch=master
   :target: https://travis-ci.org/sprockets/sprockets.clients.postgresql

.. |Coverage| image:: https://img.shields.io/coveralls/sprockets/sprockets.clients.postgresql.svg?
   :target: https://coveralls.io/r/sprockets/sprockets.clients.postgresql

.. |Downloads| image:: https://pypip.in/d/sprockets.clients.postgresql/badge.svg?
   :target: https://pypi.python.org/pypi/sprockets.clients.postgresql

.. |License| image:: https://pypip.in/license/sprockets.clients.postgresql/badge.svg?
   :target: https://sprocketsclientspostgresql.readthedocs.org