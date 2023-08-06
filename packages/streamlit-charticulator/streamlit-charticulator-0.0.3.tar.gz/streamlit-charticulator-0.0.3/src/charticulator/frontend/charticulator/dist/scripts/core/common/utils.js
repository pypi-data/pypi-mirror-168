"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
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
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.defineCategories = exports.getRandom = exports.parseSafe = exports.getFormat = exports.tickFormatParserExpression = exports.getTimeFormatFunction = exports.isUtcTimeZone = exports.setTimeZone = exports.setFormatOptions = exports.getFormatOptions = exports.replaceSymbolByTab = exports.replaceSymbolByNewLine = exports.replaceTabBySymbol = exports.splitStringByNewLine = exports.replaceNewLineBySymbol = exports.getTimeZoneOffset = exports.refineColumnName = exports.compareMarkAttributeNames = exports.colorAttributes = exports.applyDateFormat = exports.getSortDirection = exports.getSortFunctionByData = exports.hexToRgb = exports.rgbToHex = exports.compareVersion = exports.parseVersion = exports.MultistringHashMap = exports.HashMap = exports.KeyNameMap = exports.stableSortBy = exports.sortBy = exports.stableSort = exports.gather = exports.getIndexByName = exports.getByName = exports.getIndexById = exports.getById = exports.indexOf = exports.fillDefaults = exports.getField = exports.setField = exports.argMin = exports.min = exports.argMax = exports.max = exports.shallowClone = exports.deepClone = exports.makeRange = exports.transpose = exports.zipArray = exports.zip = void 0;
var d3_time_format_1 = require("d3-time-format");
var d3_format_1 = require("d3-format");
var _1 = require(".");
var types_1 = require("../specification/types");
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/** zip two arrays, return an iterator */
function zip(a, b) {
    var i;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                i = 0;
                _a.label = 1;
            case 1:
                if (!(i < a.length)) return [3 /*break*/, 4];
                return [4 /*yield*/, [a[i], b[i]]];
            case 2:
                _a.sent();
                _a.label = 3;
            case 3:
                i++;
                return [3 /*break*/, 1];
            case 4: return [2 /*return*/];
        }
    });
}
exports.zip = zip;
/** zip two arrays, return a new array */
function zipArray(a, b) {
    if (a.length < b.length) {
        return a.map(function (elem, idx) { return [elem, b[idx]]; });
    }
    else {
        return b.map(function (elem, idx) { return [a[idx], elem]; });
    }
}
exports.zipArray = zipArray;
/** Transpose a matrix r[i][j] = matrix[j][i] */
function transpose(matrix) {
    if (matrix == undefined) {
        return undefined;
    }
    if (matrix.length == 0) {
        return [];
    }
    var jLength = matrix[0].length;
    var r = [];
    for (var j = 0; j < jLength; j++) {
        var rj = [];
        for (var i = 0; i < matrix.length; i++) {
            rj.push(matrix[i][j]);
        }
        r.push(rj);
    }
    return r;
}
exports.transpose = transpose;
/** Generate a range of integers: [start, end) */
function makeRange(start, end) {
    var r = [];
    for (var i = start; i < end; i++) {
        r.push(i);
    }
    return r;
}
exports.makeRange = makeRange;
/** Deep clone an object. The object must be JSON-serializable */
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}
exports.deepClone = deepClone;
function shallowClone(obj) {
    var r = {};
    for (var key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            r[key] = obj[key];
        }
    }
    return r;
}
exports.shallowClone = shallowClone;
function max(array, accessor) {
    // Credit: https://github.com/d3/d3-array/blob/master/src/max.js
    var i = -1;
    var n = array.length;
    var value;
    var max;
    while (++i < n) {
        if ((value = accessor(array[i], i, array)) != null && value >= value) {
            max = value;
            while (++i < n) {
                if ((value = accessor(array[i], i, array)) != null && value > max) {
                    max = value;
                }
            }
        }
    }
    return max;
}
exports.max = max;
function argMax(array, accessor) {
    var i = -1;
    var n = array.length;
    var value;
    var max;
    var argmax = -1;
    while (++i < n) {
        if ((value = accessor(array[i], i, array)) != null && value >= value) {
            max = value;
            argmax = i;
            while (++i < n) {
                if ((value = accessor(array[i], i, array)) != null && value > max) {
                    max = value;
                    argmax = i;
                }
            }
        }
    }
    return argmax;
}
exports.argMax = argMax;
function min(array, accessor) {
    // Credit: https://github.com/d3/d3-array/blob/master/src/min.js
    var i = -1;
    var n = array.length;
    var value;
    var min;
    while (++i < n) {
        if ((value = accessor(array[i], i, array)) != null && value >= value) {
            min = value;
            while (++i < n) {
                if ((value = accessor(array[i], i, array)) != null && min > value) {
                    min = value;
                }
            }
        }
    }
    return min;
}
exports.min = min;
function argMin(array, accessor) {
    var i = -1;
    var n = array.length;
    var value;
    var min;
    var argmin;
    while (++i < n) {
        if ((value = accessor(array[i], i, array)) != null && value >= value) {
            min = value;
            argmin = i;
            while (++i < n) {
                if ((value = accessor(array[i], i, array)) != null && min > value) {
                    min = value;
                    argmin = i;
                }
            }
        }
    }
    return argmin;
}
exports.argMin = argMin;
function setField(obj, field, value) {
    var p = obj;
    if (typeof field == "string" || typeof field == "number") {
        p[field] = value;
    }
    else {
        for (var i = 0; i < field.length - 1; i++) {
            if (p[field[i]] == undefined) {
                p[field[i]] = {};
            }
            p = p[field[i]];
        }
        p[field[field.length - 1]] = value;
    }
    return obj;
}
exports.setField = setField;
function getField(obj, field) {
    var p = obj;
    if (typeof field == "string" || typeof field == "number") {
        return p[field];
    }
    else {
        var fieldList = field;
        for (var i = 0; i < fieldList.length - 1; i++) {
            if (p[fieldList[i]] == undefined) {
                return undefined;
            }
            p = p[fieldList[i]];
        }
        return p[fieldList[fieldList.length - 1]];
    }
}
exports.getField = getField;
/** Fill default values into an object */
function fillDefaults(obj, defaults) {
    if (obj == null) {
        obj = {};
    }
    for (var key in defaults) {
        if (Object.prototype.hasOwnProperty.call(defaults, key)) {
            if (!Object.prototype.hasOwnProperty.call(obj, key)) {
                obj[key] = defaults[key];
            }
        }
    }
    return obj;
}
exports.fillDefaults = fillDefaults;
/** Find the index of the first element that satisfies the predicate, return -1 if not found */
function indexOf(array, predicate) {
    for (var i = 0; i < array.length; i++) {
        if (predicate(array[i], i)) {
            return i;
        }
    }
    return -1;
}
exports.indexOf = indexOf;
/** Get the first element with element._id == id, return null if not found */
function getById(array, id) {
    for (var i = 0; i < array.length; i++) {
        if (array[i]._id == id) {
            return array[i];
        }
    }
    return null;
}
exports.getById = getById;
/** Get the index of the first element with element._id == id, return -1 if not found */
function getIndexById(array, id) {
    for (var i = 0; i < array.length; i++) {
        if (array[i]._id == id) {
            return i;
        }
    }
    return -1;
}
exports.getIndexById = getIndexById;
/** Get the first element with element.name == name, return null if not found */
function getByName(array, name) {
    for (var i = 0; i < array.length; i++) {
        if (array[i].name == name) {
            return array[i];
        }
    }
    return null;
}
exports.getByName = getByName;
/** Get the index of the first element with element.name == name, return -1 if not found */
function getIndexByName(array, name) {
    for (var i = 0; i < array.length; i++) {
        if (array[i].name == name) {
            return i;
        }
    }
    return -1;
}
exports.getIndexByName = getIndexByName;
function gather(array, keyFunction) {
    var e_1, _a;
    var map = new Map();
    array.forEach(function (item, index) {
        var key = keyFunction(item, index);
        if (map.has(key)) {
            map.get(key).push(item);
        }
        else {
            map.set(key, [item]);
        }
    });
    var r = [];
    try {
        for (var _b = __values(map.values()), _c = _b.next(); !_c.done; _c = _b.next()) {
            var array_1 = _c.value;
            r.push(array_1);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return r;
}
exports.gather = gather;
/**
 * Sort an array with compare function, make sure when compare(a, b) == 0,
 * a and b are still in the original order (i.e., stable)
 */
function stableSort(array, compare) {
    return (array
        // Convert to [ item, index ]
        .map(function (x, index) { return [x, index]; })
        // Sort by compare then by index to stabilize
        .sort(function (a, b) {
        var c = compare(a[0], b[0]);
        if (c != 0) {
            return c;
        }
        else {
            return a[1] - b[1];
        }
    })
        // Extract items back
        .map(function (x) { return x[0]; }));
}
exports.stableSort = stableSort;
/** Sort an array by key given by keyFunction */
function sortBy(array, keyFunction, reverse) {
    if (reverse === void 0) { reverse = false; }
    if (reverse) {
        return array.sort(function (a, b) {
            var ka = keyFunction(a);
            var kb = keyFunction(b);
            if (ka == kb) {
                return 0;
            }
            return ka < kb ? +1 : -1;
        });
    }
    else {
        return array.sort(function (a, b) {
            var ka = keyFunction(a);
            var kb = keyFunction(b);
            if (ka == kb) {
                return 0;
            }
            return ka < kb ? -1 : +1;
        });
    }
}
exports.sortBy = sortBy;
/** Stable sort an array by key given by keyFunction */
function stableSortBy(array, keyFunction, reverse) {
    if (reverse === void 0) { reverse = false; }
    if (reverse) {
        return stableSort(array, function (a, b) {
            var ka = keyFunction(a);
            var kb = keyFunction(b);
            if (ka == kb) {
                return 0;
            }
            return ka < kb ? +1 : -1;
        });
    }
    else {
        return stableSort(array, function (a, b) {
            var ka = keyFunction(a);
            var kb = keyFunction(b);
            if (ka == kb) {
                return 0;
            }
            return ka < kb ? -1 : +1;
        });
    }
}
exports.stableSortBy = stableSortBy;
/** Map object that maps (Object, string) into ValueType */
var KeyNameMap = /** @class */ (function () {
    function KeyNameMap() {
        this.mapping = new Map();
    }
    /** Add a new entry to the map */
    KeyNameMap.prototype.add = function (key, name, value) {
        if (this.mapping.has(key)) {
            this.mapping.get(key)[name] = value;
        }
        else {
            var item = {};
            item[name] = value;
            this.mapping.set(key, item);
        }
    };
    /** Delete an entry (do nothing if not exist) */
    KeyNameMap.prototype.delete = function (key, name) {
        if (this.mapping.has(key)) {
            delete this.mapping.get(key)[name];
        }
    };
    /** Determine if the map has an entry */
    KeyNameMap.prototype.has = function (key, name) {
        if (this.mapping.has(key)) {
            return Object.prototype.hasOwnProperty.call(this.mapping.get(key), name);
        }
        return false;
    };
    /** Get the value corresponding to an entry, return null if not found */
    KeyNameMap.prototype.get = function (key, name) {
        if (this.mapping.has(key)) {
            var m = this.mapping.get(key);
            if (Object.prototype.hasOwnProperty.call(m, name)) {
                return m[name];
            }
            return null;
        }
        return null;
    };
    KeyNameMap.prototype.forEach = function (callback) {
        this.mapping.forEach(function (v, key) {
            for (var p in v) {
                if (Object.prototype.hasOwnProperty.call(v, p)) {
                    callback(v[p], key, p);
                }
            }
        });
    };
    return KeyNameMap;
}());
exports.KeyNameMap = KeyNameMap;
var HashMap = /** @class */ (function () {
    function HashMap() {
        this.map = new Map();
    }
    HashMap.prototype.set = function (key, value) {
        this.map.set(this.hash(key), value);
    };
    HashMap.prototype.get = function (key) {
        return this.map.get(this.hash(key));
    };
    HashMap.prototype.has = function (key) {
        return this.map.has(this.hash(key));
    };
    HashMap.prototype.delete = function (key) {
        this.map.delete(this.hash(key));
    };
    HashMap.prototype.clear = function () {
        this.map.clear();
    };
    HashMap.prototype.values = function () {
        return this.map.values();
    };
    return HashMap;
}());
exports.HashMap = HashMap;
var MultistringHashMap = /** @class */ (function (_super) {
    __extends(MultistringHashMap, _super);
    function MultistringHashMap() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // eslint-disable-next-line
        _this.separator = Math.random().toString(36).substr(2);
        return _this;
    }
    MultistringHashMap.prototype.hash = function (key) {
        return key.join(this.separator);
    };
    return MultistringHashMap;
}(HashMap));
exports.MultistringHashMap = MultistringHashMap;
/** Parse semver version string into a ParsedVersion */
function parseVersion(version) {
    var m = version.match(/^(\d+)\.(\d+)\.(\d+)$/);
    return {
        major: +m[1],
        minor: +m[2],
        patch: +m[3],
    };
}
exports.parseVersion = parseVersion;
/**
 * Compare two version strings
 * @param version1 version number 1
 * @param version2 version number 2
 * @returns negative if version1 < version2, zero if version1 == version2, positive if version1 > version2
 */
function compareVersion(version1, version2) {
    var p1 = parseVersion(version1);
    var p2 = parseVersion(version2);
    // Compare major version first, then minor and patch.
    if (p1.major != p2.major) {
        return p1.major - p2.major;
    }
    if (p1.minor != p2.minor) {
        return p1.minor - p2.minor;
    }
    return p1.patch - p2.patch;
}
exports.compareVersion = compareVersion;
function componentToHex(c) {
    var hex = Math.round(c).toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
/**
 * Converts Color object to Hex
 * @param color Color object
 * @returns Hex representation of color
 */
function rgbToHex(color) {
    if (!color) {
        return null;
    }
    return ("#" +
        componentToHex(color.r) +
        componentToHex(color.g) +
        componentToHex(color.b));
}
exports.rgbToHex = rgbToHex;
/**
 * Converts Hex to Color object
 * @param color Color object
 * @returns Hex representation of color
 */
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
        }
        : null;
}
exports.hexToRgb = hexToRgb;
/**
 * Return common comparator for two values or sope specific comparator for specific data type
 * testToRange function compares properly, strings with numbers: number-number, number-, number+
 * to sort value ranges list properly
 */
