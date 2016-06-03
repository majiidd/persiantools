PersianTools
===
[![pypi-ver](https://img.shields.io/pypi/v/persiantools.svg)](https://pypi.python.org/pypi/persiantools)
[![PyPI-license](https://img.shields.io/pypi/l/persiantools.svg)](https://pypi.python.org/pypi/persiantools)
[![travic-build](https://travis-ci.org/mhajiloo/persiantools.png?branch=master)](https://travis-ci.org/mhajiloo/persiantools)
[![Coverage Status](https://coveralls.io/repos/github/mhajiloo/persiantools/badge.svg?branch=master)](https://coveralls.io/github/mhajiloo/persiantools?branch=master)
[![python-ver](https://img.shields.io/pypi/pyversions/persiantools.svg)](https://pypi.python.org/pypi/persiantools)

Python Library for Persian. Convert Arabic character to Persian

### Install Package
```
pip install persiantools
```

### How to use
```python
from persiantools import characters
from persiantools import digits

digits.en_to_fa("0987654321") # return: ۰۹۸۷۶۵۴۳۲۱
digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١") # return: ۰۹۸۷۶۵۴۳۲۱
digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱") # return: 0987654321
digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱") # return: ٠٩٨٧٦٥٤٣٢١

characters.ar_to_fa("راك") # return: راک
characters.fa_to_ar("ای چرخ فلک خرابی از کینه تست") # return: اي چرخ فلك خرابي از كينه تست
```
