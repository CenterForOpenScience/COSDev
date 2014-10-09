Testing the OSF
===============

Docs in progress.

.. seealso::

    This page includes information testing the OSF codebase. For more general testing
    guidelines, see the :ref:`Testing <testing>` page.


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
    from tests.base import fake

    class TestUser(OsfTestCase):

        def test_a_method_of_the_user_class(self):
            user = UserFactory()  # creates a user
            user2 = UserFactory()  # creates a user with a different email address

            # You can also specify attributes when needed
            user3 = UserFactory(username='fredmercury@queen.io')
            user4 = UserFactory(password=fake.md5())
            # ...


Unit tests
**********

Testing models
--------------

Unit tests for models belong in ``tests/test_models.py``. Each model should have its own test class. You can have multiple test classes for a single model if necessary.

.. code-block:: python

    from frameworks.auth.core import User

    from tests.base import OsfTestCase, fake

    class TestUser(OsfTestCase):

        def test_check_password(self):
            user = User(username=fake.email(), fullname='Nick Cage')
            user.set_password('ghostrider')
            user.save()
            assert_true(user.check_password('ghostrider'))
            assert_false(user.check_password('ghostride'))

        # ...

Views tests
************

Views tests are used to test that our endpoints return the expected responses. We use the `webtest <http://webtest.readthedocs.org/en/latest/>`_ library to interact with our application under test.

The :class:`OsfTestCase` provides a `self.app` attribute that is a `webtest_plus.TestApp` object.

Things to test:

- Status codes
- JSON responses
- Records are updated appropriately in the database

.. code-block:: python

    from tests.base import OsfTestCase
    from tests.factories import ProjectFactory, AuthUserFactory

    class TestProjectViews(OsfTestCase):

        def setUp(self):
            OsfTestCase.setUp(self)
            # The AuthUserFactory automatically generates an
            # API key for the user. It can be accessed from the
            #  `auth` attribute
            self.user = AuthUserFactory()
            self.project = ProjectFactory(creator=self.user)

        # Status codes should be tested
        def test_get_project_returns_200_with_auth(self):
            url = self.project.api_url_for('project_get')
            # This endpoint requires authentication. We use the user's API key to
            # circumvent the login process
            res = self.app.get(url, auth=self.user.auth)
            assert_equal(res.status_code, 200)

            # The JSON response is correct
            assert_equal(res.json['id'], self.project._id)
            assert_equal(res.json['title'], self.project.title)
            # ...

        def test_get_project_returns_403_with_no_auth(self):
            url = self.project.api_url_for('project_get')
            # Make sure to pass expect_error=True if you expect an error response.
            res = self.app.get(url, auth=self.user.auth, expect_errors=True)
            assert_equal(res.status_code, 403)

Functional tests
****************

Functional tests in the OSF also use webtest. These tests mimic how a user would interact with the application through their browser.

Things to test:

- User interactions, such as clicking on links, `filling out forms <http://webtest.readthedocs.org/en/latest/forms.html>`_
- Content that you expect to appear on the page.

.. code-block:: python

    from tests.base import OsfTestCase
    from tests.factories import ProjectFactory, AuthUserFactory

    class TestProjectDashboard(OsfTestCase):

        def setUp(self):
            OsfTestCase.setUp(self)
            self.user = AuthUserFactory()
            self.project = ProjectFactory(creator=self.user)

        # Use line comments to write out user stories
        def test_can_access_wiki_from_project_dashboard(self):
            # Goes to project dashboard (user is logged in)
            url = self.project.web_url_for('view_project')
            res = self.app.get(url, auth=self.user.auth)

            # Clicks the Wiki link,
            # follows redirect to wiki home page
            res = res.click('Wiki').follow()

            # Sees 'home' on the page
            assert_in('home', res)


.. note::

    The :meth:`TestResponse.showbrowser()` method is especially useful for debugging functional
    tests. It allows you to open the current page in your browser at a given point in the test.

    .. code-block:: python

        res = self.app.get(url)
        res.showbrowser()  # for debugging

    Just be sure to remove the line when you are done debugging.


Javascript tests
****************
