Javascript
==========

Style
*****

Follow `Felix's Node Style <https://github.com/felixge/node-style-guide>`_ and `airbnb's Style Guide <https://github.com/airbnb/javascript>`_ with a few exceptions:

- Use **4 spaces** for indentation.
- Use ``self`` to save a reference to ``this``.
- One ``var`` statement per line (same as Felix's guide, but different from Airbnb's).


.. code-block:: javascript

    // bad
    var foo, bar, baz;
    foo = 1;
    bar =  42;
    baz = 'qwerty';

    // good
    var foo = 1;
    var bar = 42;
    var baz = 'qwerty';

jQuery
******

Follow `Abhinay Rathore's jQuery Coding Standards Guide <http://lab.abhinayrathore.com/jquery-standards/>`_.


AJAX
----

For PUTting and POSTing to JSON endpoints in the OSF, use the ``$.osf.postJSON`` and ``$.osf.putJSON`` functions (located in ``site.js``). This will handle JSON stringification as well as set the correct dataType and contentType.


Utility functions
-----------------

Put any reusable helper functions and plugins on the ``$.osf`` namespace. **Do not pollute the global namespace.**

.. code-block:: javascript

    $.osf.myCopaceticFunction = function() {...}

Writing modules in the OSF
**************************

- Make your module compatible with `RequireJS <http://requirejs.org/>`_ or no module loader. This can be done simply by wrapping your module with a snippet, as shown in the example below.
- Use the Combination Constructor/Prototype pattern for encapsulation (it's simpler than it sounds). A good write-up on this can be found `here <http://javascriptissexy.com/oop-in-javascript-what-you-need-to-know/#Encapsulation_in_JavaScript>`_.


.. code-block:: javascript

    // website/static/js/markdownParser.js

    // Initial semicolon for safe minification
    ;(function (global, factory) {
        // Support RequireJS/AMD or no module loader
        if (typeof define === 'function' && define.amd) {
            // Dependency IDs here
            define(['jquery'], factory);
        } else { // No module loader, just attach to global namespace
            global.OSFMarkdownParser = factory(jQuery);
        }
    }(this, function($) {  // named dependencies here
        'use strict';
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

        return OSFMarkdownParser;
    }));


**website/templates/some_template.mako**

.. code-block:: html

    <script>
        $script(['/static/js/markdownParser.js'], function(){
            var markdown = new OSFMarkdownParser('#markdownEditor');
        });
    </script>

Naming Modules
--------------

Use lower camel case for the filename. The filename should correspond to the name of the exported class. For example, if you module has the ``LogFeed`` class, the JS file should be named ``logFeed.js``.

Examples
--------

- `folderPicker.js <https://github.com/CenterForOpenScience/osf/blob/develop/website/static/js/folderPicker.js>`_


Knockout
********

A module contains the Knockout model(s) and ViewModel(s) for a single unit of funtionality (e.g. login form, contributor manager, log list, etc.)

Knockout modules aren't much different from regular modules.

- Apply bindings in the constructor. Use the ``$.osf.applyBindings`` helper. This will ensure that your ViewModel will be bound to the element that you expect (and not fall back to <body>, as ``ko.applyBindings`` will sometimes do). You can also pass ``$.osf.applyBindings`` a selector instead of an ``HTMLElement``.
- Name the HTML ID that you bind to with "Scope". Example: ``<div id="logfeedScope">``.
- Adding the ``scripted`` CSS class to the div you bind to will hide the div until ``$.osf.applyBindings`` finishes executing. This is useful if you don't want to show any HTML for your component until the ViewModel is bound.


**website/static/js/logFeed.js**

.. code-block:: javascript

    /**
     * Renders a log feed.
     */
    ;(function (global, factory) {
        if (typeof define === 'function' && define.amd) {
            // The osfutils module (site.js) contains $.osf.applyBindings
            define(['knockout', 'jquery', 'osfutils'], factory);
        } else {
            global.RevisionTable  = factory(ko, jQuery);
        }
    }(this, function(ko, $) {
        'use strict';
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
            $.osf.applyBindings(new LogViewModel(self.logs), self.selector);
        };

        return LogFeed;
    }));

**website/templates/some_template_with_logs.mako**


.. code-block:: html

    <div class="scripted" id="logScope">
        <ul data-bind="foreach: {data: logs, as: 'log'}">
            ...
        </ul>
    </div>

    <%def name="javascript_bottom()">
        <script>
            // Initialize the LogFeed
            $script(['/static/js/logFeed.js'], function() {
                var logFeed = new LogFeed("#logScope", {
                    data: // Array of logs...
                });
            });
        </script>
    </%def>

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
    ;(function (global, factory) {
        if (typeof define === 'function' && define.amd) {
            define(['jquery'], factory);
        } else {
            global.MyModule  = factory(jQuery);
        }
    }(this, function($) {
        'use strict';

        function MyModule () {
            // YOUR CODE HERE
        }

        return MyModule;

    }));

Knockout Module Template
------------------------

.. code-block:: javascript

    /**
     * [description]
     */
    ;(function (global, factory) {
        if (typeof define === 'function' && define.amd) {
            define(['knockout', 'jquery', 'osfutils'], factory);
        } else {
            global.MyModule  = factory(ko, jQuery);
        }
    }(this, function(ko, $) {
        'use strict';

        function ViewModel(url) {
            var self = this;
            // YOUR CODE HERE
        }

        function MyModule(selector, url) {
            this.viewModel = new ViewModel(url);
            $.osf.applyBindings(this.viewModel, selector);
        }

        return MyModule;
    }));
