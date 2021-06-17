#!/usr/bin/env python
# -*- coding: utf-8 -*-

KANSUUJI = '〇一二三四五六七八九'
KETA = '千百十'
tais2 = '京兆億万'
suuji = {'〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', \
         '百', '千', '万', '億', '兆', \
         '０', '１', '２', '３', '４', '５', '６', '７', '８', '９', \
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}



# 4桁までの漢数字（例：六千五百八）を数値変換する関数
def kans2num_lower(text):
    ans = 0 # 初期値（計算結果を加算していく）
    poss = 0 # スタート位置
    for i, tmp in enumerate(KETA):
        pos = text.find(tmp) # 大数（千百十）の位置を順次特定
        if pos == -1: # 対象となる大数（千百十）が無い場合
            block = 0
            pos = poss - 1
        elif  pos == poss: # '二千百'のように'千'と'百'の間に数字がない場合
            block = 1
        else:
            block = int(kan2num_simple(text[poss:pos])) # 'possとposの間の漢数字を数値に変換
        ans += block * (10 ** (len(KETA) - i))
        poss = pos + 1 # possをposの次の位置に設定
    if poss != len(text): # 一の位の数字がある場合
        ans += int(kan2num_simple(text[poss:len(text)]))
    return ans


# 関数(3)_20桁までの漢数字（例：六兆五千百億十五万八千三十二）を数値変換する関数
def kan2num_translate(text):
    ans = 0
    poss = 0
    for i, tmp in enumerate(tais2):
        pos = text.find(tmp)
        if pos == -1:
            block = 0
            pos = poss - 1
        elif  pos == poss:
            block = 1
        else:
            block = kans2num_lower(text[poss:pos])
        ans += block * (10 ** (4 * (len(tais2) - i)))
        poss = pos + 1
    if poss != len(text):
        ans += kans2num_lower(text[poss:len(text)])
    return ans


# 単純変換する関数
def kan2num_simple(text: str) -> str:
    for i, s in enumerate(KANSUUJI):
        text = text.replace(s, str(i))
    return text


def kan2num(text: str) -> str:
    for s in text:
        if s in KETA:
            return kan2num_translate(text)
    return kan2num_simple(text)
