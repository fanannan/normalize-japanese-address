#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import Callable, Final, List, Tuple, Union
import unicodedata
#
from .zen2han import zen2han

# JIS 第2水準 => 第1水準 及び 旧字体 => 新字体
JIS_OLD_KANJI: Final[List[str]] = \
    '亞,圍,壹,榮,驛,應,櫻,假,會,懷,覺,樂,陷,歡,氣,戲,據,挾,區,徑,溪,輕,藝,儉,圈,權,嚴,恆,' \
    '國,齋,雜,蠶,殘,兒,實,釋,從,縱,敍,燒,條,剩,壤,釀,眞,盡,醉,髓,聲,竊,淺,錢,禪,爭,插,騷,' \
    '屬,對,滯,擇,單,斷,癡,鑄,敕,鐵,傳,黨,鬪,屆,腦,廢,發,蠻,拂,邊,瓣,寶,沒,滿,藥,餘,樣,亂,' \
    '兩,禮,靈,爐,灣,惡,醫,飮,營,圓,歐,奧,價,繪,擴,學,罐,勸,觀,歸,犧,擧,狹,驅,莖,經,繼,缺,' \
    '劍,檢,顯,廣,鑛,碎,劑,參,慘,絲,辭,舍,壽,澁,肅,將,證,乘,疊,孃,觸,寢,圖,穗,樞,齊,攝,戰,' \
    '潛,雙,莊,裝,藏,續,體,臺,澤,膽,彈,蟲,廳,鎭,點,燈,盜,獨,貳,霸,賣,髮,祕,佛,變,辯,豐,飜,' \
    '默,與,譽,謠,覽,獵,勵,齡,勞,壓,爲,隱,衞,鹽,毆,穩,畫,壞,殼,嶽,卷,關,顏,僞,舊,峽,曉,勳,' \
    '惠,螢,鷄,縣,險,獻,驗,效,號,濟,册,棧,贊,齒,濕,寫,收,獸,處,稱,奬,淨,繩,讓,囑,愼,粹,隨,' \
    '數,靜,專,踐,纖,壯,搜,總,臟,墮,帶,瀧,擔,團,遲,晝,聽,遞,轉,當,稻,讀,惱,拜,麥,拔,濱,竝,' \
    '辨,舖,襃,萬,譯,豫,搖,來,龍,壘,隸,戀,樓,鰺,鶯,蠣,攪,竈,灌,諫,頸,礦,蘂,靱,賤,壺,礪,檮,' \
    '濤,邇,蠅,檜,儘,藪,籠'.split(',')

JIS_NEW_KANJI: Final[List[str]] = \
    '亜,囲,壱,栄,駅,応,桜,仮,会,懐,覚,楽,陥,歓,気,戯,拠,挟,区,径,渓,軽,芸,倹,圏,権,厳,恒,' \
    '国,斎,雑,蚕,残,児,実,釈,従,縦,叙,焼,条,剰,壌,醸,真,尽,酔,髄,声,窃,浅,銭,禅,争,挿,騒,' \
    '属,対,滞,択,単,断,痴,鋳,勅,鉄,伝,党,闘,届,脳,廃,発,蛮,払,辺,弁,宝,没,満,薬,余,様,乱,' \
    '両,礼,霊,炉,湾,悪,医,飲,営,円,欧,奥,価,絵,拡,学,缶,勧,観,帰,犠,挙,狭,駆,茎,経,継,欠,' \
    '剣,検,顕,広,鉱,砕,剤,参,惨,糸,辞,舎,寿,渋,粛,将,証,乗,畳,嬢,触,寝,図,穂,枢,斉,摂,戦,' \
    '潜,双,荘,装,蔵,続,体,台,沢,胆,弾,虫,庁,鎮,点,灯,盗,独,弐,覇,売,髪,秘,仏,変,弁,豊,翻,' \
    '黙,与,誉,謡,覧,猟,励,齢,労,圧,為,隠,衛,塩,殴,穏,画,壊,殻,岳,巻,関,顔,偽,旧,峡,暁,勲,' \
    '恵,蛍,鶏,県,険,献,験,効,号,済,冊,桟,賛,歯,湿,写,収,獣,処,称,奨,浄,縄,譲,嘱,慎,粋,随,' \
    '数,静,専,践,繊,壮,捜,総,臓,堕,帯,滝,担,団,遅,昼,聴,逓,転,当,稲,読,悩,拝,麦,抜,浜,並,' \
    '弁,舗,褒,万,訳,予,揺,来,竜,塁,隷,恋,楼,鯵,鴬,蛎,撹,竃,潅,諌,頚,砿,蕊,靭,賎,壷,砺,梼,' \
    '涛,迩,蝿,桧,侭,薮,篭'.split(',')

JIS_KANJI_REGEXES = [[f'{old}|{new}', old, new] for old, new in zip(JIS_OLD_KANJI, JIS_NEW_KANJI)]

