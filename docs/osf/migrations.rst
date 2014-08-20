Migrations
==========


- Migrations go in the ``scripts/`` directory.
- Use a ``main()`` function which runs the migration. Avoid import side-effects.
- When possible, include a function that lists the records that will be affected by the migration. These are useful in an interactive session for doing dry runs.

.. code-block:: python

    def get_targets():
        """Generate the nodes to migrate."""
        return (node for node in Node.find(Q('category', 'nin', Node.VALID_CATEGORIES)))

- Migrations should have automated tests. These can go in the same file as the migration script.

Below is the skeleton of an example migration.

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    """Script to migrate nodes with invalid categories."""

    import sys

    from website.app import init_app
    from tests.base import OsfTestCase

    def do_migration(records):
        # ... perform the migration ...

    def get_targets():
        # ... return the StoredObjects to migrate ...

    def main():
        init_app(routes=False)  # Sets the storage backends on all models
        if 'dry' in sys.argv:
            # print list of affected nodes, totals, etc.
        else:
            do_migration(get_targets())

    class TestMigrateNodeCategories(OsfTestCase):

        def test_get_targets(self):
            # ...

        def test_do_migration(self):
            # ...

    if __name__ == '__main__':
        main()


After performing a migration
----------------------------

After running a migration script on a production machine, add a timestamped log in the docstring of the script, documenting what was done.

.. code-block:: python

    """Script to remove invalid GUID tag objects from the database.

    Log:

        Performed on production by sloria on 2014-08-15 at 11.45AM. 892 invalid GUID
        objects were removed.
    """
