PersianTools
============

| |pypi-ver| |PyPI-license| |travic-build| |Coverage Status| |python-ver|


-  Jalali (Shamsi) date and datetime (based on python datetime's module)
    -  Convert Jalali to Gregorian date/datetime and vice versa
    -  Support comparition and arithmetic operators such as +, -, ==, >=
    -  Support timezone
-  Convert Arabic and Persian characters/digits to each other

Install Package
---------------

.. code:: bash

    $ pip install persiantools

How to use
----------

Date:
^^^^^

.. code:: python

    >>> from persiantools.jdatetime import JalaliDate
    >>> import datetime

    >>> JalaliDate.today()
    JalaliDate(1395, 04, 18, Jomeh)

    >>> JalaliDate.today().to_gregorian()
    datetime.date(2016, 7, 8)

    >>> JalaliDate(1369, 7, 1)
    JalaliDate(1369, 07, 01, Yekshanbeh)

    >>> JalaliDate(datetime.date(1990, 9, 23))
    JalaliDate(1369, 07, 01, Yekshanbeh)

    >>> JalaliDate.to_jalali(2013, 9, 16)
    JalaliDate(1392, 06, 25, Doshanbeh)

Datetime:
^^^^^^^^^

.. code:: python

    >>> from persiantools.jdatetime import JalaliDateTime
    >>> import datetime, pytz

    >>> JalaliDateTime.now()
    JalaliDateTime(1395, 4, 18, 1, 43, 24, 720505)

    >>> JalaliDateTime.now().to_gregorian()
    datetime.datetime(2016, 7, 8, 1, 43, 24, 720505)

    >>> JalaliDateTime.now(pytz.timezone("Asia/Tehran"))
    JalaliDateTime(1395, 4, 18, 1, 53, 30, 407770, tzinfo=<DstTzInfo 'Asia/Tehran' IRDT+4:30:00 DST>)
    
    >>> JalaliDateTime.now(pytz.utc)
    JalaliDateTime(1395, 4, 17, 21, 23, 53, 474618, tzinfo=<UTC>)

Digit/Character converter:
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> from persiantools import characters
    >>> from persiantools import digits

    >>> digits.en_to_fa("0987654321")
    '۰۹۸۷۶۵۴۳۲۱'
    
    >>> digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١")
    '۰۹۸۷۶۵۴۳۲۱'
    
    >>> digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱")
    '0987654321'
    
    >>> digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱") 
    '٠٩٨٧٦٥٤٣٢١'
    
    >>> characters.ar_to_fa("راك")
    'راک'
    
    >>> characters.fa_to_ar("ای چرخ فلک خرابی از کینه تست")
    'اي چرخ فلك خرابي از كينه تست'

Operators
^^^^^^^^^

.. code:: python

    >>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
    >>> import datetime

    >>> JalaliDate(1367, 2, 14) == JalaliDate(datetime.date(1988, 5, 4))
    True

    >>> JalaliDateTime(1367, 2, 14, 4, 30) >= JalaliDateTime(1369, 7, 1, 1, 0)
    False

    >>> JalaliDate(1395, 2, 14) + datetime.timedelta(days=38)
    JalaliDate(1395, 03, 21, Jomeh)

    >>> JalaliDateTime(1395, 12, 30) - JalaliDateTime(1395, 1, 1)
    datetime.timedelta(365)

Serializing and de-serializing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> from persiantools.jdatetime import JalaliDate
    >>> import pickle

    >>> # Serializing
    >>> file = open("save.p", "wb")
    >>> pickle.dump(JalaliDate(1369, 7, 1), file)
    >>> file.close()

    >>> # de-serializing
    >>> file = open("save.p", "rb")
    >>> jalali = pickle.load(file)
    >>> file.close()
    >>> jalali
    JalaliDate(1369, 07, 01, Yekshanbeh)

.. |pypi-ver| image:: https://img.shields.io/pypi/v/persiantools.svg
   :target: https://pypi.python.org/pypi/persiantools
.. |PyPI-license| image:: https://img.shields.io/pypi/l/persiantools.svg
   :target: https://pypi.python.org/pypi/persiantools
.. |travic-build| image:: https://travis-ci.org/mhajiloo/persiantools.png?branch=master
   :target: https://travis-ci.org/mhajiloo/persiantools
.. |Coverage Status| image:: https://coveralls.io/repos/github/mhajiloo/persiantools/badge.svg?branch=master
   :target: https://coveralls.io/github/mhajiloo/persiantools?branch=master
.. |python-ver| image:: https://img.shields.io/pypi/pyversions/persiantools.svg
   :target: https://pypi.python.org/pypi/persiantools