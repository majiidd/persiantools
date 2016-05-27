# -*- coding: utf-8 -*-
from persiantools import utils


def ar_to_fa(string):
    """Convert Arabic characters to Persian

        Usage::
            from persiantools import characters
            converted = characters.ar_to_fa("السلام عليكم")

        :param string: A string, will be converted
        :rtype: str
        """
    dic = {
        'ي': 'ی',
        'ك': 'ک'
    }

    return utils.replace(string, dic)


def fa_to_ar(string):
    """Convert Persian characters to Arabic

        Usage::
            from persiantools import characters
            converted = characters.ar_to_fa("ای چرخ فلک خرابی از کینه تست")

        :param string: A string, will be converted
        :rtype: str
        """
    dic = {
        'ی': 'ي',
        'ک': 'ك'
    }

    return utils.replace(string, dic)
