.. _javascript_style:

Javascript
==========

Style guidelines for writing Javascript.

.. seealso::
    Writing a JS module for the OSF? See the :ref:`Javascript Modules <osf_js_modules>` page in the OSF section.

Style
*****

Follow `Felix's Node Style <https://github.com/felixge/node-style-guide>`_ and `airbnb's Style Guide <https://github.com/airbnb/javascript>`_ with a few exceptions:

- Use **4 spaces** for indentation.
- Use ``self`` to save a reference to ``this``.
- One ``var`` statement per line (same as Felix's guide, but different from Airbnb's).


.. code-block:: javascript

    // yes
    var foo = 1;
    var bar = 42;
    var baz = 'qwerty';

    // no
    var foo, bar, baz;
    foo = 1;
    bar =  42;
    baz = 'qwerty';


CommonJS Modules
****************

- Group imports in the following order, separated by a blank line:

1. Third party libraries
2. Local application/library-specific imports

- ``module.exports`` are always grouped at the end of a file. Do not use ``export`` throughout the file.
- Keep testability in mind in deciding what to export.

.. code-block:: javascript

    // Yes
    module.exports = {
        SomeClass: SomeClass,
        _privateFunction: privateFunction
    }

    // Yes
    function SomeClass() { ... }
    SomeClass._privateFunction = function() {...}

    module.exports = SomeClass;

    // No
    var SomeClass = exports.SomeClass = function() { ... };
    var privateFunction = exports._privateFunction = function() { ... };


Documentation
*************

Use the `YUIDoc <https://yui.github.io/yuidoc/>`_ standard for writing JS comment blocks.

Example:

.. code-block:: javascript

    /**
    * A wrapper around the ACE editor that asynchronously loads
    * and publishes its content.
    *
    * @param {String} selector Selector for the editor element
    * @param {String} url URL for retrieving and posting content.
    */

For simple functions and methods, a single-line docstring will suffice.

.. code-block:: javascript

    /** Update the viewModel with data fetched from a server. */

jQuery
******

Follow `Abhinay Rathore's jQuery Coding Standards Guide <http://lab.abhinayrathore.com/jquery-standards/>`_.


AJAX
----

For PUTting and POSTing to JSON endpoints in the OSF, use the ``$osf.postJSON`` and ``$osf.putJSON`` functions (located in ``osfHelpers.js``). This will handle JSON stringification as well as set the correct dataType and contentType.

When using ``$osf.postJSON``, ``$osf.putJSON``, or ``jQuery.ajax``, use the Promises interface.

.. code-block:: javascript

    function successHandler(response) { ... }
    function failureHandler(jqXHR, status, error) {...}


    var request = $.ajax({ ... });
    request.done(successHandler);
    request.fail(failureHandler);

    // OR
    $.ajax({ ... }).then(successHandler, failureHandler);


Encapsulation
*************

Use the Combination Constructor/Prototype pattern for encapsulation. A good write-up on this can be found `here <http://javascriptissexy.com/oop-in-javascript-what-you-need-to-know/#Encapsulation_in_JavaScript>`_.


.. code-block:: javascript

    // Private functions/helpers
    var somePrivateFunction = function() {...}

    // Public interface is below

    // The constructor
    function Person(name) {
        var self = this;
        self.name = name;
    };

    // Methods
    Person.prototype.sayHello() = function() {
        var self = this;
        window.console.log('Greetings! My name is ' + self.name);
    };

    module.exports = {
        Person: Person,
        _somePrivateFunction: somePrivateFunction
    };

Recommended Syntax Checkers
***************************

We recommend using a syntax checker to help you find errors quickly and easily format your code to abide by the guidelines above. `JSHint <http://jshint.com>`_ is our recommended checker for Javascript. It can be installed with ``npm``: ::

    $ npm install -g jshint

There are a number of plugins for integrating jshint with your preferred text editor.

Vim

- `syntastic <https://github.com/scrooloose/syntastic>`_ (multi-language)

Sublime Text

- `Sublime Linter <https://sublime.wbond.net/packages/SublimeLinter>`_ with `SublimeLinter-jshint <https://sublime.wbond.net/packages/SublimeLinter-jshint>`_ (must install both)

PyCharm

- Follow these docs: `http://www.jetbrains.com/pycharm/webhelp/jshint.html <http://www.jetbrains.com/pycharm/webhelp/jshint.html>`_
