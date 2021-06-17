#!/usr/bin/env python
# -*- coding: utf-8 -*-

KANSUUJI = '〇一二三四五六七八九'
KETADORI = '千百十'


def read_kansuji(s: str) -> int:
    r: int = 0
    next_pos: int = 0
    for i, keta in enumerate(KETADORI):
        pos = s.find(keta)  # 桁取り
        if pos < 0:
            block = 0
            pos = next_pos - 1
        elif pos == next_pos: # '二千百'のように'千'と'百'の間に数字がない場合
            block = 1
        else:
            block = int(kan2num_simple(s[next_pos:pos]))  # 'next_posとposの間の漢数字を数値に変換
        r += block*(10**(len(KETADORI) - i))
        next_pos = pos + 1
    if next_pos != len(s): # 一の位の数字がある場合
        r += kan2num_simple(s[next_pos:len(s)])
    return r


def kan2num_simple(s: str) -> int:
    for i, k in enumerate(KANSUUJI):
        s = s.replace(k, str(i))
    return int(s)


def kan2num(s: str) -> int:
    for c in s:
        if c in KETADORI:
            return read_kansuji(s)
    return kan2num_simple(s)
