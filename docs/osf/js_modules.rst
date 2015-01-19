.. _osf_js_modules:

Javascript Modules How-To
=========================

This section describes how to write Javascript modules for the OSF, use `webpack <https://webpack.github.io/docs/>`_ to build assets, and include built assets in HTML. We also provide starter templates for new JS modules.

.. seealso::
    Looking for the JS style guidelines? See :ref:`here <javascript_style>` .

Writing Modules
***************

- Use the CommonJS module style.
- Reuseable modules go in ``website/static/js/``. Name modules in ``lowerCamelCase``.
- Initialization code for a page goes in a module within ``website/static/js/pages/``. Name page modules with ``lower-dashed-case``.

A Note on Utility Functions
---------------------------

Put any reusable utility functions in ``website/static/osfHelpers.js``. **Do not pollute the global namespace.**

.. code-block:: javascript

    // osfHelpers.js

    var myCopaceticFunction = function() {...}

    // ...
    module.exports = {
        // ...
        myCopaceticFunction: myCopaceticFunction
    };

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


The initialization of your Markdown parser would go in ``website/static/js/pages/wiki-edit-page.js`` (assume that this file already exists).

**website/static/js/pages/wiki-edit-page.js**

.. code-block:: javascript

    // Initialization of the Markdown parser
    var OSFMarkdownParser = require('../osfMarkdownParser.js');

    new OSFMarkdownParser('#wikiInput', {...});

    // ... other wiki-related initialization.

Third-party Libraries
*********************

The following libraries can be imported in your JS modules (using ``require('name')``):

- Any library listed in `bower.json <https://github.com/CenterForOpenScience/osf.io/blob/develop/bower.json>`_
- Any library listed in `package.json <https://github.com/CenterForOpenScience/osf.io/blob/develop/package.json>`_
- Any library listed in the `resolve.alias <https://github.com/CenterForOpenScience/osf.io/blob/d504cefa315d00f4dce3c6ca4310ad3d4e126987/webpack.common.config.js#L77-103>`_ entry of ``webpack.common.config.js``


.. note::

    Some commonly-used internal modules, such as ``osfHelpers.js`` are also aliased in ``resolve.alias``. This allows you to write ``require('osfHelpers')`` rather than ``require('relative/path/to/osfHelpers.js')``.


Building and Using Modules
**************************

Webpack Entry Points
--------------------

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

Building with Webpack
---------------------

Webpack parses the dependency graphs of the modules defined in the entry points and builds them into single files which can be included on HTML pages. The built files reside in ``website/static/public/js/``. Therefore, the built file which would include your Markdown parser initialization would be in ``/static/public/js/wiki-edit-page.<hash>.js``. This is the file that would be included in the HTML template.


.. note::
    Webpack will add a hash to the filenames of the built files to prevent users' browsers from caching old versions (example: ``wiki-edit-page.js`` becomes ``wiki-edit-page.4ec1318376695bcd241b.js``).

    Therefore, we need to resolve the short filenames to the full filenames when we include them in the HTML. More on that in the next section.

To build the assets for local development, use the ``assets`` invoke task. ::

    $ inv assets --debug --watch
    # OR
    $ inv assets -dw

Loading the Modules in HTML with ``webpack_asset``
--------------------------------------------------

Once you have the built assets, you can include them on HTML pages with a `<script>` tag. In order to resolve the short filenames to the filenames on disk (which include hashes), use the ``webpack_asset`` Mako filter.

**website/templates/wiki/edit.mako**

.. code-block:: mako

    <%def name="javascript_bottom()">
    <script src=${"/static/public/js/wiki-edit-page.js" | webpack_asset}></script>
    </%def>

Examples
--------

- `js/folderPicker.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/folderPicker.js>`_
- `js/nodeControl.js <https://github.com/CenterForOpenScience/osf.io/blob/develop/website/static/js/nodeControl.js>`_ is used within `js/pages/project-base-page.js <https://github.com/CenterForOpenScience/osf.io/blob/12cce5b9578c4d129f9d6f12ed78516b7e1640a0/website/static/js/pages/project-base-page.js#L4>`_. The built file is included in `templates/project_base.mako <https://github.com/CenterForOpenScience/osf.io/blob/d504cefa315d00f4dce3c6ca4310ad3d4e126987/website/templates/project/project_base.mako#L65>`_.


Knockout Modules
****************

A module contains the Knockout model(s) and ViewModel(s) for a single unit of funtionality (e.g. login form, contributor manager, log list, etc.)

Knockout modules aren't much different from regular modules.

- Apply bindings in the constructor.
- Use the ``osfHelpers.applyBindings`` helper. This will ensure that your ViewModel will be bound to the element that you expect (and not fall back to <body>, as ``ko.applyBindings`` will sometimes do). You can also pass ``$osf.applyBindings`` a selector instead of an ``HTMLElement``.
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

**website/static/pages/some-template-page.js**

.. code-block:: javascript

    'use strict';

    var LogFeed = require('../logFeed.js');

    // Initialize the LogFeed
    new LogFeed('#logScope', {data: ...});

**website/templates/some_template.mako**

.. code-block:: mako

    <div class="scripted" id="logScope">
        <ul data-bind="foreach: {data: logs, as: 'log'}">
            ...
        </ul>
    </div>

    <%def name="javascript_bottom()">
    <script src=${"/static/public/js/some-template-page.js" | webpack_asset}></script>
    </%def>


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

    var $osf = require('osfHelpers');

    function ViewModel(url) {
        var self = this;
        // YOUR CODE HERE
    }

    function MyModule(selector, url) {
        this.viewModel = new ViewModel(url);
        $osf.applyBindings(this.viewModel, selector);
    }

    module.exports = MyModule;
