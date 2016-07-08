# -*- coding: utf-8 -*-
from persiantools import utils


def en_to_fa(string):
    """Convert EN digits to Persian

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.en_to_fa("0123456789")

        :param string:  A string, will be converted
        :rtype: str
    """
    dic = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹'
    }

    return utils.replace(string, dic)


def ar_to_fa(string):
    """Convert Arabic digits to Persian

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.ar_to_fa("٠١٢٣٤٥٦٧٨٩")

        :param string: A string, will be converted
        :rtype: str
        """
    dic = {
        '٠': '۰',
        '١': '۱',
        '٢': '۲',
        '٣': '۳',
        '٤': '۴',
        '٥': '۵',
        '٦': '۶',
        '٧': '۷',
        '٨': '۸',
        '٩': '۹'
    }

    return utils.replace(string, dic)


def fa_to_en(string):
    """Convert Persian digits to EN

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.fa_to_en("۰۱۲۳۴۵۶۷۸۹")

        :param string: A string, will be converted
        :rtype: str
        """
    dic = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }

    return utils.replace(string, dic)


def fa_to_ar(string):
    """Convert Persian digits to Arabic

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.fa_to_ar("۰۱۲۳۴۵۶۷۸۹")

        :param string: A string, will be converted
        :rtype: str
        """
    dic = {
        '۰': '٠',
        '۱': '١',
        '۲': '٢',
        '۳': '٣',
        '۴': '٤',
        '۵': '٥',
        '۶': '٦',
        '۷': '٧',
        '۸': '٨',
        '۹': '٩'
    }

    return utils.replace(string, dic)
