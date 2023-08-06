"use strict";
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
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CharticulatorWorker = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var core_1 = require("../core");
var communication_1 = require("./communication");
var worker_main_1 = require("./worker_main");
Object.defineProperty(exports, "CharticulatorWorkerProcess", { enumerable: true, get: function () { return worker_main_1.CharticulatorWorkerProcess; } });
/**
 * The representation of the background worker. This is used from the main process.
 */
var CharticulatorWorker = /** @class */ (function (_super) {
    __extends(CharticulatorWorker, _super);
    function CharticulatorWorker(workerLocation) {
        return _super.call(this, workerLocation) || this;
    }
    CharticulatorWorker.prototype.initialize = function (config) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.rpc("initialize", config)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    // eslint-disable-next-line
    CharticulatorWorker.prototype.solveChartConstraints = function (chart, chartState, dataset, preSolveValues, mappingOnly) {
        if (mappingOnly === void 0) { mappingOnly = false; }
        return __awaiter(this, void 0, void 0, function () {
            var result, shallowCopyAttributes, i, elementState, resultElementState, plotSegmentState, resultPlotSegmentState, _a, _b, _c, glyphState, resultGlyphState, _d, _e, _f, markState, resultMarkState, _g, _h, _j, element, resultElement;
            var e_1, _k, e_2, _l, e_3, _m;
            return __generator(this, function (_o) {
                switch (_o.label) {
                    case 0: return [4 /*yield*/, this.rpc("solveChartConstraints", chart, chartState, dataset, preSolveValues, mappingOnly)];
                    case 1:
                        result = _o.sent();
                        shallowCopyAttributes = function (dest, src) {
                            for (var key in src) {
                                if (Object.prototype.hasOwnProperty.call(src, key)) {
                                    dest[key] = src[key];
                                }
                            }
                        };
                        shallowCopyAttributes(chartState.attributes, result.attributes);
                        for (i = 0; i < chartState.elements.length; i++) {
                            elementState = chartState.elements[i];
                            resultElementState = result.elements[i];
                            shallowCopyAttributes(elementState.attributes, resultElementState.attributes);
                            // Is this a plot segment
                            if (core_1.Prototypes.isType(chart.elements[i].classID, "plot-segment")) {
                                plotSegmentState = elementState;
                                resultPlotSegmentState = (resultElementState);
                                try {
                                    for (_a = (e_1 = void 0, __values(core_1.zipArray(plotSegmentState.glyphs, resultPlotSegmentState.glyphs))), _b = _a.next(); !_b.done; _b = _a.next()) {
                                        _c = __read(_b.value, 2), glyphState = _c[0], resultGlyphState = _c[1];
                                        shallowCopyAttributes(glyphState.attributes, resultGlyphState.attributes);
                                        try {
                                            for (_d = (e_2 = void 0, __values(core_1.zipArray(glyphState.marks, resultGlyphState.marks))), _e = _d.next(); !_e.done; _e = _d.next()) {
                                                _f = __read(_e.value, 2), markState = _f[0], resultMarkState = _f[1];
                                                shallowCopyAttributes(markState.attributes, resultMarkState.attributes);
                                            }
                                        }
                                        catch (e_2_1) { e_2 = { error: e_2_1 }; }
                                        finally {
                                            try {
                                                if (_e && !_e.done && (_l = _d.return)) _l.call(_d);
                                            }
                                            finally { if (e_2) throw e_2.error; }
                                        }
                                    }
                                }
                                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                                finally {
                                    try {
                                        if (_b && !_b.done && (_k = _a.return)) _k.call(_a);
                                    }
                                    finally { if (e_1) throw e_1.error; }
                                }
                            }
                        }
                        try {
                            for (_g = __values(core_1.zipArray(chartState.scales, result.scales)), _h = _g.next(); !_h.done; _h = _g.next()) {
                                _j = __read(_h.value, 2), element = _j[0], resultElement = _j[1];
                                shallowCopyAttributes(element.attributes, resultElement.attributes);
                            }
                        }
                        catch (e_3_1) { e_3 = { error: e_3_1 }; }
                        finally {
                            try {
                                if (_h && !_h.done && (_m = _g.return)) _m.call(_g);
                            }
                            finally { if (e_3) throw e_3.error; }
                        }
                        return [2 /*return*/, chartState];
                }
            });
        });
    };
    return CharticulatorWorker;
}(communication_1.WorkerRPC));
exports.CharticulatorWorker = CharticulatorWorker;
//# sourceMappingURL=index.js.map