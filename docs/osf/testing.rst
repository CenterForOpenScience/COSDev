Testing the OSF
===============

Docs in progress.


The ``OsfTestCase``
*******************

The :class:`tests.base.OsfTestCase` class is the base class for all OSF tests that require a database. Its class setup and teardown methods will create a temporary database that only lives for the duration of the test class.

A few things to note about the :class:`OsfTestCase`:

- Its ``setUp`` method will instantiate a :class:`webtest_plus.TestApp`. You should **not** instantiate a ``TestApp`` yourself. Just use ``self.app``.
- If you override ``setUp`` or ``tearDown``, you must **always** call ``super(YourTestClass, self).setUp`` or ``super(YourTestClass, self).tearDown()``, respectively.
- Following the above two rules ensures that your tests execute within a Flask `app context <http://flask.pocoo.org/docs/appcontext/>`_.
- The test database lives for the duration of a test class. This means that database records created within a TestCase's methods may interact with each other in unexpected ways. Use :ref:`factories <factories>` and the ``tests.base.fake`` generator for creating unique test objects.


.. _factories:

Factories
*********

We use the `factory-boy <https://github.com/rbarrois/factory_boy>`_ library for defining our factories. Factories allow you to create test objects customized for the current test, while only declaring test-specific fields.

Using Factories
---------------

.. code-block:: python

    from tests.factories import UserFactory

    class TestUser(OsfTestCase):

        def test_a_method_of_the_user_class(self):
            user = UserFactory()  # creates a user
            user2 = UserFactory()  # creates a user with a different email address

            # You can also specify attributes when needed
            user3 = UserFactory(username='fredmercury@queen.io')
            # ...


Unit tests
**********

Testing models
--------------

Unit tests for models belong in ``tests/test_models.py``. Each model should have its own test class.

.. todo::
    Write example model test.

Views tests
***********

.. todo::
    Show webtest example

Functional tests
****************

.. todo::
    Show webtest functional test example


Javascript tests
****************
