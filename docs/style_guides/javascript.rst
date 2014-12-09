Javascript
==========

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

For PUTting and POSTing to JSON endpoints in the OSF, use the ``$.osf.postJSON`` and ``$.osf.putJSON`` functions (located in ``site.js``). This will handle JSON stringification as well as set the correct dataType and contentType.

When using ``$.osf.postJSON``, ``$.osf.putJSON``, or ``jQuery.ajax``, use the Promises interface.

.. code-block:: javascript

    function successHandler(response) { ... }
    function failureHandler(jqXHR, status, error) {...}


    var request = $.ajax({ ... });
    request.done(successHandler);
    request.fail(failureHandler);

    // OR
    $.ajax({ ... }).then(successHandler, failureHandler);

Utility functions
-----------------

Put any reusable helper functions and plugins on the ``$.osf`` namespace. **Do not pollute the global namespace.**

.. code-block:: javascript

    $.osf.myCopaceticFunction = function() {...}

Writing modules in the OSF
**************************

- Use the CommonJS module style.
- Use the Combination Constructor/Prototype pattern for encapsulation (it's simpler than it sounds). A good write-up on this can be found `here <http://javascriptissexy.com/oop-in-javascript-what-you-need-to-know/#Encapsulation_in_JavaScript>`_.
- Reuseable modules go in ``website/static/js/``. Name modules in ``lowerCamelCase``.
- Initialization code for a single web page goes in module within ``website/static/js/pages/``. Name page modules with ``lower-dashed-case``.

**website/static/js/osfMarkdownParser.js**

.. code-block:: javascript
    
    /**
     * A Markdown parser with special syntax for linking to 
     * OSF projects.
    **/
    'use strict';

    // CommonJS/Node-style imports at the top of the file
    
    var $osf = require('osf-helpers');

    // Private methods go up here
    function someHelper() {
        // ....
    }
    // This is the public API
    // The constructor
    function OSFMarkdownParser (selector, options) {
        this.selector = selector;
        this.options = options;
        this.init();
    }
    // Methods
    OSFMarkdownParser.prototype.init = function() {
        //...
    }

    OSFMarkdownParser.prototype.somePublicMethod = function() {
        //...
    }

    module.exports = OSFMarkdownParser;

**website/static/js/pages/wiki-edit-page.js**

.. code-block:: javascript

    // Initialization of the Markdown parser

    var OSFMarkdownParser = require('../osfMarkdownParser.js');

    new OSFMarkdownParser('#wikiInput', {...});


Each module in ``website/static/js/pages`` corresponds to an entry point in `webpack <https://webpack.github.io/docs/multiple-entry-points.html>`_. 

**webpack.config.js**

.. code-block:: javascript

    // Entry points built by webpack. The keys of this object correspond to the 
    // names of the built files which are put in /website/static/public/js/. The values
    // in the object are the source files.
    var entry = {
        //...
        'project-base-page': staticPath('js/pages/project-base-page.js'),
        // ...
    }

Webpack parses the dependency graphs of these modules and builds them into single files which can be included on HTML pages. The built files reside in ``website/static/public/js``.

**website/templates/wiki/edit.mako**

.. code-block:: html

    <script src="/static/public/js/wiki-edit-page.js"></script>

Examples
--------

- `folderPicker.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/folderPicker.js>`_
- `nodeControl.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/nodeControl.js>`_ is used within `project-base-page.js <https://github.com/CenterForOpenScience/osf.io/blob/12cce5b9578c4d129f9d6f12ed78516b7e1640a0/website/static/js/pages/project-base-page.js#L4>`_. The built template is included in `project_base.mako <https://github.com/CenterForOpenScience/osf.io/blob/8a0fa0ae1c1a383cc51616c190f72d47d2ae694a/website/templates/project/project_base.mako#L65>`_


Knockout
********

A module contains the Knockout model(s) and ViewModel(s) for a single unit of funtionality (e.g. login form, contributor manager, log list, etc.)

Knockout modules aren't much different from regular modules.

- Apply bindings in the constructor. Use the ``$osf.applyBindings`` helper. This will ensure that your ViewModel will be bound to the element that you expect (and not fall back to <body>, as ``ko.applyBindings`` will sometimes do). You can also pass ``$osf.applyBindings`` a selector instead of an ``HTMLElement``.
- Name the HTML ID that you bind to with "Scope". Example: ``<div id="logfeedScope">``.
- Adding the ``scripted`` CSS class to the div you bind to will hide the div until ``$osf.applyBindings`` finishes executing. This is useful if you don't want to show any HTML for your component until the ViewModel is bound.


**website/static/js/logFeed.js**

.. code-block:: javascript

    /**
     * Renders a log feed.
     **/
    'use strict';
    var ko = require('knockout');
    var $osf = require('osf-helpers');

    /**
    * Log model.
    */
    var Log = function(params) {
        var self = this;
        self.text = ko.observable('');
        // ...
    };

    /**
    * View model for a log list.
    * @param {Log[]} logs An array of Log model objects to render.
    */
    var LogViewModel = function(logs) {
        var self = this;
        self.logs = ko.observableArray(logs);
        // ...
    };

    ////////////////
    // Public API //
    ////////////////

    var defaults = {
        data: null,
        progBar: '#logProgressBar'
    };

    function LogFeed(selector, options) {
        var self = this;
        self.selector = selector;
        self.options = $.extend({}, defaults, options);
        self.$progBar = $(self.options.progBar);
        self.logs = self.options.data.map(function(log) {
            return new Log(log.params);
        })
    };
    // Apply ViewModel bindings
    LogFeed.prototype.init = function() {
        var self = this;
        self.$progBar.hide();
        $osf.applyBindings(new LogViewModel(self.logs), self.selector);
    };

    module.exports = LogFeed;

**website/templates/some_template.mako**


.. code-block:: html

    <div class="scripted" id="logScope">
        <ul data-bind="foreach: {data: logs, as: 'log'}">
            ...
        </ul>
    </div>

    <!-- assuming there's an entry for `some-template-page` in webpack.config.js -->
    <!-- some-template-page.js would initialize the `LogFeed` class -->
    <script src="/static/public/js/some-template-page.js"></script>


Examples
--------

- `revisions.js <https://github.com/CenterForOpenScience/osf/blob/develop/website/addons/dropbox/static/revisions.js>`_ (small example)
- `Full LogFeed module <https://github.com/CenterForOpenScience/osf/blob/develop/website/static/js/logFeed.js>`_
- `comment.js <https://github.com/CenterForOpenScience/osf/blob/develop/website/static/js/comment.js>`_


Templates
*********

To help you get started on your JS modules, here are some templates that you can copy and paste.

JS Module Template
------------------

.. code-block:: javascript

    /**
     * [description]
     */
    'use strict';
    var $ = require('jquery');


    function MyModule () {
        // YOUR CODE HERE
    }

    module.exports = MyModule;


Knockout Module Template
------------------------

.. code-block:: javascript

    /**
     * [description]
     */
    'use strict';
    var ko = require('knockout');

    var $osf = require('osf-helpers');

    function ViewModel(url) {
        var self = this;
        // YOUR CODE HERE
    }

    function MyModule(selector, url) {
        this.viewModel = new ViewModel(url);
        $osf.applyBindings(this.viewModel, selector);
    }

    module.exports = MyModule;

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