function getSortFunctionByData(values) {
    var testToRange = function (value) {
        var reg = /(\d-)|(\d+-\d+)|(\d+\+)/;
        var match = value.match(reg);
        if (match && match.length) {
            return true;
        }
        return false;
    };
    if (values.length > 0) {
        var testResult = values
            .map(function (val) { return testToRange(val); })
            .reduceRight(function (a, b) { return a && b; });
        if (testResult) {
            return function (a, b) {
                if (a && b) {
                    var aNum = a.match(/\d+/)[0];
                    var bNum = b.match(/\d+/)[0];
                    return +aNum < +bNum
                        ? 1
                        : +a.split("-").pop() < +b.split("-").pop()
                            ? 1
                            : -1;
                }
            };
        }
    }
    return function (a, b) { return (a < b ? -1 : 1); };
}
exports.getSortFunctionByData = getSortFunctionByData;
/**
 * Retunrs sort direction by comparing the first and the last values of string array
 */
function getSortDirection(values) {
    var direction = "ascending";
    if (values && values[0] && values[values.length - 1]) {
        var a = values[0].toString();
        var b = values[values.length - 1].toString();
        if (b && a && b.localeCompare(a) > -1) {
            direction = "ascending";
        }
        else {
            direction = "descending";
        }
    }
    return direction;
}
exports.getSortDirection = getSortDirection;
/**
 * Applies timeFormat function of d3 to value
 * @param value date value
 * @param format date format of d3
 */
