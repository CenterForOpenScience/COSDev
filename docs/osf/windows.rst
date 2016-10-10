Connecting a Windows VM to a local OSF
======================================

Follow these instructions to install your Windows VM.
The instructions here were created with IE 11 on Windows 8.1
https://docs.google.com/document/d/1BJ20XDHlVVeW_pRgsNUMKAJg6r3yoVWAZCZ9Sf-Idzw/edit

**NOTE:** local.py and defaults.py changes will need to be reverted for your local osf to work properly on localhost again. It can be found on osf.localhost instead.

1. In your mac OSF dist open ``local.py`` and change:

  ``DOMAIN = PROTOCOL + 'osf.localhost:5000/'``

  ``API_DOMAIN = PROTOCOL + 'osf.localhost:8000/'``

2. In ``defaults.py`` change:

  ``CAS_SERVER_URL = 'http://osf.localhost:8080'``

3. Once your VM is working, open the windows commandline and run: ``ipconfig`` and note the Default Gateway IP (e.g., 10.0.2.2)

4. Run ``explorer C:\Windows\System32\drivers\etc`` and a files window will open.

5. Right click ``hosts`` and click ``properties``. Under the ``Security`` tab, under groups click ``Users`` and grant full control (fine for a VM just used for development, but not advised for normal machines)

6. Open ``hosts`` with notepad and add to the bottom of the file:
  ``10.0.2.2 osf.localhost``
where 10.0.2.2 is your Default Gateway IP from step 3

7. Open IE and navigate to ``http://osf.localhost:5000``
