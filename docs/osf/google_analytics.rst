.. _osf_google_web_analytics

Running Google Analytics Locally
================================

This section describes how to set up and test Google Web Analytics features locally.

Getting a Google Analytics Account
**********************************

Open a web browser and navigate to `Google Analytics <http://www.google.com/analytics/>`_.

Click **Access Google Analytics**. If you have not used Google Analytics before, you will
be prompted to sign up. Follow the process and confirm your account.

Click **Admin** on the nav bar.

Click the **Property** drop down and select **Create New Property**.

Fill out **Website Name** and **Website URL** -- they don't need to point to real URLs.
In this example the former will be *osf analytics testing* and the latter will be
**test.osf.io**

Once completed, click **Get Tracking ID** and you will be redirected to a page containing
the tracking info you will need.

Take note of copy the **Tracking ID**. It should look similar to *UA-43352009-1*.

Update Your Local local.py
**************************

Ensure that you have set up your ``website/settings/local.py`` file as outlined in :ref:`Setting up the OSF <osf_setup>` .

Add ``GOOGLE_ANALYTICS_ID = <your_tracking_id>`` to your ``website/settings/local.py`` file.

.. note::

    Now any events that trigger Google Analytics, currently or new things you implement, will be sent to the property
    we set up in the previous section.

Viewing Live Events Within Google Analytics
*******************************************

Click **Home** on the nav bar.

.. note::
    You will see one, or more if you have previously created properties, folders. The descriptions
    match the **Website Name** of the associated property.

Click on the property you created, **osf analytics testing** in your example.

Click **All Website Data** and you will be redirected to an overview page for this property.

On the left hand navigation bar, click **Real-Time** -> **Overview**.

(Optional) Follow the **ANALYTICS EDUCATION** if you are unfamiliar with Google Analytics.

Click **Events** flag underneath the **Real-Time** section of the left hand navigation bar.

.. note::

    From here you can view live events (events received within the last 30 minutes) triggered by either you or your
    test code from your local environment.
    