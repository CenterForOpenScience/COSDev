Testing the OSF
===============

Docs in progress.


The OsfTestCase
***************

The ``tests.base.OsfTestCase`` class is the base class for all OSF tests that require a database. Its class setup and teardown methods will create a temporary database that only lives for the duration of the test class.

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
