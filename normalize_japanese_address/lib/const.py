#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Final

PREF: Final[str] = 'pref'
CITY: Final[str] = 'city'
TOWN: Final[str] = 'town'
ADDRESS: Final[str] = 'address'
#
LEVEL: Final[str] = 'level'
#
PATTERN: Final[str] = "pattern"
RESULT: Final[str] = "result"
#
API_URL: str = 'https://geolonia.github.io/japanese-addresses/api/'
BASE_JSON_FILE: str = 'ja.json'

HYPHNES: Final[str] = '[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]'
KANSUJI: Final[str] = '一二三四五六七八九'
KANSUJI_W_TEN: Final[str] = f'{KANSUJI}十'
NUMS: Final[str] = f'[0-9{KANSUJI}〇十百千]'
NUMS_WO_MARU: Final[str] = f'[0-9{KANSUJI}十百千]'
NUMS_W_ZEN: Final[str] = f'[0-9０-９{KANSUJI}〇十]'
