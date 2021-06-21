#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import Dict, Optional, Tuple, Union


from .lib.cacheRegexes import estimatePref, getCity, getPrefectures, normalizePref, normalizeTownName
#
from .lib.config import Config, DEFAULT_CONFIG, DEFAULT_OPTION, Option
from .lib.const import ADDRESS, CITY, LEVEL, PREF, TOWN, HYPHNES, NUMS
from .lib.dict import preprocess
from .lib.kan2num import kan2num
from .lib.num2kan import num2kanji
from .lib.patch_addr import patch_address


# def test_normalize_nelogod():
#      assert "-" == normalize_neologd("－")
#      assert "＝。、・「」" == normalize_neologd("＝。、・「」")
#      assert "南アルプスの天然水-Sparking*Lemon+レモン一絞り" == \
#         normalize_neologd("南アルプスの　天然水-　Ｓｐａｒｋｉｎｇ*　Ｌｅｍｏｎ+　レモン一絞り", remove_space=True)


def normalize(
        address: str,
        config: Config = DEFAULT_CONFIG,
        option: Option = DEFAULT_OPTION) -> Dict[str, Union[str, int]]:
    city: Optional[str] = None
    town: Optional[str] = None
    level: int = 0

    # 事前処理
    addr: str = preprocess(address)
    # 都道府県名の正規化
    prefectures: Dict[str, Tuple[str, ...]] = getPrefectures(config, option)
    pref, addr = normalizePref(prefectures, addr)
    # 省略された都道府県の補足
    if pref is None:
        pref = estimatePref(prefectures, addr, config, option)
    # 市区町村名
    if pref and option.level >= 2:
        city, addr = getCity(prefectures, pref, addr, option)
    # 町丁目以降の正規化
    if city and option.level >= 3:
        _town, _addr = normalizeTownName(addr, pref, city, config, option)
        if _town is not None:
            town = _town
            addr = _addr
    city = city if city else ''
    town = town if town else ''

    # そのほか全般
    addr = re.sub('^-', '', addr)

    # .replace(/([0-9]+)(丁目)/g, (match) => {
    #             return match.replace(/([0-9]+)/g, (num) => {
    #                 return number2kanji(Number(num))
    #             })
    #         })
    # addr = re.sub("([0-9]+)丁目", lambda m: num2kanji(int(m.groups()[0])), addr) #kan2numでもんだがあるので一時退避
    addr = re.sub("([0-9]+)丁目", lambda m: str(int(m.groups()[0])), addr)


    #   /(([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号)\s*(.+)/, '$1 $5',
    #   /([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号?/, '$1-$3',
    #   /([0-9〇一二三四五六七八九十百千]+)番地?/, '$1')
    #   /([0-9〇一二三四五六七八九十百千]+)の/g, '$1-')
    BANCHI_PATTERNS = (
            (f'(({NUMS}+)(番地?)({NUMS}+)号)\\s*(.+)', r'\1 \5'),
            (f'({NUMS}+)(番地?)({NUMS}+)号?', r'\1-\3'),
            (f'({NUMS}+)番地?', r'\1'),
            (f'({NUMS}+)の', r'\1-'))
    for p, r in BANCHI_PATTERNS:
        addr = re.sub(p, r, addr)


    #   .replace(
    #     /([0-9〇一二三四五六七八九十百千]+)[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g,
    #     (match) => {
    #       return kan2num(match).replace(/[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g, '-')
    #     },
    #   )
    #   .replace(
    #     /[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]([0-9〇一二三四五六七八九十百千]+)/g,
    #     (match) => {
    #       return kan2num(match).replace(/[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g, '-')
    #     },
    #   )
    f = lambda x: re.sub(HYPHNES, '-', x.group())
    # f = lambda x: re.sub(HYPHNES, '-', kan2num(x.group()))  #kan2numでもんだがあるので一時退避
    # _ = addr
    for p in [f'({NUMS}+){HYPHNES}', f'{HYPHNES}({NUMS}+)']:
        addr = re.sub(p, f, addr)
        # if _ != addr:
        #     print(_, addr)
        #     print([ord(c) for c in _])
        #     print([ord(c) for c in addr])


    BANCHI_PATTERNS2 = (
            f'({NUMS}+)-',  # `1-` のようなケース
            f'-({NUMS}+)',  # `-1` のようなケース
            f'-[^0-9]+({NUMS}+)',  # `-あ1` のようなケース
            f'({NUMS}+)$',)  # `串本町串本１２３４` のようなケース
    for p in BANCHI_PATTERNS2:
        # x = addr
        addr = re.sub(p, lambda x: x.group().replace(x.groups()[0], str(kan2num(x.groups()[0]))), addr)
        # addr = re.sub(p, lambda x: re.sub(x.groups()[0], kan2num(x.groups()[0]), x.group()), addr)
        # addr = re.sub(p, lambda x: re.sub(x.groups()[0], x.groups()[0], x.group()), addr)
        # if x != addr:
        #     print(p, x, addr)

    # レベル判定
    addr = patch_address(pref, city, town, addr).strip()
    for k in [pref, city, town]:
        if k:
            level += 1
    return {PREF: pref, CITY: city, TOWN: town, ADDRESS: addr, LEVEL: level}