function applyDateFormat(value, format) {
    return getTimeFormatFunction()(format)(value);
}
exports.applyDateFormat = applyDateFormat;
exports.colorAttributes = ["fill", "stroke", "color"];
/**
 * Compares attribute names
 */
function compareMarkAttributeNames(a, b) {
    if (a === b) {
        return true;
    }
    else {
        // fill and stroke uses with color. Those preoperties has the same meaning for marks
        if (exports.colorAttributes.indexOf(b) > -1 && exports.colorAttributes.indexOf(a) > -1) {
            return true;
        }
    }
}
exports.compareMarkAttributeNames = compareMarkAttributeNames;
function refineColumnName(name) {
    return name.replace(/[^0-9a-zA-Z_]/g, "_");
}
exports.refineColumnName = refineColumnName;
function getTimeZoneOffset(date) {
    return new Date(date).getTimezoneOffset() * 60 * 1000;
}
exports.getTimeZoneOffset = getTimeZoneOffset;
function replaceNewLineBySymbol(str) {
    return str === null || str === void 0 ? void 0 : str.replace(/\\n/g, "\n");
}
exports.replaceNewLineBySymbol = replaceNewLineBySymbol;
function splitStringByNewLine(str) {
    return str === null || str === void 0 ? void 0 : str.split(/\\n/g);
}
exports.splitStringByNewLine = splitStringByNewLine;
function replaceTabBySymbol(str) {
    return str === null || str === void 0 ? void 0 : str.replace(/\\t/g, "\t");
}
exports.replaceTabBySymbol = replaceTabBySymbol;
function replaceSymbolByNewLine(str) {
    return str === null || str === void 0 ? void 0 : str.replace(/\n/g, "\\n");
}
exports.replaceSymbolByNewLine = replaceSymbolByNewLine;
function replaceSymbolByTab(str) {
    return str === null || str === void 0 ? void 0 : str.replace(/\t/g, "\\t");
}
exports.replaceSymbolByTab = replaceSymbolByTab;
// eslint-disable-next-line no-var
var formatOptions = {
    decimal: ".",
    thousands: ",",
    grouping: [3],
    currency: ["$", ""],
};
// eslint-disable-next-line no-var
var utcTimeZoneOption = {
    utcTimeZone: true,
};
function getFormatOptions() {
    return __assign({}, formatOptions);
}
exports.getFormatOptions = getFormatOptions;
function setFormatOptions(options) {
    formatOptions = __assign({}, options);
}
exports.setFormatOptions = setFormatOptions;
function setTimeZone(utcTimeZone) {
    utcTimeZoneOption = {
        utcTimeZone: utcTimeZone,
    };
}
exports.setTimeZone = setTimeZone;
function isUtcTimeZone() {
    return utcTimeZoneOption.utcTimeZone;
}
exports.isUtcTimeZone = isUtcTimeZone;
function getTimeFormatFunction() {
    return isUtcTimeZone() ? d3_time_format_1.utcFormat : d3_time_format_1.timeFormat;
}
exports.getTimeFormatFunction = getTimeFormatFunction;
exports.tickFormatParserExpression = function () { return /\{([^}]+)\}/g; };
function getFormat() {
    return d3_format_1.formatLocale(formatOptions).format;
}
exports.getFormat = getFormat;
function parseSafe(value, defaultValue) {
    if (defaultValue === void 0) { defaultValue = null; }
    try {
        var parsedValue = JSON.parse(value);
        return parsedValue != undefined ? parsedValue : defaultValue;
    }
    catch (ex) {
        return defaultValue;
    }
}
exports.parseSafe = parseSafe;
function getRandom(startRange, endRange) {
    // eslint-disable-next-line
    return startRange + Math.random() * (endRange - startRange);
}
exports.getRandom = getRandom;
function defineCategories(vector) {
    var scale = new _1.Scale.CategoricalScale();
    vector = vector.sort(function (a, b) { return a - b; });
    scale.inferParameters(vector, types_1.OrderMode.order);
    var categories = new Array(scale.length);
    scale.domain.forEach(function (index, x) { return (categories[index] = x.toString()); });
    return categories;
}
exports.defineCategories = defineCategories;
//# sourceMappingURL=utils.js.map