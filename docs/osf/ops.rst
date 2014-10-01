Ops
===


Generating a new SSL certificate
********************************


* Generate a certificate signing request (see instructions from `this post <http://blog.wensheng.org/2012/03/using-namecheap-ssl-with-nginx.html>`_)
    * goto osf:/opt/certs/namecheap
    * ``openssl genrsa -des3 -out osf.io.key 2048``
    * ``openssl rsa -in osf.io.key -out osf.io.key.nopass``
    * ``openssl req -new -key osf.io.key.nopass -out osf.io.csr``
        * fqdn: osf.io
        * don't enter "challenge password"

* Get signed certificate
    * submit CSR to NameCheap
    * follow verification email
    * download and expand zip file of certs
    * ``cat osf_io.crt COMODORSADomainValidationSecureServerCA.crt COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt > osf.io.bundle.crt``

* On staging
    * copy osf.io.bundle.crt to /opt/certs/namecheap
    * edit ``/opt/nginx/sites-enabled/000-osf``
        * ``ssl_certificate /opt/certs/namecheap/osf.io.bundle.crt;``
        * ``ssl_certificate_key /opt/certs/namecheap/osf.io.key.nopass;``

* On production
    * goto linode nodebalancer config
    * edit production settings
    * paste osf.io.bundle.crt into "Certificate" field
    * paste osf.io.key.nopass into "Private Key" field


Upgrading Unsupported releases of Ubuntu
****************************************

- `EOLUpgrades <https://help.ubuntu.com/community/EOLUpgrades/>`_
- `How to install software or upgrade from old unsupported release? <https://askubuntu.com/questions/91815/how-to-install-software-or-upgrade-from-old-unsupported-release/91821#91821?newreg=55cb4b0054814dbe9fdf36b3a0a08f27>`_ (AskUbuntu)

NOTE: The command from the AskUbuntu answer needs slight modification to include replacement of ``us.archive.ubuntu.com``: ::

    sudo sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com\us.archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

NOTE: When prompted if you want to replace ``/etc/mongodb.conf`` and ``/etc/nginx/nginx.conf``, etc., press ``X`` to enter the shell and back these files up (``sudo cp /etc/mongodb.conf /etc/mongodb.conf.bak``)


Migrating to a new machine
**************************

- On Linode dashboard, go to the Linode you want to restore *from*.
- Go to Backups -> Daily Backups.
- Click "Restore to this Linode" next to the Linode you want to restore *to*.
- Once restoration is complete, resize the data image.
- On the new machine, add a new SSH key pair. ::

    # Replace "sloria" with your username
    $ ssh-keygen -t rsa -C "sloria-osf"

- Copy the new public key to the old machine at  ``/home/<your-username>/.ssh/authorized_keys``
- On the new machine, edit /root/.ssh/config with the correct SSH settings. ::

    Host osf-old
        HostName <ip-of-old-linode>
        User sloria
        IdentityFile /home/sloria/.ssh/id_rsa


- rsync /opt/data/mongodb. ::

    # On the new machine
    $ sudo rsync -vaz --delete osf-old:/opt/data/mongodb /opt/data

.. note::
    You'll probably want to use ``screen`` or ``nohup`` to run this as a background process.


- rsync /opt/data/uploads. ::

    $ sudo rsync -vaz --delete osf-old:/opt/data/uploads /opt/data/

put up osf_down page,private ips on node balancer, restart new server then old
