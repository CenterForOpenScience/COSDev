Migrations
==========


- Migrations go in the ``scripts/`` directory.
- Use a ``main()`` function which runs the migration. Avoid import side-effects.
- When possible, include a function that lists the records that will be affected by the migration. These are useful in an interactive session for doing dry runs.

.. code-block:: python

    def get_targets():
        """Generate the nodes to migrate."""
        return (node for node in Node.find(Q('category', 'nin', Node.VALID_CATEGORIES)))

- Use Python's ``logging`` module for logging output. In addition, use ``scripts.utils.add_file_logger`` to add a file handler that will add timestamped log file in ``website.settings.LOG_PATH``.
- Add tests in the `scripts/tests` directory.

Below is the skeleton of an example migration.

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    """Script to migrate nodes with invalid categories."""

    import sys
    import logging

    from website.app import init_app
    from scripts import utils as script_utils

    logger = logging.getLogger(__name__)

    def do_migration(records, dry=True):
        # ... perform the migration ...

    def get_targets():
        # ... return the StoredObjects to migrate ...

    def main(dry=True):
        init_app(set_backends=True, routes=False, mfr=False)  # Sets the storage backends on all models
        do_migration(get_targets(), dry=dry)

    if __name__ == '__main__':
        dry = 'dry' in sys.argv
        if not dry:
            script_utils.add_file_logger(logger, __file__)
        main(dry=dry)


.. code-block:: python

    from tests.base import OsfTestCase

    class TestMigrateNodeCategories(OsfTestCase):

        def test_get_targets(self):
            # ...

        def test_do_migration(self):
            # ...


After performing a migration
----------------------------

After running a migration script on a production machine, add a timestamped log in the docstring of the script, documenting what was done.

.. code-block:: python

    """Script to remove invalid GUID tag objects from the database.

    Log:

        Performed on production by sloria on 2014-08-15 at 11.45AM. 892 invalid GUID
        objects were removed.
    """
