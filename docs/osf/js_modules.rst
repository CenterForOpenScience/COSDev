.. _osf_js_modules:

Javascript Modules How-To
=========================

Writing Modules
***************

- Use the CommonJS module style.
- Reuseable modules go in ``website/static/js/``. Name modules in ``lowerCamelCase``.
- Initialization code for a page goes in a module within ``website/static/js/pages/``. Name page modules with ``lower-dashed-case``.

Example
-------

Let's say you're creating a reuseable Markdown parser module for the wiki edit page. Your module would go in ``website/static/js/``.

**website/static/js/osfMarkdownParser.js**

.. code-block:: javascript

    /**
     * A Markdown parser with special syntax for linking to
     * OSF projects.
    **/
    'use strict';

    // CommonJS/Node-style imports at the top of the file

    var $osf = require('osfHelpers');

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

    // Export the constructor
    module.exports = OSFMarkdownParser;


The initialization of your Markdown parser would go in ``website/static/js/pages/wiki-edit-page.js``. Assume that this file already exists.

**website/static/js/pages/wiki-edit-page.js**

.. code-block:: javascript

    // Initialization of the Markdown parser
    var OSFMarkdownParser = require('../osfMarkdownParser.js');

    new OSFMarkdownParser('#wikiInput', {...});

    // ... other wiki-related initialization.

Each module in ``website/static/js/pages`` corresponds to an entry point in `webpack <https://webpack.github.io/docs/multiple-entry-points.html>`_ and has a rough one-to-one mapping with a page on the OSF. Here is what the ``wiki-edit-page`` entry would look like in the webpack configuration file.

**webpack.common.config.js**

.. code-block:: javascript

    // Entry points built by webpack. The keys of this object correspond to the
    // names of the built files which are put in /website/static/public/js/. The values
    // in the object are the source files.
    var entry = {
        //...
        'wiki-edit-page': staticPath('js/pages/wiki-edit-page.js'),
        // ...
    }

.. note::

    You will seldom have to modify ``webpack.common.config.js``. The only time you may need to care about it is when a completely new page is added to the OSF.

Webpack parses the dependency graphs of these modules and builds them into single files which can be included on HTML pages. The built files reside in ``website/static/public/js``. Therefore, the built file which would include your Markdown parser initialization would be in ``/static/public/js/wiki-edit-page.js``. This is the file that would be included in the HTML template.

**website/templates/wiki/edit.mako**

.. code-block:: html

    <script src="/static/public/js/wiki-edit-page.js"></script>

Examples
--------

- `js/folderPicker.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/folderPicker.js>`_
- `js/nodeControl.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/nodeControl.js>`_ is used within `js/pages/project-base-page.js <https://github.com/CenterForOpenScience/osf.io/blob/12cce5b9578c4d129f9d6f12ed78516b7e1640a0/website/static/js/pages/project-base-page.js#L4>`_. The built template is included in `templates/project_base.mako <https://github.com/CenterForOpenScience/osf.io/blob/8a0fa0ae1c1a383cc51616c190f72d47d2ae694a/website/templates/project/project_base.mako#L65>`_.


Knockout Modules
****************

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

- `revisions.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/addons/dropbox/static/revisions.js>`_ (small example)
- `Full LogFeed module <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/logFeed.js>`_
- `comment.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/comment.js>`_

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

