"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getTownRegexes = exports.getTowns = exports.getCityRegexes = exports.getPrefectureRegexes = exports.getPrefectures = void 0;
var axios_1 = require("axios");
var dict_1 = require("./dict");
var kan2num_1 = require("./kan2num");
var config_1 = require("../config");
var cachedPrefectureRegexes = undefined;
var cachedCityRegexes = {};
var cachedTownRegexes = {};
var cachedPrefectures = undefined;
var cachedTowns = {};
exports.getPrefectures = function () { return __awaiter(void 0, void 0, void 0, function () {
    var resp;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                if (typeof cachedPrefectures !== 'undefined') {
                    return [2 /*return*/, cachedPrefectures];
                }
                return [4 /*yield*/, axios_1.default.get(config_1.currentConfig.japaneseAddressesApi + ".json")];
            case 1:
                resp = _a.sent();
                return [2 /*return*/, (cachedPrefectures = resp.data)];
        }
    });
}); };
exports.getPrefectureRegexes = function (prefs) {
    if (cachedPrefectureRegexes) {
        return cachedPrefectureRegexes;
    }
    cachedPrefectureRegexes = prefs.map(function (pref) {
        var _pref = pref.replace(/(都|道|府|県)$/, ''); // `東京` の様に末尾の `都府県` が抜けた住所に対応
        var reg = new RegExp("^" + _pref + "(\u90FD|\u9053|\u5E9C|\u770C)");
        return [pref, reg];
    });
    return cachedPrefectureRegexes;
};
exports.getCityRegexes = function (pref, cities) {
    var cachedResult = cachedCityRegexes[pref];
    if (typeof cachedResult !== 'undefined') {
        return cachedResult;
    }
    // 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    cities.sort(function (a, b) {
        return b.length - a.length;
    });
    var regexes = cities.map(function (city) {
        var regex;
        if (city.match(/(町|村)$/)) {
            regex = new RegExp("^" + dict_1.toRegex(city).replace(/(.+?)郡/, '($1郡)?')); // 郡が省略されてるかも
        }
        else {
            regex = new RegExp("^" + dict_1.toRegex(city));
        }
        return [city, regex];
    });
    cachedCityRegexes[pref] = regexes;
    return regexes;
};
exports.getTowns = function (pref, city) { return __awaiter(void 0, void 0, void 0, function () {
    var cacheKey, cachedTown, responseTowns, towns;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                cacheKey = pref + "-" + city;
                cachedTown = cachedTowns[cacheKey];
                if (typeof cachedTown !== 'undefined') {
                    return [2 /*return*/, cachedTown];
                }
                return [4 /*yield*/, axios_1.default.get([
                        config_1.currentConfig.japaneseAddressesApi,
                        encodeURI(pref),
                        encodeURI(city) + '.json',
                    ].join('/'))];
            case 1:
                responseTowns = _a.sent();
                towns = responseTowns.data;
                return [2 /*return*/, (cachedTowns[cacheKey] = towns)];
        }
    });
}); };
exports.getTownRegexes = function (pref, city) { return __awaiter(void 0, void 0, void 0, function () {
    var cachedResult, towns, regexes;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                cachedResult = cachedTownRegexes[pref + "-" + city];
                if (typeof cachedResult !== 'undefined') {
                    return [2 /*return*/, cachedResult];
                }
                return [4 /*yield*/, exports.getTowns(pref, city)
                    // 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
                ];
            case 1:
                towns = _a.sent();
                // 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
                towns.sort(function (a, b) {
                    return b.length - a.length;
                });
                regexes = towns.map(function (town) {
                    var regex = dict_1.toRegex(town
                        .replace(/大?字/g, '(大?字)?')
                        // 以下住所マスターの町丁目に含まれる数字を正規表現に変換する
                        .replace(/([壱一二三四五六七八九十]+)(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/g, function (match) {
                        var regexes = [];
                        regexes.push(match
                            .toString()
                            .replace(/(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/, '')); // 漢数字
                        if (match.match(/^壱/)) {
                            regexes.push('一');
                            regexes.push('1');
                            regexes.push('１');
                        }
                        else {
                            var num = match
                                .replace(/([一二三四五六七八九十]+)/g, function (match) {
                                return kan2num_1.kan2num(match);
                            })
                                .replace(/(丁目?|番(町|丁)|条|軒|線|(の|ノ)町|地割)/, '');
                            regexes.push(num.toString()); // 半角アラビア数字
                        }
                        // 以下の正規表現は、上のよく似た正規表現とは違うことに注意！
                        var _regex = "(" + regexes.join('|') + ")((\u4E01|\u753A)\u76EE?|\u756A(\u753A|\u4E01)|\u6761|\u8ED2|\u7DDA|\u306E\u753A?|\u5730\u5272|[-\uFF0D\uFE63\u2212\u2010\u2043\u2011\u2012\u2013\u2014\uFE58\u2015\u23AF\u23E4\u30FC\uFF70\u2500\u2501])";
                        return _regex; // デバッグのときにめんどくさいので変数に入れる。
                    }));
                    if (city.match(/^京都市/)) {
                        return [town, new RegExp(".*" + regex)];
                    }
                    else {
                        return [town, new RegExp("^" + regex)];
                    }
                });
                cachedTownRegexes[pref + "-" + city] = regexes;
                return [2 /*return*/, regexes];
        }
    });
}); };
