import codecs

import setuptools

setuptools.setup(
    name='sprockets.clients.postgresql',
    version='1.0.1',
    description=('PostgreSQL client library wrapper providing environment '
                 'variable based configuration'),
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    url='https://github.com/sprockets/sprockets.clients.postgresql.git',
    author='AWeber Communications',
    author_email='api@aweber.com',
    license=codecs.open('LICENSE', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['sprockets',
              'sprockets.clients',
              'sprockets.clients.postgresql'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    namespace_packages=['sprockets', 'sprockets.clients'],
    install_requires=['queries'],
    zip_safe=False)
