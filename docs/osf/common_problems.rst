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

"My view test keeps failing"
****************************

Solution: You have to reload the database record.

.. code-block:: python

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

Error when importing uritemplate
********************************

If invoking assets or server commands throw an error about uritemplate, run the following to resolve the conflict:

    ::

        pip uninstall uritemplate.py --yes
        pip install uritemplate.py==0.3.0

and then re run the command that failed.

Using PyCharm's Remote Debugger
*******************************

Some debugging tasks make it difficult to use the standard debug tools (i.e. pdb, ipdb, or PyCharm's debugger). 
Usually this is becuase you're running code in a way where you don't have ready access to the process's 
standard in/out. Examples of this include:

- celery tasks
- local testing/debugging using uWSGI

One way to debug code running in these kinds of enviornments is to use the PyCharm remote debugger. Follow the 
JetBrains documentation for creating a new run configuration for the remote debugger: https://www.jetbrains.com/pycharm/help/remote-debugging.html. At some point you may be required to add pycharm-debug.egg to your system's PYTHONPATH. The 
easist way to do this is to modify your ~/.bash_profile to automatically append this module to the python path. This looks like:

:: 
    
    export PYTHONPATH="$PYTHONPATH:<your_path_to>/pycharm-debug.egg"

To apply these changes to the current bash session, simply

::

   source ~/.bash_profile

When you start the remote debug server in PyCharm you will get some console output like:

::

    Use the following code to connect to the debugger:
    import pydevd
    pydevd.settrace('localhost', port=54735, stdoutToServer=True, stderrToServer=True)

So to use, simple copy paste the bottom two lines wherever you need to run a debugger. In celery tasks for example,
this often means inside a task definition where it would be otherwise impossible to step into the code. Trigger 
whatever is needed to queue the celery task, and watch the PyCharm console to see when a new connection is initiated. 

Happy remote-debugging.




