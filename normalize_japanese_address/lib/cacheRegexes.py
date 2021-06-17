import re
import urllib.parse
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Tuple

import requests

from .config import Config
from .const import ADDRESS, CITY, PREF
from .dict import toRegex
#
from .kan2num import kan2num


@lru_cache
def getPrefectures(config: Config) -> Dict[str, Tuple[str, ...]]:
    response = requests.get(config.japaneseAddressesApi+'.json')
    d: Dict[str, List[str]] = response.json()
    prefectures: Dict[str, Tuple[str, ...]] = {k: tuple(v) for k, v in d.items()}
    return prefectures


@lru_cache
def getPrefectureRegexes(prefs: Iterable[str]) -> Tuple[Tuple[str, str,]]:
    # `東京` の様に末尾の `都府県` が抜けた住所に対応
    def make_regex(p: str):
        q = re.sub('(都|道|府|県)$', '', p)
        return f'{q}(都|道|府|県)*'  # ^を外し*を追加

    return tuple([(pref, make_regex(pref)) for pref in prefs])


@lru_cache
def getCityRegexes(cities: Iterable[str]) -> Tuple[Tuple[str, str,], ...]:
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
    return tuple([(city, toRegex(make_regex(city))) for city in cities])


@lru_cache
def getTowns(pref: str, city: str, config: Config) -> List[str]:
    encoded_pref: str = urllib.parse.quote(pref)
    encoded_city: str = urllib.parse.quote(city)
    url: str = f'{config.japaneseAddressesApi}/{encoded_pref}/{encoded_city}.json'
    response = requests.get(url)
    towns: List[str] = response.json()
    # towns: Dict[str, Tuple[str, ...]] = {k: tuple(v) for k, v in d.items()}
    return towns


@lru_cache
def getTownRegexes(pref: str, city: str, config: Config) -> Tuple[Tuple[str, str,], ...]:
    # 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    towns = getTowns(pref, city, config)
    towns = sorted(towns, key=lambda x: len(x), reverse=True)
    return tuple([(town, toRegex(make_town_regex(city, town))) for town in towns])


