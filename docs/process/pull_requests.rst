.. _pull_requests:

Sending a Pull Request
======================

Use the following checklist to make sure your pull request can be reviewed and merged as efficiently as possible:

- For projects that use git-flow (such as the OSF): Feature branches should request to the ``develop`` branch. Hotfix branches should request to the ``master`` branch.
- New features must be :ref:`tested appropriately <testing>` (views, functional, and/or unit tests). Fixes should include regression tests.
- Your code must be sufficiently documented. Add docstrings to new classes, functions, and methods.
- Your code must be passing on TravisCI.
- Feel free to reference relevant Github issues in the PR description.
- On Github, rename your pull request with the prefix "Feature" or "Hotfix", as appropriate.
- Write a descriptive Pull Request description. Ideally, it should communicate:
    - The purpose of the changes you made.
    - Which Github issue the PR addresses, if applicable.
    - If you are only sending the PR for code review and not for merge, make this very clear. Include a note such as: "Sending for review **only**. Do not merge. Please review feature X; feature Y is still a work in progress."
    - Potential concerns, esp. regarding security, privacy, and provenance, which will requires extra care during review.
