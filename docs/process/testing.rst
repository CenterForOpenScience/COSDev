.. _testing:

Testing
=======

.. note::

    The below examples are in Python, but the concepts apply to testing in any language.

.. seealso::

    Looking for OSF-specific testing guidelines? See the :ref:`Testing the OSF <osftesting>` page.


General Testing Guidelines
--------------------------

- Use long, descriptive names. This often obviates the need for doctrings in test methods. This also makes it easier to locate tests that fail.
- Tests should be isolated. Don't interact with a real database or network. Use a separate test database that gets torn down or use mock objects.
- Prefer `factories <https://github.com/rbarrois/factory_boy>`_ to fixtures.
- Never let incomplete tests pass, else you run the risk of forgetting about them. Instead, add a placeholder like ``assert False, "TODO: finish me"``. If you are stubbing out a test that will be written in the future, use the :meth:`@unittest.skip` decorator.
- Strive for 100% code coverage, but don't get obsess over coverage scores.
- When testing the contents of a dictionary, test the keys individually.

.. code-block:: python

    # Yes
    assert_equal(result['foo'], 42)
    assert_equal(result['bar'], 24)

    # No
    assert_equal(result, {'foo': 42, 'bar': 24})

Unit Tests
----------

- Focus on one tiny bit of functionality.
- Should be fast, but a slow test is better than no test.
- It often makes sense to have one testcase class for a single class or model.

.. code-block:: python

    import unittest
    import factories

    class PersonTest(unittest.TestCase):
        def setUp(self):
            self.person = factories.PersonFactory()

        def test_has_age_in_dog_years(self):
             assert self.person.dog_years == self.person.age / 7

Functional Tests
----------------

Functional tests are higher level tests that are closer to how an end-user would interact with your application. They are typically used for web and GUI applications.

- Write tests as scenarios. Testcase and test method names should read like a scenario description.
- Use comments to write out stories, *before writing the test code*.

.. code-block:: python

    class TestAUser(unittest.TestCase):
        def test_can_write_a_blog_post(self):
            # Goes to the her dashboard
            ...
            # Clicks "New Post"
            ...
            # Fills out the post form
            ...
            # Clicks "Submit"
            ...
            # Can see the new post
            ...

Notice how the testcase and test method read together like "Test A User can write a blog post".



Supporting Libraries
--------------------

Python
******

- `nose <https://nose.readthedocs.org/en/latest/>`_: Extends Python's unittest. Includes a test runner and various utilities.
- `pytest <http://pytest.org/latest/contents.html>`_: A powerful test runner and library for writing automated tests.
- `factory-boy <https://github.com/rbarrois/factory_boy>`_: Utility library for creating test objects. Replaces fixtures with "factories".
- `mock <http://www.voidspace.org.uk/python/mock/>`_: Allows you to mock and patch objects for testing purposes.
- `webtest <http://webtest.readthedocs.org/en/latest/>`_ / `webtest-plus <https://github.com/sloria/webtest-plus>`_ : Provides a :class:`TestApp` with which to send test requests and make assertions about the responses.
- `faker <https://github.com/joke2k/faker>`_ : A fake data generator.


Javascript
**********

- `qunit <http://qunitjs.com/>`_: Unit testing framework.
- `sinon <http://sinonjs.org/>`_: Provides test spies and mocks.
