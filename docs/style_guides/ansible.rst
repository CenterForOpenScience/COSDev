Ansible
=======

- Prefer dictionary syntax for passing many arguments to a module.

.. code-block:: yaml

    - name: Ensure proper permissions on apps directory
      file:
        path: "/opt/apps/"
        mode: 0755
        group: "osf"
        owner: "www-data"

- Do *not* prefix task names with the name of the role.


.. code-block:: yaml

    # YES
    - name: Make user python is installed
      apt: name="python-dev"

    # NO
    - name: uwsgi | Make user python is installed
      apt: name="python-dev"


