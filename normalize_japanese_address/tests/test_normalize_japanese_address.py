#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple

from ..lib.const import ADDRESS, CITY, LEVEL, PREF, TOWN
from ..lib.config import DEFAULT_OPTION
from ..normalize import normalize


TEST_PATTERNS: List[Tuple[str, Dict[str, str]]] = [

        # 追加テスト
        ('東京都府中市南町6-32', {PREF: "東京都", CITY: "府中市", TOWN: "南町", ADDRESS: "6", LEVEL: 3}),
        # 市制施行
        ('福岡県筑紫郡那珂川町大字松木4', {PREF: "福岡県", CITY: "那珂川市", TOWN: "松木", ADDRESS: "4", LEVEL: 3}),
        # 合併
        ('下都賀郡岩舟町大字静5132番地2', {PREF: "栃木県", CITY: "栃木市", TOWN: "岩舟町静", ADDRESS: "5132-2", LEVEL: 3}),
        # 該当データなし
        ('名古屋市瑞穂区彌富町字月見ケ岡32', {PREF: "愛知県", CITY: "名古屋市瑞穂区", TOWN: "弥富町月見ケ岡", ADDRESS: "32", LEVEL: 3}),
        ('愛知県名古屋市瑞穂区弥富町月見ケ岡32', {PREF: "愛知県", CITY: "名古屋市瑞穂区", TOWN: "弥富町月見ケ岡", ADDRESS: "32", LEVEL: 3}),
        # そのほか
        ('宮崎県都城市北原町24', {PREF: "宮崎県", CITY: "都城市", TOWN: "北原町", ADDRESS: "24", LEVEL: 3}),
        ('都城市北原町24', {PREF: "宮崎県", CITY: "都城市", TOWN: "北原町", ADDRESS: "24", LEVEL: 3}),
        ('山梨県都留市上谷一丁目1番1号', {PREF: "山梨県", CITY: "都留市", TOWN: "上谷一丁目", ADDRESS: "1-1", LEVEL: 3}),
        ('広島県安芸郡府中町大通三丁目5番1号', {PREF: "広島県", CITY: "安芸郡府中町", TOWN: "大通三丁目", ADDRESS: "5-1", LEVEL: 3}),
        ('広島県府中市行縢町38', {PREF: "広島県", CITY: "府中市", TOWN: "行縢町", ADDRESS: "38", LEVEL: 3}),

        ### TrueScript版のテスト
        ('大阪府堺市北区新金岡町4丁1−8', {PREF: "大阪府", CITY: "堺市北区", TOWN: "新金岡町四丁", ADDRESS: "1-8", LEVEL: 3}),
        ('大阪府堺市北区新金岡町４丁１ー８', {PREF: "大阪府", CITY: "堺市北区", TOWN: "新金岡町四丁", ADDRESS: "1-8", LEVEL: 3}),
        ('和歌山県串本町串本1234', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本1234', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本千二百三十四', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本一千二百三十四', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本一二三四', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町くじ野川一二三四', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "鬮野川", ADDRESS: "1234", LEVEL: 3}),
        ('京都府京都市中京区寺町通御池上る上本能寺前町488番地', {PREF: "京都府", CITY: "京都市中京区", TOWN: "上本能寺前町", ADDRESS: "488", LEVEL: 3}),
        ('京都府京都市中京区上本能寺前町488', {PREF: "京都府", CITY: "京都市中京区", TOWN: "上本能寺前町", ADDRESS: "488", LEVEL: 3}),
        ('大阪府大阪市中央区大手前２-１', {PREF: "大阪府", CITY: "大阪市中央区", TOWN: "大手前二丁目", ADDRESS: "1", LEVEL: 3}),
        ('北海道札幌市西区24-2-2-3-3', {PREF: "北海道", CITY: "札幌市西区", TOWN: "二十四軒二条二丁目", ADDRESS: "3-3", LEVEL: 3}),
        ('京都府京都市東山区大和大路2-537-1', {PREF: "京都府", CITY: "京都市東山区", TOWN: "大和大路二丁目", ADDRESS: "537-1", LEVEL: 3}),
        ('京都府京都市東山区大和大路2丁目五百三十七の1', {PREF: "京都府", CITY: "京都市東山区", TOWN: "大和大路二丁目", ADDRESS: "537-1", LEVEL: 3}),
        ('愛知県蒲郡市旭町17番1号', {PREF: "愛知県", CITY: "蒲郡市", TOWN: "旭町", ADDRESS: "17-1", LEVEL: 3}),
        ('北海道岩見沢市栗沢町万字寿町１−２', {PREF: "北海道", CITY: "岩見沢市", TOWN: "栗沢町万字寿町", ADDRESS: "1-2", LEVEL: 3}),
        ('北海道久遠郡せたな町北檜山区北檜山１９３', {PREF: "北海道", CITY: "久遠郡せたな町",
                                  TOWN: "北檜山区北檜山" if DEFAULT_OPTION.is_exact else '北桧山区北桧山', ADDRESS: "193",
        LEVEL: 3}),
        ('北海道久遠郡せたな町北桧山区北桧山１９３', {PREF: "北海道", CITY: "久遠郡せたな町",
                                  TOWN: "北檜山区北檜山" if DEFAULT_OPTION.is_exact else '北桧山区北桧山', ADDRESS: "193", LEVEL: 3}),
        ('京都府京都市中京区錦小路通大宮東入七軒町466', {PREF: "京都府", CITY: "京都市中京区", TOWN: "七軒町", ADDRESS: "466", LEVEL: 3}),
        ('栃木県佐野市七軒町2201', {PREF: "栃木県", CITY: "佐野市", TOWN: "七軒町", ADDRESS: "2201", LEVEL: 3}),
        ('京都府京都市東山区大和大路通三条下る東入若松町393', {PREF: "京都府", CITY: "京都市東山区", TOWN: "若松町", ADDRESS: "393", LEVEL: 3}),
        ('長野県長野市長野東之門町2462', {PREF: "長野県", CITY: "長野市", TOWN: "大字長野", ADDRESS: "東之門町2462", LEVEL: 3}),
        ('岩手県下閉伊郡普代村第１地割上村４３−２５', {PREF: "岩手県", CITY: "下閉伊郡普代村", TOWN: "第一地割字上村", ADDRESS: "43-25", LEVEL: 3}),
        ('岩手県花巻市下北万丁目１７４−１', {PREF: "岩手県", CITY: "花巻市", TOWN: "下北万丁目", ADDRESS: "174-1", LEVEL: 3}),
        ('岩手県花巻市十二丁目１１９２', {PREF: "岩手県", CITY: "花巻市", TOWN: "十二丁目", ADDRESS: "1192", LEVEL: 3}),
        ('岩手県滝沢市後２６８−５６６', {PREF: "岩手県", CITY: "滝沢市", TOWN: "後", ADDRESS: "268-566", LEVEL: 3}),
        ('青森県五所川原市金木町喜良市千苅６２−８', {PREF: "青森県", CITY: "五所川原市", TOWN: "金木町喜良市", ADDRESS: "千苅62-8", LEVEL: 3}),
        ('岩手県盛岡市盛岡駅西通２丁目９番地１号', {PREF: "岩手県", CITY: "盛岡市", TOWN: "盛岡駅西通二丁目", ADDRESS: "9-1", LEVEL: 3}),
        ('岩手県盛岡市盛岡駅西通２丁目９の１', {PREF: "岩手県", CITY: "盛岡市", TOWN: "盛岡駅西通二丁目", ADDRESS: "9-1", LEVEL: 3}),
        ('岩手県盛岡市盛岡駅西通２の９の１', {PREF: "岩手県", CITY: "盛岡市", TOWN: "盛岡駅西通二丁目", ADDRESS: "9-1", LEVEL: 3}),
        ('岩手県盛岡市盛岡駅西通２丁目９番地１号 マリオス10F',
         {PREF: "岩手県", CITY: "盛岡市", TOWN: "盛岡駅西通二丁目", ADDRESS: "9-1 マリオス10F", LEVEL: 3}),
        ('東京都文京区千石4丁目15-7', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('東京都文京区千石四丁目15-7', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('東京都文京区千石4丁目15－7', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('東京都 文京区千石4丁目15－7', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('東京都文京区 千石4丁目15－7', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('東京都文京区千石4-15-7 ', {PREF: "東京都", CITY: "文京区", TOWN: "千石四丁目", ADDRESS: "15-7", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本 833', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "833", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町串本　833', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "833", LEVEL: 3}),
        ('東京都世田谷区上北沢４の９の２', {PREF: "東京都", CITY: "世田谷区", TOWN: "上北沢四丁目", ADDRESS: "9-2", LEVEL: 3}),
        ('東京都品川区東五反田２丁目５－１１', {PREF: "東京都", CITY: "品川区", TOWN: "東五反田二丁目", ADDRESS: "5-11", LEVEL: 3}),
        ('東京都世田谷区上北沢四丁目2-1', {PREF: "東京都", CITY: "世田谷区", TOWN: "上北沢四丁目", ADDRESS: "2-1", LEVEL: 3}),
        ('東京都世田谷区上北沢4-2-1', {PREF: "東京都", CITY: "世田谷区", TOWN: "上北沢四丁目", ADDRESS: "2-1", LEVEL: 3}),
        ('東京都世田谷区上北沢４ー２ー１', {PREF: "東京都", CITY: "世田谷区", TOWN: "上北沢四丁目", ADDRESS: "2-1", LEVEL: 3}),
        ('東京都世田谷区上北沢４－２－１', {PREF: "東京都", CITY: "世田谷区", TOWN: "上北沢四丁目", ADDRESS: "2-1", LEVEL: 3}),
        ('東京都品川区西五反田2丁目31-6', {PREF: "東京都", CITY: "品川区", TOWN: "西五反田二丁目", ADDRESS: "31-6", LEVEL: 3}),
        ('東京都品川区西五反田2-31-6', {PREF: "東京都", CITY: "品川区", TOWN: "西五反田二丁目", ADDRESS: "31-6", LEVEL: 3}),
        ('大阪府大阪市此花区西九条三丁目２－１６', {PREF: "大阪府", CITY: "大阪市此花区", TOWN: "西九条三丁目", ADDRESS: "2-16", LEVEL: 3}),
        ('大阪府大阪市此花区西九条三丁目2番16号', {PREF: "大阪府", CITY: "大阪市此花区", TOWN: "西九条三丁目", ADDRESS: "2-16", LEVEL: 3}),
        ('大阪府大阪市此花区西九条3-2-16', {PREF: "大阪府", CITY: "大阪市此花区", TOWN: "西九条三丁目", ADDRESS: "2-16", LEVEL: 3}),
        ('大阪府大阪市此花区西九条３丁目２－１６', {PREF: "大阪府", CITY: "大阪市此花区", TOWN: "西九条三丁目", ADDRESS: "2-16", LEVEL: 3}),
        ('大阪府大阪市此花区西九条3-2-16', {PREF: "大阪府", CITY: "大阪市此花区", TOWN: "西九条三丁目", ADDRESS: "2-16", LEVEL: 3}),
        ('千葉県鎌ケ谷市中佐津間２丁目１５－１４－９', {PREF: "千葉県", CITY: "鎌ヶ谷市", TOWN: "中佐津間二丁目", ADDRESS: "15-14-9", LEVEL: 3}),
        ('岐阜県不破郡関ケ原町関ヶ原１７０１−６', {PREF: "岐阜県", CITY: "不破郡関ケ原町", TOWN: "大字関ケ原", ADDRESS: "1701-6", LEVEL: 3}),
        ('岐阜県関ケ原町関ヶ原１７０１−６', {PREF: "岐阜県", CITY: "不破郡関ケ原町", TOWN: "大字関ケ原", ADDRESS: "1701-6", LEVEL: 3}),
        ('東京都町田市木曽東4丁目14-イ22', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('東京都町田市木曽東4丁目14ーイ22', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('東京都町田市木曽東四丁目十四ーイ二十二', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('東京都町田市木曽東四丁目１４ーイ２２', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('東京都町田市木曽東四丁目１４のイ２２', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('岩手県花巻市南万丁目127', {PREF: "岩手県", CITY: "花巻市", TOWN: "南万丁目", ADDRESS: "127", LEVEL: 3}),
        ('和歌山県東牟婁郡串本町田並1512', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "田並", ADDRESS: "1512", LEVEL: 3}),
        ('神奈川県川崎市多摩区東三田1-2-2', {PREF: "神奈川県", CITY: "川崎市多摩区", TOWN: "東三田一丁目", ADDRESS: "2-2", LEVEL: 3}),
        ('東京都町田市木曽東４の１４のイ２２', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('東京都町田市木曽東４ー１４ーイ２２', {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22", LEVEL: 3}),
        ('富山県富山市三番町1番23号', {PREF: "富山県", CITY: "富山市", TOWN: "三番町", ADDRESS: "1-23", LEVEL: 3}),
        ('富山県富山市3-1-23', {PREF: "富山県", CITY: "富山市", TOWN: "三番町", ADDRESS: "1-23", LEVEL: 3}),
        ('富山県富山市中央通り3-1-23', {PREF: "富山県", CITY: "富山市", TOWN: "中央通り三丁目", ADDRESS: "1-23", LEVEL: 3}),
        ('埼玉県南埼玉郡宮代町大字国納３０9－１', {PREF: "埼玉県", CITY: "南埼玉郡宮代町", TOWN: "大字国納", ADDRESS: "309-1", LEVEL: 3}),
        ('埼玉県南埼玉郡宮代町国納３０9－１', {PREF: "埼玉県", CITY: "南埼玉郡宮代町", TOWN: "大字国納", ADDRESS: "309-1", LEVEL: 3}),
        ('大阪府高槻市奈佐原２丁目１－２ メゾンエトワール',
         {PREF: "大阪府", CITY: "高槻市", TOWN: "奈佐原二丁目", ADDRESS: "1-2 メゾンエトワール", LEVEL: 3}),
        ('埼玉県八潮市大字大瀬１丁目１－１', {PREF: "埼玉県", CITY: "八潮市", TOWN: "大瀬一丁目", ADDRESS: "1-1", LEVEL: 3}),
        ('岡山県笠岡市大宜1249－1', {PREF: "岡山県", CITY: "笠岡市", TOWN: "大宜", ADDRESS: "1249-1", LEVEL: 3}),
        ('岡山県笠岡市大宜1249－1', {PREF: "岡山県", CITY: "笠岡市", TOWN: "大宜", ADDRESS: "1249-1", LEVEL: 3}),
        ('岡山県笠岡市大冝1249－1', {PREF: "岡山県", CITY: "笠岡市", TOWN: "大宜", ADDRESS: "1249-1", LEVEL: 3}),
        ('岡山県岡山市中区さい33-2', {PREF: "岡山県", CITY: "岡山市中区", TOWN: "さい", ADDRESS: "33-2", LEVEL: 3}),
        ('岡山県岡山市中区穝33-2', {PREF: "岡山県", CITY: "岡山市中区", TOWN: "さい", ADDRESS: "33-2", LEVEL: 3}),
        ('千葉県松戸市栄町３丁目１６６－５', {PREF: "千葉県", CITY: "松戸市", TOWN: "栄町三丁目", ADDRESS: "166-5", LEVEL: 3}),
        ('東京都新宿区三栄町１７－１６', {PREF: "東京都", CITY: "新宿区", TOWN: "四谷三栄町", ADDRESS: "17-16", LEVEL: 3}),
        ('東京都新宿区三榮町１７－１６', {PREF: "東京都", CITY: "新宿区", TOWN: "四谷三栄町", ADDRESS: "17-16", LEVEL: 3}),
        ('新潟県新潟市中央区礎町通１ノ町１９６８−１', {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "礎町通一ノ町", ADDRESS: "1968-1", LEVEL: 3}),
        ('新潟県新潟市中央区礎町通１の町１９６８−１', {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "礎町通一ノ町", ADDRESS: "1968-1", LEVEL: 3}),
        ('新潟県新潟市中央区礎町通１の町１９６８の１', {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "礎町通一ノ町", ADDRESS: "1968-1", LEVEL: 3}),
        ('新潟県新潟市中央区礎町通1-1968-1', {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "礎町通一ノ町", ADDRESS: "1968-1", LEVEL: 3}),
        ('新潟県新潟市中央区上大川前通11番町1881-2',
         {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "上大川前通十一番町", ADDRESS: "1881-2", LEVEL: 3}),
        ('新潟県新潟市中央区上大川前通11-1881-2',
         {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "上大川前通十一番町", ADDRESS: "1881-2", LEVEL: 3}),
        ('新潟県新潟市中央区上大川前通十一番町1881-2',
         {PREF: "新潟県", CITY: "新潟市中央区", TOWN: "上大川前通十一番町", ADDRESS: "1881-2", LEVEL: 3}),
        ('埼玉県上尾市壱丁目１１１', {PREF: "埼玉県", CITY: "上尾市", TOWN: "大字壱丁目", ADDRESS: "111", LEVEL: 3}),
        ('埼玉県上尾市一丁目１１１', {PREF: "埼玉県", CITY: "上尾市", TOWN: "大字壱丁目", ADDRESS: "111", LEVEL: 3}),
        ('埼玉県上尾市一町目１１１', {PREF: "埼玉県", CITY: "上尾市", TOWN: "大字壱丁目", ADDRESS: "111", LEVEL: 3}),
        ('埼玉県上尾市壱町目１１１', {PREF: "埼玉県", CITY: "上尾市", TOWN: "大字壱丁目", ADDRESS: "111", LEVEL: 3}),
        ('埼玉県上尾市1-111', {PREF: "埼玉県", CITY: "上尾市", TOWN: "大字壱丁目", ADDRESS: "111", LEVEL: 3}),
        ('神奈川県横浜市港北区大豆戸町１７番地１１', {PREF: "神奈川県", CITY: "横浜市港北区", TOWN: "大豆戸町", ADDRESS: "17-11", LEVEL: 3}),
        ('神奈川県横浜市港北区大豆戸町１７番地１１', {LEVEL: 1},
         {PREF: "神奈川県", CITY: "", TOWN: "", ADDRESS: "横浜市港北区大豆戸町17番地11", LEVEL: 1}),
        ('神奈川県横浜市港北区大豆戸町１７番地１１', {LEVEL: 2},
         {PREF: "神奈川県", CITY: "横浜市港北区", TOWN: "", ADDRESS: "大豆戸町17番地11", LEVEL: 2}),
        ('神奈川県横浜市港北区大豆戸町１７番地１１', {LEVEL: 3},
         {PREF: "神奈川県", CITY: "横浜市港北区", TOWN: "大豆戸町", ADDRESS: "17-11", LEVEL: 3}),
        ('神奈川県横浜市港北区', {LEVEL: 3}, {PREF: "神奈川県", CITY: "横浜市港北区", TOWN: "", ADDRESS: "", LEVEL: 2}),
        ('神奈川県', {LEVEL: 3}, {PREF: "神奈川県", CITY: "", TOWN: "", ADDRESS: "", LEVEL: 1}),
        ('神奈川県あいうえお市', {PREF: "神奈川県", CITY: "", TOWN: "", ADDRESS: "あいうえお市", LEVEL: 1}),
        ('東京都港区あいうえお', {PREF: "東京都", CITY: "港区", TOWN: "", ADDRESS: "あいうえお", LEVEL: 2}),
        ('あいうえお', {PREF: "", CITY: "", TOWN: "", ADDRESS: "あいうえお", LEVEL: 0}),
        ('東京都江東区豊洲1丁目2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都江東区豊洲 1丁目2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都江東区豊洲 1-2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都 江東区 豊洲 1-2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都江東区豊洲 １ー２ー２７', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都町田市木曽東四丁目１４ーイ２２ ジオロニアマンション',
         {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-イ22 ジオロニアマンション", LEVEL: 3}),
        ('東京都町田市木曽東四丁目１４ーＡ２２ ジオロニアマンション',
         {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-A22 ジオロニアマンション", LEVEL: 3}),
        ('東京都町田市木曽東四丁目一四━Ａ二二 ジオロニアマンション',
         {PREF: "東京都", CITY: "町田市", TOWN: "木曽東四丁目", ADDRESS: "14-A22 ジオロニアマンション", LEVEL: 3}),
        ('東京都江東区豊洲 一丁目2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲一丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('東京都江東区豊洲 四-2-27', {PREF: "東京都", CITY: "江東区", TOWN: "豊洲四丁目", ADDRESS: "2-27", LEVEL: 3}),
        ('石川県七尾市藤橋町亥45番地1', {PREF: "石川県", CITY: "七尾市", TOWN: "藤橋町", ADDRESS: "亥45-1", LEVEL: 3}),
        ('石川県七尾市藤橋町亥四十五番地1', {PREF: "石川県", CITY: "七尾市", TOWN: "藤橋町", ADDRESS: "亥45-1", LEVEL: 3}),
        ('石川県七尾市藤橋町 亥 四十五番地1', {PREF: "石川県", CITY: "七尾市", TOWN: "藤橋町", ADDRESS: "亥45-1", LEVEL: 3}),
        ('石川県七尾市藤橋町 亥 45-1', {PREF: "石川県", CITY: "七尾市", TOWN: "藤橋町", ADDRESS: "亥45-1", LEVEL: 3}),
        ('和歌山県和歌山市 七番丁 19', {PREF: "和歌山県", CITY: "和歌山市", TOWN: "七番丁", ADDRESS: "19", LEVEL: 3}),
        ('和歌山県和歌山市7番町19', {PREF: "和歌山県", CITY: "和歌山市", TOWN: "七番丁", ADDRESS: "19", LEVEL: 3}),
        ('和歌山県和歌山市十二番丁45', {PREF: "和歌山県", CITY: "和歌山市", TOWN: "十二番丁", ADDRESS: "45", LEVEL: 3}),
        ('和歌山県和歌山市12番丁45', {PREF: "和歌山県", CITY: "和歌山市", TOWN: "十二番丁", ADDRESS: "45", LEVEL: 3}),
        ('和歌山県和歌山市12-45', {PREF: "和歌山県", CITY: "和歌山市", TOWN: "十二番丁", ADDRESS: "45", LEVEL: 3}),
        ('兵庫県宝塚市東洋町1番1号', {PREF: "兵庫県", CITY: "宝塚市", TOWN: "東洋町", ADDRESS: "1-1", LEVEL: 3}),
        ('兵庫県宝塚市東洋町1番1号', {PREF: "兵庫県", CITY: "宝塚市", TOWN: "東洋町", ADDRESS: "1-1", LEVEL: 3}),
        ('北海道札幌市中央区北三条西３丁目１－５６マルゲンビル３Ｆ',
         {PREF: "北海道", CITY: "札幌市中央区", TOWN: "北三条西三丁目", ADDRESS: "1-56マルゲンビル3F", LEVEL: 3}),
        ('北海道札幌市北区北２４条西６丁目１−１', {PREF: "北海道", CITY: "札幌市北区", TOWN: "北二十四条西六丁目", ADDRESS: "1-1", LEVEL: 3}),
        ('堺市北区新金岡町4丁1−8', {PREF: "大阪府", CITY: "堺市北区", TOWN: "新金岡町四丁", ADDRESS: "1-8", LEVEL: 3}),
        ('串本町串本1234', {PREF: "和歌山県", CITY: "東牟婁郡串本町", TOWN: "串本", ADDRESS: "1234", LEVEL: 3}),
        ('広島県府中市府川町315', {PREF: "広島県", CITY: "府中市", TOWN: "府川町", ADDRESS: "315", LEVEL: 3}),
        ('府中市府川町315', {PREF: "広島県", CITY: "府中市", TOWN: "府川町", ADDRESS: "315", LEVEL: 3}),
        ('府中市宮西町2丁目24番地', {PREF: "東京都", CITY: "府中市", TOWN: "宮西町二丁目", ADDRESS: "24", LEVEL: 3}),
        ('三重県三重郡菰野町大字大強原2796', {PREF: "三重県", CITY: "三重郡菰野町", TOWN: "大字大強原", ADDRESS: "2796", LEVEL: 3}),
        ('三重県三重郡菰野町大強原2796', {PREF: "三重県", CITY: "三重郡菰野町", TOWN: "大字大強原", ADDRESS: "2796", LEVEL: 3}),
        ('福岡県北九州市小倉南区大字井手浦874', {PREF: "福岡県", CITY: "北九州市小倉南区", TOWN: "大字井手浦", ADDRESS: "874", LEVEL: 3}),
        ('福岡県北九州市小倉南区井手浦874', {PREF: "福岡県", CITY: "北九州市小倉南区", TOWN: "大字井手浦", ADDRESS: "874", LEVEL: 3}),
        ('沖縄県那覇市小禄１丁目５番２３号１丁目マンション３０１',
         {PREF: "沖縄県", CITY: "那覇市", TOWN: "小禄一丁目", ADDRESS: "5-23 一丁目マンション301", LEVEL: 3}),
        ('香川県仲多度郡まんのう町勝浦字家六２０９４番地１',
         {PREF: "香川県", CITY: "仲多度郡まんのう町", TOWN: "勝浦", ADDRESS: "家六2094-1", LEVEL: 3}),
        ('香川県仲多度郡まんのう町勝浦家六２０９４番地１', {PREF: "香川県", CITY: "仲多度郡まんのう町", TOWN: "勝浦", ADDRESS: "家六2094-1", LEVEL: 3}),
        ('愛知県あま市西今宿梶村一３８番地４', {PREF: "愛知県", CITY: "あま市", TOWN: "西今宿", ADDRESS: "梶村一38-4", LEVEL: 3}),
        ('香川県丸亀市原田町字東三分一１９２６番地１', {PREF: "香川県", CITY: "丸亀市", TOWN: "原田町", ADDRESS: "東三分一1926-1", LEVEL: 3})
        ]


def test_normalize_japanese_address(patterns: List[Tuple[str, Dict[str, str]]] = TEST_PATTERNS) -> None:
    count: int = 0
    errors: int = 0
    for i, p in enumerate(patterns):
        if len(p) == 2:
            raw, expected = p
        elif len(p) == 3:
            raw, option, expected = p
        else:
            raise Exception('invalid pattern found')
        # print(i+1, p)
        answer: Dict[str, str] = normalize(raw)
        count += 1
        error_flag = 0
        if answer != expected:
            print(f'#{i+1:04} test failed: {raw}')
            r: List[str] = list()
            for k in [PREF, CITY, TOWN, ADDRESS]:
                if answer[k] != expected[k]:
                    error_flag = True
                    r.append(f'{k}:{expected[k]} ({answer[k]})')
            if error_flag:
                errors += 1
            print(f'                   {r}')
    ratio: float = errors/float(count)
    print(f'total num errors: {errors}/{count} ({ratio:.1%})')


if __name__ == '__main__':
    test_normalize_japanese_address()

