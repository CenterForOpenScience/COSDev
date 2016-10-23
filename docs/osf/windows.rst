Connecting a Windows VM to a local OSF
======================================

Follow these instructions to install your Windows VM.
The instructions here were created with IE 11 on Windows 8.1
https://docs.google.com/document/d/1BJ20XDHlVVeW_pRgsNUMKAJg6r3yoVWAZCZ9Sf-Idzw/edit

**NOTE:** local.py and defaults.py changes will need to be reverted for your local osf to work properly on localhost again. It can be found on osf.localhost instead.

1. In your mac OSF dist open ``local.py`` and change:

  ``DOMAIN = PROTOCOL + 'osf.localhost:5000/'``

  ``API_DOMAIN = PROTOCOL + 'osf.localhost:8000/'``

2. In your mac OSF dist ``local.py`` add:

  ``CAS_SERVER_URL = 'http://osf.localhost:8080'``

3. If you need WATERBUTLER to work:
  a. In your mac OSF dist ``local.py`` add:
  
  ``WATERBUTLER_URL = 'http://osf.localhost:7777'`` 
    
  b. In your WATERBUTLER repo ``waterbutler/auth/osf/settings.py`` change:
  
  ``API_URL = config.get('API_URL', 'http://osf.localhost:5000/api/v1/files/auth/')``
  
  c. In your WATERBUTLER repo ``waterbutler/serser/setting.py`` change:
  
  ``ADDRESS = config.get('ADDRESS', 'osf.localhost')``
  
  ``DOMAIN = config.get('DOMAIN', "http://osf.localhost:7777")``

4. If you need MFR to work:
  a. In your mac OSF dist ``local.py`` add:
  
  ``MFR_SERVER_URL = 'http://osf.localhost:7778'``
  
  b. In your MFR repo ``mfr/server/settings.py`` change:
  
  ``ADDRESS = config.get('ADDRESS', 'osf.localhost')``
  
  ``ALLOWED_PROVIDER_DOMAINS = config.get('ALLOWED_PROVIDER_DOMAINS', ['http://osf.localhost:5000/', 'http://osf.localhost:7777/'])``
  
  b. In your WATERBUTLER repo ``waterbutler/auth/osf/settings.py`` change:
  
  ``MFR_DOMAIN = analytics_config.get('MFR_DOMAIN', 'http://osf.localhost:7778').rstrip('/')``
  
5. Once your VM is working, open the windows commandline and run: ``ipconfig`` and note the Default Gateway IP (e.g., 10.0.2.2)

6. Run ``explorer C:\Windows\System32\drivers\etc`` and a files window will open.

7. Right click ``hosts`` and click ``properties``. Under the ``Security`` tab, under groups click ``Users`` and grant full control (fine for a VM just used for development, but not advised for normal machines)

8. Open ``hosts`` with notepad and add to the bottom of the file:
  ``10.0.2.2 osf.localhost``
where 10.0.2.2 is your Default Gateway IP from step 3

9. Open IE and navigate to ``http://osf.localhost:5000``
