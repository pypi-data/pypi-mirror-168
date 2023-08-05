"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""

from math import sin as m_sin
from math import cos as m_cos


def sum_list(list_of_nums):
    total = 0
    for i in range(len(list_of_nums)):
        total += list_of_nums[i]
    return total


def sin(num):
    return m_sin(num)


def cos(num):
    return m_cos(num)
