Version Control
===============

General Guidelines
******************

We use git for version control. Some general guidelines:

- Use Vincent Driessen's `Successful Git Branching Model <http://nvie.com/posts/a-successful-git-branching-model/>`_ (aka git-flow)
- In your **feature** branches, pull from ``develop`` frequently.
- **DO NOT** merge ``develop`` into **hotfix** branches.
- Follow the :ref:`Git style guide <git>`.
- Package and app maintainers: Use `semantic versioning <http://semver.org>`_.


Useful Tools
************

- `SourceTree <http://www.sourcetreeapp.com/>`_ - Mac OS X; GUI.
- `gitflow <https://github.com/nvie/gitflow>`_ - Cross-platform; CLI.
- `hub <https://github.com/github/hub>`_ - GitHub integration with the git CLI. Very useful for checking out pull requests.


An Important Note About Hotfixes
********************************

Many git-flow tools will try to force you to merge hotfix branches into master *before* publishing code to a hosting service (e.g. Github). Do **not** do this. Just push your hotfix branch on its own and :ref:`send a pull request <pull_requests>`. ::

    # Push a new hotfix branch up to origin
    $ git push -u origin hotfix/nav-header-size

Package and App Maintainers: Release How-to
*******************************************

Hotfix releases
---------------

- Once a hotfix PR has been checked out locally and :ref:`code review <code_review>` is complete, rename the hotfix branch with the incremented PATCH number.

::

    # hotfix/fix-serialization-bug is currently checked out
    # rename with version number
    $ git branch -m hotfix/0.16.3

- Finish the hotfix with git-flow.

::

    $ git flow hotfix finish 0.16.3

- When prompted to add a tag message, write a brief (1-2 sentence) description of the hotfix.


.. note::

    You can also use the ``release.hotfix`` invoke task to automatically rename the current hotfix branch and finish it. ::

        $ invoke hotfix --finish

- Push ``develop`` and ``master``. Push tags.


::

    $ git push origin develop
    $ git push origin master
    $ git push --tags

- Once Travis tests pass, deploy to production and staging.


Feature releases
----------------

- Once ``develop`` is ready for release, start a release branch with git-flow.

::

    $ git flow release start 0.17.0

- Update the CHANGELOG and bump the version where necessary. Commit changes.
- Finish the release with git-flow

::

    $ git flow release finish 0.17.0

- If prompted to add a tag message, write ``See CHANGELOG``.
- Push ``develop`` and ``master``. Push tags.


::

    $ git push origin develop
    $ git push origin master
    $ git push --tags

- Once Travis tests pass, deploy to production and staging.
