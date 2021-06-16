#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

UNIT_TABLE: Dict[int, str] = {
        0: '', 1: '十', 2: '百', 3: '千', 4: '万', 8: '億', 12: '兆', 16: '京',
        }

NUMBER_TABLE: Dict[int, str] = {
        0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九',
        }


def num2kanji(num: int) -> str:
    if num == 0:
        return '零'
    num_str: str = str(num)[::-1]
    s: List = [str]
    for n, v in enumerate(map(int, num_str)):
        i = n if n in UNIT_TABLE else n%4
        sep = i > 3 and ' ' or ''
        if v == 0 and i > 3 and num_str[n:n+4] != '0000':
            s.append(UNIT_TABLE[i]+sep)
        elif v > 1 or (i > 3 and v == 1):
            s.append(NUMBER_TABLE[v]+UNIT_TABLE[i]+sep)
        elif v > 0:
            s.append(UNIT_TABLE[i] or NUMBER_TABLE[v]+sep)
    return ''.join(reversed(s)).rstrip()
