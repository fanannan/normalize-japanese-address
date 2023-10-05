
This is to standardize Japanese addresses by separating them into sets of prefecture, city, town, and additional details, based on Geolonia's TypeScript library (https://github.com/geolonia/normalize-japanese-addresses). 
It is 
currently still in the early stage and does not behave exactly the same as Geolonia's original library (fails 
in 7.1% of tests). 

Geolonia様のオープンソースの住所正規化ライブラリ( https://github.com/geolonia/normalize-japanese-addresses )をPythonに移植したものです。
現在まだ試作段階であり、Geolonia様のもとのライブラリと完全に同じ動作にはなっていません（テストのうち7.1%で失敗）。

## インストール方法

- Windows環境の場合は、インストールの前に環境変数を設定してください
```
set PYTHONUTF8=1
```

```
pip install --upgrade normalize_japanese_address
```

## 使い方

```python
from normalize_japanese_address.normalize import normalize

result = normalize('大阪府堺市北区新金岡町4丁1−8')
print(result)
```

とすると、resultに
```python
{'pref': '大阪府', 'city': '堺市北区', 'town': '新金岡町四丁', 'address': '1-8', 'level': 3, 'lat': 34.568184,  'long': 135.519409}
```
を返します。levelは、住所文字列のどこまでを判別できたかを以下の数値で示しています。

* `0` - 都道府県も判別できなかった。
* `1` - 都道府県まで判別できた。
* `2` - 市区町村まで判別できた。
* `3` - 町丁目まで判別できた。

## ライブラリの名称
- normalize-japanese-addressesではなく、normalize_japanese_address という名称になっています。ハイフンがアンダーバーになっているほか、addressが単数になっているのに深い意味はありません。


## メンテナンス
- https://github.com/geolonia/japanese-addresses/tree/develop/api が更新された場合、それに対応している japanese_address/api 以下を新しいものに差し替えれることで更新できます。

## ライセンス、利用規約
- 本プログラムは、下記のプログラムをもとに開発されています。住所データのライセンスは CC BY 4.0、それ以外はMITとされており、本プログラムもそれに従います。

https://github.com/geolonia/normalize-japanese-addresses
https://github.com/geolonia/japanese-addresses
