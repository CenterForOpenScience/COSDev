Issue Management
================

We are currently using `HuBoard`_ for issue management.

Columns are defined as follows:

- **Deferred**: Issues not ready to be claimed. These may still be under discussion or need more information.
- **Ready**: Issues ready to be claimed. Check here to see if you are assigned to an issue.
- **Working**: Issues being actively addressed by one or more developers.
- **Pending Review**: Issues that have been implemented, have automated tests, and have a pull request sent to COS/develop (for feature branches) or COS/master (for hotfixes)
- **Ready to Merge**: Code review complete, all appropriate tests are written and passing. Ready to merge into COS/develop and deploy to staging.
- **On Staging**: Feature is on staging server, ready for manual testing

.. _HuBoard: https://huboard.com/CenterForOpenScience/osf.io
