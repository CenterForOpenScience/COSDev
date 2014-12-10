Developing an addon
===================

**In Progress**: Help out by sending a PR!

Notes and gotchas
*****************

- A new AddonSettings record is created upon enabling your addon's checkbox on the user settings page and submitting the form. You should *not* instantiate an `MyAddonUserSettings` object yourself
- The view for rendering a file **must** include the return value of `website.project.util.serialize_project` (an alias of `_view_project`).
- The view for rendering a file **must** use `website.addons.base.views.check_file_guid` and redirect if necessary
- `to_json` returns the mako context for the settings pages
- Log templates: the `id` of each script tag correspond to log actions.
- Don't forget to do error handling! This includes handling errors that might occur if 3rd party HTTP APIs cause a failure and any exceptions that a client library might raise
- Any static assets that you put in ``website/addons/<addon_name>/static/`` will be served from ``/static/addons/<addon_name>/``. This means that ``<link>`` and ``<script>`` tags should always point to URLs that begin with ``/static/``.

Installing Addons
*****************


Open terminal and switch to the folder where your OSF installation is located. We will install the addons to the website folder. So navigate to

::

    cd website/addons

During your installation you created a virtual environment for OSF. Switch to the environment by typing workon followed by the name of your virtual environment

::

    # If you use virtualenvwrapper
    $ workon osf

Addon cookiecutter
------------------

While this should not be used when creating your first add-on, the Cookie cutter is designed to get you started with a new addon by filling out standard information and using boilerplate code to connect your add on.

Install Cookiecutter

::

    $ pip install cookiecutter

Then run the following to create the project scaffold.

::

    $ cookiecutter https://github.com/chrisseto/osf-Addon-cookiecutter.git

This will prompt a few questions:

**full_name (default is "Amazon Simple Storage Service")?**: Enter a descriptive name that can have spaces. Describe your add on in a few words.

**short_name (default is "s3")?**: Enter a lowercase, single word name. This name will be used in the file structure and as variables. You can use CamelCase if you need to have more words, or you can combine with numbers, but don't use any spaces or hyphens.

**categories (default is "'storage'")?**: Enter a one word category, lowercase.


Logs
****

Some common log examples

- ``dropbox_node_authorized``
- ``dropbox_node_authorized``
- ``dropbox_file_added``
- ``dropbox_file_removed``
- ``dropbox_folder_selected``, ``github_repo_linked``, etc.

Use the ``NodeLog`` class's named constants when possible,

.. code-block:: python

    'dropbox_' + NodeLog.FILE_ADDED

Every log action requires a template in ``youraddon/templates/log_templates.mako``. Each template's id corresponds to the name of the log action.


Static files for addons
***********************

.. todo:: Add detail.

The following files in the ``static`` folder of your addon directory will be built by webpack:

- user-cfg.js : Executed on the user addon configuration page.
- node-cfg.js : Executed on the node addon configuration page.
- files.js : Executed on the files page of a node.

**You do not have to include these files in a ``<script>`` tag in your templates.** They will dynamically be included when your addon is enabled.

Rubeus and the FileBrowser
**************************

For an addon to be included in the files view they must first define the following in the addon's ``__init__.py``:

.. code-block:: python

    HAS_HGRID_FILES = True
    GET_HGRID_DATA = views.hgrid.{{addon}}_hgrid_data


Has hgrid files is just a flag to attempt to load files from the addon.
get hgrid data is a function that will return FileBrowser formatted data.


Rubeus
------

Rubeus is a helper module for filebrowser compatible add ons.

``rubeus.FOLDER,KIND,FILE`` are rubeus constants for use when defining filebrowser data.

``rubeus.to_hgrid`` Todo document me

``rubeus.build_addon_root``:

Builds the root or "dummy" folder for an addon.

