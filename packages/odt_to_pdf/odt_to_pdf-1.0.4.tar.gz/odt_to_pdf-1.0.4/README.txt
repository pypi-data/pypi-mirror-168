OdtToPdfCelery
--------------

A Celery shared task to transform an odt file (or its UTF8-decoded representation) to PDF

Worker
======

The worker needs to be run in an environment which has access to
- the Celery broker
- the Celery result backend
- The `libreoffice` executable
