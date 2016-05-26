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
        'ك': 'ک',
        'إ': 'ا',
    }

    return utils.replace(string, dic)
