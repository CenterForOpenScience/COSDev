.. _javascript_style:

Javascript
==========

Style guidelines for writing Javascript.

.. seealso::
    Writing a JS module for the OSF? See the :ref:`Javascript Modules <osf_js_modules>` page in the OSF section.

Style
*****

Follow `Felix's Node Style <https://github.com/felixge/node-style-guide>`_ and `airbnb's Style Guide <https://github.com/airbnb/javascript/tree/es5-deprecated/es5>`_ with a few exceptions:

- Use **4 spaces** for indentation.
- Use ``self`` to save a reference to ``this``.


Errors
******

- Always throw ``Error`` instances, not strings.

.. code-block:: javascript

    // Yes
    throw new Error('Something went wrong');

    // No
    throw 'Something went wrong';

    // No
    throw Error('Something went wrong');


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


Promises
********

- Prefer promises to callbacks.

.. code-block:: javascript

    // Yes
    function makeRequest() {
        var request = $.getJSON('/api/projects/');
        return request;
    }
    var request = makeRequest();
    request.done(function(response) { console.log(response); })

    // No
    function makeRequest(callback){
        $.getJSON('/api/projects/', function(response) {
            callback && callback(response);
        }) ;
    }
    makeRequest(function(response) {console.log(response)});


- When doing AJAX requests or other async work, it's often useful to return a promise that resolves to a useful value (e.g. model objects or "unwrapped" responses).

.. code-block:: javascript

    function User(data) {
        this._id = data._id;
        this.username = data.username;
    }

    /** Return a promise that resolves to a list of Users */
    var getUsers = function() {
        var ret = $.Deferred();

        var request = $.getJSON('/users/');
        request.done(function(response) {
            var users = $.map(response.users, function(data){
                return User(data);
            });
            ret.resolve(users);
        });
        request.fail(function(xhr, status, error) {
            Raven.captureMessage(...);
            ret.reject(xhr, status, error);
        });
        return ret.promise();
    };

    getUsers().done(function(users){ 
        users.forEach(function(user)){
            console.log(user._id); 
            console.log(user.username); 
        };
    })


Encapsulation
*************

Use the Combination Constructor/Prototype pattern for encapsulation. You can use the following functions to provide syntactic sugar for creating "classes":

.. code-block:: javascript
    
    function noop() {}

    function defclass(prototype) {
        var constructor = prototype.hasOwnProperty('constructor') ? prototype.constructor : noop;
        constructor.prototype = prototype;
        return constructor;
    }
    
    function extend(cls, sub) {
        var prototype = Object.create(cls.prototype);
        for (var key in sub) { prototype[key] = sub[key]; }
        prototype.super = cls.prototype;
        return defclass(prototype);
    }

    // Example usage:
    var Animal = defclass({
        constructor: function(name) {
            this.name = name || 'unnamed';
            this.sleeping = false;
        },
        sayHi: function() {
            console.log('Hi, my name is ' + this.name);
        }
    });
 
    var Person = extend(Animal, {
        constructor: function(name) {
            this.super.constructor.call(name);
            this.name = name || 'Steve';
        }
    });


.. note::

    In the OSF, the ``defclass`` and ``extend`` functions are available in the ``oop.js`` module.

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
