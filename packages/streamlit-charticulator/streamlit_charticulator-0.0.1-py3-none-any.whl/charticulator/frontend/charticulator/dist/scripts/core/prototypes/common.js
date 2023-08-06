"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable @typescript-eslint/no-namespace */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !exports.hasOwnProperty(p)) __createBinding(exports, m, p);
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
exports.strokeStyleToDashArray = exports.getProperty = exports.setProperty = exports.forEachMapping = exports.forEachObject = exports.ObjectItemKind = exports.findObjectById = exports.SnappingGuidesVisualTypes = exports.Handles = exports.Controls = void 0;
var common_1 = require("../common");
var Controls = require("./controls");
exports.Controls = Controls;
__exportStar(require("./chart_element"), exports);
__exportStar(require("./object"), exports);
var Handles;
(function (Handles) {
    var HandleActionType;
    (function (HandleActionType) {
        HandleActionType["Property"] = "property";
        HandleActionType["Attribute"] = "attribute";
        HandleActionType["AttributeValueMapping"] = "attribute-value-mapping";
    })(HandleActionType = Handles.HandleActionType || (Handles.HandleActionType = {}));
})(Handles = exports.Handles || (exports.Handles = {}));
var SnappingGuidesVisualTypes;
(function (SnappingGuidesVisualTypes) {
    SnappingGuidesVisualTypes[SnappingGuidesVisualTypes["Guide"] = 0] = "Guide";
    SnappingGuidesVisualTypes[SnappingGuidesVisualTypes["Coordinator"] = 1] = "Coordinator";
    SnappingGuidesVisualTypes[SnappingGuidesVisualTypes["Point"] = 2] = "Point";
})(SnappingGuidesVisualTypes = exports.SnappingGuidesVisualTypes || (exports.SnappingGuidesVisualTypes = {}));
function findObjectById(spec, id) {
    var e_1, _a;
    if (spec._id == id) {
        return spec;
    }
    var obj = common_1.getById(spec.scales, id) ||
        common_1.getById(spec.elements, id) ||
        common_1.getById(spec.glyphs, id);
    if (obj != null) {
        return obj;
    }
    try {
        for (var _b = __values(spec.glyphs), _c = _b.next(); !_c.done; _c = _b.next()) {
            var glyph = _c.value;
            obj = common_1.getById(glyph.marks, id);
            if (obj != null) {
                return obj;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return null;
}
exports.findObjectById = findObjectById;
var ObjectItemKind;
(function (ObjectItemKind) {
    ObjectItemKind["Chart"] = "chart";
    ObjectItemKind["ChartElement"] = "chart-element";
    ObjectItemKind["Glyph"] = "glyph";
    ObjectItemKind["Mark"] = "mark";
    ObjectItemKind["Scale"] = "scale";
})(ObjectItemKind = exports.ObjectItemKind || (exports.ObjectItemKind = {}));
function forEachObject(chart) {
    var _a, _b, chartElement, e_2_1, _c, _d, glyph, _e, _f, mark, e_3_1, e_4_1, _g, _h, scale, e_5_1;
    var e_2, _j, e_4, _k, e_3, _l, e_5, _m;
    return __generator(this, function (_o) {
        switch (_o.label) {
            case 0: return [4 /*yield*/, { kind: ObjectItemKind.Chart, object: chart }];
            case 1:
                _o.sent();
                _o.label = 2;
            case 2:
                _o.trys.push([2, 7, 8, 9]);
                _a = __values(chart.elements), _b = _a.next();
                _o.label = 3;
            case 3:
                if (!!_b.done) return [3 /*break*/, 6];
                chartElement = _b.value;
                return [4 /*yield*/, {
                        kind: ObjectItemKind.ChartElement,
                        object: chartElement,
                        chartElement: chartElement,
                    }];
            case 4:
                _o.sent();
                _o.label = 5;
            case 5:
                _b = _a.next();
                return [3 /*break*/, 3];
            case 6: return [3 /*break*/, 9];
            case 7:
                e_2_1 = _o.sent();
                e_2 = { error: e_2_1 };
                return [3 /*break*/, 9];
            case 8:
                try {
                    if (_b && !_b.done && (_j = _a.return)) _j.call(_a);
                }
                finally { if (e_2) throw e_2.error; }
                return [7 /*endfinally*/];
            case 9:
                _o.trys.push([9, 21, 22, 23]);
                _c = __values(chart.glyphs), _d = _c.next();
                _o.label = 10;
            case 10:
                if (!!_d.done) return [3 /*break*/, 20];
                glyph = _d.value;
                return [4 /*yield*/, { kind: ObjectItemKind.Glyph, object: glyph, glyph: glyph }];
            case 11:
                _o.sent();
                _o.label = 12;
            case 12:
                _o.trys.push([12, 17, 18, 19]);
                _e = (e_3 = void 0, __values(glyph.marks)), _f = _e.next();
                _o.label = 13;
            case 13:
                if (!!_f.done) return [3 /*break*/, 16];
                mark = _f.value;
                return [4 /*yield*/, { kind: ObjectItemKind.Mark, object: mark, glyph: glyph, mark: mark }];
            case 14:
                _o.sent();
                _o.label = 15;
            case 15:
                _f = _e.next();
                return [3 /*break*/, 13];
            case 16: return [3 /*break*/, 19];
            case 17:
                e_3_1 = _o.sent();
                e_3 = { error: e_3_1 };
                return [3 /*break*/, 19];
            case 18:
                try {
                    if (_f && !_f.done && (_l = _e.return)) _l.call(_e);
                }
                finally { if (e_3) throw e_3.error; }
                return [7 /*endfinally*/];
            case 19:
                _d = _c.next();
                return [3 /*break*/, 10];
            case 20: return [3 /*break*/, 23];
            case 21:
                e_4_1 = _o.sent();
                e_4 = { error: e_4_1 };
                return [3 /*break*/, 23];
            case 22:
                try {
                    if (_d && !_d.done && (_k = _c.return)) _k.call(_c);
                }
                finally { if (e_4) throw e_4.error; }
                return [7 /*endfinally*/];
            case 23:
                _o.trys.push([23, 28, 29, 30]);
                _g = __values(chart.scales), _h = _g.next();
                _o.label = 24;
            case 24:
                if (!!_h.done) return [3 /*break*/, 27];
                scale = _h.value;
                return [4 /*yield*/, { kind: ObjectItemKind.Scale, object: scale, scale: scale }];
            case 25:
                _o.sent();
                _o.label = 26;
            case 26:
                _h = _g.next();
                return [3 /*break*/, 24];
            case 27: return [3 /*break*/, 30];
            case 28:
                e_5_1 = _o.sent();
                e_5 = { error: e_5_1 };
                return [3 /*break*/, 30];
            case 29:
                try {
                    if (_h && !_h.done && (_m = _g.return)) _m.call(_g);
                }
                finally { if (e_5) throw e_5.error; }
                return [7 /*endfinally*/];
            case 30: return [2 /*return*/];
        }
    });
}
exports.forEachObject = forEachObject;
function forEachMapping(mappings) {
    var _a, _b, key, e_6_1;
    var e_6, _c;
    return __generator(this, function (_d) {
        switch (_d.label) {
            case 0:
                _d.trys.push([0, 5, 6, 7]);
                _a = __values(Object.keys(mappings)), _b = _a.next();
                _d.label = 1;
            case 1:
                if (!!_b.done) return [3 /*break*/, 4];
                key = _b.value;
                return [4 /*yield*/, [key, mappings[key]]];
            case 2:
                _d.sent();
                _d.label = 3;
            case 3:
                _b = _a.next();
                return [3 /*break*/, 1];
            case 4: return [3 /*break*/, 7];
            case 5:
                e_6_1 = _d.sent();
                e_6 = { error: e_6_1 };
                return [3 /*break*/, 7];
            case 6:
                try {
                    if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
                }
                finally { if (e_6) throw e_6.error; }
                return [7 /*endfinally*/];
            case 7: return [2 /*return*/];
        }
    });
}
exports.forEachMapping = forEachMapping;
function setProperty(object, property, value) {
    if (typeof property == "string") {
        object.properties[property] = value;
    }
    else if (property.subfield) {
        common_1.setField(object.properties[property.property][property.field], property.subfield, value);
    }
    else {
        common_1.setField(object.properties[property.property], property.field, value);
    }
}
exports.setProperty = setProperty;
function getProperty(object, property) {
    if (typeof property == "string") {
        return object.properties[property];
    }
    else {
        if (property.subfield) {
            return common_1.getField(object.properties[property.property][property.field], property.subfield);
        }
        else {
            return common_1.getField(object.properties[property.property], property.field);
        }
    }
}
exports.getProperty = getProperty;
function strokeStyleToDashArray(strokeStyle) {
    switch (strokeStyle) {
        case "dashed": {
            return "8";
        }
        case "dotted": {
            return "1 10";
        }
        default: {
            return "";
        }
    }
}
exports.strokeStyleToDashArray = strokeStyleToDashArray;
//# sourceMappingURL=common.js.map