::

    :param node_settings addonNodeSettingsBase: Addon settings

    :param name String: Additional information for the folder title

        eg. Repo name for Github or bucket name for S3

    :param permissions dict or Auth: Dictionary of permissions for the addon's content or Auth for use in node.can_X methods

    :param urls dict: Hgrid related urls

    :param extra String: Html to be appened to the addon folder name

        eg. Branch switcher for github

    :param kwargs dict: Any additional information to add to the root folder

    :return dict: Hgrid formatted dictionary for the addon root folder


Rendering files
***************

First requirement here is a render template, which should consist mainly of 1. the rendered file 2. a version history of the file

Building File GUIDs
*******************

whenever a file is rendered a GUID should be created for it

.. code-block:: python

    try:
        guid = S3GuidFile.find_one(
            Q('node', 'eq', node) &
            Q('path', 'eq', path)
        )
    except:
        guid = S3GuidFile(
            node=node,
            path=path,
        )
        guid.save()

    redirect_url = check_file_guid(guid)
    if redirect_url:
        return redirect(redirect_url)`


Deselecting and Deauthorizing
-----------------------------

Many add-ons will have both user and node settings. It is important to ensure that, if a user's add-on settings are deleted or authorization to that add-on is removed, every node authorized by the user is deauthorized, which includes resetting all fields including its user settings.

It is necessary to override the ``delete`` method for ``MyAddonUserSettings`` in order to clear all fields from the user settings.

.. code-block:: python

    class MyAddonUserSettings(AddonUserSettingsBase):

        def delete(self):
            self.clear()
            super(MyAddonUserSettings, self).delete()

        def clear(self):
            self.addon_id = None
            self.access_token= None
            for node_settings in self.myaddonnodesettings__authorized:
                node_settings.deauthorize(Auth(self.owner))
                node_settings.save()
            return self

You will also have to override the ``delete`` method for ``MyAddonNodeSettings``.

.. code-block:: python


    class MyAddonNodeSettings(AddonNodeSettingsBase):

        def delete(self):
            self.deauthorize(Auth(self.user_settings.owner), add_log=False)
            super(AddonDataverseNodeSettings, self).delete()

        def deauthorize(self, auth, add_log=True):
            self.example_field = None
            self.user_settings = None

            if add_log:
                ...

IMPORTANT Privacy Considerations
********************************

Every add-on will come with its own unique set of privacy considerations. There are a number of ways to make small errors with a *large* impact.

General

- **Using ``must_be_contributor_or_public``, ``must_have_addon``, etc. is not enough.** While you should make sure that you correctly decorate your views, that does not ensure that *non-OSF*-related permissions have been handled.
- For file storage add-ons, make sure that contributors can only see the folder that the authorizing user has selected to share.
- Think carefully about security when writing the node settings view ({{addon}}_node_settings.mako / {{addon}}NodeConfig.js}}. For example, in the GitHub add-on, the user should only be able to see the list of repos from the authenticating account if the user is the authenticator for the current node. Most add-ons will need to tell the view (1) whether the current user is the authenticator of the current node and (2) whether the current user has added an auth token for the current add-on to her OSF account.

Example: When a Dropbox folder is shared on a project, contributors (and the public, if the project is public) should only perform CRUD operations on files and folders that are within that shared folder. An error should be thrown if a user tries to access anything outside of that folder.

.. code-block:: python

    @must_be_contributor_or_public
    @must_have_addon('dropbox', 'node')
    def dropbox_view_file(path, node_addon, auth, **kwargs):
        """Web view for the file detail page."""
        if not path:
            raise HTTPError(http.NOT_FOUND)
        # check that current user was the one who authorized the Dropbox addon
        if not is_authorizer(auth, node_addon):
            # raise HTTPError(403) if path is a not a subdirectory of the shared folder
            abort_if_not_subdir(path, node_addon.folder)
        ...

Make sure that any view (CRUD, settings views...) that accesses resources from a 3rd-party service is secured in this way.
