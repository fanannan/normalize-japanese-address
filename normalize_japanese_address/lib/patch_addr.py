#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List
import re

from .const import CITY, PATTERN, PREF, RESULT, TOWN


ADDRESS_PATCHES: List[Dict[str, str]] = [
        {
                PREF:    '香川県',
                CITY:    '仲多度郡まんのう町',
                TOWN:    '勝浦',
                PATTERN: r'^字?家6',
                RESULT:  '家六',
                },
        {
                PREF:    '愛知県',
                CITY:    'あま市',
                TOWN:    '西今宿',
                PATTERN: r'^字?梶村1',
                RESULT:  '梶村一',
                },
        {
                PREF:    '香川県',
                CITY:    '丸亀市',
                TOWN:    '原田町',
                PATTERN: r'^字?東三分1',
                RESULT:  '東三分一',
                },
        ]


def patch_address(pref: str, city: str, town: str, addr: str) -> str:
    for patch in ADDRESS_PATCHES:
        if patch[PREF] == pref and patch[CITY] == city and patch[TOWN] == town:
            addr = re.sub(patch[PATTERN], patch[RESULT], addr)
            return addr
    return addr
