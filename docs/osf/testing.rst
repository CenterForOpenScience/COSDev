.. _osftesting:

Testing the OSF
===============

This page includes information about testing the OSF codebase.

.. seealso::

     For more general testing guidelines, see the :ref:`Testing <testing>` page.


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


Unit Tests
**********

Testing Models
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

Views Tests
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

Functional Tests
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

Regression Tests
****************

Regression tests may fall under any one of the categories above (unit, model, views, functional). If you write a regression test for a specific issue, it is often helpful to link to the issue in a line comment above the test.

.. code-block:: python

    # Regression test for https://github.com/CenterForOpenScience/openscienceframework.org/issues/1136
    def test_cannot_create_project_with_blank_name(self):
        # ...


Javascript Tests
****************

Running tests
-------------

Before running tests, make sure you have the dependencies installed. ::

    $ npm install

Javascript tests are run with ::

    $ inv karma

This will start a `Karma <https://karma-runner.github.io/>`_ process which will run the tests on every JS code change.

You can specify which browser to run your tests against by passing the ``--browser`` (or ``-b``, for short) option. ::

    $ inv karma -b Chrome

Chrome and Firefox are supported after you've run ``npm install``. To run on other browsers, install the appropriate launcher with ``npm`` (see `here <https://karma-runner.github.io/0.12/config/browsers.html>`_ for available launchers). ::

    $ npm install karma-safari-launcher
    $ inv karma -b Safari

Writing Tests
-------------

We use the following libraries for writing tests:

- `Mocha <http://mochajs.org/>`_: Provides the interface for test cases.
- `Chai <http://chaijs.com/>`_: Provides assertion functions.
- `Sinon <http://sinonjs.org/>`_: Provides test spies, stubs, and mocks.

See the official docs for these libraries for more information.

OSF-specific Guidelines
+++++++++++++++++++++++

- Core OSF tests go in `website/static/js/tests/`. Addons tests go in `website/addons/<addon_name>/static/tests/`
- Karma will run every module that has the ``.test.js`` extension.
- Use Chai's ``assert`` `interface <http://chaijs.com/api/assert/>`_.
- To mock HTTP requests, use the ``createServer`` utility from the ``js/tests/utils`` module.


Gotchas and Pitfalls
++++++++++++++++++++

- When mocking out endpoints with sinon, be careful when dealing with URLs that accept query parameters. You can pass a regex as a ``url`` value to ``createServer``.

.. code-block:: javascript

    var endpoints = {
        // Use regex to handle query params
        {url: /\/api\/users\/.+/, response: {...}}
    ];
    server = utils.createServer(sinon, endpoints);

- Remember for async tests, you need to pass and call the 'done' callback. Failing to pass and call done in async tests can cause unpredictable and untracable errors in your test suite.
In particular you might see failed assertions from another test being printed to the console as if they're happening in some other test. Since we're concatenating test files together with webpack,
this error could be coming from any of the tests run before the error occurs (maybe from another file altogether).

.. code-block:: javascript

    describe('My feature', () => {
      ...
      it('Does something asnyc', (done) => {
         myFeature.myAsyncFunction()
           .always(function() {
             // make some assertions
             done();
           });
      });
    });


Test Boilerplate
----------------

The following boilerplate should be included at the top of every test module.

.. code-block:: javascript

    /*global describe, it, expect, example, before, after, beforeEach, afterEach, mocha, sinon*/
    'use strict';
    var assert = require('chai').assert;
    // Add sinon asserts to chai.assert, so we can do assert.calledWith instead of sinon.assert.calledWith
    sinon.assert.expose(assert, {prefix: ''});

Debugging tests
---------------

- Run karma: ``inv karma``
- Browse to ``localhost:9876`` in your browser.
- Click the DEBUG button on the top right.
- Open dev tools and open up the debugger tab.
- Add breakpoints or ``debugger;`` statements where necessary.
