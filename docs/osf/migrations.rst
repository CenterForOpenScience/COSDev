Migrations
==========


- Migrations go in the ``scripts/`` directory.
- Use a ``main()`` function which runs the migration. Avoid import side-effects.
- When possible, include a function that lists the records that will be affected by the migration. These are useful in an interactive session.
- Migrations should have automated tests.
