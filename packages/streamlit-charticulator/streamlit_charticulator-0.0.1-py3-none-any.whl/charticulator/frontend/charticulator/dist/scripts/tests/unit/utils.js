"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.waitSolver = exports.loadJSON = exports.pathPrefix = exports.parseSVGTransform = exports.expect_deep_approximately_equals = exports.makeDefaultAttributes = void 0;
var chai_1 = require("chai");
var core_1 = require("../../core");
function makeDefaultAttributes(state) {
    var defaultAttributes = {};
    var elements = state.chart.elements;
    for (var i = 0; i < elements.length; i++) {
        var el = elements[i];
        defaultAttributes[el._id] = core_1.deepClone(state.chartState.elements[i].attributes);
    }
    return defaultAttributes;
}
exports.makeDefaultAttributes = makeDefaultAttributes;
/** Test if a deep equals b with tolerance on numeric values */
function expect_deep_approximately_equals(a, b, tol, context) {
    var e_1, _a;
    try {
        if (a == null && b == null) {
            return;
        }
        if (a == null || b == null) {
            // If either of a, b is null/undefined
            chai_1.expect(a).equals(b, "" + JSON.stringify(context, null, ""));
        }
        else if (typeof a == "object" && typeof b == "object") {
            if (a instanceof Array && b instanceof Array) {
                // Both are arrays, recursively test for each item in the arrays
                chai_1.expect(a.length).to.equals(b.length, "" + JSON.stringify(context, null, ""));
                for (var i = 0; i < a.length; i++) {
                    expect_deep_approximately_equals(a[i], b[i], tol, {
                        a: a,
                        b: b,
                    });
                }
            }
            else if (a instanceof Array || b instanceof Array) {
                // One of them is an array, the other one isn't, error
                throw new Error("type mismatch");
            }
            else {
                // Both are objects, recursively test for each key in the objects
                var keysA = Object.keys(a).sort();
                var keysB = Object.keys(b).sort();
                chai_1.expect(keysA).to.deep.equals(keysB, "" + JSON.stringify(context, null, ""));
                try {
                    for (var keysA_1 = __values(keysA), keysA_1_1 = keysA_1.next(); !keysA_1_1.done; keysA_1_1 = keysA_1.next()) {
                        var key = keysA_1_1.value;
                        expect_deep_approximately_equals(a[key], b[key], tol, { a: a, b: b, key: key });
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (keysA_1_1 && !keysA_1_1.done && (_a = keysA_1.return)) _a.call(keysA_1);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
            }
        }
        else {
            try {
                /**
                 Numeric attributes in the SVG tree are stored as strings and we are trying to
                 convert them to numbers and check for null. Such a check is needed to process
                 the SVG path. Example d="M 0,7.20843424 L 4.16179145,0 L 0,-7.20843424 L -4.16179145,0 Z"
                 It contains numbers and letters
                 */
                if (!isNaN(+a) && a != null) {
                    a = +a;
                }
                if (!isNaN(+b) && b != null) {
                    b = +b;
                }
            }
            catch (_b) { }
            if (typeof a == "number" && typeof b == "number") {
                // If both are numbers, test approximately equals
                chai_1.expect(a).to.approximately(b, tol, "" + JSON.stringify(context, null, ""));
            }
            else {
                var svgTransformA = parseSVGTransform(a);
                var svgTransformB = parseSVGTransform(b);
                if (Object.keys(svgTransformA).length &&
                    Object.keys(svgTransformB).length) {
                    expect_deep_approximately_equals(svgTransformA, svgTransformB, tol, {
                        a: a,
                        b: b,
                    });
                }
                if (context.key) {
                    if (context.key.localeCompare("d") === 0) {
                        var aT = parseSVGPath(a);
                        var bT = parseSVGPath(b);
                        expect_deep_approximately_equals(aT, bT, tol, {
                            a: a,
                            b: b,
                            key: context.key,
                        });
                    }
                }
                else {
                    // Otherwise, use regular equals
                    chai_1.expect(a).equals(b, "" + JSON.stringify(context, null, ""));
                }
            }
        }
    }
    catch (er) {
        console.log(er, context);
        throw er;
    }
}
exports.expect_deep_approximately_equals = expect_deep_approximately_equals;
/* tslint:disable */
function parseSVGTransform(a) {
    var b = {};
    for (var i in (a = a.match(/(\w+\((\-?\d+\.?\d*e?\-?\d*,?)+\))+/g))) {
        var c = a[i].match(/[\w\.\-]+/g);
        b[c.shift()] = c;
    }
    return b;
}
exports.parseSVGTransform = parseSVGTransform;
// The directory containing chart cases
exports.pathPrefix = "tests/unit/charts";
function loadJSON(url) {
    return __awaiter(this, void 0, void 0, function () {
        var responce, json;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(url)];
                case 1:
                    responce = _a.sent();
                    return [4 /*yield*/, responce.text()];
                case 2:
                    json = _a.sent();
                    return [2 /*return*/, JSON.parse(json)];
            }
        });
    });
}
exports.loadJSON = loadJSON;
function waitSolver() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, new Promise(function (resolve) { return setTimeout(resolve, 5000); })];
        });
    });
}
exports.waitSolver = waitSolver;
function parseSVGPath(d) {
    d = d.replace(/\s{2,}/g, " "); // Remove multiple spaces
    d = d.replace(/\\n/g, "");
    d = d.replace(/,/g, " ");
    d = d.replace(/([a-zA-Z])\s[0-9]/g, "$1,"); // Add letters to coords group
    var d1 = d.split(" "); // Split on space
    var coords = [];
    for (var i = 0; i < d1.length; i++) {
        var coordString = d1[i];
        var m = coordString.match(/\d+\.*\d*/);
        if (m && m.length) {
            coords.push(Math.round(+m[0]));
        }
        else {
            coords.push(coordString);
        }
    }
    return coords;
}
//# sourceMappingURL=utils.js.map