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
