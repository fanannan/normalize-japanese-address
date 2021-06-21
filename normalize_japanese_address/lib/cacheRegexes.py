#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib.parse
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Tuple
import requests
import orjson
import os
from logging import getLogger
#
from .config import Config, Option
from .const import ADDRESS, CITY, PREF, KANSUJI_W_TEN, HYPHNES, BASE_JSON_FILE
from .dict import toRegex, jisKanji
#
from .kan2num import kan2num

logger = getLogger(__name__)


def read_json(path: str):
    with open(path, encoding='utf-8') as f:
        return orjson.loads(f.read())


@lru_cache
def getPrefectures(config: Config, option: Option) -> Dict[str, Tuple[str, ...]]:
    if option.use_api:
        response = requests.get(config.japaneseAddressesApi+BASE_JSON_FILE).json()
    else:
        response = read_json(os.path.join(config.api_data_path, BASE_JSON_FILE))
    d: Dict[str, List[str]] = response
    prefectures: Dict[str, Tuple[str, ...]] = {k: tuple(v if option.is_exact else [jisKanji(s, False) for s in v])
                                               for k, v in d.items()}
    return prefectures


@lru_cache
def getPrefectureRegexes(prefs: Iterable[str]) -> Tuple[Tuple[str, str,]]:
    # `東京` の様に末尾の `都府県` が抜けた住所に対応
    def make_regex(p: str):
        q = re.sub('(都|道|府|県)$', '', p)
        if q == '東京':
            return f'{q}都?'
        elif q == '北海':
            return f'{q}道?'
        elif q in ['京都', '大阪']:
            return f'{q}府?'
        return f'{q}県?'

    return tuple([(pref, make_regex(pref)) for pref in prefs])


@lru_cache(maxsize=None)
def getCityRegexes(cities: Iterable[str], option: Option) -> Tuple[Tuple[str, str,], ...]:
    # 郡が省略された住所に対応
    def make_regex(p: str) -> str:
        m = re.search('(町|村)$', p)
        if m is not None:
            q = re.sub('(.+?)郡', r'(\1郡)?', p)
        else:
            q = p
        return f'{q}'  # ^$なし

    # 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    cities = sorted(cities, key=lambda x: len(x), reverse=True)
    return tuple([(city, toRegex(make_regex(city), option.is_exact)) for city in cities])


@lru_cache(maxsize=None)
def getTowns(pref: str, city: str, config: Config, option: Option) -> List[str]:
    if option.use_api:
        encoded_pref: str = urllib.parse.quote(pref)
        encoded_city: str = urllib.parse.quote(city)
        url: str = f'{config.japaneseAddressesApi}/ja/{encoded_pref}/{encoded_city}.json'
        response = requests.get(url).json()
    else:
        file_path: str = os.path.join(config.api_data_path, f'ja/{pref}/{city}.json')
        if os.path.exists(file_path):
            response = read_json(file_path)
        else:
            response = {}
            logger.info(f'{pref}{city}のデータファイルがありません({file_path})')
    towns: List[str] = response if option.is_exact else [jisKanji(r, is_exact=False) for r in response]
    return towns


@lru_cache(maxsize=None)
def getTownRegexes(pref: str, city: str, config: Config, option: Option) -> Tuple[Tuple[str, str,], ...]:
    # 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    towns = getTowns(pref, city, config, option)
    towns = sorted(towns, key=lambda x: len(x), reverse=True)
    return tuple([(town, toRegex(make_town_regex(city, town), option.is_exact)) for town in towns])


def make_town_regex(city: str, town: str) -> str:
    q = re.sub('大?字', '(大?字)?', town)
    # 以下住所マスターの町丁目に含まれる数字を正規表現に変換する
    regex = re.sub(
            f'([壱{KANSUJI_W_TEN}]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)',
            make_regexes,
            q)
    return f'.*{regex}' if re.match('京都市', city) else f'{regex}'


def make_regexes(m: re.Match):
    s: str = m.group()
    regexes: List[str] = list()
    regexes.append(re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', s))
    if re.match('壱', s):
        # 漢数字
        regexes += ['一', '1', '１']
    else:
        # 半角アラビア数字
        s = re.sub(f'([{KANSUJI_W_TEN}]+)', lambda x: str(kan2num(x.group())), s)
        s = re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', s)
        regexes.append(s)
    mr = '|'.join(regexes)
    regex: str = f'({mr})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|{HYPHNES})'
    return regex


# 地名照合
def match_regexes(regexes: Iterable[Tuple[str, str,]], addr: str) -> Tuple[Optional[str], str]:
    addr = addr.strip()  # todo: 高速化のため外出し
    for name, reg in regexes:
        m = re.match(reg, addr)
        if m is not None:
            return name, addr[len(m.group()):]
    return None, addr


# 都道府県名の正規化
def normalizePref(prefectures: Dict[str, Iterable[str]], addr: str) -> Tuple[Optional[str], str]:
    prefs: Tuple[str, ...] = tuple(prefectures.keys())
    prefRegexes: Tuple[Tuple[str, str,]] = getPrefectureRegexes(prefs)
    return match_regexes(prefRegexes, addr)


# 市区町村名
def getCity(prefectures: Dict[str, Iterable[str]], pref: str, addr: str, option: Option) -> Tuple[Optional[str], str]:
    cities: Tuple[str, ...] = tuple(prefectures.get(pref, tuple()))
    cityRegexes: Tuple[Tuple[str, str,]] = getCityRegexes(cities, option)
    return match_regexes(cityRegexes, addr)


def normalizeTownName(addr: str, pref: str, city: str, config: Config, option: Option) -> Tuple[Optional[str], str]:
    townRegexes: Tuple[Tuple[str, str,]] = getTownRegexes(pref, city, config, option)
    addr = re.sub('^大字', '', addr)
    return match_regexes(townRegexes, addr)


# 都道府県名の推測
def estimatePref(prefectures: Dict[str, Iterable[str]], addr: str, config: Config, option: Option) -> str:
    # 都道府県名が省略されている
    matched: List = []
    for _pref in prefectures:
        cities = prefectures.get(_pref, None)
        cityRegexes = getCityRegexes(cities, option)
        addr = addr.strip()
        for _city, reg in cityRegexes:
            m = re.match(reg, addr)
            if m is not None:
                matched.append({PREF: _pref, CITY: _city, ADDRESS: addr[len(m.group()):], })

    # マッチする都道府県が複数ある場合は町名まで正規化して都道府県名を判別する。（例: 東京都府中市と広島県府中市など）
    if len(matched) == 1:
        return matched[0][PREF]
    for m in matched:
        pref, addr = normalizeTownName(m[ADDRESS], m[PREF], m[CITY], config, option)
        if pref is not None:
            return pref
    return ''