# 以下なるべく文字数が多いものほど上にすること
REGEX_CUSTOM_PATTERNS: List[Tuple[str, str]] = [
        ("三栄町|四谷三栄町", '(三栄町|四谷三栄町)'),
        ("鬮野川|くじ野川|くじの川", '(鬮野川|くじ野川|くじの川)'),
        ("通り|とおり", '(通り|とおり)'),
        ("埠頭|ふ頭", '(埠頭|ふ頭)'),
        ("番町|番丁", '(番町|番丁)'),
        ("大冝|大宜", '(大冝|大宜)'),
        ("穝|さい", '(穝|さい)'),
        ("杁|えぶり", '(杁|えぶり)'),
        ("薭|稗|ひえ|ヒエ", '(薭|稗|ひえ|ヒエ)'),
        ("[之ノの]", '[之ノの]'),
        ("[ヶケが]", '[ヶケが]'),
        ("[ヵカか力]", '[ヵカか力]'),
        ("[ッツっつ]", '[ッツっつ]'),
        ("[ニ二]", '[ニ二]'),
        ("[ハ八]", '[ハ八]'),
        ("塚|塚", '(塚|塚)'),
        ("釜|竈", '(釜|竈)'),
        ("條|条", '(條|条)'),
        ("狛|拍", '(狛|拍)'),
        ("藪|薮", '(藪|薮)'),
        ("渕|淵", '(渕|淵)'),
        ("エ|ヱ|え", '(エ|ヱ|え)'),
        ("曾|曽", '(曾|曽)'),
        ]


def rep(s: str, search_pattern: str, replacee: str, replacement: Union[str, Callable]) -> str:
    matches: List[Tuple[Tuple[int, int], str]] = []
    for m in re.finditer(search_pattern, s):
        if isinstance(replacement, str):
            mx = [(m.span(), re.sub(replacee, replacement, m.group()))]
        else:
            mm = re.search(replacee, m.group())
            for scan, new in mm.groups():
                mx = []
        matches = mx+matches
    #
    t: str = s[:]
    for span, new in matches:
        t = t[:span[0]]+new+t[span[1]:]
    return t


# 本関数の出典
# https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja
def unicode_normalize(cls, s):
    pt = re.compile('([{}]+)'.format(cls))

    def norm(c):
        return unicodedata.normalize('NFKC', c) if pt.match(c) else c

    s = ''.join(norm(x) for x in re.split(pt, s))
    s = re.sub('－', '-', s)
    return s


# 本関数の出典
# https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja
def remove_extra_spaces(s: str, remove_spaces_inbetween: bool) -> str:
    s = re.sub('[ 　]+', ' ', s)
    blocks = ''.join(('\u4E00-\u9FFF',  # CJK UNIFIED IDEOGRAPHS
                      '\u3040-\u309F',  # HIRAGANA
                      '\u30A0-\u30FF',  # KATAKANA
                      '\u3000-\u303F',  # CJK SYMBOLS AND PUNCTUATION
                      '\uFF00-\uFFEF'   # HALFWIDTH AND FULLWIDTH FORMS
                      ))
    basic_latin = '\u0000-\u007F'

    def remove_space_between(cls1, cls2, s):
        p = re.compile('([{}]) ([{}])'.format(cls1, cls2))
        while p.search(s):
            s = p.sub(r'\1\2', s)
        return s

    if remove_spaces_inbetween:
        s = remove_space_between(blocks, blocks, s)
        s = remove_space_between(blocks, basic_latin, s)
        s = remove_space_between(basic_latin, blocks, s)
    return s


# 本関数の出典
# https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja
def normalize_neologd(s: str, remove_spaces_inbetween:bool=False) -> str:
    s = s.strip()
    s = unicode_normalize('０-９Ａ-Ｚａ-ｚ｡-ﾟ', s)

    def maketrans(f, t):
        return {ord(x): ord(y) for x, y in zip(f, t)}

    s = re.sub('[˗֊‐‑‒–⁃⁻₋−]+', '-', s)  # normalize hyphens
    s = re.sub('[﹣－ｰ—―─━ー]+', 'ー', s)  # normalize choonpus
    s = re.sub('[~∼∾〜〰～]', '', s)  # remove tildes
    s = s.translate(
        maketrans('!"#$%&\'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣',
              '！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」'))

    s = remove_extra_spaces(s, remove_spaces_inbetween=remove_spaces_inbetween)
    s = unicode_normalize('！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜', s)  # keep ＝,・,「,」
    s = re.sub('[’]', '\'', s)
    s = re.sub('[”]', '"', s)
    return s


def preprocess(address: str):
    # 入力された住所に対して以下の正規化を予め行う。
    # 1. `1-2-3` や `四-五-六` のようなフォーマットのハイフンを半角に統一。
    # 2. 町丁目以前にあるスペースをすべて削除。
    # 3. 最初に出てくる `1-` や `五-` のような文字列を町丁目とみなして、それ以前のスペースをすべて削除する。
    addr: str = unicodedata.normalize('NFKC', address).replace('　', ' ').replace(' +', ' ')
    # 全角のアラビア数字[０-９Ａ-Ｚａ-ｚ]+は問答無用で半角にする
    addr = zen2han(addr)
    addr = rep(addr,
               "([0-9０-９一二三四五六七八九〇十百千][-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])|([-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])[0-9０-９一二三四五六七八九〇十]",
               "/[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", '-')
    # 町丁目名以前のスペースはすべて削除
    addr = rep(addr,
               "(.+)(丁目?|番(町|地|丁)|条|軒|線|(の|ノ)町|地割)",
               " ", '')
    # 1番はじめに出てくるアラビア数字以前のスペースを削除
    addr = rep(addr,
               ".+?[0-9一二三四五六七八九〇十百千]-",
               " ", '')
    return addr


def jisKanji(s: str) -> str:
    for regex, old, new in JIS_KANJI_REGEXES:
        s = s.replace(regex, f'({old}|{new})')
    return s


def toRegex(s: str):
    for regex, p in REGEX_CUSTOM_PATTERNS:
        s = rep(s, regex, regex, p)
    s = jisKanji(s)
    return s

