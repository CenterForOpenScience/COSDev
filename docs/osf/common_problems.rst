Troubleshooting Common Problems
===============================

This document is intended to serve as a knowledge repository - it should contain
solutions to commonly encountered problems when running the OSF, as well as
solutions to hard-to-debug issues that developers have encountered that might be
seen by others in the course of their work

"Emails not working on my development server"
*********************************************

Solution: You may not have a celery worker running. If you have Celery and RabbitMQ installed (see the `README <https://github.com/CenterForOpenScience/osf>`_ for installation instructions), run ``invoke celery``.

Less ideally, you can turn Celery off and send emails synchronously by adding ``USE_CELERY = False`` to your ``website/settings/local.py`` file.

### "My view test keeps failing"

Solution: You have to reload the database record.

    def test_change_name_view(self):
        user = UserFactory()
        # Hit some endpoint that updates the user's database record
        res = self.app.post_json('/{}/changename/'.format(user._primary_key),
            {'name': 'Freddie Mercurial'})
        user.reload()  # Make sure object is up to date
        assert_equal(res.status_code, 200)


ImportError: No module named five
*********************************

Celery may raise an exception when attempting to run the OSF tests. A partial
traceback:

::

    Exception occurred:
      File "<...>", line 49, in <module>
        from kombu.five import monotonic
    ImportError: No module named five

error: [Errno 61] Connection refused` is raised in ampq/transport.py
********************************************************************

Solution: You may have to start your Rabbitmq and Celery workers.

::

    $ invoke rabbitmq
    $ invoke celery_worker

webassets.exceptions.BundleError
********************************

Solution: Make sure your bower components are installed. If you have bower installed, just run ``bower install``. If you need to install bower, consult the OSF README.
