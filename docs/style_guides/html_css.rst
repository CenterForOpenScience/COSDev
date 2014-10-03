HTML and CSS
============

- Follow `mdo's Code Guide <http://mdo.github.io/code-guide/>`_, with one exception: Use four spaces for indentation (instead of two).
- Use ``.lowercase-and-dashes`` for class names and ``#camelCase`` for IDs.
- Add a comment marking the end of large blocks. Use ``<!-- end class-name -->``

.. code-block:: html

    <div class="container-fluid">
        Lots of markup...
    </div><!-- end container-fluid -->

- Avoid inline CSS. Prefer CSS classes for maintainability and reuseability.