def __make_town_regex(city: str, town: str) -> str:
    q = re.sub('大?字', '(大?字)?', town)
    # 以下住所マスターの町丁目に含まれる数字を正規表現に変換する
    regexes: List[str] = []
    m = re.search('([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', q)
    if m is not None:
        match = m.group()
        regexes.append(re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', match))
        if re.match('壱', match):
            # 漢数字
            regexes.append('一')
            regexes.append('1')
            regexes.append('１')
        else:
            # 半角アラビア数字
            num = match
            mm = re.match('([一二三四五六七八九十]+)', num)
            if mm is not None:
                for i, x in enumerate(mm.groups()):
                    # num[mm.span(i)[0]] = kan2num(x)
                    index: int = mm.span(i)[0]
                    num = num[:index]+kan2num(x)+num[index+1:]
            num = re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', num)
            regexes.append(num)
    # 以下の正規表現は、上のよく似た正規表現とは違うことに注意！
    # _regex = `(${regexes.join('|',)})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])`
    mr = '|'.join(regexes)
    regex = f'({mr})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])'
    if re.match('京都市', city):
        return f'.*{regex}'
    return f'{regex}'


def make_town_regex(city: str, town: str) -> str:
    q = re.sub('大?字', '(大?字)?', town)
    # 以下住所マスターの町丁目に含まれる数字を正規表現に変換する
    regex = re.sub(
            '([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)',
            make_regexes,
            q)
    return f'.*{regex}' if re.match('京都市', city) else f'{regex}'

    # 以下の正規表現は、上のよく似た正規表現とは違うことに注意！


# if m := re.search('([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', q):
#     g = m.group()
#     regexes = [q.replace(g, s) for s in make_regexes(g)]
# # 以下の正規表現は、上のよく似た正規表現とは違うことに注意！
# # _regex = `(${regexes.join('|',)})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])`
# mr = '|'.join(regexes)
# regex: str = f'({mr})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])'
# return f'.*{regex}' if re.match('京都市', city) else f'{regex}'


def make_regexes(m: re.Match):
    s: str = m.group()
    regexes: List[str] = list()
    regexes.append(re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', s))
    if re.match('壱', s):
        # 漢数字
        regexes.append('一')
        regexes.append('1')
        regexes.append('１')
    else:
        # 半角アラビア数字
        s = re.sub('([一二三四五六七八九十]+)', lambda x: str(kan2num(x.group())), s)
        s = re.sub('(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)', '', s)
        regexes.append(s)
    mr = '|'.join(regexes)
    regex: str = f'({mr})((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])'
    return regex


"""
(set!
  (.-getTownRegexes exports)
  (fn [pref city]
    (__awaiter
      (void 0)
      (void 0)
      (void 0)
      (fn []
        (let [cachedResult nil]
          (__generator
            (this-as this)
            (fn [_a]
              (case (.-label _a)
                0
                  (do
                    (set!
                      cachedResult
                      (aget cachedTownRegexes (+ (+ pref "-") city)))
                    (when (not= (typeof cachedResult) "undefined")
                      #js [2 cachedResult])
                    #js [4 (.getTowns exports pref city)])
                1
                  (do
                    (set! towns (.sent _a))
                    (.sort towns (fn [a b] (- (.-length b) (.-length a))))
                    (set! regexes
                      (.map towns
                        (fn [town]
                          (let [regex
                               (.toRegex
                                 dict_1
                                 (.replace (.replace town #"大?字" "(大?字)?")
                                           #"([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)"
                                   (fn [match]
                                     (let [regexes #js []]
                                       (.push regexes
                                              (.replace (.toString match)
                                                        #"(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)"
                                                        ""))
                                       (if (.match match #"^壱")
                                         (do (.push regexes "一") (.push regexes "1") (.push regexes "１"))
                                         (let [num (.replace (.replace match
                                                                       #"([一二三四五六七八九十]+)"
                                                                       (fn [match] (.kan2num kan2num_1 match)))
                                                    #"(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)"
                                                    "")]
                                               (.push regexes (.toString num))))
                                       (def _regex
                                         (+ (+ "(" 
                                               (.join regexes "|"))
                                               ")((丁|町)目?|番(町|丁)|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])"))
                                       _regex))))]
                            (if (.match city #"^京都市")
                              #js [town (new RegExp (+ ".*" regex))]
                              #js [town (new RegExp (+ "^" regex))])))))
                    (aset cachedTownRegexes (+ (+ pref "-") city) regexes)
                    #js [2 regexes])))))))))
"""


# exports.getTownRegexes = function (pref, city) { return __awaiter(void 0, void 0, void 0, function () {
#     var cachedResult, towns, regexes;
#     return __generator(this, function (_a) {
#         switch (_a.label) {
#             case 0:
#                 cachedResult = cachedTownRegexes[pref + "-" + city];
#                 if (typeof cachedResult !== 'undefined') {
#                     return [2 /*return*/, cachedResult];
#                 }
#                 return [4 /*yield*/, exports.getTowns(pref, city)
#                     // 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
#                 ];
#             case 1:
#                 towns = _a.sent();
#                 // 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
#                 towns.sort(function (a, b) {
#                     return b.length - a.length;
#                 });
#                 regexes = towns.map(function (town) {
#                     var regex = dict_1.toRegex(town
#                         .replace(/大?字/g, '(大?字)?')
#                         // 以下住所マスターの町丁目に含まれる数字を正規表現に変換する
#                         .replace(/([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/g, function (match) {
#                         var regexes = [];
#                         regexes.push(match
#                             .toString()
#                             .replace(/(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/, '')); // 漢数字
#                         if (match.match(/^壱/)) {
#                             regexes.push('一');
#                             regexes.push('1');
#                             regexes.push('１');
#                         }
#                         else {
#                             var num = match
#                                 .replace(/([一二三四五六七八九十]+)/g, function (match) {
#                                 return kan2num_1.kan2num(match);
#                             })
#                                 .replace(/(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/, '');
#                             regexes.push(num.toString()); // 半角アラビア数字
#                         }
#                         // 以下の正規表現は、上のよく似た正規表現とは違うことに注意！
#                         var _regex = "(" + regexes.join('|') + ")((\u4E01|\u753A)\u76EE?|\u756A(\u753A|\u4E01)|\u6761|\u8ED2|\u7DDA|\u306E\u753A?|\u5730\u5272|[-\uFF0D\uFE63\u2212\u2010\u2043\u2011\u2012\u2013\u2014\uFE58\u2015\u23AF\u23E4\u30FC\uFF70\u2500\u2501])";
#                         return _regex; // デバッグのときにめんどくさいので変数に入れる。
#                     }));
#                     if (city.match(/^京都市/)) {
#                         return [town, new RegExp(".*" + regex)];
#                     }
#                     else {
#                         return [town, new RegExp("^" + regex)];
#                     }
#                 });
#                 cachedTownRegexes[pref + "-" + city] = regexes;
#                 return [2 /*return*/, regexes];
#         }
#     });
# }); };

# 地名照合
def match_regexes(regexes: Iterable[Tuple[str, str,]], addr: str) -> Tuple[Optional[str], str]:
    addr = addr.strip()
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
def getCity(prefectures: Dict[str, Iterable[str]], pref: str, addr: str) -> Tuple[Optional[str], str]:
    cities: Tuple[str, ...] = tuple(prefectures.get(pref, tuple()))
    cityRegexes: Tuple[Tuple[str, str,]] = getCityRegexes(cities)
    return match_regexes(cityRegexes, addr)


def normalizeTownName(addr: str, pref: str, city: str, config: Config) -> Tuple[Optional[str], str]:
    townRegexes: Tuple[Tuple[str, str,]] = getTownRegexes(pref, city, config)
    addr = addr.replace(r'^大字', '')
    return match_regexes(townRegexes, addr)


# 都道府県名の推測
def estimatePref(prefectures: Dict[str, Iterable[str]], addr: str, config: Config) -> Optional[str]:
    # 都道府県名が省略されている
    matched: List = []
    for _pref in prefectures:
        cities = prefectures.get(_pref, None)
        cityRegexes = getCityRegexes(cities)
        addr = addr.strip()
        for _city, reg in cityRegexes:
            m = re.match(reg, addr)
            if m is not None:
                matched.append({PREF: _pref, CITY: _city, ADDRESS: addr[len(m.group()):], })

    # マッチする都道府県が複数ある場合は町名まで正規化して都道府県名を判別する。（例: 東京都府中市と広島県府中市など）
    if len(matched) == 1:
        return matched[0][PREF]
    for m in matched:
        pref, addr = normalizeTownName(m[ADDRESS], m[PREF], m[CITY], config)
        if pref is not None:
            return pref
    return None
