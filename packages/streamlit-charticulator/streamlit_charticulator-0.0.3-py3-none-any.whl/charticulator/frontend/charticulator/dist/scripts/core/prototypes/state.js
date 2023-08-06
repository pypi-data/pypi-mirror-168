"use strict";
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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
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
exports.ChartStateManager = exports.defaultDifferenceApproximation = void 0;
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../common");
var Expression = require("../expression");
var specification_1 = require("../specification");
var Prototypes = require("./index");
var index_1 = require("./index");
var cache_1 = require("./cache");
var dataflow_1 = require("./dataflow");
var filter_1 = require("./filter");
var object_1 = require("./object");
var solver_1 = require("../solver");
var utils_1 = require("../../app/utils");
var types_1 = require("../specification/types");
exports.defaultDifferenceApproximation = 0.01;
/** Handles the life cycle of states and the dataflow */
var ChartStateManager = /** @class */ (function () {
    function ChartStateManager(chart, dataset, state, defaultAttributes, options, chartOrigin) {
        if (state === void 0) { state = null; }
        if (defaultAttributes === void 0) { defaultAttributes = {}; }
        if (options === void 0) { options = {}; }
        this.classCache = new cache_1.ObjectClassCache();
        this.idIndex = new Map();
        this.onUpdateListeners = [];
        this.chart = chart;
        this.chartOrigin = chartOrigin ? chartOrigin : common_1.deepClone(chart);
        this.dataset = dataset;
        this.dataflow = new dataflow_1.DataflowManager(dataset);
        this.options = options;
        if (state == null) {
            this.initialize(defaultAttributes);
        }
        else {
            this.setState(state);
        }
    }
    ChartStateManager.prototype.getOriginChart = function () {
        return this.chartOrigin;
    };
    ChartStateManager.prototype.updateState = function (chart, dataset, state) {
        this.chart = chart;
        this.dataset = dataset;
        this.chartState = state;
        this.initialize({});
    };
    ChartStateManager.prototype.resetDifference = function () {
        this.chartOrigin = common_1.deepClone(this.chart);
    };
    ChartStateManager.prototype.onUpdate = function (callback) {
        this.onUpdateListeners.push(callback);
    };
    ChartStateManager.prototype.clearOnUpdateListener = function (callback) {
        var index = this.onUpdateListeners.findIndex(function (func) { return func === callback; });
        if (index != -1) {
            this.onUpdateListeners = __spread(this.onUpdateListeners.slice(0, index), this.onUpdateListeners.slice(index + 1, this.onUpdateListeners.length));
        }
    };
    // eslint-disable-next-line max-lines-per-function
    ChartStateManager.prototype.hasUnsavedChanges = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        var origin = this.chartOrigin;
        var chart = this.chart;
        var currentProperties = chart.properties;
        var originProperties = origin.properties;
        try {
            utils_1.expect_deep_approximately_equals(currentProperties, originProperties, exports.defaultDifferenceApproximation, true);
        }
        catch (_l) {
            return true;
        }
        if (origin.constraints.length !== chart.constraints.length) {
            return true;
        }
        else {
            for (var index = 0; index < origin.constraints.length; index++) {
                var originConstraints = origin.constraints[index];
                var current = chart.constraints[index];
                try {
                    utils_1.expect_deep_approximately_equals(originConstraints, current, exports.defaultDifferenceApproximation, true);
                }
                catch (ex) {
                    return true;
                }
            }
        }
        var chartElements = __spread(index_1.forEachObject(chart));
        var originElements = __spread(index_1.forEachObject(origin));
        // forEachObject retuns all objects in the chart
        // if any object was added or removed to the chart it means chart has changes
        // don't need to compare in details
        if (chartElements.length != originElements.length) {
            return true;
        }
        else {
            for (var index = 0; index < chartElements.length; index++) {
                var currentElement = chartElements[index];
                var originElement = originElements[index];
                if (currentElement.kind != originElement.kind) {
                    return true;
                }
                if (((_a = currentElement.glyph) === null || _a === void 0 ? void 0 : _a.classID) != ((_b = originElement.glyph) === null || _b === void 0 ? void 0 : _b.classID)) {
                    return true;
                }
                if (((_c = currentElement.object) === null || _c === void 0 ? void 0 : _c._id) != ((_d = originElement.object) === null || _d === void 0 ? void 0 : _d._id)) {
                    return true;
                }
                if (((_e = currentElement.scale) === null || _e === void 0 ? void 0 : _e._id) != ((_f = originElement.scale) === null || _f === void 0 ? void 0 : _f._id)) {
                    return true;
                }
                if (currentElement.kind == index_1.ObjectItemKind.ChartElement &&
                    currentElement.kind == index_1.ObjectItemKind.ChartElement) {
                    if (currentElement.chartElement && originElement.chartElement) {
                        if (currentElement.chartElement._id != originElement.chartElement._id) {
                            return true;
                        }
                        if (currentElement.chartElement.classID !=
                            originElement.chartElement.classID) {
                            return true;
                        }
                    }
                    if (Prototypes.isType(currentElement.chartElement.classID, "plot-segment") &&
                        Prototypes.isType(originElement.chartElement.classID, "plot-segment")) {
                        var currentPlotSegment = currentElement.chartElement;
                        var originPlotSegment = originElement.chartElement;
                        if (currentPlotSegment.glyph != originPlotSegment.glyph) {
                            return true;
                        }
                        if (currentPlotSegment.table != originPlotSegment.table) {
                            return true;
                        }
                        try {
                            utils_1.expect_deep_approximately_equals(currentPlotSegment.filter, originPlotSegment.filter, exports.defaultDifferenceApproximation, true);
                            utils_1.expect_deep_approximately_equals(currentPlotSegment.groupBy, originPlotSegment.groupBy, exports.defaultDifferenceApproximation, true);
                            utils_1.expect_deep_approximately_equals(currentPlotSegment.order, originPlotSegment.order, exports.defaultDifferenceApproximation, true);
                            utils_1.expect_deep_approximately_equals(currentPlotSegment.mappings, originPlotSegment.mappings, exports.defaultDifferenceApproximation, true);
                            utils_1.expect_deep_approximately_equals(currentPlotSegment.properties, originPlotSegment.properties, exports.defaultDifferenceApproximation, true);
                        }
                        catch (ex) {
                            return true;
                        }
                    }
                    try {
                        var currentProperties_1 = currentElement.chartElement.properties;
                        var originProperties_1 = originElement.chartElement.properties;
                        utils_1.expect_deep_approximately_equals(currentProperties_1, originProperties_1, exports.defaultDifferenceApproximation, true);
                    }
                    catch (ex) {
                        return true;
                    }
                }
                if (currentElement.kind == index_1.ObjectItemKind.Glyph &&
                    originElement.kind == index_1.ObjectItemKind.Glyph) {
                    if (currentElement.glyph.table != originElement.glyph.table) {
                        return true;
                    }
                }
                if (currentElement.kind == index_1.ObjectItemKind.Mark &&
                    originElement.kind == index_1.ObjectItemKind.Mark) {
                    if (((_g = currentElement.mark) === null || _g === void 0 ? void 0 : _g.classID) != ((_h = originElement.mark) === null || _h === void 0 ? void 0 : _h.classID)) {
                        return true;
                    }
                    try {
                        var currentProperties_2 = currentElement.mark.properties;
                        var originProperties_2 = originElement.mark.properties;
                        utils_1.expect_deep_approximately_equals(currentProperties_2, originProperties_2, exports.defaultDifferenceApproximation, true);
                    }
                    catch (ex) {
                        return true;
                    }
                }
                try {
                    var currentMappings = currentElement.object.mappings;
                    var originMappings = originElement.object.mappings;
                    utils_1.expect_deep_approximately_equals(currentMappings, originMappings, exports.defaultDifferenceApproximation, true);
                }
                catch (ex) {
                    return true;
                }
                //scale mappings
                try {
                    var currentProperties_3 = (_j = currentElement.object) === null || _j === void 0 ? void 0 : _j.properties;
                    var originProperties_3 = (_k = originElement.object) === null || _k === void 0 ? void 0 : _k.properties;
                    utils_1.expect_deep_approximately_equals(currentProperties_3, originProperties_3, exports.defaultDifferenceApproximation, true);
                }
                catch (ex) {
                    return true;
                }
            }
        }
        return false;
    };
    /** Set an existing state */
    ChartStateManager.prototype.setState = function (state) {
        this.chartState = state;
        this.rebuildID2Object();
        this.initializeCache();
    };
    /** Set a new dataset, this will reset the state */
    ChartStateManager.prototype.setDataset = function (dataset) {
        this.dataset = dataset;
        this.dataflow = new dataflow_1.DataflowManager(dataset);
        this.initialize({});
    };
    /** Get data table by name */
    ChartStateManager.prototype.getTable = function (name) {
        return this.dataflow.getTable(name);
    };
    /** Get an object by its unique ID */
    ChartStateManager.prototype.getObjectById = function (id) {
        return this.idIndex.get(id)[0];
    };
    /** Get a chart-level element or scale by its id */
    ChartStateManager.prototype.getClassById = function (id) {
        // eslint-disable-next-line
        var _a = __read(this.idIndex.get(id), 2), object = _a[0], state = _a[1];
        return this.classCache.getClass(state);
    };
    /** Get classes for chart elements */
    ChartStateManager.prototype.getElements = function () {
        var _this = this;
        return common_1.zipArray(this.chart.elements, this.chartState.elements).map(
        // eslint-disable-next-line
        function (_a) {
            var _b = __read(_a, 2), element = _b[0], elementState = _b[1];
            return _this.classCache.getClass(elementState);
        });
    };
    /** Create an empty chart state using chart and dataset */
    ChartStateManager.prototype.createChartState = function () {
        var _this = this;
        var chart = this.chart;
        // Build the state hierarchy
        var elementStates = chart.elements.map(function (element) {
            // Initialie the element state
            var elementState = {
                attributes: {},
            };
            // Special case for plot segment
            if (Prototypes.isType(element.classID, "plot-segment")) {
                _this.mapPlotSegmentState(element, elementState);
            }
            return elementState;
        });
        var scaleStates = chart.scales.map(function () {
            var state = {
                attributes: {},
            };
            return state;
        });
        return {
            elements: elementStates,
            scales: scaleStates,
            scaleMappings: chart.scaleMappings,
            attributes: {},
        };
    };
    /** Initialize the object class cache */
    ChartStateManager.prototype.initializeCache = function () {
        var e_1, _a, e_2, _b;
        this.classCache = new cache_1.ObjectClassCache();
        var chartClass = this.classCache.createChartClass(null, this.chart, this.chartState);
        chartClass.setDataflow(this.dataflow);
        chartClass.setManager(this);
        try {
            for (var _c = __values(common_1.zip(this.chart.scales, this.chartState.scales)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), scale = _e[0], scaleState = _e[1];
                this.classCache.createScaleClass(chartClass, scale, scaleState);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_1) throw e_1.error; }
        }
        try {
            for (var _f = __values(common_1.zip(this.chart.elements, this.chartState.elements)), _g = _f.next(); !_g.done; _g = _f.next()) {
                var _h = __read(_g.value, 2), element = _h[0], elementState = _h[1];
                this.classCache.createChartElementClass(chartClass, element, elementState);
                // For plot segment, handle data mapping
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    this.initializePlotSegmentCache(element, elementState);
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_2) throw e_2.error; }
        }
    };
    /** Enumerate all object classes */
    ChartStateManager.prototype.enumerateClasses = function (callback) {
        var e_3, _a, e_4, _b, e_5, _c, e_6, _d;
        var chartClass = this.classCache.getChartClass(this.chartState);
        callback(chartClass, this.chartState);
        try {
            // eslint-disable-next-line
            for (var _e = __values(common_1.zip(this.chart.scales, this.chartState.scales)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var _g = __read(_f.value, 2), scale = _g[0], scaleState = _g[1];
                var scaleClass = this.classCache.getClass(scaleState);
                callback(scaleClass, scaleState);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
            }
            finally { if (e_3) throw e_3.error; }
        }
        try {
            for (var _h = __values(common_1.zip(this.chart.elements, this.chartState.elements)), _j = _h.next(); !_j.done; _j = _h.next()) {
                var _k = __read(_j.value, 2), element = _k[0], elementState = _k[1];
                var elementClass = this.classCache.getClass(elementState);
                callback(elementClass, elementState);
                // For plot segment, handle data mapping
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    var plotSegmentState = elementState;
                    var glyph = (this.getObjectById(plotSegment.glyph));
                    try {
                        for (var _l = (e_5 = void 0, __values(plotSegmentState.glyphs)), _m = _l.next(); !_m.done; _m = _l.next()) {
                            var glyphState = _m.value;
                            var glyphClass = this.classCache.getClass(glyphState);
                            callback(glyphClass, glyphState);
                            try {
                                // eslint-disable-next-line
                                for (var _o = (e_6 = void 0, __values(common_1.zip(glyph.marks, glyphState.marks))), _p = _o.next(); !_p.done; _p = _o.next()) {
                                    var _q = __read(_p.value, 2), mark = _q[0], markState = _q[1];
                                    var markClass = this.classCache.getClass(markState);
                                    callback(markClass, markState);
                                }
                            }
                            catch (e_6_1) { e_6 = { error: e_6_1 }; }
                            finally {
                                try {
                                    if (_p && !_p.done && (_d = _o.return)) _d.call(_o);
                                }
                                finally { if (e_6) throw e_6.error; }
                            }
                        }
                    }
                    catch (e_5_1) { e_5 = { error: e_5_1 }; }
                    finally {
                        try {
                            if (_m && !_m.done && (_c = _l.return)) _c.call(_l);
                        }
                        finally { if (e_5) throw e_5.error; }
                    }
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
            }
            finally { if (e_4) throw e_4.error; }
        }
    };
    /** Enumerate classes, only return a specific type */
    ChartStateManager.prototype.enumerateClassesByType = function (type, callback) {
        this.enumerateClasses(function (cls, state) {
            if (Prototypes.isType(cls.object.classID, type)) {
                callback(cls, state);
            }
        });
    };
    ChartStateManager.prototype.enumeratePlotSegments = function (callback) {
        var e_7, _a;
        try {
            for (var _b = __values(common_1.zip(this.chart.elements, this.chartState.elements)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var _d = __read(_c.value, 2), element = _d[0], elementState = _d[1];
                var elementClass = this.classCache.getClass(elementState);
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    callback(elementClass);
                }
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_7) throw e_7.error; }
        }
    };
    /** Initialize the chart state with default parameters */
    ChartStateManager.prototype.initializeState = function (defaultAttributes) {
        if (defaultAttributes === void 0) { defaultAttributes = {}; }
        this.enumerateClasses(function (cls) {
            cls.initializeState();
            var attributesToAdd = defaultAttributes[cls.object._id];
            if (attributesToAdd) {
                cls.state.attributes = __assign(__assign({}, cls.state.attributes), attributesToAdd);
            }
        });
    };
    /** Recreate the chart state from scratch */
    ChartStateManager.prototype.initialize = function (defaultAttributes) {
        this.chartState = this.createChartState();
        this.rebuildID2Object();
        this.initializeCache();
        this.initializeState(defaultAttributes);
    };
    /** Rebuild id to object map */
    ChartStateManager.prototype.rebuildID2Object = function () {
        var e_8, _a, e_9, _b, e_10, _c, e_11, _d;
        this.idIndex.clear();
        try {
            // Chart elements
            for (var _e = __values(common_1.zipArray(this.chart.elements, this.chartState.elements)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var _g = __read(_f.value, 2), element = _g[0], elementState = _g[1];
                this.idIndex.set(element._id, [element, elementState]);
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
            }
            finally { if (e_8) throw e_8.error; }
        }
        try {
            // Scales
            for (var _h = __values(common_1.zipArray(this.chart.scales, this.chartState.scales)), _j = _h.next(); !_j.done; _j = _h.next()) {
                var _k = __read(_j.value, 2), scale = _k[0], scaleState = _k[1];
                this.idIndex.set(scale._id, [scale, scaleState]);
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
            }
            finally { if (e_9) throw e_9.error; }
        }
        try {
            // Glyphs
            for (var _l = __values(this.chart.glyphs), _m = _l.next(); !_m.done; _m = _l.next()) {
                var glyph = _m.value;
                this.idIndex.set(glyph._id, [glyph, null]);
                try {
                    for (var _o = (e_11 = void 0, __values(glyph.marks)), _p = _o.next(); !_p.done; _p = _o.next()) {
                        var element = _p.value;
                        this.idIndex.set(element._id, [element, null]);
                    }
                }
                catch (e_11_1) { e_11 = { error: e_11_1 }; }
                finally {
                    try {
                        if (_p && !_p.done && (_d = _o.return)) _d.call(_o);
                    }
                    finally { if (e_11) throw e_11.error; }
                }
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (_m && !_m.done && (_c = _l.return)) _c.call(_l);
            }
            finally { if (e_10) throw e_10.error; }
        }
    };
    /** Test if a name is already used */
    ChartStateManager.prototype.isNameUsed = function (candidate) {
        var e_12, _a, e_13, _b, e_14, _c, e_15, _d;
        var chart = this.chart;
        var names = new Set();
        try {
            for (var _e = __values(chart.scales), _f = _e.next(); !_f.done; _f = _e.next()) {
                var scale = _f.value;
                names.add(scale.properties.name);
            }
        }
        catch (e_12_1) { e_12 = { error: e_12_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
            }
            finally { if (e_12) throw e_12.error; }
        }
        try {
            for (var _g = __values(chart.elements), _h = _g.next(); !_h.done; _h = _g.next()) {
                var element = _h.value;
                names.add(element.properties.name);
            }
        }
        catch (e_13_1) { e_13 = { error: e_13_1 }; }
        finally {
            try {
                if (_h && !_h.done && (_b = _g.return)) _b.call(_g);
            }
            finally { if (e_13) throw e_13.error; }
        }
        try {
            for (var _j = __values(chart.glyphs), _k = _j.next(); !_k.done; _k = _j.next()) {
                var mark = _k.value;
                names.add(mark.properties.name);
                try {
                    for (var _l = (e_15 = void 0, __values(mark.marks)), _m = _l.next(); !_m.done; _m = _l.next()) {
                        var element = _m.value;
                        names.add(element.properties.name);
                    }
                }
                catch (e_15_1) { e_15 = { error: e_15_1 }; }
                finally {
                    try {
                        if (_m && !_m.done && (_d = _l.return)) _d.call(_l);
                    }
                    finally { if (e_15) throw e_15.error; }
                }
            }
        }
        catch (e_14_1) { e_14 = { error: e_14_1 }; }
        finally {
            try {
                if (_k && !_k.done && (_c = _j.return)) _c.call(_j);
            }
            finally { if (e_14) throw e_14.error; }
        }
        return names.has(candidate);
    };
    /** Find an unused name given a prefix, will try prefix1, prefix2, and so on. */
    ChartStateManager.prototype.findUnusedName = function (prefix) {
        for (var i = 1;; i++) {
            var candidate = prefix + i.toString();
            if (!this.isNameUsed(candidate)) {
                return candidate;
            }
        }
    };
    /** Create a new object */
    ChartStateManager.prototype.createObject = function (classID) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        var namePrefix = "Object";
        var metadata = object_1.ObjectClasses.GetMetadata(classID);
        if (metadata && metadata.displayName) {
            namePrefix = metadata.displayName;
        }
        var object = object_1.ObjectClasses.CreateDefault.apply(object_1.ObjectClasses, __spread([classID], args));
        var name = this.findUnusedName(namePrefix);
        object.properties.name = name;
        return object;
    };
    /** Add a new glyph */
    ChartStateManager.prototype.addGlyph = function (classID, table) {
        var newGlyph = {
            _id: common_1.uniqueID(),
            classID: classID,
            properties: { name: this.findUnusedName("Glyph") },
            table: table,
            marks: [
                {
                    _id: common_1.uniqueID(),
                    classID: "mark.anchor",
                    properties: { name: "Anchor" },
                    mappings: {
                        x: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "icx",
                        },
                        y: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "icy",
                        },
                    },
                },
            ],
            mappings: {},
            constraints: [],
        };
        this.idIndex.set(newGlyph._id, [newGlyph, null]);
        this.idIndex.set(newGlyph.marks[0]._id, [newGlyph.marks[0], null]);
        this.chart.glyphs.push(newGlyph);
        return newGlyph;
    };
    /** Remove a glyph */
    ChartStateManager.prototype.removeGlyph = function (glyph) {
        var e_16, _a, e_17, _b, e_18, _c;
        var idx = this.chart.glyphs.indexOf(glyph);
        if (idx < 0) {
            return;
        }
        this.idIndex.delete(glyph._id);
        try {
            for (var _d = __values(glyph.marks), _e = _d.next(); !_e.done; _e = _d.next()) {
                var element = _e.value;
                this.idIndex.delete(element._id);
            }
        }
        catch (e_16_1) { e_16 = { error: e_16_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
            }
            finally { if (e_16) throw e_16.error; }
        }
        this.chart.glyphs.splice(idx, 1);
        // Delete all plot segments using this glyph
        var elementsToDelete = [];
        try {
            for (var _f = __values(this.chart.elements), _g = _f.next(); !_g.done; _g = _f.next()) {
                var element = _g.value;
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    if (plotSegment.glyph == glyph._id) {
                        elementsToDelete.push(plotSegment);
                    }
                }
            }
        }
        catch (e_17_1) { e_17 = { error: e_17_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_17) throw e_17.error; }
        }
        try {
            for (var elementsToDelete_1 = __values(elementsToDelete), elementsToDelete_1_1 = elementsToDelete_1.next(); !elementsToDelete_1_1.done; elementsToDelete_1_1 = elementsToDelete_1.next()) {
                var plotSegment = elementsToDelete_1_1.value;
                this.removeChartElement(plotSegment);
            }
        }
        catch (e_18_1) { e_18 = { error: e_18_1 }; }
        finally {
            try {
                if (elementsToDelete_1_1 && !elementsToDelete_1_1.done && (_c = elementsToDelete_1.return)) _c.call(elementsToDelete_1);
            }
            finally { if (e_18) throw e_18.error; }
        }
    };
    /** Add a new element to a glyph */
    ChartStateManager.prototype.addMarkToGlyph = function (mark, glyph) {
        var _this = this;
        glyph.marks.push(mark);
        // Create element state in all plot segments using this glyph
        this.enumeratePlotSegments(function (plotSegmentClass) {
            var e_19, _a;
            if (plotSegmentClass.object.glyph == glyph._id) {
                try {
                    for (var _b = __values(plotSegmentClass.state.glyphs), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var glyphState = _c.value;
                        var glyphClass = _this.classCache.getGlyphClass(glyphState);
                        var markState = {
                            attributes: {},
                        };
                        glyphState.marks.push(markState);
                        var markClass = _this.classCache.createMarkClass(glyphClass, mark, markState);
                        markClass.initializeState();
                    }
                }
                catch (e_19_1) { e_19 = { error: e_19_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_19) throw e_19.error; }
                }
            }
        });
    };
    /** Remove an element from a glyph */
    ChartStateManager.prototype.removeMarkFromGlyph = function (mark, glyph) {
        var idx = glyph.marks.indexOf(mark);
        if (idx < 0) {
            return;
        }
        glyph.marks.splice(idx, 1);
        glyph.constraints = this.validateConstraints(glyph.constraints, glyph.marks);
        this.idIndex.delete(mark._id);
        // Remove the element state from all elements using this glyph
        this.enumeratePlotSegments(function (plotSegmentClass) {
            var e_20, _a;
            if (plotSegmentClass.object.glyph == glyph._id) {
                try {
                    for (var _b = __values(plotSegmentClass.state.glyphs), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var glyphState = _c.value;
                        glyphState.marks.splice(idx, 1);
                    }
                }
                catch (e_20_1) { e_20 = { error: e_20_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_20) throw e_20.error; }
                }
            }
        });
    };
    /** Add a chart element */
    ChartStateManager.prototype.addChartElement = function (element, index) {
        if (index === void 0) { index = null; }
        var elementState = {
            attributes: {},
        };
        if (Prototypes.isType(element.classID, "plot-segment")) {
            this.mapPlotSegmentState(element, elementState);
        }
        if (index != null && index >= 0 && index <= this.chart.elements.length) {
            this.chart.elements.splice(index, 0, element);
            this.chartState.elements.splice(index, 0, elementState);
        }
        else {
            this.chart.elements.push(element);
            this.chartState.elements.push(elementState);
        }
        var elementClass = this.classCache.createChartElementClass(this.classCache.getChartClass(this.chartState), element, elementState);
        if (Prototypes.isType(element.classID, "plot-segment")) {
            this.initializePlotSegmentCache(element, elementState);
        }
        elementClass.initializeState();
        if (Prototypes.isType(element.classID, "plot-segment")) {
            this.initializePlotSegmentState(elementClass);
        }
        this.idIndex.set(element._id, [element, elementState]);
    };
    ChartStateManager.prototype.reorderArray = function (array, fromIndex, toIndex) {
        var x = array.splice(fromIndex, 1)[0];
        if (fromIndex < toIndex) {
            array.splice(toIndex - 1, 0, x);
        }
        else {
            array.splice(toIndex, 0, x);
        }
    };
    ChartStateManager.prototype.reorderChartElement = function (fromIndex, toIndex) {
        if (toIndex == fromIndex || toIndex == fromIndex + 1) {
            return;
        } // no effect
        this.reorderArray(this.chart.elements, fromIndex, toIndex);
        this.reorderArray(this.chartState.elements, fromIndex, toIndex);
    };
    ChartStateManager.prototype.reorderGlyphElement = function (glyph, fromIndex, toIndex) {
        var e_21, _a, e_22, _b;
        if (toIndex == fromIndex || toIndex == fromIndex + 1) {
            return;
        } // no effect
        try {
            for (var _c = __values(common_1.zip(this.chart.elements, this.chartState.elements)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), element = _e[0], elementState = _e[1];
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    var plotSegmentState = elementState;
                    if (plotSegment.glyph == glyph._id) {
                        try {
                            for (var _f = (e_22 = void 0, __values(plotSegmentState.glyphs)), _g = _f.next(); !_g.done; _g = _f.next()) {
                                var glyphState = _g.value;
                                this.reorderArray(glyphState.marks, fromIndex, toIndex);
                            }
                        }
                        catch (e_22_1) { e_22 = { error: e_22_1 }; }
                        finally {
                            try {
                                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                            }
                            finally { if (e_22) throw e_22.error; }
                        }
                    }
                }
            }
        }
        catch (e_21_1) { e_21 = { error: e_21_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_21) throw e_21.error; }
        }
        this.reorderArray(glyph.marks, fromIndex, toIndex);
    };
    ChartStateManager.prototype.applyScrollingFilter = function (data, tableName) {
        var _a;
        var filteredIndices = [];
        // TODO fix expression (get column name from expression properly)
        var table = this.getTable(tableName);
        //in default we dont have expression, we should return all rows
        if (data.type === types_1.AxisDataBindingType.Default) {
            return table.rows.map(function (row, id) { return id; });
        }
        var parsed = (_a = Expression.parse(data === null || data === void 0 ? void 0 : data.expression)) === null || _a === void 0 ? void 0 : _a.args[0];
        if (data.type === types_1.AxisDataBindingType.Categorical) {
            var _loop_1 = function (i) {
                var rowContext = table.getRowContext(i);
                if (data.categories.find(function (category) { return category === parsed.getStringValue(rowContext); }) !== undefined ||
                    !data.allCategories) {
                    filteredIndices.push(i);
                }
            };
            for (var i = 0; i < table.rows.length; i++) {
                _loop_1(i);
            }
        }
        else if (data.type === types_1.AxisDataBindingType.Numerical) {
            for (var i = 0; i < table.rows.length; i++) {
                var rowContext = table.getRowContext(i);
                var value = parsed.getValue(rowContext);
                if (data.domainMin < data.domainMax) {
                    if (value >= data.domainMin && value <= data.domainMax) {
                        filteredIndices.push(i);
                    }
                }
                else {
                    if (value >= data.domainMax && value <= data.domainMin) {
                        filteredIndices.push(i);
                    }
                }
            }
        }
        return filteredIndices;
    };
    /**
     * Map/remap plot segment glyphs
     * @param plotSegment
     * @param plotSegmentState
     */
    ChartStateManager.prototype.mapPlotSegmentState = function (plotSegment, plotSegmentState) {
        var e_23, _a, e_24, _b;
        var glyphObject = (common_1.getById(this.chart.glyphs, plotSegment.glyph));
        var table = this.getTable(glyphObject.table);
        var index2ExistingGlyphState = new Map();
        if (plotSegmentState.dataRowIndices) {
            try {
                for (var _c = __values(common_1.zip(plotSegmentState.dataRowIndices, plotSegmentState.glyphs)), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var _e = __read(_d.value, 2), rowIndex = _e[0], glyphState = _e[1];
                    index2ExistingGlyphState.set(rowIndex.join(","), glyphState);
                }
            }
            catch (e_23_1) { e_23 = { error: e_23_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                }
                finally { if (e_23) throw e_23.error; }
            }
        }
        var filteredIndices = table.rows.map(function (r, i) { return i; });
        // scrolling filters
        if (plotSegment.properties.xData && plotSegment.properties.yData) {
            var dataX = plotSegment.properties.xData;
            var filteredIndicesX = this.applyScrollingFilter(dataX, plotSegment.table);
            var dataY = plotSegment.properties.yData;
            var filteredIndicesY_1 = this.applyScrollingFilter(dataY, plotSegment.table);
            filteredIndices = filteredIndicesX.filter(function (value) {
                return filteredIndicesY_1.includes(value);
            });
        }
        else {
            if (plotSegment.properties.xData) {
                var data = plotSegment.properties.xData;
                filteredIndices = this.applyScrollingFilter(data, plotSegment.table);
            }
            if (plotSegment.properties.yData) {
                var data = plotSegment.properties.yData;
                filteredIndices = this.applyScrollingFilter(data, plotSegment.table);
            }
        }
        if (plotSegment.properties.axis) {
            var data = plotSegment.properties.axis;
            filteredIndices = this.applyScrollingFilter(data, plotSegment.table);
        }
        plotSegmentState.dataRowIndices = filteredIndices.map(function (i) { return [i]; });
        if (plotSegment.filter) {
            try {
                var filter_2 = new filter_1.CompiledFilter(plotSegment.filter, this.dataflow.cache);
                filteredIndices = filteredIndices.filter(function (i) {
                    return filter_2.filter(table.getRowContext(i));
                });
            }
            catch (e) {
                //Plot segment empty filter expression
            }
        }
        if (plotSegment.groupBy) {
            if (plotSegment.groupBy.expression) {
                var expr = this.dataflow.cache.parse(plotSegment.groupBy.expression);
                var groups = new Map();
                plotSegmentState.dataRowIndices = [];
                try {
                    for (var filteredIndices_1 = __values(filteredIndices), filteredIndices_1_1 = filteredIndices_1.next(); !filteredIndices_1_1.done; filteredIndices_1_1 = filteredIndices_1.next()) {
                        var i = filteredIndices_1_1.value;
                        var groupBy = expr.getStringValue(table.getRowContext(i));
                        if (groups.has(groupBy)) {
                            groups.get(groupBy).push(i);
                        }
                        else {
                            var g = [i];
                            groups.set(groupBy, g);
                            plotSegmentState.dataRowIndices.push(g);
                        }
                    }
                }
                catch (e_24_1) { e_24 = { error: e_24_1 }; }
                finally {
                    try {
                        if (filteredIndices_1_1 && !filteredIndices_1_1.done && (_b = filteredIndices_1.return)) _b.call(filteredIndices_1);
                    }
                    finally { if (e_24) throw e_24.error; }
                }
            }
            else {
                // TODO: emit error
            }
        }
        else {
            plotSegmentState.dataRowIndices = filteredIndices.map(function (i) { return [i]; });
        }
        // Resolve filter
        plotSegmentState.glyphs = plotSegmentState.dataRowIndices.map(function (rowIndex) {
            if (index2ExistingGlyphState.has(rowIndex.join(","))) {
                return index2ExistingGlyphState.get(rowIndex.join(","));
            }
            else {
                var glyphState = {
                    marks: glyphObject.marks.map(function () {
                        var elementState = {
                            attributes: {},
                        };
                        return elementState;
                    }),
                    attributes: {},
                };
                return glyphState;
            }
        });
    };
    ChartStateManager.prototype.initializePlotSegmentCache = function (element, elementState) {
        var e_25, _a, e_26, _b;
        var plotSegment = element;
        var plotSegmentState = elementState;
        var plotSegmentClass = this.classCache.getPlotSegmentClass(plotSegmentState);
        var glyph = this.getObjectById(plotSegment.glyph);
        try {
            for (var _c = __values(plotSegmentState.glyphs), _d = _c.next(); !_d.done; _d = _c.next()) {
                var glyphState = _d.value;
                if (this.classCache.hasClass(glyphState)) {
                    continue;
                }
                var glyphClass = this.classCache.createGlyphClass(plotSegmentClass, glyph, glyphState);
                try {
                    for (var _e = (e_26 = void 0, __values(common_1.zip(glyph.marks, glyphState.marks))), _f = _e.next(); !_f.done; _f = _e.next()) {
                        var _g = __read(_f.value, 2), mark = _g[0], markState = _g[1];
                        this.classCache.createMarkClass(glyphClass, mark, markState);
                    }
                }
                catch (e_26_1) { e_26 = { error: e_26_1 }; }
                finally {
                    try {
                        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                    }
                    finally { if (e_26) throw e_26.error; }
                }
            }
        }
        catch (e_25_1) { e_25 = { error: e_25_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_25) throw e_25.error; }
        }
    };
    ChartStateManager.prototype.initializePlotSegmentState = function (plotSegmentClass) {
        var e_27, _a, e_28, _b;
        var glyph = (this.getObjectById(plotSegmentClass.object.glyph));
        try {
            for (var _c = __values(plotSegmentClass.state.glyphs), _d = _c.next(); !_d.done; _d = _c.next()) {
                var glyphState = _d.value;
                var glyphClass = this.classCache.getGlyphClass(glyphState);
                glyphClass.initializeState();
                try {
                    // eslint-disable-next-line
                    for (var _e = (e_28 = void 0, __values(common_1.zip(glyph.marks, glyphState.marks))), _f = _e.next(); !_f.done; _f = _e.next()) {
                        var _g = __read(_f.value, 2), mark = _g[0], markState = _g[1];
                        var markClass = this.classCache.getMarkClass(markState);
                        markClass.initializeState();
                    }
                }
                catch (e_28_1) { e_28 = { error: e_28_1 }; }
                finally {
                    try {
                        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                    }
                    finally { if (e_28) throw e_28.error; }
                }
            }
        }
        catch (e_27_1) { e_27 = { error: e_27_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_27) throw e_27.error; }
        }
    };
    ChartStateManager.prototype.triggerUpdateListeners = function () {
        var _this = this;
        this.onUpdateListeners.forEach(function (listener) { return listener(_this.chart); });
    };
    /** Remove a chart element */
    ChartStateManager.prototype.removeChartElement = function (element) {
        var idx = this.chart.elements.indexOf(element);
        if (idx < 0) {
            return;
        }
        this.chart.elements.splice(idx, 1);
        this.chartState.elements.splice(idx, 1);
        this.idIndex.delete(element._id);
        this.chart.constraints = this.validateConstraints(this.chart.constraints, this.chart.elements);
    };
    ChartStateManager.prototype.remapPlotSegmentGlyphs = function (plotSegment) {
        var idx = this.chart.elements.indexOf(plotSegment);
        if (idx < 0) {
            return;
        }
        var plotSegmentState = (this.chartState.elements[idx]);
        this.mapPlotSegmentState(plotSegment, plotSegmentState);
        this.initializePlotSegmentCache(plotSegment, plotSegmentState);
        this.solveConstraints();
        this.triggerUpdateListeners();
    };
    /** Add a new scale */
    ChartStateManager.prototype.addScale = function (scale) {
        var scaleState = {
            attributes: {},
        };
        this.chart.scales.push(scale);
        this.chartState.scales.push(scaleState);
        var scaleClass = this.classCache.createScaleClass(this.classCache.getChartClass(this.chartState), scale, scaleState);
        scaleClass.initializeState();
        this.idIndex.set(scale._id, [scale, scaleState]);
    };
    /** Remove a scale */
    ChartStateManager.prototype.removeScale = function (scale) {
        var idx = this.chart.scales.indexOf(scale);
        if (idx < 0) {
            return;
        }
        this.chart.scales.splice(idx, 1);
        this.chartState.scales.splice(idx, 1);
        this.idIndex.delete(scale._id);
    };
    ChartStateManager.prototype.getMarkClass = function (state) {
        return this.classCache.getMarkClass(state);
    };
    ChartStateManager.prototype.getGlyphClass = function (state) {
        return this.classCache.getGlyphClass(state);
    };
    ChartStateManager.prototype.getChartElementClass = function (state) {
        return this.classCache.getChartElementClass(state);
    };
    ChartStateManager.prototype.getPlotSegmentClass = function (state) {
        return this.classCache.getPlotSegmentClass(state);
    };
    ChartStateManager.prototype.getScaleClass = function (state) {
        return this.classCache.getScaleClass(state);
    };
    ChartStateManager.prototype.getChartClass = function (state) {
        return this.classCache.getChartClass(state);
    };
    ChartStateManager.prototype.getClass = function (state) {
        return this.classCache.getClass(state);
    };
    ChartStateManager.prototype.findGlyphState = function (plotSegment, glyph, glyphIndex) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        if (glyphIndex == null) {
            glyphIndex = 0;
        }
        var plotSegmentClass = (this.getClassById(plotSegment._id));
        return plotSegmentClass.state.glyphs[glyphIndex];
    };
    ChartStateManager.prototype.findMarkState = function (plotSegment, glyph, mark, glyphIndex) {
        var _a;
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var markIndex = glyph.marks.indexOf(mark);
        return (_a = this.findGlyphState(plotSegment, glyph, glyphIndex)) === null || _a === void 0 ? void 0 : _a.marks[markIndex];
    };
    /** Remove constraints that relate to non-existant element */
    ChartStateManager.prototype.validateConstraints = function (constraints, elements) {
        var e_29, _a;
        var elementIDs = new Set();
        try {
            for (var elements_1 = __values(elements), elements_1_1 = elements_1.next(); !elements_1_1.done; elements_1_1 = elements_1.next()) {
                var e = elements_1_1.value;
                elementIDs.add(e._id);
            }
        }
        catch (e_29_1) { e_29 = { error: e_29_1 }; }
        finally {
            try {
                if (elements_1_1 && !elements_1_1.done && (_a = elements_1.return)) _a.call(elements_1);
            }
            finally { if (e_29) throw e_29.error; }
        }
        return constraints.filter(function (constraint) {
            switch (constraint.type) {
                case "snap": {
                    return (elementIDs.has(constraint.attributes.element) &&
                        elementIDs.has(constraint.attributes.targetElement));
                }
                default:
                    return true;
            }
        });
    };
    ChartStateManager.prototype.resolveResource = function (description) {
        var e_30, _a;
        var m = description.match(/^resource:([.*]+)$/);
        if (m && this.chart.resources) {
            var id = m[1];
            try {
                for (var _b = __values(this.chart.resources), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    if (item.id == id) {
                        return item.data;
                    }
                }
            }
            catch (e_30_1) { e_30 = { error: e_30_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_30) throw e_30.error; }
            }
        }
        else {
            return description;
        }
    };
    /** Get chart-level data context for a given table */
    ChartStateManager.prototype.getChartDataContext = function (tableName) {
        if (tableName == null) {
            return null;
        }
        var table = this.dataflow.getTable(tableName);
        return table.getGroupedContext(common_1.makeRange(0, table.rows.length));
    };
    /** Get glyph-level data context for the glyphIndex-th glyph */
    ChartStateManager.prototype.getGlpyhDataContext = function (plotSegment, glyphIndex) {
        var table = this.dataflow.getTable(plotSegment.table);
        var plotSegmentClass = (this.getClassById(plotSegment._id));
        var indices = plotSegmentClass.state.dataRowIndices[glyphIndex];
        return table.getGroupedContext(indices);
    };
    /** Get all glyph-level data contexts for a given plot segment */
    ChartStateManager.prototype.getGlpyhDataContexts = function (plotSegment, 
    // eslint-disable-next-line
    glyphIndex) {
        var table = this.dataflow.getTable(plotSegment.table);
        var plotSegmentClass = (this.getClassById(plotSegment._id));
        return plotSegmentClass.state.dataRowIndices.map(function (indices) {
            return table.getGroupedContext(indices);
        });
    };
    ChartStateManager.prototype.getGroupedExpressionVector = function (tableName, groupBy, expression) {
        var expr = this.dataflow.cache.parse(expression);
        var table = this.dataflow.getTable(tableName);
        if (!table) {
            return [];
        }
        var indices = [];
        for (var i = 0; i < table.rows.length; i++) {
            indices.push(i);
        }
        if (groupBy && groupBy.expression) {
            var groupExpression_1 = this.dataflow.cache.parse(groupBy.expression);
            var groups = common_1.gather(indices, function (i) {
                return groupExpression_1.getStringValue(table.getRowContext(i));
            });
            return groups.map(function (g) { return expr.getValue(table.getGroupedContext(g)); });
        }
        else {
            return indices.map(function (i) { return expr.getValue(table.getGroupedContext([i])); });
        }
    };
    ChartStateManager.prototype.solveConstraints = function (additional, mappingOnly) {
        var e_31, _a;
        if (additional === void 0) { additional = null; }
        if (mappingOnly === void 0) { mappingOnly = false; }
        if (mappingOnly) {
            var solver = new solver_1.ChartConstraintSolver("glyphs");
            solver.setup(this);
            solver.destroy();
        }
        else {
            var iterations = additional != null ? 2 : 1;
            var phases = ["chart", "glyphs"];
            for (var i = 0; i < iterations; i++) {
                try {
                    for (var phases_1 = (e_31 = void 0, __values(phases)), phases_1_1 = phases_1.next(); !phases_1_1.done; phases_1_1 = phases_1.next()) {
                        var phase = phases_1_1.value;
                        var solver = new solver_1.ChartConstraintSolver(phase);
                        solver.setup(this);
                        if (additional) {
                            additional(solver);
                        }
                        solver.solve();
                        solver.destroy();
                    }
                }
                catch (e_31_1) { e_31 = { error: e_31_1 }; }
                finally {
                    try {
                        if (phases_1_1 && !phases_1_1.done && (_a = phases_1.return)) _a.call(phases_1);
                    }
                    finally { if (e_31) throw e_31.error; }
                }
                additional = null;
            }
        }
    };
    return ChartStateManager;
}());
exports.ChartStateManager = ChartStateManager;
//# sourceMappingURL=state.js.map