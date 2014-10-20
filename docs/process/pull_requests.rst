.. _pull_requests:

Sending a Pull Request
======================

Use the following checklist to make sure your pull request can be reviewed and merged as efficiently as possible:

- For projects that use git-flow (such as the OSF): Feature branches should request to the ``develop`` branch. Hotfix branches should request to the ``master`` branch.
- New features must be :ref:`tested appropriately <testing>` (views, functional, and/or unit tests). Fixes should include regression tests.
- Your code must be sufficiently documented. Add docstrings to new classes, functions, and methods.
- Your code must be passing on TravisCI.
- On Github, rename your PR title with the prefix "[feature]", "[feature fix]" (fixes to develop), or "[hotfix]", as appropriate.
- If you are sending the PR for code review only and *not* for merge, add the "[WIP]" prefix to the PR's title.
- Write a descriptive Pull Request description. Ideally, it should communicate:
    - The purpose of the changes you made.
    - Which Github issue the PR addresses, if applicable.
    - Potential concerns, esp. regarding security, privacy, and provenance, which will requires extra care during review.
- Once your PR is ready, ask for code review on Flowdock.


.. note::

    Make sure to follow the :ref:`Git style guidelines <git>`.
