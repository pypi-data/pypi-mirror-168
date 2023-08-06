# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgtransaction']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'django-pgtransaction',
    'version': '1.0.0',
    'description': "A context manager/decorator which extends Django's atomic function with the ability to set isolation level and retries for a given transaction.",
    'long_description': 'django-pgtransaction\n====================\n\ndjango-pgtransaction offers a drop-in replacement for the\ndefault ``django.db.transaction`` module which, when used on top of a PostgreSQL\ndatabase, extends the functionality of that module with Postgres-specific features.\n\nAt present, django-pgtransaction offers an extension of the\n``django.db.transaction.atomic`` context manager/decorator which allows one to\ndynamically set the `isolation level <https://www.postgresql.org/docs/current/transaction-iso.html>`__\nwhen opening a transaction, as well as specifying\na retry policy for when an operation in that transaction results in a Postgres locking\nexception. See the quickstart below or `the docs <https://django-pgtransaction.readthedocs.io/>`__ for examples.\n\nQuickstart\n==========\n\nSet the isolation level of a transaction by using ``pgtransaction.atomic``:\n\n.. code-block:: python\n\n    import pgtransaction\n\n    with pgtransaction.atomic(isolation_level=pgtransaction.SERIALIZABLE):\n        # Do queries...\n\nThere are three isolation levels: ``pgtransaction.READ_COMMITTED``, ``pgtransaction.REPEATABLE_READ``,\nand ``pgtransaction.SERIALIZABLE``. By default it inherits the parent isolation level, which is Django\'s\ndefault of "READ COMMITTED".\n\nWhen using stricter isolation levels like ``pgtransaction.SERIALIZABLE``, Postgres will throw\nserialization errors upon concurrent updates to rows. Use the ``retry`` argument with the decorator\nto retry these failures:\n\n.. code-block:: python\n\n    @pgtransaction.atomic(isolation_level=pgtransaction.SERIALIZABLE, retry=3)\n    def do_queries():\n        # Do queries...\n\nNote that the ``retry`` argument will not work when used as a context manager. A ``RuntimeError``\nwill be thrown.\n\nBy default, retries are only performed when ``psycopg2.errors.SerializationError`` or\n``psycopg2.errors.DeadlockDetected`` errors are raised. Configure retried psycopg2 errors with\n``settings.PGTRANSACTION_RETRY_EXCEPTIONS``. You can set a default retry amount with\n``settings.PGTRANSACTION_RETRY``.\n\n``pgtransaction.atomic`` can be nested, but keep the following in mind:\n\n1. The isolation level cannot be changed once a query has been performed.\n2. The retry argument only works on the outermost invocation as a decorator, otherwise ``RuntimeError`` is raised.\n\nDocumentation\n=============\n\nCheck out the `Postgres docs <https://www.postgresql.org/docs/current/transaction-iso.html>`__\nto learn about transaction isolation in Postgres. \n\n`View the django-pgtransaction docs here\n<https://django-pgtransaction.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-pgtransaction with::\n\n    pip3 install django-pgtransaction\n\nAfter this, add ``pgtransaction`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgtransaction for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- `Paul Gilmartin <https://github.com/PaulGilmartin>`__\n- `Wes Kendall <https://github.com/wesleykendall>`__\n',
    'author': 'Opus 10 Engineering',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Opus10/django-pgtransaction',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
