=============================
Libreoffice Developing Helper
=============================


This tool helps developing LibreOffice Extension. It mainly does:

    - build an LibreOffice extension from your source

    - install / uninstall extension

    - create shortcut from installed extension to development files

WHY
---
When developing for LibreOffice, it is common to often reinstall the extension
to test it. It means compiling, uninstalling, installing. This tasks are time
consuming. Beside, if you want to make modification of your code without
reinstalling, you need to create some shortcuts from the installation path to
your code. This command line tool helps achieving this goal.


Installation
------------

::

  $ pip install lo-extension-dev
