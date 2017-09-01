==============================
How to add a preprint provider
==============================

Requirements
============
New preprint providers must have the following:

* A name
* A square logo
* A rectangular/wide logo
* 3 unique colors
* A list of acceptable subjects (taxonomies)
* A list of acceptable licenses 
* Emails for:

  * Contact (defaults to ``contact+provider_name@osf.io``)
  * Support (defaults to ``support+provider_name@osf.io``)

Recommended:

* A Twitter_ account
* A Facebook_ Page
* An Instagram_ account

.. _Twitter: https://twitter.com/signup
.. _Facebook: https://www.facebook.com/business/products/pages
.. _Instagram: https://business.instagram.com/gettingstarted/

Creating a new Preprint Provider
================================
1. Update the Populate Preprint Providers script
2. Format and save images to the in the ember-preprints assets directory
3. Add the config entry
4. Create the stylesheet

osf.io Updates
--------------
Create a new feature branch in the **osf.io** repository ``git checkout develop && git checkout -b feature/add-preprint-provider-provider_id``


ember-preprints Updates
-----------------------
Create a new feature branch in the **ember-preprints** repository ``git checkout develop && git checkout -b feature/add-preprint-provider-provider_id``

Formatting the images
~~~~~~~~~~~~~~~~~~~~~
In the ember-preprints repository: ``public/assets/img/provider_logos``. Commit the original images (before edits) to the repository, but don't reference the original images in the CSS.
SVG images are preferred, but if the provider does not have those available, use or convert to the PNG format.

You'll need:

* White foreground with transparent background (Used on the main OSF Preprints landing page, under the *Preprint Services* Section)

  * width: <= ``350px``
  * height: ``140px``

* Black foreground with transparent background (Used on the OSF Preprints discover page, under *Partner Repositories*)

  * width: <= ``350px``
  * height: ``120px``

* Square logo with a transparent background (can have color foreground)

  * width: ``48px``
  * height: ``48px``

* Rectangular/wide logo with a transparent background (can have color foreground, this can be the white foreground image)

  * width: <= ``600px``
  * height: ``140px``

* A *sharing logo* that will be displayed on social media sites

  * width: >= ``200px``, ``1500px`` preferred
  * height: >= ``200px``, ``1500px`` preferred


You may need to edit the images to meet the requirements. Use ``brew cask install gimp`` to install gimp or use Pixlr_.

Optimitize the images with Optimizilla_ or a similar service. See the `Google Image Optimization Guide`_

.. _Pixlr: https://pixlr.com/editor/
.. _Optimizilla: http://optimizilla.com/
.. _Google Image Optimization Guide: https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/image-optimization

Adding an entry in the config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``config/environment.js``, there will be a ``PREPRINTS`` object and a ``providers`` array. You will need to add another
object to that ``providers`` array.

If adding a provider domain, you'll need to run ``sudo ./scripts/add-domains.js``

.. code-block:: javascript

    {
        id: 'provider_id', // This must match the ID in the OSF Repo
        domain: 'provider.org', // If using a domain. Otherwise, delete this line
        logoSharing: {
            path: '/assets/img/provider_logos/provider_id-sharing.png', // The path to the provider's sharing logo
            type: 'image/png', // The mime type of the image
            width: 1500, // minimum 200, 1500 preferred (this is the width of the image, in pixels)
            height: 1500 // minimum 200, 1500 preferred (this is the height of the image, in pixels)
        },
        permissionLanguage: 'provider_permission_language'
    }


Adding permission language to the footer text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The branded preprint partners need to show permissions to use content/titles from the owner institutions/organizations. For example, engrXiv, SocArXiv, and PsyArXiv are using the -rXiv extension with permission from Cornell and there is a need to have a language on their pages stating such.

Adding an entry in the translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``translation.js``, there will be a permission-language entry where you will need to add the provider permission language. 
   
.. code-block:: javascript

    'permission-language': {
        arxiv_trademark_license,
        arxiv_non_endorsement: `${arxiv_trademark_license} This license should not be understood to indicate endorsement of content on {{provider}} by Cornell University or arXiv.`
    }

Note that if the permission language is expecting to be used fully or partially by other providers then it is preferable to be defined as a constant at the beginning of the `translation.js` file. The const can be later re-used within the permission-language entry.

.. code-block:: javascript

   const arxiv_trademark_license = 'arXiv is a trademark of Cornell University, used under license.'; 

Creating the stylesheet
~~~~~~~~~~~~~~~~~~~~~~~
The basic stylesheet must be named ``app/styles/brands/provider_id.scss`` and contain the following:

.. code-block:: scss

    @import 'brand';

    @include brand(
        #ABCDEF,                                // Color, theme color #1 (header backgrounds, hover backgrounds)
        white,                                  // Color, theme color #2 (text color mostly, usually white or black)
        #012345,                                // Color, theme color #3 (navbar color, preferably a dark color)
        #6789AB,                                // Color, theme color #4 (used in link colors)
        black,                                  // Color, theme color #5 (text color that contrasts with #2, usually black or white)
        $logo-dir + 'engrxiv-small.png',        // String, path to the rectangular provider logo
        $logo-dir + 'engrxiv-square-small.png', // String, path to the square provider logo
        true,                                   // Boolean, whether to use the white share logo or not
        false,                                  // Boolean, whether to use theme color 4 or theme color 2 for the navbar link color
        true                                    // Boolean, whether to use the contracts link color (theme color 4)
    );

    // Add any custom styles or overrides here

You may need to manipulate the colors and options to get them to look good. Avoid overriding styles, if at all possible.

Open Pull Requests
------------------
Open pull requests against osf.io and ember-preprints with your changes. Be sure to cross-reference in the PR description that it requires the other PR.
If the PR includes adding a domain, Add a "Notes for Reviewers" section with a reminder to run the add-domains script.
Add notes for QA that include screenshots of the newly added provider

In your PR against osf.io, add a section called "Notes for Deployment" with a reminder to request an API key from SHARE. This is necessary, because the provider's preprints will not be indexed by SHARE without the API Key.

CAS Support for Login and Sign Up
=================================
Create a ticket in `CAS Board <https://openscience.atlassian.net/secure/RapidBoard.jspa?rapidView=78&useStoredSettings=true with title>`_ with "Login and Sign Up Support: <the name of the preprint provider>" as the summary. Basic features are guaranteed and extra ones are welcome. Make this ticket block the OSF or EOSF tickets for this provider.

Basic Features
--------------

1. Register the preprint provider to CAS Registered Service.
2. Whitelist the provider's external domain to OSF Authentication Logic.
3. Customize the login page (CAS) and the sign up page (OSF).

Extra Features
--------------

Please add other requirements in the description.

Resources To Provide
--------------------

1. Preferred display name: e.g. ``PsyArxiv``.
2. The default, black and colored logo images (if available).
3. Preferred CSS background color: the main background color of the home page.
4. OSF domain and external domain: e.g. ``osf.io/preprints/psyarxiv/`` and ``preprints.psyarxiv.org/``

DevOps
======
If the provider is using a domain, create a DevOps ticket to update the proxy redirects and for them to contact the domain admin to get the domain pointed at the correct IP address. Include the contact information from the product team.
