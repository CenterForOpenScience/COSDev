OSF Guidelines
==============

General
*******

- For node endpoints, use ``node.url_for`` and ``node.api_url_for`` for URL lookup

.. code-block:: python

    # Assuming a URL Rule:
    # Rule(
    #     [
    #         '/project/<pid>/tags/<tid>',
    #         '/project/<pid>/node/<nid>/tags/<tid>/',
    #     ],
    #      'put',
    #      node_views.node_tags_put,
    #      json_renderer,
    # )

    # Yes
    # Pass the name of the view function and URL params as keyword arguments
    url = node.api_url_for('node_tags_put', tid=tag._id)
    # => /project/1rdsf/tags/mytag/

    # No
    url = os.path.join('/api', 'v1', node._primary_key, 'tags', tag._id)

- Use ``website.utils.api_url_for`` and ``website.utils.web_url_for`` for general URL lookup.

.. code-block:: python

    # Yes
    from website.utils import api_url_for
    url = api_url_for('user_settings')

    # No
    url = os.path.join('/user', 'settings')

- Use the above functions in Mako templates; they are available by default.

.. code-block:: html+mako

    <!-- Yes -->
    <p>Visit your <a href="${ web_url_for('user_settings') }">user settings</a>.

    <!-- No -->
    <p>Visit your <a href="/settings/">user settings</a>.

Views
*****

- If a decorator injects keyword arguments, declare the keyword arguments whenever possible. Avoid pulling them from the kwargs dictionary.

.. code-block:: python

    # Yes
    @must_be_logged_in
    def user_settings_put(auth, **kwargs):
        #...

    # No
    @must_be_logged_in
    def user_settings_put(**kwargs):
        auth = kwargs['auth']
        #...

    # Exception: when node and/or project are injected, you must pull off kwargs
    @must_be_contributor_or_public
    def get_project_comments(auth, **kwargs):
        node = kwargs['node'] or kwargs['project']
        # ...

- Use ``framework.flask.redirect`` to return redirect responses. It has the same functionality as ``flask.redirect`` except that it will reappend querystring parameters for view-only links when necessary. Do **not** use ``flask.redirect``.

Responses
*********

- Use `correct HTTP status codes <http://www.restapitutorial.com/httpstatuscodes.html>`_. You can used the constants in ``httplib`` to help.

.. code-block:: python

    # Yes
    @must_be_logged_in
    def user_token_post(auth, **kwargs):
        #...
        return serialized_settings, 201
        # OR
        # return serialized_settings, httplib.CREATED

    # No
    @must_be_logged_in
    def user_token_post(auth, **kwargs):
        #...
        return serialized_settings  # Implicitly returns 200 response

- Be consistent with your response format.

 **TODO**: Come up with a standard format. The Dropbox add-on uses the following, though we may decide on a different convention later.

::

    {
        "result": {"name": "New Project", "id": ...} # ... the requested object(s) ,
        "message": "Successfully created project" # ... an optional message
    }

- Prefer namespaced representations to arbitrary prefixes in response data.

.. code-block:: javascript

    // Yes
    {
        'node': {
            '_id': '123abc',
            'urls': {
                'api': '/api/v1/123abc',
                'web': '/123abc/'
            }
        },
        'urls': {
            'latest': '/files/some-file-id/latest/',
            'detail': '/files/some-file-id/'
        }
    }

    // No
    {
        'node_id': '123abc',
        'node_api_url': '/api/v1/123abc',
        'node_web_url': '/123abc/',
        'latest_file_url': '/files/some-file-id/latest/',
        'file_detail_url': '/files/some-file-id/'
    }

Running Migrations
******************

Migrations are located in the ``scripts`` directory.

To run them: ::

    $ python -m scripts.script_name

To migrate search records:

::

    invoke migrate_search

Error Handling
**************

Server-side
-----------

If a view should return an error response, raise a ``framework.exceptions.HTTPError``, optionally passing a short and long message. This will ensure that a properly formatted HTML or JSON response is returned (depending on whether the route is an API or web route). **Do NOT** return a dictionary.

.. code-block:: python

    from framework.exceptions import HTTPError

    @must_be_logged_in
    def user_settings_get(auth, **kwargs):
        """Return the current user's settings."""
        try:
            settings = get_user_settings(auth)
        except ModularOdmException:
            raise HTTPError(404,
                msg_short='User not found',
                msg_long='The user could not be in our database.'
            )
        return serialized_settings(settings), 200

Client-side
-----------

All client-side HTTP requests should have proper error handlers. As an example, you might display an error message in a modal if a request fails.

.. note::

    Use `RavenJS <https://raven-js.readthedocs.org/en/latest/>`_ (a JS client for Sentry) to log unexpected errors to our Sentry server.


.. code-block:: javascript

    var url = '/api/v1/profile';
    var request = $.osf.putJSON(url, {'email': 'foo@bar.com'});

    request.done(function(response) { ... });

    request.fail(function(jqxhr, status, error) {
        bootbox.alert({
            title: "Error",
            message: "We're sorry. Your profile could not be updated at this time. Please try again later."
        });
        // Log error to Sentry
        // Add context (e.g. error status, error messages) as the 2nd argument
        Raven.captureMessage('Error while updating user profile', {
            url: url, status: status, error: error
        });
    });

When appropriate, you can use the generic `$.osf.handleJSONError`, which will display a generic error message in a modal to the user if a failure occurs.

.. code-block:: javascript

    // ...
    request.fail($.osf.handleJSONError);

Documentation
*************

Docstrings
----------

- Write function docstrings using Sphinx conventions (see `here <https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions>`_).
- For parameters that are not passed directly to the function (e.g. query string arguments, POST arguments), include the source of the parameter in the docstring:

.. code-block:: python

    def my_view(my_param):
        """Do something rad.

        :param str my_param: My directly passed parameter
        :param-query str foo: A parameter included in the query string; look me up in `request.args`
        :param-post str bar: A parameter included in the POST payload; look me up in `request.form`
        :param-json str baz: A parameter included in the JSON payload; look me up in `request.json`

        """
        # Rad code here


Misc
****

Generating fake data
--------------------

1. Install fake-factory
::

    $ pip install fake-factory


2. Create your an account on your local osf. Remember the email address you use.

3. Run the fake data generator script, passing in your username (email)
::

    $ python -m scripts.create_fakes --user fred@cos.io


where ``fred@cos.io`` is the email of the user you created.

After you run the script, you will have 3 fake projects, each with 3 fake contributors (with you as the creator).

Dialogs
-------

We use `Bootbox <http://bootboxjs.com/>`_ to generate modal dialogs in the OSF. When calling a ``bootbox`` method, always pass in an object of arguments rather than positional arguments. This allows you to include a title in the dialog.


.. code-block:: javascript

    // Yes
    bootbox.confirm({
        title: 'Permanently delete file?',
        message: 'Are you sure you want to delete this file?',
        callback: function(confirmed) {
            // ..
        }
    })

    // No
    bootbox.confirm('Are you sure you want to delete this file?',
        function(confirmed) {
            // ...
        }
    )
