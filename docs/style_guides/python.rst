Python
======

Follow `PEP8`_, when sensible.

Naming
******

- Variables, functions, methods, packages, modules
    - ``lower_case_with_underscores``
- Classes and Exceptions
    - ``CapWords``
- Protected methods and internal functions
    - ``_single_leading_underscore(self, ...)``
- Private methods
    - ``__double_leading_underscore(self, ...)``
- Constants
    - ``ALL_CAPS_WITH_UNDERSCORES``

General Naming Guidelines
-------------------------

Use singlequotes for strings, unless doing so requires lots of escaping.

Avoid one-letter variables (esp. ``l``, ``O``, ``I``).

*Exception*: In very short blocks, when the meaning is clearly visible from the immediate context

.. code-block:: python

    for e in elements:
        e.mutate()

Avoid redundant labeling.

.. code-block:: python

    # Yes
    import audio

    core = audio.Core()
    controller = audio.Controller()

    # No
    import audio

    core = audio.AudioCore()
    controller = audio.AudioController()

Prefer "reverse notation".

.. code-block:: python

    # Yes
    elements = ...
    elements_active = ...
    elements_defunct = ...

    # No
    elements = ...
    active_elements = ...
    defunct_elements ...


Avoid getter and setter methods.


.. code-block:: python

    # Yes
    person.age = 42

    # No
    person.set_age(42)


Indentation
***********

Use 4 spaces--never tabs. You may need to change the settings in your
text editor of choice.

Imports
*******

Import entire modules instead of individual symbols within a module. For example, for a top-level module `canteen` that has a file `canteen/sessions.py`,

.. code-block:: python

    # Yes

    import canteen
    import canteen.sessions
    from canteen import sessions

    # No
    from canteen import get_user  # Symbol from canteen/__init__.py
    from canteen.sessions import get_session  # Symbol from canteen/sessions.py

*Exception*: For third-party code where documentation explicitly says to import individual symbols.

*Rationale*: Avoids circular imports. See `here <https://sites.google.com/a/khanacademy.org/forge/for-developers/styleguide/python#TOC-Imports>`_.

Put all imports at the top of the page with three sections, each separated by a blank line, in this order:

1. System imports
2. Third-party imports
3. Local source tree imports

*Rationale*: Makes it clear where each module is coming from.

If you have intentionally have an unused import that exists only to make imports less verbose, be explicit about it. This will make sure that someone doesn't accidentally remove the import (not to mention that it keeps linters happy)


.. code-block:: python

    from my.very.distant.module import Frob

    Frob = Frob

String formatting
*****************

Prefer ``str.format`` to "%-style" formatting.

.. code-block:: python

    # Yes
    'Hello {}'.format('World')
     # OR
    'Hello {name}'.format(name='World')

    # No

    'Hello %s' % ('World', )

Print statements
****************

Use the ``print()`` function rather than the ``print`` keyword (even if you're using Python 2).

.. code-block:: python

    # Yes
    print('Hello {}'.format(name))

    # No
    print 'Hello %s ' % name

Documentation
*************

Follow  `PEP257`_'s docstring guidelines. `reStructured Text <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ and `Sphinx <http://sphinx-doc.org/>`_ can help to enforce these standards.

All functions should have a docstring - for very simple functions, one line may be enough:

::

    """Return the pathname of ``foo``."""


Multiline docstrings should include:

- Summary line
- Use case, if appropriate
- Args
- Return type and semantics, unless ``None`` is returned

::

    """Train a model to classify Foos and Bars.

    Usage::

        >>> import klassify
        >>> data = [("green", "foo"), ("orange", "bar")]
        >>> classifier = klassify.train(data)

    :param train_data: A list of tuples of the form ``(color, label)``.
    :return: A trained :class:`Classifier <Classifier>`
    """

Notes

- Use action words ("Return") rather than descriptions ("Returns").
- Document ``__init__`` methods in the docstring for the class.

.. code-block:: python

    class Person(object):
        """A simple representation of a human being.

        :param name: A string, the person's name.
        :param age: An int, the person's age.
        """
        def __init__(self, name, age):
            self.name = name
            self.age = age

On Comments
***********

Use them sparingly. Prefer code readability to writing a lot of comments. Often, small methods and functions are more effective than comments.

.. code-block:: python


    # Yes
    def is_stop_sign(sign):
        return sign.color == 'red' and sign.sides == 8

    if is_stop_sign(sign):
        stop()

    # No
    # If the sign is a stop sign
    if sign.color == 'red' and sign.sides == 8:
        stop()

When you do write comments, use them to explain *why* a piece code was used, not *what* it does.

Method Overrides
----------------

One useful place for comments are method overrides.


.. code-block:: python

    class UserDetail(generics.RetrieveUpdateAPIView, UserMixin):

        # overrides RetrieveUpdateAPIView
        def get_serializer_context(self):
            return {'request': self.request}

Calling Superclasses' Methods
*****************************

Use `super` when there is only one superclass.

.. code-block:: python

    class Employee(Person):

        def __init__(self, name):
            super(Employee, self).__init__(name)
            # or super().__init__(name) on Python 3
            # ...


Call the method directly when there are multiple superclasses.

.. code-block:: python

    class DevOps(Developer, Operations):

        def __init__(self):
            Developer.__init__(self)
            # ...

Line lengths
************

Don't stress over it. 80-100 characters is fine.

Use parentheses for line continuations.

.. code-block:: python

    wiki = (
        "The Colt Python is a .357 Magnum caliber revolver formerly manufactured "
        "by Colt's Manufacturing Company of Hartford, Connecticut. It is sometimes "
        'referred to as a "Combat Magnum". It was first introduced in 1955, the '
        "same year as Smith & Wesson's M29 .44 Magnum."
    )

Recommended Syntax Checkers
***************************

We recommend using a syntax checker to help you find errors quickly and easily format your code to abide by the guidelines above. `Flake8 <http://flake8.readthedocs.org/en/latest/>`_ is our recommended checker for Python. It will check for both syntax and style errors and is easily configurable. It can be installed with pip: ::

    $ pip install flake8


Once installed, you can run a check with: ::

    $ flake8

.. note::

    We highly recommend that you add a git hook to check your code before you commit it. You only need to run the following command once:
    ::

        # Current directory must be a git repo
        $ flake8 --install-hook

    This adds the proper hook to ``.git/hooks/pre-commit``.

There are a number of plugins for integrating Flake8 with your preferred text editor.

Vim

- `syntastic <https://github.com/scrooloose/syntastic>`_ (multi-language)

Sublime Text

- `Sublime Linter <https://sublime.wbond.net/packages/SublimeLinter>`_ with `SublimeLinter-flake8 <https://sublime.wbond.net/packages/SublimeLinter-flake8>`_ (must install both)

Credits
*******

- `PEP8`_ (Style Guide for Python)
- `Pythonic Sensibilities <http://www.nilunder.com/blog/2013/08/03/pythonic-sensibilities/>`_
- `Python Best Practice Patterns <http://youtu.be/GZNUfkVIHAY>`_


.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _PEP257: http://www.python.org/dev/peps/pep-0257/
