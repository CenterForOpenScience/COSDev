COS Development Docs
====================

To get requirements: ::

    $ pip install -r requirements.txt


To build the docs: ::

    $ invoke docs -wb


The ``-w`` option will trigger builds when files change.
The ``-b`` option will open the built docs in your browser.

The docs will be served at http://127.0.0.1:1234.
