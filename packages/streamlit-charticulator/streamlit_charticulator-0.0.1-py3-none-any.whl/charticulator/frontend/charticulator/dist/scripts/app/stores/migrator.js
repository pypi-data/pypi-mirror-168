"use strict";
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.Migrator = void 0;
var core_1 = require("../../core");
var dataset_1 = require("../../core/dataset");
var migrator_baseline_1 = require("./migrator_baseline");
var specification_1 = require("../../core/specification");
var prototypes_1 = require("../../core/prototypes");
var utils_1 = require("../utils");
var types_1 = require("../../core/specification/types");
var linear_1 = require("../../core/prototypes/scales/linear");
var utils_2 = require("../../core/prototypes/plot_segments/utils");
var types_2 = require("../../core/prototypes/legends/types");
var color_legend_1 = require("../../core/prototypes/legends/color_legend");
var axis_1 = require("../../core/prototypes/plot_segments/axis");
var links_1 = require("../../core/prototypes/links");
/** Upgrade old versions of chart spec and state to newer version */
var Migrator = /** @class */ (function () {
    function Migrator() {
    }
    // eslint-disable-next-line
    Migrator.prototype.migrate = function (state, targetVersion) {
        // First, fix version if missing
        if (!state.version) {
            // Initially we didn't have the version field, so fix it.
            state.version = "1.0.0";
        }
        // console.log(`Migrate state from ${state.version} to ${targetVersion}`);
        if (core_1.compareVersion(state.version, "1.3.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.3.0") >= 0) {
            // Major change at version 1.3.0: MainStoreState => AppStoreState
            var stateOld = state;
            state = {
                version: stateOld.version,
                dataset: stateOld.dataset.dataset,
                chart: stateOld.chart.chart,
                chartState: stateOld.chart.chartState,
            };
        }
        if (core_1.compareVersion(state.version, "1.1.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.1.0") >= 0) {
            // Major change in spec from 1.1.0: the dataRowIndices are changed from number[] to number[][]
            state = this.fixDataRowIndices(state);
            state = this.fixDataMappingExpressions(state);
        }
        if (core_1.compareVersion(state.version, "1.4.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.4.0") >= 0) {
            // Major change at version 1.4.0: Links are not automatically sorted in rendering now
            state = this.fixLinkOrder_v130(state);
        }
        if (core_1.compareVersion(state.version, "1.5.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.5.0") >= 0) {
            // Minor change at version 1.5.0: Links are not automatically sorted in rendering now
            state = this.addScaleMappings(state);
        }
        if (core_1.compareVersion(state.version, "1.5.1") < 0 &&
            core_1.compareVersion(targetVersion, "1.5.1") >= 0) {
            // Minor change at version 1.5.1: Links are not automatically sorted in rendering now
            state = this.addTableTypes(state);
        }
        if (core_1.compareVersion(state.version, "1.6.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.6.0") >= 0) {
            // Minor change at version 1.6.0: Links are not automatically sorted in rendering now
            state = this.addOriginDataSet(state);
        }
        if (core_1.compareVersion(state.version, "1.7.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.7.0") >= 0) {
            // Minor change at version 1.7.0: Interactivity properties for marks
            state = this.addInteractivityProperties(state);
            // Minor change at version 1.7.0: Guides now have a baseline prop
            state = migrator_baseline_1.upgradeGuidesToBaseline(state);
        }
        if (core_1.compareVersion(state.version, "1.8.0") < 0 &&
            core_1.compareVersion(targetVersion, "1.8.0") >= 0) {
            // Minor change at version 1.8.0: Add default value for property layout in legend
            state = this.setValueToLayoutPropertyOfLegend(state);
        }
        if (core_1.compareVersion(state.version, "2.0.0") < 0 &&
            core_1.compareVersion(targetVersion, "2.0.0") >= 0) {
            // Major change at version 2.0.0: Add default value for property layout in legend
            state = this.setValueItemShapeOfLegend(state);
        }
        if (core_1.compareVersion(state.version, "2.0.1") < 0 &&
            core_1.compareVersion(targetVersion, "2.0.1") >= 0) {
            // Patch change at version 2.0.1: Add polar/angular legend
            state = this.setPolarAngularLegend(state);
        }
        if (core_1.compareVersion(state.version, "2.0.2") < 0 &&
            core_1.compareVersion(targetVersion, "2.0.2") >= 0) {
            state = this.setAllowFlipToMarks(state);
        }
        if (core_1.compareVersion(state.version, "2.0.4") < 0 &&
            core_1.compareVersion(targetVersion, "2.0.4") >= 0) {
            state = this.setMissedProperties(state);
        }
        if (core_1.compareVersion(state.version, "2.1.0") < 0 &&
            core_1.compareVersion(targetVersion, "2.1.0") >= 0) {
            state = this.setMissedGlyphRectProperties(state);
        }
        if (core_1.compareVersion(state.version, "2.1.1") < 0 &&
            core_1.compareVersion(targetVersion, "2.1.1") >= 0) {
            state = this.setMissedSortProperties(state);
        }
        if (core_1.compareVersion(state.version, "2.1.2") < 0 &&
            core_1.compareVersion(targetVersion, "2.1.2") >= 0) {
            state = this.setMissedSortProperties(state);
        }
        if (core_1.compareVersion(state.version, "2.1.5") < 0 &&
            core_1.compareVersion(targetVersion, "2.1.5") >= 0) {
            state = this.setMissedLegendProperties(state);
        }
        if (core_1.compareVersion(state.version, "2.1.6") < 0 &&
            core_1.compareVersion(targetVersion, "2.1.6") >= 0) {
            state = this.setMissedProperties_2_1_6(state);
        }
        // After migration, set version to targetVersion
        state.version = targetVersion;
        return state;
    };
    /**
     * Adds enableTooltips, enableSelection, enableContextMenu properties with default balue true
     * @param state current state
     */
    Migrator.prototype.addInteractivityProperties = function (state) {
        var e_1, _a, e_2, _b, e_3, _c;
        try {
            for (var _d = __values(state.chart.elements), _e = _d.next(); !_e.done; _e = _d.next()) {
                var mark = _e.value;
                mark.properties.enableTooltips = true;
                mark.properties.enableSelection = true;
                mark.properties.enableContextMenu = true;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
            }
            finally { if (e_1) throw e_1.error; }
        }
        try {
            for (var _f = __values(state.chart.glyphs), _g = _f.next(); !_g.done; _g = _f.next()) {
                var glyph = _g.value;
                try {
                    for (var _h = (e_3 = void 0, __values(glyph.marks)), _j = _h.next(); !_j.done; _j = _h.next()) {
                        var mark = _j.value;
                        mark.properties.enableTooltips = true;
                        mark.properties.enableSelection = true;
                        mark.properties.enableContextMenu = true;
                    }
                }
                catch (e_3_1) { e_3 = { error: e_3_1 }; }
                finally {
                    try {
                        if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
                    }
                    finally { if (e_3) throw e_3.error; }
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
        return state;
    };
    Migrator.prototype.addOriginDataSet = function (state) {
        state.originDataset = core_1.deepClone(state.dataset);
        return state;
    };
    Migrator.prototype.addScaleMappings = function (state) {
        state.chart.scaleMappings = [];
        return state;
    };
    Migrator.prototype.addTableTypes = function (state) {
        state.dataset.tables[0].type = dataset_1.TableType.Main;
        if (state.dataset.tables[1]) {
            state.dataset.tables[1].type = dataset_1.TableType.Links;
        }
        // TODO append current mappings
        return state;
    };
    Migrator.prototype.fixDataRowIndices = function (state) {
        var e_4, _a;
        try {
            // Convert all data row indices in plot segment states to
            for (var _b = __values(core_1.zip(state.chart.elements, state.chartState.elements)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var _d = __read(_c.value, 2), element = _d[0], elementState = _d[1];
                if (core_1.Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegmentState = elementState;
                    plotSegmentState.dataRowIndices = plotSegmentState.dataRowIndices.map(function (i) { return [i]; });
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_4) throw e_4.error; }
        }
        return state;
    };
    Migrator.prototype.addAggregationToExpression = function (expr, valueType) {
        if (valueType == "number") {
            return "avg(" + expr + ")";
        }
        else {
            return "first(" + expr + ")";
        }
    };
    Migrator.prototype.fixAxisDataMapping = function (mapping) {
        if (!mapping) {
            return;
        }
        mapping.expression = this.addAggregationToExpression(mapping.expression, mapping.valueType);
    };
    Migrator.prototype.fixDataMappingExpressions = function (state) {
        var e_5, _a, e_6, _b, e_7, _c, e_8, _d, e_9, _e;
        var _this = this;
        try {
            for (var _f = __values(core_1.zip(state.chart.elements, state.chartState.elements)), _g = _f.next(); !_g.done; _g = _f.next()) {
                var _h = __read(_g.value, 1), element = _h[0];
                if (core_1.Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    this.fixAxisDataMapping(plotSegment.properties.xData);
                    this.fixAxisDataMapping(plotSegment.properties.yData);
                    if (plotSegment.properties.sublayout) {
                        var sublayout = plotSegment.properties.sublayout;
                        if (sublayout.order) {
                            var parsed = core_1.Expression.parse(sublayout.order);
                            var expr = null;
                            // This is supposed to be in the form of sortBy((x) => x.Column);
                            if (parsed instanceof core_1.Expression.FunctionCall) {
                                if (parsed.name == "sortBy") {
                                    if (parsed.args[0] instanceof core_1.Expression.LambdaFunction) {
                                        var lambda = parsed.args[0];
                                        if (lambda.expr instanceof core_1.Expression.FieldAccess) {
                                            var field = lambda.expr;
                                            var column = field.fields[0];
                                            expr = core_1.Expression.functionCall("first", core_1.Expression.variable(column)).toString();
                                        }
                                    }
                                }
                            }
                            if (expr) {
                                sublayout.order = { expression: expr };
                            }
                        }
                    }
                    if (plotSegment.filter) {
                        if (plotSegment.filter.categories.column) {
                            var column = plotSegment.filter.categories.column;
                            delete plotSegment.filter.categories.column;
                            plotSegment.filter.categories.expression = core_1.Expression.variable(column).toString();
                        }
                    }
                }
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_a = _f.return)) _a.call(_f);
            }
            finally { if (e_5) throw e_5.error; }
        }
        try {
            // Fix data mapping on glyphs/marks
            for (var _j = __values(state.chart.glyphs), _k = _j.next(); !_k.done; _k = _j.next()) {
                var glyph = _k.value;
                try {
                    for (var _l = (e_7 = void 0, __values(glyph.marks)), _m = _l.next(); !_m.done; _m = _l.next()) {
                        var mark = _m.value;
                        for (var key in mark.mappings) {
                            if (Object.prototype.hasOwnProperty.call(mark.mappings, key)) {
                                var mapping = mark.mappings[key];
                                if (mapping.type == specification_1.MappingType.scale) {
                                    var scaleMapping = mapping;
                                    scaleMapping.expression = this.addAggregationToExpression(scaleMapping.expression, scaleMapping.valueType);
                                }
                                if (mapping.type == specification_1.MappingType.scale ||
                                    mapping.type == specification_1.MappingType.text) {
                                    mapping.table = glyph.table;
                                }
                            }
                        }
                    }
                }
                catch (e_7_1) { e_7 = { error: e_7_1 }; }
                finally {
                    try {
                        if (_m && !_m.done && (_c = _l.return)) _c.call(_l);
                    }
                    finally { if (e_7) throw e_7.error; }
                }
            }
        }
        catch (e_6_1) { e_6 = { error: e_6_1 }; }
        finally {
            try {
                if (_k && !_k.done && (_b = _j.return)) _b.call(_j);
            }
            finally { if (e_6) throw e_6.error; }
        }
        try {
            // Fix axis data mappings for data-axes
            for (var _o = __values(state.chart.glyphs), _p = _o.next(); !_p.done; _p = _o.next()) {
                var glyph = _p.value;
                var _loop_1 = function (mark) {
                    if (core_1.Prototypes.isType(mark.classID, "mark.data-axis")) {
                        var properties = mark.properties;
                        var valueType_1 = properties.axis.valueType;
                        properties.axis.expression = this_1.addAggregationToExpression(properties.axis.expression, valueType_1);
                        if (properties.dataExpressions) {
                            properties.dataExpressions = properties.dataExpressions.map(function (x, index) { return ({
                                name: index.toString(),
                                expression: _this.addAggregationToExpression(x, valueType_1),
                            }); });
                        }
                    }
                };
                var this_1 = this;
                try {
                    for (var _q = (e_9 = void 0, __values(glyph.marks)), _r = _q.next(); !_r.done; _r = _q.next()) {
                        var mark = _r.value;
                        _loop_1(mark);
                    }
                }
                catch (e_9_1) { e_9 = { error: e_9_1 }; }
                finally {
                    try {
                        if (_r && !_r.done && (_e = _q.return)) _e.call(_q);
                    }
                    finally { if (e_9) throw e_9.error; }
                }
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_p && !_p.done && (_d = _o.return)) _d.call(_o);
            }
            finally { if (e_8) throw e_8.error; }
        }
        return state;
    };
    Migrator.prototype.fixLinkOrder_v130 = function (state) {
        var linkIndices = [];
        var otherIndices = [];
        for (var i = 0; i < state.chart.elements.length; i++) {
            if (core_1.Prototypes.isType(state.chart.elements[i].classID, "links")) {
                linkIndices.push(i);
            }
            else {
                otherIndices.push(i);
            }
        }
        var allIndices = linkIndices.concat(otherIndices);
        state.chart.elements = allIndices.map(function (i) { return state.chart.elements[i]; });
        state.chartState.elements = allIndices.map(function (i) { return state.chartState.elements[i]; });
        return state;
    };
    Migrator.prototype.setValueToLayoutPropertyOfLegend = function (state) {
        var e_10, _a;
        try {
            for (var _b = __values(state.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (core_1.Prototypes.isType(element.classID, "legend.categorical") ||
                    core_1.Prototypes.isType(element.classID, "legend.custom")) {
                    var legend = element;
                    if (legend.properties.orientation === undefined) {
                        legend.properties.orientation = "vertical";
                    }
                }
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_10) throw e_10.error; }
        }
        return state;
    };
    Migrator.prototype.setValueItemShapeOfLegend = function (state) {
        var e_11, _a;
        try {
            for (var _b = __values(state.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (core_1.Prototypes.isType(element.classID, "legend")) {
                    var legend = element;
                    if (legend.properties.markerShape === undefined) {
                        legend.properties.markerShape = "circle";
                    }
                }
            }
        }
        catch (e_11_1) { e_11 = { error: e_11_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_11) throw e_11.error; }
        }
        return state;
    };
    Migrator.prototype.setPolarAngularLegend = function (state) {
        for (var i = 0; i < state.chart.elements.length; i++) {
            var element = state.chart.elements[i];
            if (core_1.Prototypes.isType(element.classID, "legend")) {
                var attrs = state.chartState.elements[i]
                    .attributes;
                // add new properties
                attrs.cx = 0;
                attrs.cy = 0;
                attrs.radius = 0;
                attrs.startAngle = 0;
                attrs.endAngle = 0;
            }
        }
        return state;
    };
    Migrator.prototype.updateAxis = function (axis) {
        return __assign(__assign({}, axis), { side: utils_1.replaceUndefinedByNull(axis.side), type: utils_1.replaceUndefinedByNull(axis.type), visible: utils_1.replaceUndefinedByNull(axis.visible), autoDomainMax: utils_1.replaceUndefinedByNull(axis.autoDomainMax), autoDomainMin: utils_1.replaceUndefinedByNull(axis.autoDomainMin), orderMode: utils_1.replaceUndefinedByNull(axis.orderMode), style: utils_1.replaceUndefinedByNull(axis.style), categories: utils_1.replaceUndefinedByNull(axis.categories), dataKind: utils_1.replaceUndefinedByNull(axis.dataKind), domainMax: utils_1.replaceUndefinedByNull(axis.domainMax), domainMin: utils_1.replaceUndefinedByNull(axis.domainMin), enablePrePostGap: utils_1.replaceUndefinedByNull(axis.enablePrePostGap), expression: utils_1.replaceUndefinedByNull(axis.expression), gapRatio: utils_1.replaceUndefinedByNull(axis.gapRatio), numericalMode: utils_1.replaceUndefinedByNull(axis.numericalMode), order: utils_1.replaceUndefinedByNull(axis.order), rawExpression: utils_1.replaceUndefinedByNull(axis.rawExpression), tickDataExpression: utils_1.replaceUndefinedByNull(axis.tickDataExpression), tickFormat: utils_1.replaceUndefinedByNull(axis.tickFormat), valueType: utils_1.replaceUndefinedByNull(axis.valueType), allowScrolling: utils_1.replaceUndefinedByNull(axis.allowScrolling), windowSize: utils_1.replaceUndefinedByNull(axis.windowSize), barOffset: utils_1.replaceUndefinedByNull(axis.barOffset), offset: utils_1.replaceUndefinedByNull(axis.offset), tickFormatType: utils_1.replaceUndefinedByNull(axis.tickFormatType), numberOfTicks: utils_1.replaceUndefinedByNull(axis.numberOfTicks), autoNumberOfTicks: utils_1.replaceUndefinedByNull(axis.autoNumberOfTicks) });
    };
    Migrator.prototype.setMissedProperties = function (state) {
        var e_12, _a;
        try {
            for (var _b = __values(prototypes_1.forEachObject(state.chart)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (item.kind == prototypes_1.ObjectItemKind.Chart) {
                    item.object.properties.exposed = true;
                }
                if (item.kind == prototypes_1.ObjectItemKind.ChartElement) {
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.cartesian")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if (element.properties.xData === undefined) {
                                element.properties.xData = null;
                            }
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if (element.properties.yData === undefined) {
                                element.properties.yData = null;
                            }
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.polar")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.line")) {
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.curve")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
                if (item.kind == prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.mark;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
            }
        }
        catch (e_12_1) { e_12 = { error: e_12_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_12) throw e_12.error; }
        }
        return state;
    };
    Migrator.prototype.setAllowFlipToMarks = function (state) {
        var e_13, _a;
        try {
            for (var _b = __values(prototypes_1.forEachObject(state.chart)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (item.kind == "mark") {
                    // legend with column names
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.rect")) {
                        item.mark.properties.allowFlipping = true;
                    }
                }
            }
        }
        catch (e_13_1) { e_13 = { error: e_13_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_13) throw e_13.error; }
        }
        return state;
    };
    Migrator.prototype.setMissedGlyphRectProperties = function (state) {
        var e_14, _a;
        var _b, _c, _d, _e, _f, _g;
        try {
            for (var _h = __values(prototypes_1.forEachObject(state.chart)), _j = _h.next(); !_j.done; _j = _h.next()) {
                var item = _j.value;
                if (item.kind == prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.rect")) {
                        if (item.mark.properties.rx === undefined) {
                            item.mark.properties.rx = 0;
                        }
                        if (item.mark.properties.ry === undefined) {
                            item.mark.properties.ry = 0;
                        }
                    }
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.symbol")) {
                        item.mark.properties.rotation = 0;
                    }
                }
                if (item.kind == prototypes_1.ObjectItemKind.ChartElement) {
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.cartesian")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if (element.properties.xData === undefined) {
                                element.properties.xData = null;
                            }
                            if (element.properties.xData.offset === undefined) {
                                element.properties.xData.offset = 0;
                            }
                            if (element.properties.xData.tickFormatType == undefined) {
                                element.properties.xData.tickFormatType = types_1.TickFormatType.None;
                            }
                            if ((_b = element.properties.xData) === null || _b === void 0 ? void 0 : _b.style) {
                                element.properties.xData.style.showTicks = (_c = element.properties.xData.style.showTicks) !== null && _c !== void 0 ? _c : true;
                                element.properties.xData.style.showBaseline = (_d = element.properties.xData.style.showBaseline) !== null && _d !== void 0 ? _d : true;
                            }
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if (element.properties.yData === undefined) {
                                element.properties.yData = null;
                            }
                            if (element.properties.yData.offset === undefined) {
                                element.properties.yData.offset = 0;
                            }
                            if (element.properties.yData.tickFormatType === undefined) {
                                element.properties.yData.tickFormatType = types_1.TickFormatType.None;
                            }
                            if ((_e = element.properties.yData) === null || _e === void 0 ? void 0 : _e.style) {
                                element.properties.yData.style.showTicks = (_f = element.properties.yData.style.showTicks) !== null && _f !== void 0 ? _f : true;
                                element.properties.yData.style.showBaseline = (_g = element.properties.yData.style.showBaseline) !== null && _g !== void 0 ? _g : true;
                            }
                        }
                    }
                }
            }
        }
        catch (e_14_1) { e_14 = { error: e_14_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_a = _h.return)) _a.call(_h);
            }
            finally { if (e_14) throw e_14.error; }
        }
        //updated visibility number options
        var scales = state.chart.scales;
        if (scales) {
            for (var i = 0; i < scales.length; i++) {
                if (scales[i].classID == "scale.linear<number,boolean>") {
                    var scaleProperties = scales[i].properties;
                    if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) && (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) === "interval") {
                        scaleProperties.mode = linear_1.LinearBooleanScaleMode.Between;
                    }
                    if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) && (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) === "greater") {
                        if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) &&
                            (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) == "true") {
                            scaleProperties.mode =
                                linear_1.LinearBooleanScaleMode.GreaterThanOrEqualTo;
                        }
                        if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) &&
                            (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) == "false") {
                            scaleProperties.mode = linear_1.LinearBooleanScaleMode.GreaterThan;
                        }
                    }
                    if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) && (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.mode) === "less") {
                        if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) &&
                            (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) == "true") {
                            scaleProperties.mode = linear_1.LinearBooleanScaleMode.LessThanOrEqualTo;
                        }
                        if ((scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) &&
                            (scaleProperties === null || scaleProperties === void 0 ? void 0 : scaleProperties.inclusive) == "false") {
                            scaleProperties.mode = linear_1.LinearBooleanScaleMode.LessThan;
                        }
                    }
                }
            }
        }
        return state;
    };
    Migrator.prototype.parseExpression = function (axisExpression) {
        try {
            var expression = void 0;
            var parsed = core_1.Expression.parse(axisExpression);
            if (parsed instanceof core_1.Expression.FunctionCall) {
                expression = parsed.args[0].toString();
                expression = expression === null || expression === void 0 ? void 0 : expression.split("`").join("");
                //need to provide date.year() etc.
                expression = utils_2.parseDerivedColumnsExpression(expression);
            }
            return expression;
        }
        catch (e) {
            return axisExpression;
        }
    };
    Migrator.prototype.setMissedSortProperties = function (state) {
        var e_15, _a;
        var _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s, _t, _u, _v, _w, _x, _y, _z, _0, _1, _2;
        try {
            for (var _3 = __values(prototypes_1.forEachObject(state.chart)), _4 = _3.next(); !_4.done; _4 = _3.next()) {
                var item = _4.value;
                if (item.kind == prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.rect")) {
                        if (item.mark.properties.rx === undefined) {
                            item.mark.properties.rx = 0;
                        }
                        if (item.mark.properties.ry === undefined) {
                            item.mark.properties.ry = 0;
                        }
                    }
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.symbol")) {
                        item.mark.properties.rotation = 0;
                    }
                }
                if (item.kind == prototypes_1.ObjectItemKind.Chart) {
                    item.object.properties.exposed = true;
                }
                if (item.kind == prototypes_1.ObjectItemKind.ChartElement) {
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.cartesian")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if ((_b = element.properties.xData) === null || _b === void 0 ? void 0 : _b.style) {
                                element.properties.xData.style.showTicks = (_c = element.properties.xData.style.showTicks) !== null && _c !== void 0 ? _c : true;
                                element.properties.xData.style.showBaseline = (_d = element.properties.xData.style.showBaseline) !== null && _d !== void 0 ? _d : true;
                            }
                            if (element.properties.xData.offset === undefined) {
                                element.properties.xData.offset = 0;
                            }
                            element.properties.xData.barOffset = 0;
                            if (element.properties.xData.orderByCategories == undefined) {
                                element.properties.xData.orderByCategories =
                                    element.properties.xData.categories;
                            }
                            if (element.properties.xData.orderByExpression == undefined) {
                                element.properties.xData.orderByExpression = this.parseExpression(element.properties.xData.expression);
                            }
                            element.properties.xData.enableSelection = true;
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if ((_e = element.properties.yData) === null || _e === void 0 ? void 0 : _e.style) {
                                element.properties.yData.style.showTicks = (_f = element.properties.yData.style.showTicks) !== null && _f !== void 0 ? _f : true;
                                element.properties.yData.style.showBaseline = (_g = element.properties.yData.style.showBaseline) !== null && _g !== void 0 ? _g : true;
                            }
                            if (element.properties.yData.offset === undefined) {
                                element.properties.yData.offset = 0;
                            }
                            element.properties.yData.barOffset = 0;
                            if (element.properties.yData.orderByCategories == undefined) {
                                element.properties.yData.orderByCategories =
                                    element.properties.yData.categories;
                            }
                            if (element.properties.yData.orderByExpression == undefined) {
                                element.properties.yData.orderByExpression = this.parseExpression(element.properties.yData.expression);
                            }
                            element.properties.yData.enableSelection = true;
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.polar")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if ((_h = element.properties.xData) === null || _h === void 0 ? void 0 : _h.style) {
                                element.properties.xData.style.showTicks = (_j = element.properties.xData.style.showTicks) !== null && _j !== void 0 ? _j : true;
                                element.properties.xData.style.showBaseline = (_k = element.properties.xData.style.showBaseline) !== null && _k !== void 0 ? _k : true;
                            }
                            if (element.properties.xData.offset === undefined) {
                                element.properties.xData.offset = 0;
                            }
                            element.properties.xData.barOffset = 0;
                            if (element.properties.xData.orderByCategories == undefined) {
                                element.properties.xData.orderByCategories =
                                    element.properties.xData.categories;
                            }
                            if (element.properties.xData.orderByExpression == undefined) {
                                element.properties.xData.orderByExpression = this.parseExpression(element.properties.xData.expression);
                            }
                            element.properties.xData.enableSelection = true;
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if ((_l = element.properties.yData) === null || _l === void 0 ? void 0 : _l.style) {
                                element.properties.yData.style.showTicks = (_m = element.properties.yData.style.showTicks) !== null && _m !== void 0 ? _m : true;
                                element.properties.yData.style.showBaseline = (_o = element.properties.yData.style.showBaseline) !== null && _o !== void 0 ? _o : true;
                            }
                            if (element.properties.yData.orderByCategories == undefined) {
                                element.properties.yData.orderByCategories =
                                    element.properties.yData.categories;
                            }
                            if (element.properties.yData.orderByExpression == undefined) {
                                element.properties.yData.orderByExpression = this.parseExpression(element.properties.yData.expression);
                            }
                            if (element.properties.yData.offset === undefined) {
                                element.properties.yData.offset = 0;
                            }
                            element.properties.yData.barOffset = 0;
                            element.properties.yData.enableSelection = true;
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.line")) {
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                            if ((_p = element.properties.axis) === null || _p === void 0 ? void 0 : _p.style) {
                                element.properties.axis.style.showBaseline = (_q = element.properties.axis.style.showBaseline) !== null && _q !== void 0 ? _q : true;
                                element.properties.axis.style.showTicks = (_r = element.properties.axis.style.showTicks) !== null && _r !== void 0 ? _r : true;
                            }
                            if (element.properties.axis.orderByCategories == undefined) {
                                element.properties.axis.orderByCategories =
                                    element.properties.axis.categories;
                            }
                            if (element.properties.axis.orderByExpression == undefined) {
                                element.properties.axis.orderByExpression = this.parseExpression(element.properties.axis.expression);
                            }
                            element.properties.axis.enableSelection = true;
                            element.properties.axis.barOffset = 0;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.curve")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if ((_s = element.properties.xData) === null || _s === void 0 ? void 0 : _s.style) {
                                element.properties.xData.style.showTicks = (_t = element.properties.xData.style.showTicks) !== null && _t !== void 0 ? _t : true;
                                element.properties.xData.style.showBaseline = (_u = element.properties.xData.style.showBaseline) !== null && _u !== void 0 ? _u : true;
                            }
                            if (element.properties.xData.offset === undefined) {
                                element.properties.xData.offset = 0;
                            }
                            element.properties.xData.barOffset = 0;
                            if (element.properties.xData.orderByCategories == undefined) {
                                element.properties.xData.orderByCategories =
                                    element.properties.xData.categories;
                            }
                            if (element.properties.xData.orderByExpression == undefined) {
                                element.properties.xData.orderByExpression = this.parseExpression(element.properties.xData.expression);
                            }
                            element.properties.xData.enableSelection = true;
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if ((_v = element.properties.yData) === null || _v === void 0 ? void 0 : _v.style) {
                                element.properties.yData.style.showTicks = (_w = element.properties.yData.style.showTicks) !== null && _w !== void 0 ? _w : true;
                                element.properties.yData.style.showBaseline = (_x = element.properties.yData.style.showBaseline) !== null && _x !== void 0 ? _x : true;
                            }
                            if (element.properties.yData.orderByCategories == undefined) {
                                element.properties.yData.orderByCategories =
                                    element.properties.yData.categories;
                            }
                            if (element.properties.yData.orderByExpression == undefined) {
                                element.properties.yData.orderByExpression = this.parseExpression(element.properties.yData.expression);
                            }
                            if (element.properties.yData.offset === undefined) {
                                element.properties.yData.offset = 0;
                            }
                            element.properties.yData.barOffset = 0;
                            element.properties.yData.enableSelection = true;
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                            if (element.properties.axis.orderByCategories == undefined) {
                                element.properties.axis.orderByCategories =
                                    element.properties.axis.categories;
                            }
                            if (element.properties.axis.orderByExpression == undefined) {
                                element.properties.axis.orderByExpression = this.parseExpression(element.properties.axis.expression);
                            }
                            element.properties.axis.enableSelection = true;
                            element.properties.axis.barOffset = 0;
                            if ((_y = element.properties.axis) === null || _y === void 0 ? void 0 : _y.style) {
                                element.properties.axis.style.showBaseline = (_z = element.properties.axis.style.showBaseline) !== null && _z !== void 0 ? _z : true;
                                element.properties.axis.style.showTicks = (_0 = element.properties.axis.style.showTicks) !== null && _0 !== void 0 ? _0 : true;
                            }
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
                if (item.kind == prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.mark;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                            element.properties.axis.orderByExpression = this.parseExpression(element.properties.axis.expression);
                            element.properties.axis.orderByCategories =
                                element.properties.axis.categories;
                            element.properties.axis.enableSelection = true;
                            if (element.properties.axis.style) {
                                element.properties.axis.style.showBaseline = (_1 = element.properties.axis.style.showBaseline) !== null && _1 !== void 0 ? _1 : true;
                                element.properties.axis.style.showTicks = (_2 = element.properties.axis.style.showTicks) !== null && _2 !== void 0 ? _2 : true;
                            }
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
            }
        }
        catch (e_15_1) { e_15 = { error: e_15_1 }; }
        finally {
            try {
                if (_4 && !_4.done && (_a = _3.return)) _a.call(_3);
            }
            finally { if (e_15) throw e_15.error; }
        }
        return state;
    };
    Migrator.prototype.setMissedLegendProperties = function (state) {
        var e_16, _a, e_17, _b;
        try {
            for (var _c = __values(state.chart.elements), _d = _c.next(); !_d.done; _d = _c.next()) {
                var element = _d.value;
                if (core_1.Prototypes.isType(element.classID, "legend.numerical-color")) {
                    var legend = element;
                    if (legend.properties.orientation === undefined) {
                        legend.properties.orientation = types_2.OrientationType.VERTICAL;
                    }
                    if (legend.properties.length === undefined) {
                        legend.properties.length =
                            color_legend_1.NumericalColorLegendClass.defaultLegendLength;
                    }
                }
            }
        }
        catch (e_16_1) { e_16 = { error: e_16_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_16) throw e_16.error; }
        }
        try {
            for (var _e = __values(prototypes_1.forEachObject(state.chart)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var item = _f.value;
                if (item.kind == prototypes_1.ObjectItemKind.ChartElement) {
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.cartesian")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if (element.properties.xData.numberOfTicks == undefined) {
                                element.properties.xData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.xData.autoNumberOfTicks == undefined) {
                                element.properties.xData.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if (element.properties.yData.numberOfTicks == undefined) {
                                element.properties.yData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.yData.autoNumberOfTicks == undefined) {
                                element.properties.yData.autoNumberOfTicks = true;
                            }
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.polar")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if (element.properties.xData.numberOfTicks == undefined) {
                                element.properties.xData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.xData.autoNumberOfTicks == undefined) {
                                element.properties.xData.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if (element.properties.yData.numberOfTicks == undefined) {
                                element.properties.yData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.yData.autoNumberOfTicks == undefined) {
                                element.properties.yData.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.line")) {
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                            if (element.properties.axis.numberOfTicks == undefined) {
                                element.properties.axis.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.axis.autoNumberOfTicks == undefined) {
                                element.properties.axis.autoNumberOfTicks = true;
                            }
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment.curve")) {
                        var element = item.chartElement;
                        if (element.properties.xData) {
                            element.properties.xData = this.updateAxis(element.properties.xData);
                            if (element.properties.xData.numberOfTicks == undefined) {
                                element.properties.xData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.xData.autoNumberOfTicks == undefined) {
                                element.properties.xData.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.xData === undefined) {
                            element.properties.xData = null;
                        }
                        if (element.properties.yData) {
                            element.properties.yData = this.updateAxis(element.properties.yData);
                            if (element.properties.yData.numberOfTicks == undefined) {
                                element.properties.yData.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.yData.autoNumberOfTicks == undefined) {
                                element.properties.yData.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.yData === undefined) {
                            element.properties.yData = null;
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.chartElement;
                        if (element.properties.axis) {
                            element.properties.axis = this.updateAxis(element.properties.axis);
                            if (element.properties.axis.numberOfTicks == undefined) {
                                element.properties.axis.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.axis.autoNumberOfTicks == undefined) {
                                element.properties.axis.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
                if (item.kind == prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.data-axis")) {
                        // eslint-disable-next-line @typescript-eslint/ban-types
                        var element = item.mark;
                        if (element.properties.axis) {
                            if (element.properties.axis.numberOfTicks == undefined) {
                                element.properties.axis.numberOfTicks =
                                    axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER;
                            }
                            if (element.properties.axis.autoNumberOfTicks == undefined) {
                                element.properties.axis.autoNumberOfTicks = true;
                            }
                        }
                        if (element.properties.axis === undefined) {
                            element.properties.axis = null;
                        }
                    }
                }
            }
        }
        catch (e_17_1) { e_17 = { error: e_17_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_17) throw e_17.error; }
        }
        return state;
    };
    Migrator.prototype.setMissedProperties_2_1_6 = function (state) {
        var e_18, _a, e_19, _b;
        try {
            for (var _c = __values(state.chart.elements), _d = _c.next(); !_d.done; _d = _c.next()) {
                var element = _d.value;
                if (core_1.Prototypes.isType(element.classID, "links")) {
                    var link = element;
                    if (link) {
                        link.properties.beginArrowType = links_1.ArrowType.NO_ARROW;
                        link.properties.endArrowType = links_1.ArrowType.NO_ARROW;
                    }
                }
            }
        }
        catch (e_18_1) { e_18 = { error: e_18_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_18) throw e_18.error; }
        }
        try {
            for (var _e = __values(prototypes_1.forEachObject(state.chart)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var item = _f.value;
                if (item.kind == "mark") {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.rect")) {
                        item.mark.properties.orientation =
                            types_2.OrientationType.VERTICAL;
                        item.mark.properties.cometMark = false;
                    }
                }
            }
        }
        catch (e_19_1) { e_19 = { error: e_19_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_19) throw e_19.error; }
        }
        return state;
    };
    return Migrator;
}());
exports.Migrator = Migrator;
//# sourceMappingURL=migrator.js.map