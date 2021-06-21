"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.normalize = exports.config = void 0;

var _japaneseNumeral = require("@geolonia/japanese-numeral");

var _kan2num = require("./lib/kan2num");

var _zen2han = require("./lib/zen2han");

var _patchAddr = require("./lib/patchAddr");

var _cacheRegexes = require("./lib/cacheRegexes");

var _config = require("./config");

function _slicedToArray(arr, i) {
    return (
        _arrayWithHoles(arr) ||
        _iterableToArrayLimit(arr, i) ||
        _unsupportedIterableToArray(arr, i) ||
        _nonIterableRest()
    );
}

function _nonIterableRest() {
    throw new TypeError(
        "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."
    );
}

function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(o);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))
        return _arrayLikeToArray(o, minLen);
}

function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;
    for (var i = 0, arr2 = new Array(len); i < len; i++) {
        arr2[i] = arr[i];
    }
    return arr2;
}

function _iterableToArrayLimit(arr, i) {
    var _i =
        arr &&
        ((typeof Symbol !== "undefined" && arr[Symbol.iterator]) ||
            arr["@@iterator"]);
    if (_i == null) return;
    var _arr = [];
    var _n = true;
    var _d = false;
    var _s, _e;
    try {
        for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) {
            _arr.push(_s.value);
            if (i && _arr.length === i) break;
        }
    } catch (err) {
        _d = true;
        _e = err;
    } finally {
        try {
            if (!_n && _i["return"] != null) _i["return"]();
        } finally {
            if (_d) throw _e;
        }
    }
    return _arr;
}

function _arrayWithHoles(arr) {
    if (Array.isArray(arr)) return arr;
}

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
    try {
        var info = gen[key](arg);
        var value = info.value;
    } catch (error) {
        reject(error);
        return;
    }
    if (info.done) {
        resolve(value);
    } else {
        Promise.resolve(value).then(_next, _throw);
    }
}

function _asyncToGenerator(fn) {
    return function () {
        var self = this,
            args = arguments;
        return new Promise(function (resolve, reject) {
            var gen = fn.apply(self, args);

            function _next(value) {
                asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
            }

            function _throw(err) {
                asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
            }

            _next(undefined);
        });
    };
}

var config = _config.currentConfig;
exports.config = config;
var defaultOption = {
    level: 3
};

var normalizeTownName = /*#__PURE__*/ (function () {
    var _ref = _asyncToGenerator(
        /*#__PURE__*/ regeneratorRuntime.mark(function _callee(addr, pref, city) {
            var townRegexes, i, _townRegexes$i, _town, reg, match;

            return regeneratorRuntime.wrap(function _callee$(_context) {
                while (1) {
                    switch ((_context.prev = _context.next)) {
                        case 0:
                            addr = addr.trim().replace(/^大字/, "");
                            _context.next = 3;
                            return (0, _cacheRegexes.getTownRegexes)(pref, city);

                        case 3:
                            townRegexes = _context.sent;
                            i = 0;

                        case 5:
                            if (!(i < townRegexes.length)) {
                                _context.next = 13;
                                break;
                            }

                            (_townRegexes$i = _slicedToArray(townRegexes[i], 2)),
                                (_town = _townRegexes$i[0]),
                                (reg = _townRegexes$i[1]);
                            match = addr.match(reg);

                            if (!match) {
                                _context.next = 10;
                                break;
                            }

                            return _context.abrupt("return", {
                                town: _town,
                                addr: addr.substr(match[0].length)
                            });

                        case 10:
                            i++;
                            _context.next = 5;
                            break;

                        case 13:
                        case "end":
                            return _context.stop();
                    }
                }
            }, _callee);
        })
    );

    return function normalizeTownName(_x, _x2, _x3) {
        return _ref.apply(this, arguments);
    };
})();

