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

