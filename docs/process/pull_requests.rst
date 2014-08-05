.. _pull_requests:

Sending a Pull Request
======================

Use the following checklist to make sure your pull request can be reviewed and merged as efficiently as possible:

- For projects that use git-flow (such as the OSF): Feature branches should request to the ``develop`` branch. Hotfix branches should request to the ``master`` branch.
- New features must be tested appropriately (views, functional, and/or unit tests). Fixes should include regression tests.
- Your code must be sufficiently documented. Add docstrings to new classes, functions, and methods.
- Your code must be passing on TravisCI.
- On Github, rename your pull request with the prefix "Feature: " or "Hotfix", as appropriate.
- Feel free to reference relevant Github issues in the PR description.