var normalize = /*#__PURE__*/ (function () {
    var _ref2 = _asyncToGenerator(
        /*#__PURE__*/ regeneratorRuntime.mark(function _callee2(address) {
            var option,
                addr,
                pref,
                city,
                town,
                level,
                prefectures,
                prefs,
                prefRegexes,
                i,
                _prefRegexes$i,
                _pref,
                reg,
                matched,
                _pref2,
                cities,
                cityRegexes,
                _i2,
                _cityRegexes$_i,
                _city,
                regex,
                match,
                _i3,
                normalized,
                _cities,
                _cityRegexes,
                _i4,
                _cityRegexes$_i2,
                _city2,
                _regex,
                _match,
                _normalized,
                _args2 = arguments;

            return regeneratorRuntime.wrap(function _callee2$(_context2) {
                while (1) {
                    switch ((_context2.prev = _context2.next)) {
                        case 0:
                            option =
                                _args2.length > 1 && _args2[1] !== undefined
                                    ? _args2[1]
                                    : defaultOption;

                            /**
                             * 入力された住所に対して以下の正規化を予め行う。
                             *
                             * 1. `1-2-3` や `四-五-六` のようなフォーマットのハイフンを半角に統一。
                             * 2. 町丁目以前にあるスペースをすべて削除。
                             * 3. 最初に出てくる `1-` や `五-` のような文字列を町丁目とみなして、それ以前のスペースをすべて削除する。
                             */
                            addr = address
                                .replace(/　/g, " ")
                                .replace(/ +/g, " ")
                                .replace(/([０-９Ａ-Ｚａ-ｚ]+)/g, function (match) {
                                    // 全角のアラビア数字は問答無用で半角にする
                                    return (0, _zen2han.zen2han)(match);
                                })
                                .replace(
                                    /([0-9０-９一二三四五六七八九〇十百千][-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])|([-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])[0-9０-９一二三四五六七八九〇十]/g,
                                    function (match) {
                                        return match.replace(/[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g, "-");
                                    }
                                )
                                .replace(
                                    /(.+)(丁目?|番(町|地|丁)|条|軒|線|(の|ノ)町|地割)/,
                                    function (match) {
                                        return match.replace(/ /g, ""); // 町丁目名以前のスペースはすべて削除
                                    }
                                )
                                .replace(
                                    /.+?[0-9一二三四五六七八九〇十百千]-/,
                                    function (match) {
                                        return match.replace(/ /g, ""); // 1番はじめに出てくるアラビア数字以前のスペースを削除
                                    }
                                );
                            pref = "";
                            city = "";
                            town = "";
                            level = 0; // 都道府県名の正規化

                            _context2.next = 8;
                            return (0, _cacheRegexes.getPrefectures)();

                        case 8:
                            prefectures = _context2.sent;
                            prefs = Object.keys(prefectures);
                            prefRegexes = (0, _cacheRegexes.getPrefectureRegexes)(prefs);
                            i = 0;

                        case 12:
                            if (!(i < prefRegexes.length)) {
                                _context2.next = 21;
                                break;
                            }

                            (_prefRegexes$i = _slicedToArray(prefRegexes[i], 2)),
                                (_pref = _prefRegexes$i[0]),
                                (reg = _prefRegexes$i[1]);

                            if (!addr.match(reg)) {
                                _context2.next = 18;
                                break;
                            }

                            pref = _pref;
                            addr = addr.substring(pref.length); // 都道府県名以降の住所

                            return _context2.abrupt("break", 21);

                        case 18:
                            i++;
                            _context2.next = 12;
                            break;

                        case 21:
                            if (pref) {
                                _context2.next = 37;
                                break;
                            }

                            // 都道府県名が省略されている
                            matched = [];

                            for (_pref2 in prefectures) {
                                cities = prefectures[_pref2];
                                cityRegexes = (0, _cacheRegexes.getCityRegexes)(_pref2, cities);
                                addr = addr.trim();

                                for (_i2 = 0; _i2 < cityRegexes.length; _i2++) {
                                    (_cityRegexes$_i = _slicedToArray(cityRegexes[_i2], 2)),
                                        (_city = _cityRegexes$_i[0]),
                                        (regex = _cityRegexes$_i[1]);
                                    match = addr.match(regex);

                                    if (match) {
                                        matched.push({
                                            pref: _pref2,
                                            city: _city,
                                            addr: addr.substring(match[0].length)
                                        });
                                    }
                                }
                            } // マッチする都道府県が複数ある場合は町名まで正規化して都道府県名を判別する。（例: 東京都府中市と広島県府中市など）

                            if (!(1 === matched.length)) {
                                _context2.next = 28;
                                break;
                            }

                            pref = matched[0].pref;
                            _context2.next = 37;
                            break;

                        case 28:
                            _i3 = 0;

                        case 29:
                            if (!(_i3 < matched.length)) {
                                _context2.next = 37;
                                break;
                            }

                            _context2.next = 32;
                            return normalizeTownName(
                                matched[_i3].addr,
                                matched[_i3].pref,
                                matched[_i3].city
                            );

                        case 32:
                            normalized = _context2.sent;

                            if (normalized) {
                                pref = matched[_i3].pref;
                            }

                        case 34:
                            _i3++;
                            _context2.next = 29;
                            break;

                        case 37:
                            if (!(pref && option.level >= 2)) {
                                _context2.next = 52;
                                break;
                            }

                            _cities = prefectures[pref];
                            _cityRegexes = (0, _cacheRegexes.getCityRegexes)(pref, _cities);
                            addr = addr.trim();
                            _i4 = 0;

                        case 42:
                            if (!(_i4 < _cityRegexes.length)) {
                                _context2.next = 52;
                                break;
                            }

                            (_cityRegexes$_i2 = _slicedToArray(_cityRegexes[_i4], 2)),
                                (_city2 = _cityRegexes$_i2[0]),
                                (_regex = _cityRegexes$_i2[1]);
                            _match = addr.match(_regex);

                            if (!_match) {
                                _context2.next = 49;
                                break;
                            }

                            city = _city2;
                            addr = addr.substring(_match[0].length); // 市区町村名以降の住所

                            return _context2.abrupt("break", 52);

                        case 49:
                            _i4++;
                            _context2.next = 42;
                            break;

                        case 52:
                            if (!(city && option.level >= 3)) {
                                _context2.next = 58;
                                break;
                            }

                            _context2.next = 55;
                            return normalizeTownName(addr, pref, city);

                        case 55:
                            _normalized = _context2.sent;

                            if (_normalized) {
                                town = _normalized.town;
                                addr = _normalized.addr;
                            }

                            addr = addr
                                .replace(/^-/, "")
                                .replace(/([0-9]+)(丁目)/g, function (match) {
                                    return match.replace(/([0-9]+)/g, function (num) {
                                        return (0, _japaneseNumeral.number2kanji)(Number(num));
                                    });
                                })
                                .replace(
                                    /(([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号)\s*(.+)/,
                                    "$1 $5"
                                )
                                .replace(
                                    /([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号?/,
                                    "$1-$3"
                                )
                                .replace(/([0-9〇一二三四五六七八九十百千]+)番地?/, "$1")
                                .replace(/([0-9〇一二三四五六七八九十百千]+)の/g, "$1-")
                                .replace(
                                    /([0-9〇一二三四五六七八九十百千]+)[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g,
                                    function (match) {
                                        return (0, _kan2num.kan2num)(match).replace(
                                            /[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g,
                                            "-"
                                        );
                                    }
                                )
                                .replace(
                                    /[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]([0-9〇一二三四五六七八九十百千]+)/g,
                                    function (match) {
                                        return (0, _kan2num.kan2num)(match).replace(
                                            /[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]/g,
                                            "-"
                                        );
                                    }
                                )
                                .replace(/([0-9〇一二三四五六七八九十百千]+)-/, function (s) {
                                    // `1-` のようなケース
                                    return (0, _kan2num.kan2num)(s);
                                })
                                .replace(/-([0-9〇一二三四五六七八九十百千]+)/, function (s) {
                                    // `-1` のようなケース
                                    return (0, _kan2num.kan2num)(s);
                                })
                                .replace(
                                    /-[^0-9]+([0-9〇一二三四五六七八九十百千]+)/,
                                    function (s) {
                                        // `-あ1` のようなケース
                                        return (0, _kan2num.kan2num)((0, _zen2han.zen2han)(s));
                                    }
                                )
                                .replace(/([0-9〇一二三四五六七八九十百千]+)$/, function (s) {
                                    // `串本町串本１２３４` のようなケース
                                    return (0, _kan2num.kan2num)(s);
                                })
                                .trim();

                        case 58:
                            addr = (0, _patchAddr.patchAddr)(pref, city, town, addr);
                            if (pref) level = level + 1;
                            if (city) level = level + 1;
                            if (town) level = level + 1;
                            return _context2.abrupt("return", {
                                pref: pref,
                                city: city,
                                town: town,
                                addr: addr,
                                level: level
                            });

                        case 63:
                        case "end":
                            return _context2.stop();
                    }
                }
            }, _callee2);
        })
    );

    return function normalize(_x4) {
        return _ref2.apply(this, arguments);
    };
})();

exports.normalize = normalize;
