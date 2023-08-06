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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildAxisProperties = exports.buildAxisInference = exports.buildAxisWidgets = exports.buildAxisAppearanceWidgets = exports.getNumericalInterpolate = exports.getCategoricalAxis = exports.AxisRenderer = exports.AxisMode = exports.defaultAxisStyle = void 0;
var common_1 = require("../../common");
var graphics_1 = require("../../graphics");
var text_measurer_1 = require("../../graphics/renderer/text_measurer");
var index_1 = require("../../index");
var common_2 = require("../common");
var specification_1 = require("../../specification");
var strings_1 = require("../../../strings");
var defaults_1 = require("../../../app/stores/defaults");
var types_1 = require("../../specification/types");
var virtualScroll_1 = require("./virtualScroll");
var utils_1 = require("./utils");
var Expression = require("../../expression");
var group_by_1 = require("../group_by");
var common_3 = require("../../../app/views/dataset/common");
var React = require("react");
exports.defaultAxisStyle = {
    tickColor: { r: 0, g: 0, b: 0 },
    tickTextBackgroudColor: null,
    tickTextBackgroudColorId: null,
    showTicks: true,
    showBaseline: true,
    lineColor: { r: 0, g: 0, b: 0 },
    fontFamily: defaults_1.defaultFont,
    fontSize: defaults_1.defaultFontSize,
    tickSize: 5,
    wordWrap: false,
    verticalText: false,
    gridlineStyle: "none",
    gridlineColor: {
        r: 234,
        g: 234,
        b: 234,
    },
    gridlineWidth: 1,
};
function fillDefaultAxisStyle(style) {
    return common_1.fillDefaults(style, exports.defaultAxisStyle);
}
var AxisMode;
(function (AxisMode) {
    AxisMode["X"] = "x";
    AxisMode["Y"] = "y";
})(AxisMode = exports.AxisMode || (exports.AxisMode = {}));
var AxisRenderer = /** @class */ (function () {
    function AxisRenderer() {
        this.ticks = [];
        this.style = exports.defaultAxisStyle;
        this.rangeMin = 0;
        this.rangeMax = 1;
        this.oppositeSide = false;
        this.scrollRequired = false;
        this.shiftAxis = true;
        this.hiddenCategoriesRatio = 0;
        this.dataType = types_1.AxisDataBindingType.Default;
        this.windowSize = 1;
        this.chartMarginForYLabel = null;
    }
    AxisRenderer.prototype.setStyle = function (style) {
        if (!style) {
            this.style = exports.defaultAxisStyle;
        }
        else {
            this.style = fillDefaultAxisStyle(common_1.deepClone(style));
        }
        this.style.tickTextBackgroudColorId =
            "axis-tick-filter-" + common_1.getRandomNumber();
        return this;
    };
    AxisRenderer.prototype.setAxisDataBinding = function (data, rangeMin, rangeMax, enablePrePostGap, reverse, getTickFormat, plotSegment, dataflow) {
        var _a, _b;
        this.rangeMin = rangeMin;
        this.rangeMax = rangeMax;
        if (!data) {
            return this;
        }
        this.plotSegment = plotSegment;
        this.dataFlow = dataflow;
        this.data = data;
        this.setStyle(data.style);
        this.oppositeSide = data.side == "opposite";
        this.scrollRequired = data.allowScrolling;
        this.shiftAxis =
            data.allowScrolling &&
                (data.barOffset == null || data.barOffset === 0) &&
                ((data.allCategories && data.windowSize < ((_a = data.allCategories) === null || _a === void 0 ? void 0 : _a.length)) ||
                    Math.abs(data.dataDomainMax - data.dataDomainMin) > data.windowSize);
        this.dataType = data.type;
        this.hiddenCategoriesRatio =
            data.windowSize /
                (data.allCategories
                    ? data.allCategories.length
                    : Math.abs(data.dataDomainMax - data.dataDomainMin));
        if (this.shiftAxis) {
            if (data.windowSize > ((_b = data.allCategories) === null || _b === void 0 ? void 0 : _b.length) ||
                data.windowSize > Math.abs(data.dataDomainMax - data.dataDomainMin)) {
                this.windowSize = data.allCategories
                    ? Math.max(data.allCategories.length, 1)
                    : Math.abs(data.dataDomainMax - data.dataDomainMin);
            }
            else {
                this.windowSize = Math.max(data.windowSize, 1);
            }
        }
        switch (data.type) {
            case "numerical":
                {
                    if (!data.numericalMode || data.numericalMode == "linear") {
                        this.setLinearScale(data.domainMin, data.domainMax, rangeMin, rangeMax, data.tickFormat, data.numberOfTicks, data.autoNumberOfTicks);
                    }
                    if (data.numericalMode == "logarithmic") {
                        this.setLogarithmicScale(data.domainMin, data.domainMax, rangeMin, rangeMax, data.tickFormat, data.numberOfTicks, data.autoNumberOfTicks);
                    }
                    if (data.numericalMode == "temporal") {
                        this.setTemporalScale(data.domainMin, data.domainMax, rangeMin, rangeMax, data.tickFormat, data.numberOfTicks, data.autoNumberOfTicks);
                    }
                }
                break;
            case "categorical":
                {
                    this.setCategoricalScale(data.categories, getCategoricalAxis(data, enablePrePostGap, reverse).ranges, rangeMin, rangeMax, getTickFormat);
                }
                break;
            // case "default":
            //   {
            //   }
            //   break;
        }
        return this;
    };
    AxisRenderer.prototype.setTicksByData = function (ticks, tickFormatString) {
        var e_1, _a, e_2, _b;
        var position2Tick = new Map();
        try {
            for (var ticks_1 = __values(ticks), ticks_1_1 = ticks_1.next(); !ticks_1_1.done; ticks_1_1 = ticks_1.next()) {
                var tick = ticks_1_1.value;
                var pos = this.valueToPosition(tick.value);
                var label = void 0;
                var tickFormat = tickFormatString
                    ? tickFormatString === null || tickFormatString === void 0 ? void 0 : tickFormatString.replace(common_1.tickFormatParserExpression(), "$1") : null;
                if (!tickFormat || typeof tick.tick == "string") {
                    label = tick.tick;
                }
                else {
                    try {
                        //try parse numeric format
                        label = common_1.getFormat()(tickFormat)(tick.tick);
                    }
                    catch (e) {
                        try {
                            //try parse date format
                            label = common_1.applyDateFormat(new Date(tick.tick), tickFormat);
                        }
                        catch (ex) {
                            //use string format
                            label = tick.tick;
                        }
                    }
                }
                position2Tick.set(pos, label);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (ticks_1_1 && !ticks_1_1.done && (_a = ticks_1.return)) _a.call(ticks_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.ticks = [];
        try {
            for (var _c = __values(position2Tick.entries()), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), pos = _e[0], tick = _e[1];
                this.ticks.push({
                    position: pos,
                    label: tick,
                });
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
            }
            finally { if (e_2) throw e_2.error; }
        }
    };
    AxisRenderer.getTickFormat = function (tickFormat, defaultFormat) {
        if (tickFormat == null || tickFormat == "") {
            return defaultFormat;
        }
        else {
            // {.0%}
            return function (value) {
                return tickFormat.replace(common_1.tickFormatParserExpression(), function (_, spec) {
                    return common_1.getFormat()(spec)(value);
                });
            };
        }
    };
    AxisRenderer.prototype.setCartesianChartMargin = function (plotSegment) {
        var _a, _b, _c, _d, _e, _f;
        try {
            var mappings = (_a = plotSegment.object) === null || _a === void 0 ? void 0 : _a.mappings;
            var side = (_d = (_c = (_b = plotSegment.object) === null || _b === void 0 ? void 0 : _b.properties) === null || _c === void 0 ? void 0 : _c.yData) === null || _d === void 0 ? void 0 : _d.side;
            if (side === "default") {
                if (mappings.x1.type === specification_1.MappingType.parent &&
                    mappings.x1.parentAttribute == "x1") {
                    this.chartMarginForYLabel = (_e = plotSegment.parent.state.attributes) === null || _e === void 0 ? void 0 : _e.marginLeft;
                }
                else {
                    this.chartMarginForYLabel = null;
                }
            }
            else {
                if (mappings.x2.type === specification_1.MappingType.parent &&
                    mappings.x2.parentAttribute == "x2") {
                    this.chartMarginForYLabel = (_f = plotSegment.parent.state.attributes) === null || _f === void 0 ? void 0 : _f.marginRight;
                }
                else {
                    this.chartMarginForYLabel = null;
                }
            }
        }
        catch (ex) {
            this.chartMarginForYLabel = null;
        }
    };
    AxisRenderer.prototype.setLinearScale = function (domainMin, domainMax, rangeMin, rangeMax, tickFormat, numberOfTicks, autoTickNumber) {
        if (numberOfTicks === void 0) { numberOfTicks = AxisRenderer.DEFAULT_TICKS_NUMBER; }
        if (autoTickNumber === void 0) { autoTickNumber = true; }
        var scale = new common_1.Scale.LinearScale();
        scale.domainMin = domainMin;
        scale.domainMax = domainMax;
        var rangeLength = Math.abs(rangeMax - rangeMin);
        var tickNumber = numberOfTicks;
        if (autoTickNumber) {
            tickNumber = Math.round(Math.min(10, rangeLength / 40));
            if (this.data) {
                this.data.numberOfTicks = tickNumber;
            }
        }
        var ticks = scale.ticks(tickNumber);
        var defaultFormat = scale.tickFormat(tickNumber);
        var resolvedFormat = AxisRenderer.getTickFormat(tickFormat, defaultFormat);
        var r = [];
        for (var i = 0; i < ticks.length; i++) {
            var tx = ((ticks[i] - domainMin) / (domainMax - domainMin)) *
                (rangeMax - rangeMin) +
                rangeMin;
            if (!isNaN(tx)) {
                r.push({
                    position: tx,
                    label: resolvedFormat(ticks[i]),
                });
            }
        }
        this.valueToPosition = function (value) {
            return ((value - domainMin) / (domainMax - domainMin)) * (rangeMax - rangeMin) +
                rangeMin;
        };
        this.ticks = r;
        this.rangeMin = rangeMin;
        this.rangeMax = rangeMax;
        return this;
    };
    AxisRenderer.prototype.setLogarithmicScale = function (domainMin, domainMax, rangeMin, rangeMax, tickFormat, numberOfTicks, autoTickNumber) {
        if (numberOfTicks === void 0) { numberOfTicks = AxisRenderer.DEFAULT_TICKS_NUMBER; }
        if (autoTickNumber === void 0) { autoTickNumber = true; }
        var scale = new common_1.Scale.LogarithmicScale();
        scale.domainMin = domainMin;
        scale.domainMax = domainMax;
        var rangeLength = Math.abs(rangeMax - rangeMin);
        var tickNumber = numberOfTicks;
        if (autoTickNumber) {
            tickNumber = Math.round(Math.min(10, rangeLength / 40));
            if (this.data) {
                this.data.numberOfTicks = tickNumber;
            }
        }
        var ticks = scale.ticks(tickNumber);
        var defaultFormat = scale.tickFormat(tickNumber);
        var resolvedFormat = AxisRenderer.getTickFormat(tickFormat, defaultFormat);
        var r = [];
        for (var i = 0; i < ticks.length; i++) {
            var tx = ((Math.log(ticks[i]) - Math.log(domainMin)) /
                (Math.log(domainMax) - Math.log(domainMin))) *
                (rangeMax - rangeMin) +
                rangeMin;
            if (!isNaN(tx)) {
                r.push({
                    position: tx,
                    label: resolvedFormat(ticks[i]),
                });
            }
        }
        this.valueToPosition = function (value) {
            return ((value - domainMin) / (domainMax - domainMin)) * (rangeMax - rangeMin) +
                rangeMin;
        };
        this.ticks = r;
        this.rangeMin = rangeMin;
        this.rangeMax = rangeMax;
        return this;
    };
    AxisRenderer.prototype.setTemporalScale = function (domainMin, domainMax, rangeMin, rangeMax, tickFormatString, numberOfTicks, autoTickNumber) {
        if (numberOfTicks === void 0) { numberOfTicks = AxisRenderer.DEFAULT_TICKS_NUMBER; }
        if (autoTickNumber === void 0) { autoTickNumber = true; }
        var scale = new common_1.Scale.DateScale();
        scale.domainMin = domainMin;
        scale.domainMax = domainMax;
        var rangeLength = Math.abs(rangeMax - rangeMin);
        var tickNumber = numberOfTicks;
        if (autoTickNumber) {
            tickNumber = Math.round(Math.min(10, rangeLength / 40));
            if (this.data) {
                this.data.numberOfTicks = tickNumber;
            }
        }
        var ticks = scale.ticks(tickNumber);
        var tickFormat = scale.tickFormat(tickNumber, tickFormatString === null || tickFormatString === void 0 ? void 0 : tickFormatString.replace(common_1.tickFormatParserExpression(), "$1"));
        var r = [];
        for (var i = 0; i < ticks.length; i++) {
            var tx = ((ticks[i] - domainMin) / (domainMax - domainMin)) *
                (rangeMax - rangeMin) +
                rangeMin;
            if (!isNaN(tx)) {
                r.push({
                    position: tx,
                    label: tickFormat(ticks[i]),
                });
            }
        }
        this.valueToPosition = function (value) {
            return ((value - domainMin) / (domainMax - domainMin)) * (rangeMax - rangeMin) +
                rangeMin;
        };
        this.ticks = r;
        this.rangeMin = rangeMin;
        this.rangeMax = rangeMax;
        return this;
    };
    AxisRenderer.prototype.setCategoricalScale = function (domain, range, rangeMin, rangeMax, tickFormat) {
        var r = [];
        for (var i = 0; i < domain.length; i++) {
            var position = ((range[i][0] + range[i][1]) / 2) * (rangeMax - rangeMin) + rangeMin;
            if (!isNaN(position)) {
                r.push({
                    position: position,
                    label: tickFormat ? tickFormat(domain[i]) : domain[i],
                });
            }
        }
        this.valueToPosition = function (value) {
            var i = domain.indexOf(value);
            if (i >= 0) {
                return (((range[i][0] + range[i][1]) / 2) * (rangeMax - rangeMin) + rangeMin);
            }
            else {
                return 0;
            }
        };
        this.ticks = r;
        this.rangeMin = rangeMin;
        this.rangeMax = rangeMax;
        return this;
    };
    AxisRenderer.prototype.renderGridLine = function (x, y, angle, side, size) {
        var e_3, _a;
        var style = this.style;
        if (style.gridlineStyle === "none") {
            return;
        }
        if (this.oppositeSide) {
            side = -side;
        }
        var g = graphics_1.makeGroup([]);
        var cos = Math.cos(common_1.Geometry.degreesToRadians(angle));
        var sin = Math.sin(common_1.Geometry.degreesToRadians(angle));
        var tickSize = size;
        var lineStyle = {
            strokeLinecap: "round",
            // strokeColor: style.lineColor,
            strokeColor: style.gridlineColor,
            strokeWidth: style.gridlineWidth,
            strokeDasharray: common_2.strokeStyleToDashArray(style.gridlineStyle),
        };
        // Ticks
        var ticksData = this.ticks.map(function (x) { return x.position; });
        try {
            for (var ticksData_1 = __values(ticksData), ticksData_1_1 = ticksData_1.next(); !ticksData_1_1.done; ticksData_1_1 = ticksData_1.next()) {
                var tickPosition = ticksData_1_1.value;
                var tx = x + tickPosition * cos;
                var ty = y + tickPosition * sin;
                var dx = -side * tickSize * sin;
                var dy = side * tickSize * cos;
                g.elements.push(graphics_1.makeLine(tx, ty, tx + dx, ty + dy, lineStyle));
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (ticksData_1_1 && !ticksData_1_1.done && (_a = ticksData_1.return)) _a.call(ticksData_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return g;
    };
    AxisRenderer.prototype.renderGridlinesForAxes = function (x, y, axis, size) {
        switch (axis) {
            case AxisMode.X: {
                return this.renderGridLine(x, y, 0, 1, size);
            }
            case AxisMode.Y: {
                return this.renderGridLine(x, y, 90, -1, size);
            }
        }
    };
    // eslint-disable-next-line
    AxisRenderer.prototype.renderLine = function (x, y, angle, side, axisOffset) {
        var e_4, _a, e_5, _b;
        var g = graphics_1.makeGroup([]);
        var style = this.style;
        var rangeMin = this.rangeMin;
        var rangeMax = this.rangeMax;
        var tickSize = style.tickSize;
        var lineStyle = {
            strokeLinecap: "square",
            strokeColor: style.lineColor,
        };
        AxisRenderer.textMeasurer.setFontFamily(style.fontFamily);
        AxisRenderer.textMeasurer.setFontSize(style.fontSize);
        if (this.oppositeSide) {
            side = -side;
        }
        //shift axis for scrollbar space
        if (this.scrollRequired && this.shiftAxis) {
            if (angle === 90) {
                x += side * AxisRenderer.SCROLL_BAR_SIZE;
            }
            if (angle === 0) {
                y += -side * AxisRenderer.SCROLL_BAR_SIZE;
            }
        }
        var cos = Math.cos(common_1.Geometry.degreesToRadians(angle));
        var sin = Math.sin(common_1.Geometry.degreesToRadians(angle));
        var x1 = x + rangeMin * cos;
        var y1 = y + rangeMin * sin;
        var x2 = x + rangeMax * cos;
        var y2 = y + rangeMax * sin;
        // Base line
        if (style.showBaseline) {
            g.elements.push(graphics_1.makeLine(x1, y1, x2, y2, lineStyle));
        }
        // Ticks
        var visibleTicks = this.ticks.map(function (x) { return x.position; });
        if (style.showBaseline) {
            visibleTicks.push(rangeMin, rangeMax);
        }
        if (style.showTicks) {
            try {
                for (var visibleTicks_1 = __values(visibleTicks), visibleTicks_1_1 = visibleTicks_1.next(); !visibleTicks_1_1.done; visibleTicks_1_1 = visibleTicks_1.next()) {
                    var tickPosition = visibleTicks_1_1.value;
                    var tx = x + tickPosition * cos;
                    var ty = y + tickPosition * sin;
                    var dx = side * tickSize * sin;
                    var dy = -side * tickSize * cos;
                    g.elements.push(graphics_1.makeLine(tx, ty, tx + dx, ty + dy, lineStyle));
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (visibleTicks_1_1 && !visibleTicks_1_1.done && (_a = visibleTicks_1.return)) _a.call(visibleTicks_1);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
        // Tick texts
        var ticks = this.ticks.map(function (x) {
            return {
                position: x.position,
                label: x.label,
                measure: AxisRenderer.textMeasurer.measure(x.label),
            };
        });
        var maxTextWidth = 0;
        var maxTickDistance = 0;
        for (var i = 0; i < ticks.length; i++) {
            maxTextWidth = Math.max(maxTextWidth, ticks[i].measure.width);
            if (i > 0) {
                maxTickDistance = Math.max(maxTickDistance, Math.abs(ticks[i - 1].position - ticks[i].position));
            }
        }
        try {
            for (var ticks_2 = __values(ticks), ticks_2_1 = ticks_2.next(); !ticks_2_1.done; ticks_2_1 = ticks_2.next()) {
                var tick = ticks_2_1.value;
                var tx = x + tick.position * cos, ty = y + tick.position * sin;
                var offset = 3;
                var dx = side * (tickSize + offset) * sin, dy = -side * (tickSize + offset) * cos;
                if (Math.abs(cos) < 0.5) {
                    if (style.wordWrap ||
                        (typeof tick.label === "string" &&
                            common_1.splitStringByNewLine(tick.label).length > 1)) {
                        var textContent = void 0;
                        var textWidth = void 0;
                        if (this.chartMarginForYLabel != null) {
                            if (this.oppositeSide) {
                                textWidth =
                                    this.chartMarginForYLabel -
                                        AxisRenderer.DEFAULT_Y_LABEL_GAP -
                                        (axisOffset !== null && axisOffset !== void 0 ? axisOffset : 0);
                            }
                            else {
                                textWidth =
                                    this.chartMarginForYLabel -
                                        AxisRenderer.DEFAULT_Y_LABEL_GAP +
                                        (axisOffset !== null && axisOffset !== void 0 ? axisOffset : 0);
                            }
                        }
                        else {
                            textWidth = maxTickDistance;
                        }
                        textContent = text_measurer_1.splitByWidth(common_1.replaceSymbolByTab(common_1.replaceSymbolByNewLine(tick.label)), textWidth, 10000, style.fontFamily, style.fontSize);
                        textContent = textContent.flatMap(function (line) {
                            return common_1.splitStringByNewLine(line);
                        });
                        var lines = [];
                        for (var index = 0; index < textContent.length; index++) {
                            var _c = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, AxisRenderer.textMeasurer.measure(textContent[index]), style.verticalText ? "middle" : side * sin < 0 ? "right" : "left", style.verticalText
                                ? side * sin < 0
                                    ? "bottom"
                                    : "top"
                                : "middle", 0), 2), px = _c[0], py = _c[1];
                            var text = graphics_1.makeText(px, py -
                                style.fontSize * index +
                                (side * cos > 0
                                    ? 0
                                    : (textContent.length * style.fontSize - style.fontSize) / 2), textContent[index], style.fontFamily, style.fontSize, {
                                fillColor: style.tickColor,
                                backgroundColor: style.tickTextBackgroudColor,
                                backgroundColorId: style.tickTextBackgroudColorId,
                            });
                            lines.push(text);
                        }
                        var gText = graphics_1.makeGroup(lines);
                        gText.transform = {
                            x: tx + dx,
                            y: ty + dy,
                            angle: style.verticalText ? angle : 0,
                        };
                        g.elements.push(gText);
                    }
                    else {
                        // 60 ~ 120 degree
                        var _d = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, tick.measure, side * sin < 0 ? "right" : "left", "middle", 0), 2), px = _d[0], py = _d[1];
                        var gText = graphics_1.makeGroup([
                            graphics_1.makeText(px, py, tick.label, style.fontFamily, style.fontSize, {
                                fillColor: style.tickColor,
                                backgroundColor: style.tickTextBackgroudColor,
                                backgroundColorId: style.tickTextBackgroudColorId,
                            }, this.plotSegment && this.dataFlow
                                ? {
                                    enableSelection: this.data.enableSelection,
                                    glyphIndex: 1,
                                    rowIndices: applySelectionFilter(this.data, this.plotSegment.table, ticks.indexOf(tick), this.dataFlow),
                                    plotSegment: this.plotSegment,
                                }
                                : undefined),
                        ]);
                        gText.transform = {
                            x: tx + dx,
                            y: ty + dy,
                            angle: style.verticalText ? (sin > 0 ? angle - 90 : angle + 90) : 0,
                        };
                        g.elements.push(gText);
                    }
                }
                else if (Math.abs(cos) < Math.sqrt(3) / 2) {
                    var _e = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, tick.measure, side * sin < 0 ? "right" : "left", "middle", 0), 2), px = _e[0], py = _e[1];
                    var gText = graphics_1.makeGroup([
                        graphics_1.makeText(px, py, tick.label, style.fontFamily, style.fontSize, {
                            fillColor: style.tickColor,
                            backgroundColor: style.tickTextBackgroudColor,
                            backgroundColorId: style.tickTextBackgroudColorId,
                        }, this.plotSegment && this.dataFlow
                            ? {
                                enableSelection: this.data.enableSelection,
                                glyphIndex: 1,
                                rowIndices: applySelectionFilter(this.data, this.plotSegment.table, ticks.indexOf(tick), this.dataFlow),
                                plotSegment: this.plotSegment,
                            }
                            : undefined),
                    ]);
                    gText.transform = {
                        x: tx + dx,
                        y: ty + dy,
                        angle: style.verticalText ? (sin > 0 ? angle - 90 : angle + 90) : 0,
                    };
                    g.elements.push(gText);
                }
                else {
                    if (!style.wordWrap &&
                        maxTextWidth > maxTickDistance &&
                        typeof tick.label === "string" &&
                        common_1.splitStringByNewLine(tick.label).length === 1) {
                        var _f = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, tick.measure, style.verticalText
                            ? side * cos > 0
                                ? "right"
                                : "left"
                            : style.wordWrap
                                ? "middle"
                                : side * cos > 0
                                    ? "right"
                                    : "left", style.verticalText
                            ? "middle"
                            : style.wordWrap
                                ? "middle"
                                : side * cos > 0
                                    ? "top"
                                    : "bottom", 0), 2), px = _f[0], py = _f[1];
                        var gText = graphics_1.makeGroup([
                            graphics_1.makeText(px, py, tick.label, style.fontFamily, style.fontSize, {
                                fillColor: style.tickColor,
                                backgroundColor: style.tickTextBackgroudColor,
                                backgroundColorId: style.tickTextBackgroudColorId,
                            }, this.plotSegment && this.dataFlow
                                ? {
                                    enableSelection: this.data.enableSelection,
                                    glyphIndex: 1,
                                    rowIndices: applySelectionFilter(this.data, this.plotSegment.table, ticks.indexOf(tick), this.dataFlow),
                                    plotSegment: this.plotSegment,
                                }
                                : undefined),
                        ]);
                        gText.transform = {
                            x: tx + dx,
                            y: ty + dy,
                            angle: style.verticalText
                                ? cos > 0
                                    ? 90 + angle
                                    : 90 + angle - 180
                                : cos > 0
                                    ? 36 + angle
                                    : 36 + angle - 180,
                        };
                        g.elements.push(gText);
                    }
                    else {
                        if (style.wordWrap ||
                            (typeof tick.label === "string" &&
                                common_1.splitStringByNewLine(tick.label).length > 1)) {
                            var textContent = [
                                common_1.replaceSymbolByTab(common_1.replaceSymbolByNewLine(tick.label)),
                            ];
                            if (style.wordWrap) {
                                textContent = text_measurer_1.splitByWidth(common_1.replaceSymbolByTab(common_1.replaceSymbolByNewLine(tick.label)), maxTickDistance, 10000, style.fontFamily, style.fontSize);
                            }
                            textContent = textContent.flatMap(function (line) {
                                return common_1.splitStringByNewLine(line);
                            });
                            var lines = [];
                            for (var index = 0; index < textContent.length; index++) {
                                var _g = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, AxisRenderer.textMeasurer.measure(textContent[index]), style.wordWrap ? "middle" : side * cos > 0 ? "right" : "left", side * cos > 0 ? "top" : "bottom", 0), 2), px = _g[0], py = _g[1];
                                var text = graphics_1.makeText(px, py -
                                    style.fontSize * index +
                                    (side * cos > 0 ? 0 : textContent.length * style.fontSize), textContent[index], style.fontFamily, style.fontSize, {
                                    fillColor: style.tickColor,
                                    backgroundColor: style.tickTextBackgroudColor,
                                    backgroundColorId: style.tickTextBackgroudColorId,
                                }, this.plotSegment && this.dataFlow
                                    ? {
                                        enableSelection: this.data.enableSelection,
                                        glyphIndex: 1,
                                        rowIndices: applySelectionFilter(this.data, this.plotSegment.table, ticks.indexOf(tick), this.dataFlow),
                                        plotSegment: this.plotSegment,
                                    }
                                    : undefined);
                                lines.push(text);
                            }
                            var gText = graphics_1.makeGroup(lines);
                            gText.transform = {
                                x: tx + dx,
                                y: ty + dy,
                                angle: style.verticalText
                                    ? style.wordWrap
                                        ? 0
                                        : cos > 0
                                            ? 90 + angle
                                            : 90 + angle - 180
                                    : style.wordWrap
                                        ? 0
                                        : cos > 0
                                            ? 36 + angle
                                            : 36 + angle - 180,
                            };
                            g.elements.push(gText);
                        }
                        else {
                            var _h = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, 0, tick.measure, style.verticalText
                                ? side * cos > 0
                                    ? "right"
                                    : "left"
                                : "middle", style.verticalText ? "middle" : side * cos > 0 ? "top" : "bottom", 0), 2), px = _h[0], py = _h[1];
                            var gText = graphics_1.makeGroup([
                                graphics_1.makeText(px, py, tick.label, style.fontFamily, style.fontSize, {
                                    fillColor: style.tickColor,
                                    backgroundColor: style.tickTextBackgroudColor,
                                    backgroundColorId: style.tickTextBackgroudColorId,
                                }, this.plotSegment && this.dataFlow
                                    ? {
                                        enableSelection: this.data.enableSelection,
                                        glyphIndex: 1,
                                        rowIndices: applySelectionFilter(this.data, this.plotSegment.table, ticks.indexOf(tick), this.dataFlow),
                                        plotSegment: this.plotSegment,
                                    }
                                    : undefined),
                            ]);
                            gText.transform = {
                                x: tx + dx,
                                y: ty + dy,
                                angle: style.verticalText ? 90 + angle : 0,
                            };
                            g.elements.push(gText);
                        }
                    }
                }
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (ticks_2_1 && !ticks_2_1.done && (_b = ticks_2.return)) _b.call(ticks_2);
            }
            finally { if (e_5) throw e_5.error; }
        }
        if (axisOffset) {
            g.transform = {
                x: angle == 90 ? axisOffset : 0,
                y: angle == 90 ? 0 : axisOffset,
                angle: 0,
            };
        }
        return g;
    };
    AxisRenderer.prototype.renderCartesian = function (x, y, axis, offset) {
        switch (axis) {
            case AxisMode.X: {
                return this.renderLine(x, y, 0, 1, offset);
            }
            case AxisMode.Y: {
                return this.renderLine(x, y, 90, -1, offset);
            }
        }
    };
    AxisRenderer.prototype.renderPolarRadialGridLine = function (x, y, innerRadius, outerRadius) {
        var e_6, _a;
        var style = this.style;
        if (style.gridlineStyle === "none") {
            return;
        }
        var g = graphics_1.makeGroup([]);
        var gridineArcRotate = 90;
        var lineStyle = {
            strokeLinecap: "round",
            strokeColor: style.gridlineColor,
            strokeWidth: style.gridlineWidth,
            strokeDasharray: common_2.strokeStyleToDashArray(style.gridlineStyle),
        };
        try {
            for (var _b = __values(this.ticks.map(function (x) { return x.position; })), _c = _b.next(); !_c.done; _c = _b.next()) {
                var tickPosition = _c.value;
                var cos = Math.cos(common_1.Geometry.degreesToRadians(-tickPosition + gridineArcRotate));
                var sin = Math.sin(common_1.Geometry.degreesToRadians(-tickPosition + gridineArcRotate));
                var tx1 = x + cos * innerRadius;
                var ty1 = y + sin * innerRadius;
                var tx2 = x + cos * outerRadius;
                var ty2 = y + sin * outerRadius;
                g.elements.push(graphics_1.makeLine(tx1, ty1, tx2, ty2, lineStyle));
            }
        }
        catch (e_6_1) { e_6 = { error: e_6_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_6) throw e_6.error; }
        }
        return g;
    };
    AxisRenderer.prototype.renderPolarArcGridLine = function (x, y, innerRadius, outerRadius, startAngle, endAngle) {
        var e_7, _a;
        var style = this.style;
        if (style.gridlineStyle === "none") {
            return;
        }
        var g = graphics_1.makeGroup([]);
        var startCos = Math.cos(common_1.Geometry.degreesToRadians(startAngle));
        var startSin = Math.sin(common_1.Geometry.degreesToRadians(startAngle));
        var gridineArcRotate = 90;
        var lineStyle = {
            strokeLinecap: "round",
            strokeColor: style.gridlineColor,
            strokeWidth: style.gridlineWidth,
            strokeDasharray: common_2.strokeStyleToDashArray(style.gridlineStyle),
        };
        var radius = (outerRadius - innerRadius) / this.ticks.length;
        try {
            for (var _b = __values(this.ticks.map(function (x) { return x.position; })), _c = _b.next(); !_c.done; _c = _b.next()) {
                var tickPosition = _c.value;
                var tx1 = x + tickPosition * startCos;
                var ty1 = y + tickPosition * startSin;
                var arc = graphics_1.makePath(lineStyle);
                arc.moveTo(tx1, ty1);
                arc.polarLineTo(x, y, -startAngle + gridineArcRotate, tickPosition, -endAngle + gridineArcRotate, tickPosition, true);
                g.elements.push(arc.path);
                radius += radius;
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_7) throw e_7.error; }
        }
        return g;
    };
    // eslint-disable-next-line
    AxisRenderer.prototype.renderPolar = function (cx, cy, radius, side) {
        var e_8, _a;
        var style = this.style;
        var rangeMin = this.rangeMin;
        var rangeMax = this.rangeMax;
        var lineStyle = {
            strokeLinecap: "round",
            strokeColor: style.lineColor,
        };
        var g = graphics_1.makeGroup([]);
        g.transform.x = cx;
        g.transform.y = cy;
        AxisRenderer.textMeasurer.setFontFamily(style.fontFamily);
        AxisRenderer.textMeasurer.setFontSize(style.fontSize);
        var margins = 10;
        var maxTickDistance = common_1.Geometry.degreesToRadians(radius * ((rangeMax - rangeMin) / this.ticks.length)) -
            margins * 2; // lenght of arc for all ticks
        try {
            for (var _b = __values(this.ticks), _c = _b.next(); !_c.done; _c = _b.next()) {
                var tick = _c.value;
                var angle = tick.position;
                var radians = common_1.Geometry.degreesToRadians(angle);
                var tx = Math.sin(radians) * radius;
                var ty = Math.cos(radians) * radius;
                var lablel = tick.label && common_1.replaceSymbolByTab(common_1.replaceSymbolByNewLine(tick.label));
                if (lablel &&
                    (style.wordWrap ||
                        (typeof tick.label === "string" &&
                            common_1.splitStringByNewLine(lablel).length > 1))) {
                    var textContent = [lablel];
                    if (style.wordWrap) {
                        textContent = text_measurer_1.splitByWidth(lablel, maxTickDistance, 10000, style.fontFamily, style.fontSize);
                    }
                    textContent = textContent.flatMap(function (line) { return common_1.splitStringByNewLine(line); });
                    var lines = [];
                    for (var index = 0; index < textContent.length; index++) {
                        var _d = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, style.tickSize * side, AxisRenderer.textMeasurer.measure(textContent[index]), "middle", side > 0 ? "bottom" : "top", 0, 2), 2), textX = _d[0], textY = _d[1];
                        var gt_1 = graphics_1.makeText(textX, textY -
                            style.fontSize * index +
                            (side > 0
                                ? style.fontSize * textContent.length - style.fontSize
                                : 0), textContent[index], style.fontFamily, style.fontSize, {
                            fillColor: style.tickColor,
                            backgroundColor: style.tickTextBackgroudColor,
                            backgroundColorId: style.tickTextBackgroudColorId,
                        });
                        lines.push(gt_1);
                    }
                    var line = graphics_1.makeLine(0, 0, 0, style.tickSize * side, lineStyle);
                    var gt = graphics_1.makeGroup(__spread([style.showTicks ? line : null], lines));
                    gt.transform.angle = -angle;
                    gt.transform.x = tx;
                    gt.transform.y = ty;
                    g.elements.push(gt);
                }
                else {
                    var _e = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, style.tickSize * side, AxisRenderer.textMeasurer.measure(tick.label), "middle", side > 0 ? "bottom" : "top", 0, 2), 2), textX = _e[0], textY = _e[1];
                    var line = graphics_1.makeLine(0, 0, 0, style.tickSize * side, lineStyle);
                    var gt = graphics_1.makeGroup([
                        style.showTicks ? line : null,
                        graphics_1.makeText(textX, textY, tick.label, style.fontFamily, style.fontSize, {
                            fillColor: style.tickColor,
                            backgroundColor: style.tickTextBackgroudColor,
                            backgroundColorId: style.tickTextBackgroudColorId,
                        }),
                    ]);
                    gt.transform.angle = -angle;
                    gt.transform.x = tx;
                    gt.transform.y = ty;
                    g.elements.push(gt);
                }
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_8) throw e_8.error; }
        }
        return g;
    };
    AxisRenderer.prototype.renderCurve = function (coordinateSystem, y, side) {
        var e_9, _a;
        var style = this.style;
        var lineStyle = {
            strokeLinecap: "round",
            strokeColor: style.lineColor,
        };
        var g = graphics_1.makeGroup([]);
        g.transform = coordinateSystem.getBaseTransform();
        AxisRenderer.textMeasurer.setFontFamily(style.fontFamily);
        AxisRenderer.textMeasurer.setFontSize(style.fontSize);
        try {
            for (var _b = __values(this.ticks), _c = _b.next(); !_c.done; _c = _b.next()) {
                var tick = _c.value;
                var tangent = tick.position;
                var metrics = AxisRenderer.textMeasurer.measure(tick.label);
                var _d = __read(text_measurer_1.TextMeasurer.ComputeTextPosition(0, -style.tickSize * side, metrics, "middle", side < 0 ? "bottom" : "top", 0, 2), 2), textX = _d[0], textY = _d[1];
                var line = graphics_1.makeLine(0, 0, 0, -style.tickSize * side, lineStyle);
                var gt = graphics_1.makeGroup([
                    style.showTicks ? line : null,
                    graphics_1.makeText(textX, textY, tick.label, style.fontFamily, style.fontSize, {
                        fillColor: style.tickColor,
                        backgroundColor: style.tickTextBackgroudColor,
                        backgroundColorId: style.tickTextBackgroudColorId,
                    }),
                ]);
                gt.transform = coordinateSystem.getLocalTransform(tangent, y);
                g.elements.push(gt);
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_9) throw e_9.error; }
        }
        return g;
    };
    AxisRenderer.prototype.renderVirtualScrollBar = function (x, y, axis, scrollPosition, onScroll, zoom) {
        switch (axis) {
            case AxisMode.X: {
                return this.renderScrollBar(x, y, 0, 1, scrollPosition, onScroll, zoom);
            }
            case AxisMode.Y: {
                return this.renderScrollBar(x, y, 90, -1, scrollPosition, onScroll, zoom);
            }
        }
    };
    AxisRenderer.prototype.renderScrollBar = function (x, y, angle, side, handlePosition, onScroll, zoom) {
        if (!this.scrollRequired) {
            return null;
        }
        var cos = Math.cos(common_1.Geometry.degreesToRadians(angle));
        var sin = Math.sin(common_1.Geometry.degreesToRadians(angle));
        var rangeMin = this.rangeMin;
        var rangeMax = this.rangeMax;
        var x1 = x + rangeMin * cos;
        var y1 = y + rangeMin * sin;
        var x2 = x + rangeMax * cos;
        var y2 = y + rangeMax * sin;
        if (this.oppositeSide) {
            side = -side;
        }
        if (!this.oppositeSide) {
            if (angle === 90) {
                x1 += side * AxisRenderer.SCROLL_BAR_SIZE;
                x2 += side * AxisRenderer.SCROLL_BAR_SIZE;
            }
            if (angle === 0) {
                y1 += -side * AxisRenderer.SCROLL_BAR_SIZE;
                y2 += -side * AxisRenderer.SCROLL_BAR_SIZE;
            }
        }
        var width = 0;
        var height = 0;
        if (angle === 90) {
            height += Math.abs(y2 - y1);
            width = AxisRenderer.SCROLL_BAR_SIZE;
        }
        if (angle === 0) {
            width += Math.abs(x2 - x1);
            height = AxisRenderer.SCROLL_BAR_SIZE;
        }
        return React.createElement(virtualScroll_1.VirtualScrollBar, {
            onScroll: onScroll,
            handlerBarWidth: AxisRenderer.SCROLL_BAR_SIZE,
            height: height,
            width: width,
            x: x1,
            y: y1,
            initialPosition: handlePosition,
            vertical: angle === 90,
            zoom: zoom,
            scrollBarRatio: this.hiddenCategoriesRatio,
            windowSize: this.windowSize,
            dataType: this.dataType,
        });
    };
    AxisRenderer.SCROLL_BAR_SIZE = 10;
    AxisRenderer.DEFAULT_TICKS_NUMBER = 10;
    AxisRenderer.DEFAULT_Y_LABEL_GAP = 15;
    AxisRenderer.textMeasurer = new text_measurer_1.TextMeasurer();
    return AxisRenderer;
}());
exports.AxisRenderer = AxisRenderer;
function getCategoricalAxis(data, enablePrePostGap, reverse) {
    if (data.enablePrePostGap) {
        enablePrePostGap = true;
    }
    var chunkSize = (1 - data.gapRatio) / data.categories.length;
    var preGap, postGap, gap, gapScale;
    if (enablePrePostGap) {
        gap = data.gapRatio / data.categories.length;
        gapScale = 1 / data.categories.length;
        preGap = gap / 2;
        postGap = gap / 2;
    }
    else {
        if (data.categories.length == 1) {
            gap = 0;
            gapScale = 1;
        }
        else {
            gap = data.gapRatio / (data.categories.length - 1);
            gapScale = 1 / (data.categories.length - 1);
        }
        preGap = 0;
        postGap = 0;
    }
    var chunkRanges = data.categories.map(function (c, i) {
        return [
            preGap + (gap + chunkSize) * i,
            preGap + (gap + chunkSize) * i + chunkSize,
        ];
    });
    if (reverse) {
        chunkRanges.reverse();
    }
    return {
        gap: gap,
        preGap: preGap,
        postGap: postGap,
        gapScale: gapScale,
        ranges: chunkRanges,
    };
}
exports.getCategoricalAxis = getCategoricalAxis;
function getNumericalInterpolate(data) {
    if (data.numericalMode == "logarithmic") {
        var p1_1 = Math.log(data.domainMin);
        var p2 = Math.log(data.domainMax);
        var pdiff_1 = p2 - p1_1;
        return function (x) { return (Math.log(x) - p1_1) / pdiff_1; };
    }
    else {
        var p1_2 = data.domainMin;
        var p2 = data.domainMax;
        var pdiff_2 = p2 - p1_2;
        return function (x) { return (x - p1_2) / pdiff_2; };
    }
}
exports.getNumericalInterpolate = getNumericalInterpolate;
function buildAxisAppearanceWidgets(axisProperty, manager, options) {
    if (options.isVisible) {
        var vertical = null;
        if (!options.wordWrap) {
            vertical = manager.inputBoolean({ property: axisProperty, field: ["style", "verticalText"] }, {
                type: "checkbox",
                label: strings_1.strings.objects.axes.verticalText,
                searchSection: [
                    strings_1.strings.objects.style,
                    options.mainCollapsePanelHeader,
                ],
            });
        }
        return [
            manager.vertical(manager.verticalGroup({
                header: strings_1.strings.objects.visibilityAndPosition,
            }, [
                manager.inputBoolean({ property: axisProperty, field: "visible" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.visibleOn.visible,
                    searchSection: [
                        strings_1.strings.objects.visibilityAndPosition,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                options.isOnTop
                    ? manager.inputBoolean({ property: axisProperty, field: "onTop" }, {
                        type: "checkbox",
                        label: strings_1.strings.objects.onTop,
                        searchSection: [
                            strings_1.strings.objects.visibilityAndPosition,
                            options.mainCollapsePanelHeader,
                        ],
                    })
                    : null,
                manager.inputSelect({ property: axisProperty, field: "side" }, {
                    type: "dropdown",
                    showLabel: true,
                    label: strings_1.strings.objects.position,
                    options: ["default", "opposite"],
                    labels: [strings_1.strings.objects.default, strings_1.strings.objects.opposite],
                    searchSection: [
                        strings_1.strings.objects.visibilityAndPosition,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                options.isOffset
                    ? manager.inputNumber({
                        property: axisProperty,
                        field: ["offset"],
                    }, {
                        label: strings_1.strings.objects.axes.offSet,
                        showUpdown: true,
                        updownTick: 10,
                        searchSection: [
                            strings_1.strings.objects.visibilityAndPosition,
                            options.mainCollapsePanelHeader,
                        ],
                    })
                    : null,
            ]), manager.verticalGroup({
                header: strings_1.strings.objects.style,
            }, [
                manager.inputColor({
                    property: axisProperty,
                    field: ["style", "lineColor"],
                }, {
                    label: strings_1.strings.objects.axes.lineColor,
                    labelKey: "line-color-" + axisProperty,
                    allowNull: true,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputBoolean({ property: axisProperty, field: ["style", "showTicks"] }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.axes.showTickLine,
                    checkBoxStyles: {
                        root: {
                            marginTop: 5,
                        },
                    },
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputBoolean({ property: axisProperty, field: ["style", "showBaseline"] }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.axes.showBaseline,
                    checkBoxStyles: {
                        root: {
                            marginTop: 5,
                        },
                    },
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputColor({
                    property: axisProperty,
                    field: ["style", "tickColor"],
                }, {
                    label: strings_1.strings.objects.axes.tickColor,
                    labelKey: "tick-color-" + axisProperty,
                    allowNull: true,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputColor({
                    property: axisProperty,
                    field: ["style", "tickTextBackgroudColor"],
                }, {
                    label: strings_1.strings.objects.axes.tickTextBackgroudColor,
                    labelKey: "tick-text-background-color-" + axisProperty,
                    allowNull: true,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputNumber({
                    property: axisProperty,
                    field: ["style", "tickSize"],
                }, {
                    label: strings_1.strings.objects.axes.ticksize,
                    showUpdown: true,
                    updownTick: 1,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputFontFamily({
                    property: axisProperty,
                    field: ["style", "fontFamily"],
                }, {
                    label: strings_1.strings.objects.font,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputNumber({ property: axisProperty, field: ["style", "fontSize"] }, {
                    showUpdown: true,
                    updownStyle: "font",
                    updownTick: 2,
                    label: strings_1.strings.objects.fontSize,
                    minimum: 1,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                manager.inputBoolean({ property: axisProperty, field: ["style", "wordWrap"] }, {
                    type: "checkbox",
                    headerLabel: strings_1.strings.objects.text.textDisplaying,
                    label: strings_1.strings.objects.text.wrapText,
                    searchSection: [
                        strings_1.strings.objects.style,
                        options.mainCollapsePanelHeader,
                    ],
                }),
                vertical,
            ])),
        ];
    }
    else {
        return manager.verticalGroup({
            header: strings_1.strings.objects.visibilityAndPosition,
        }, [
            manager.inputBoolean({ property: axisProperty, field: "visible" }, {
                type: "checkbox",
                label: strings_1.strings.objects.visibleOn.visible,
                searchSection: [
                    strings_1.strings.objects.visibilityAndPosition,
                    options.mainCollapsePanelHeader,
                ],
            }),
        ]);
    }
}
exports.buildAxisAppearanceWidgets = buildAxisAppearanceWidgets;
function buildInteractivityGroup(axisProperty, manager, mainCollapsePanelHeader) {
    return manager.verticalGroup({
        header: strings_1.strings.objects.interactivity,
    }, [
        manager.inputBoolean({ property: axisProperty, field: "enableSelection" }, {
            type: "checkbox",
            label: strings_1.strings.objects.selection,
            searchSection: [
                strings_1.strings.objects.interactivity,
                mainCollapsePanelHeader,
            ],
        }),
    ]);
}
var defaultAxisWidgetsConfig = {
    showOffset: true,
    showScrolling: true,
    showOnTop: true,
};
function buildScrollingAxisWidgets(data, axisProperty, manager, axisName, onChange, mainCollapsePanelHeader) {
    return [
        manager.inputBoolean({
            property: axisProperty,
            field: "allowScrolling",
        }, {
            type: "checkbox",
            label: strings_1.strings.objects.dataAxis.allowScrolling,
            headerLabel: strings_1.strings.objects.dataAxis.scrolling,
            observerConfig: {
                isObserver: true,
                properties: {
                    property: axisProperty,
                    field: "windowSize",
                },
                value: 10,
            },
            searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
            onChange: onChange,
        }),
        data.allowScrolling
            ? manager.inputNumber({
                property: axisProperty,
                field: "windowSize",
            }, {
                maximum: 1000000,
                minimum: 1,
                label: strings_1.strings.objects.dataAxis.windowSize,
                searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
            })
            : null,
        data.allowScrolling
            ? manager.inputNumber({
                property: axisProperty,
                field: "barOffset",
            }, {
                maximum: 1000000,
                minimum: -1000000,
                label: strings_1.strings.objects.dataAxis.barOffset,
                searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
            })
            : null,
    ];
}
// eslint-disable-next-line
function buildAxisWidgets(data, axisProperty, manager, axisName, axisWidgetsConfig, onChange) {
    var _a;
    if (axisWidgetsConfig === void 0) { axisWidgetsConfig = defaultAxisWidgetsConfig; }
    var widgets = [];
    var dropzoneOptions = {
        dropzone: {
            type: "axis-data-binding",
            property: axisProperty,
            prompt: axisName + ": " + strings_1.strings.objects.dropData,
        },
        noLineHeight: true,
        ignoreSearch: true,
    };
    var axisType = "";
    if (data) {
        switch (data.type) {
            case types_1.AxisDataBindingType.Categorical:
                axisType = strings_1.strings.objects.axes.categoricalSuffix;
                break;
            case types_1.AxisDataBindingType.Numerical:
                axisType = strings_1.strings.objects.axes.numericalSuffix;
                break;
        }
    }
    var mainCollapsePanelHeader = axisName + axisType;
    var makeAppearance = function () {
        var _a, _b;
        return buildAxisAppearanceWidgets(axisProperty, manager, {
            isVisible: data.visible,
            wordWrap: (_b = (_a = data.style) === null || _a === void 0 ? void 0 : _a.wordWrap) !== null && _b !== void 0 ? _b : false,
            isOffset: axisWidgetsConfig.showOffset,
            isOnTop: axisWidgetsConfig.showOnTop,
            mainCollapsePanelHeader: mainCollapsePanelHeader,
        });
    };
    if (data != null) {
        var isDateExpression = data.expression
            ? (_a = data.expression) === null || _a === void 0 ? void 0 : _a.includes("date.") : false;
        var scrollingWidgets = axisWidgetsConfig.showScrolling
            ? buildScrollingAxisWidgets(data, axisProperty, manager, axisName, onChange, mainCollapsePanelHeader)
            : [];
        var tickFormatAndTickDataFields = getTickDataAndTickFormatFields(data, axisProperty, manager, mainCollapsePanelHeader);
        var categoricalTickFormatAndTickDataFields = data.valueType === "date" ? tickFormatAndTickDataFields : [];
        switch (data.type) {
            case "numerical":
                {
                    widgets.push(manager.verticalGroup({
                        header: strings_1.strings.objects.general,
                    }, __spread([
                        manager.searchWrapper({
                            searchPattern: [
                                strings_1.strings.objects.axes.data,
                                strings_1.strings.objects.general,
                                mainCollapsePanelHeader,
                            ],
                        }, [
                            manager.label(strings_1.strings.objects.axes.data, {
                                ignoreSearch: true,
                            }),
                            manager.styledHorizontal({
                                alignItems: "start",
                            }, [1, 0], manager.sectionHeader(null, manager.inputExpression({
                                property: axisProperty,
                                field: "expression",
                            }, {
                                ignoreSearch: true,
                            }), dropzoneOptions), manager.clearButton({ property: axisProperty }, null, true, {
                                marginTop: "1px",
                            })),
                        ]),
                        data.valueType == "date"
                            ? manager.searchWrapper({
                                searchPattern: [
                                    strings_1.strings.objects.dataAxis.range,
                                    strings_1.strings.objects.general,
                                    strings_1.strings.objects.dataAxis.start,
                                    strings_1.strings.objects.dataAxis.end,
                                    mainCollapsePanelHeader,
                                ],
                            }, [
                                manager.label(strings_1.strings.objects.dataAxis.range, {
                                    ignoreSearch: true,
                                }),
                                manager.searchWrapper({
                                    searchPattern: [
                                        strings_1.strings.objects.dataAxis.range,
                                        strings_1.strings.objects.general,
                                        strings_1.strings.objects.dataAxis.start,
                                        mainCollapsePanelHeader,
                                    ],
                                }, [
                                    data.allowScrolling
                                        ? manager.inputDate({
                                            property: axisProperty,
                                            field: "dataDomainMin",
                                        }, {
                                            label: strings_1.strings.objects.dataAxis.start,
                                            ignoreSearch: true,
                                        })
                                        : manager.inputDate({
                                            property: axisProperty,
                                            field: "domainMin",
                                        }, {
                                            label: strings_1.strings.objects.dataAxis.start,
                                            ignoreSearch: true,
                                        }),
                                ]),
                                manager.searchWrapper({
                                    searchPattern: [
                                        strings_1.strings.objects.dataAxis.range,
                                        strings_1.strings.objects.general,
                                        strings_1.strings.objects.dataAxis.end,
                                        mainCollapsePanelHeader,
                                    ],
                                }, [
                                    data.allowScrolling
                                        ? manager.inputDate({
                                            property: axisProperty,
                                            field: "dataDomainMax",
                                        }, {
                                            label: strings_1.strings.objects.dataAxis.end,
                                            ignoreSearch: true,
                                        })
                                        : manager.inputDate({
                                            property: axisProperty,
                                            field: "domainMax",
                                        }, {
                                            label: strings_1.strings.objects.dataAxis.end,
                                            ignoreSearch: true,
                                        }),
                                ]),
                            ])
                            : null,
                        data.valueType !== "date"
                            ? manager.searchWrapper({
                                searchPattern: [
                                    strings_1.strings.objects.dataAxis.range,
                                    strings_1.strings.objects.general,
                                    strings_1.strings.objects.axes.from,
                                    strings_1.strings.objects.axes.to,
                                    mainCollapsePanelHeader,
                                ],
                            }, [
                                manager.label(strings_1.strings.objects.dataAxis.range, {
                                    ignoreSearch: true,
                                }),
                                manager.searchWrapper({
                                    searchPattern: [
                                        strings_1.strings.objects.axes.from,
                                        strings_1.strings.objects.dataAxis.range,
                                        strings_1.strings.objects.general,
                                        mainCollapsePanelHeader,
                                    ],
                                }, [
                                    data.allowScrolling
                                        ? manager.inputNumber({
                                            property: axisProperty,
                                            field: "dataDomainMin",
                                        }, {
                                            label: strings_1.strings.objects.axes.from,
                                            observerConfig: {
                                                isObserver: true,
                                                properties: {
                                                    property: axisProperty,
                                                    field: "autoDomainMin",
                                                },
                                                value: false,
                                            },
                                            ignoreSearch: true,
                                        })
                                        : manager.inputNumber({
                                            property: axisProperty,
                                            field: "domainMin",
                                        }, {
                                            label: strings_1.strings.objects.axes.from,
                                            observerConfig: {
                                                isObserver: true,
                                                properties: {
                                                    property: axisProperty,
                                                    field: "autoDomainMin",
                                                },
                                                value: false,
                                            },
                                            ignoreSearch: true,
                                        }),
                                ]),
                                manager.searchWrapper({
                                    searchPattern: [
                                        strings_1.strings.objects.axes.to,
                                        strings_1.strings.objects.dataAxis.range,
                                        strings_1.strings.objects.general,
                                        mainCollapsePanelHeader,
                                    ],
                                }, [
                                    data.allowScrolling
                                        ? manager.inputNumber({
                                            property: axisProperty,
                                            field: "dataDomainMax",
                                        }, {
                                            label: strings_1.strings.objects.axes.to,
                                            observerConfig: {
                                                isObserver: true,
                                                properties: {
                                                    property: axisProperty,
                                                    field: "autoDomainMax",
                                                },
                                                value: false,
                                            },
                                            ignoreSearch: true,
                                        })
                                        : manager.inputNumber({
                                            property: axisProperty,
                                            field: "domainMax",
                                        }, {
                                            label: strings_1.strings.objects.axes.to,
                                            observerConfig: {
                                                isObserver: true,
                                                properties: {
                                                    property: axisProperty,
                                                    field: "autoDomainMax",
                                                },
                                                value: false,
                                            },
                                            ignoreSearch: true,
                                        }),
                                ]),
                            ])
                            : null,
                        data.numericalMode != "temporal"
                            ? manager.inputSelect({ property: axisProperty, field: "numericalMode" }, {
                                options: ["linear", "logarithmic"],
                                labels: [
                                    strings_1.strings.scale.linear,
                                    strings_1.strings.scale.logarithmic,
                                ],
                                showLabel: true,
                                type: "dropdown",
                                label: strings_1.strings.objects.scales.mode,
                                searchSection: [
                                    strings_1.strings.objects.general,
                                    mainCollapsePanelHeader,
                                ],
                            })
                            : null
                    ], tickFormatAndTickDataFields, scrollingWidgets)));
                    widgets.push(makeAppearance());
                }
                break;
            case "categorical":
                {
                    widgets.push(manager.verticalGroup({
                        header: strings_1.strings.objects.general,
                        searchSection: mainCollapsePanelHeader,
                    }, __spread([
                        manager.searchWrapper({
                            searchPattern: [
                                strings_1.strings.objects.axes.data,
                                strings_1.strings.objects.general,
                                mainCollapsePanelHeader,
                            ],
                        }, [
                            manager.label(strings_1.strings.objects.axes.data, {
                                addMargins: false,
                                ignoreSearch: true,
                            }),
                            manager.styledHorizontal({
                                alignItems: "start",
                            }, [1, 0], manager.sectionHeader(null, manager.inputExpression({
                                property: axisProperty,
                                field: "expression",
                            }, {
                                ignoreSearch: true,
                            }), dropzoneOptions), isDateExpression
                                ? manager.reorderWidget({ property: axisProperty, field: "categories" }, { allowReset: true })
                                : null, manager.clearButton({ property: axisProperty }, null, true, {
                                marginTop: "1px",
                            })),
                        ]),
                        !isDateExpression
                            ? getOrderByAnotherColumnWidgets(data, axisProperty, manager, mainCollapsePanelHeader)
                            : null,
                        manager.inputNumber({ property: axisProperty, field: "gapRatio" }, {
                            minimum: 0,
                            maximum: 1,
                            percentage: true,
                            showSlider: true,
                            label: strings_1.strings.objects.axes.gap,
                            searchSection: [
                                strings_1.strings.objects.general,
                                mainCollapsePanelHeader,
                            ],
                        })
                    ], categoricalTickFormatAndTickDataFields, scrollingWidgets)));
                    widgets.push(buildInteractivityGroup(axisProperty, manager, mainCollapsePanelHeader));
                    widgets.push(makeAppearance());
                }
                break;
            case "default":
                {
                    widgets.push(manager.styledVertical({ marginLeft: 19, marginBottom: 5 }, manager.sectionHeader(axisName + strings_1.strings.objects.axes.stackingSuffix, manager.clearButton({ property: axisProperty }, null, true), __assign(__assign({}, dropzoneOptions), { noLineHeight: false })), manager.inputNumber({ property: axisProperty, field: "gapRatio" }, {
                        minimum: 0,
                        maximum: 1,
                        percentage: true,
                        showSlider: true,
                        label: strings_1.strings.objects.axes.gap,
                        searchSection: mainCollapsePanelHeader,
                    })));
                }
                break;
        }
        widgets.push(manager.verticalGroup({
            header: axisName + strings_1.strings.objects.dataAxis.exportProperties,
        }, [
            manager.inputBoolean({
                property: axisProperty,
                field: "autoDomainMin",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoMin,
                searchSection: [
                    axisName + strings_1.strings.objects.dataAxis.exportProperties,
                    mainCollapsePanelHeader,
                ],
            }),
            manager.inputBoolean({
                property: axisProperty,
                field: "autoDomainMax",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoMax,
                searchSection: [
                    axisName + strings_1.strings.objects.dataAxis.exportProperties,
                    mainCollapsePanelHeader,
                ],
            }),
        ]));
    }
    else {
        widgets.push(
        // manager.sectionHeader(
        //   axisName + ": " + strings.core.none,
        //   null,
        //   dropzoneOptions
        // )
        manager.verticalGroup({
            header: strings_1.strings.objects.general,
        }, [
            manager.searchWrapper({
                searchPattern: [
                    strings_1.strings.objects.general,
                    strings_1.strings.objects.axes.data,
                    mainCollapsePanelHeader,
                ],
            }, [
                manager.label(strings_1.strings.objects.axes.data, {
                    addMargins: false,
                    ignoreSearch: true,
                }),
                manager.horizontal([1, 0, 0, 0], manager.sectionHeader(null, manager.inputText({
                    property: null,
                }, {
                    disabled: true,
                    value: strings_1.strings.core.none,
                    ignoreSearch: true,
                }), dropzoneOptions)),
            ]),
        ]));
    }
    return widgets;
}
exports.buildAxisWidgets = buildAxisWidgets;
function buildAxisInference(plotSegment, property) {
    var axis = (plotSegment.properties[property]);
    return {
        objectID: plotSegment._id,
        dataSource: {
            table: plotSegment.table,
            groupBy: plotSegment.groupBy,
        },
        axis: {
            expression: axis.expression,
            type: axis.type,
            style: axis.style,
            order: axis.order,
            orderMode: axis.orderMode,
            rawExpression: axis.rawExpression,
            property: property,
            defineCategories: true,
        },
    };
}
exports.buildAxisInference = buildAxisInference;
function buildAxisProperties(plotSegment, property) {
    var axisObject = plotSegment.properties[property];
    var style = axisObject.style;
    if (!style) {
        return [];
    }
    return [
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "style",
                    subfield: "tickSize",
                },
            },
            type: index_1.Specification.AttributeType.Number,
            default: style.tickSize,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "style",
                    subfield: "fontSize",
                },
            },
            type: index_1.Specification.AttributeType.Number,
            default: style.fontSize,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "style",
                    subfield: "fontFamily",
                },
            },
            type: index_1.Specification.AttributeType.FontFamily,
            default: style.fontFamily,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "style",
                    subfield: "lineColor",
                },
            },
            type: index_1.Specification.AttributeType.Color,
            default: common_1.rgbToHex(style.lineColor),
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "style",
                    subfield: "tickColor",
                },
            },
            type: index_1.Specification.AttributeType.Color,
            default: common_1.rgbToHex(style.tickColor),
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "tickFormat",
                },
            },
            type: index_1.Specification.AttributeType.Text,
            default: null,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "tickDataExpression",
                },
            },
            type: index_1.Specification.AttributeType.Text,
            default: null,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "offset",
                },
            },
            type: index_1.Specification.AttributeType.Number,
            default: 0,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "numberOfTicks",
                },
            },
            type: index_1.Specification.AttributeType.Number,
            default: 10,
        },
        {
            objectID: plotSegment._id,
            target: {
                property: {
                    property: property,
                    field: "autoNumberOfTicks",
                },
            },
            type: index_1.Specification.AttributeType.Boolean,
            default: true,
        },
    ];
}
exports.buildAxisProperties = buildAxisProperties;
function getTable(dataflow, name) {
    return dataflow.getTable(name);
}
function applySelectionFilter(data, tableName, index, dataflow) {
    var _a;
    var filteredIndices = [];
    var table = getTable(dataflow, tableName);
    if (data.type === types_1.AxisDataBindingType.Default ||
        data.type === types_1.AxisDataBindingType.Numerical) {
        return table.rows.map(function (row, id) { return id; });
    }
    var parsed = (_a = Expression.parse(data === null || data === void 0 ? void 0 : data.expression)) === null || _a === void 0 ? void 0 : _a.args[0];
    if (data.type === types_1.AxisDataBindingType.Categorical) {
        for (var i = 0; i < table.rows.length; i++) {
            var rowContext = table.getRowContext(i);
            if (data.categories[index] == parsed.getStringValue(rowContext)) {
                filteredIndices.push(i);
            }
        }
    }
    return filteredIndices;
}
var orderChanged = false;
function getOrderByAnotherColumnWidgets(data, axisProperty, manager, mainCollapsePanelHeader) {
    var _a, _b;
    var widgets = [];
    var tableColumns = utils_1.getTableColumns(manager);
    var columnsDisplayNames = tableColumns
        .filter(function (item) { var _a; return !((_a = item.metadata) === null || _a === void 0 ? void 0 : _a.isRaw); })
        .map(function (column) { return column.displayName; });
    var columnsNames = tableColumns
        .filter(function (item) { var _a; return !((_a = item.metadata) === null || _a === void 0 ? void 0 : _a.isRaw); })
        .map(function (column) { return utils_1.transformOrderByExpression(column.name); });
    var derivedColumns = [];
    var derivedColumnsNames = [];
    for (var i = 0; i < tableColumns.length; i++) {
        if (!((_a = tableColumns[i].metadata) === null || _a === void 0 ? void 0 : _a.isRaw)) {
            derivedColumns.push(common_3.type2DerivedColumns[tableColumns[i].type]);
            derivedColumnsNames.push(tableColumns[i].name);
        }
    }
    var removeIdx = [];
    //remove empty
    for (var i = 0; i < derivedColumns.length; i++) {
        if (!Array.isArray(derivedColumns[i])) {
            removeIdx.push(i);
        }
    }
    var filteredDerivedColumns = derivedColumns.filter(function (item, idx) { return !removeIdx.includes(idx); });
    var filteredDerivedColumnsNames = derivedColumnsNames.filter(function (item, idx) { return !removeIdx.includes(idx); });
    //Date columns
    for (var i = 0; i < filteredDerivedColumns.length; i++) {
        var currentDerivedColumn = filteredDerivedColumns[i];
        for (var j = 0; j < (currentDerivedColumn === null || currentDerivedColumn === void 0 ? void 0 : currentDerivedColumn.length); j++) {
            var currentColumn = currentDerivedColumn[j];
            var currentColumnName = filteredDerivedColumnsNames[i];
            columnsDisplayNames.push((_b = currentColumn.displayName) !== null && _b !== void 0 ? _b : currentColumn.name);
            columnsNames.push(currentColumn.function + ("(" + currentColumnName + ")"));
        }
    }
    var table = manager.store.getTables()[0].name;
    var store = manager.store;
    var df = new index_1.Prototypes.Dataflow.DataflowManager(store.dataset);
    var getExpressionVector = function (expression, table, groupBy) {
        var newExpression = utils_1.transformOrderByExpression(expression);
        groupBy.expression = utils_1.transformOrderByExpression(groupBy.expression);
        var expr = Expression.parse(newExpression);
        var tableContext = df.getTable(table);
        var indices = groupBy
            ? new group_by_1.CompiledGroupBy(groupBy, df.cache).groupBy(tableContext)
            : common_1.makeRange(0, tableContext.rows.length).map(function (x) { return [x]; });
        return indices.map(function (is) {
            return expr.getValue(tableContext.getGroupedContext(is));
        });
    };
    var parsed = Expression.parse(data.expression);
    var groupByExpression = null;
    if (parsed instanceof Expression.FunctionCall) {
        groupByExpression = parsed.args[0].toString();
        groupByExpression = groupByExpression === null || groupByExpression === void 0 ? void 0 : groupByExpression.split("`").join("");
        //need to provide date.year() etc.
        groupByExpression = utils_1.parseDerivedColumnsExpression(groupByExpression);
    }
    var isOriginalColumn = groupByExpression === data.orderByExpression;
    var vectorData = getExpressionVector(data.orderByExpression, table, {
        expression: groupByExpression,
    });
    var items = vectorData.map(function (item) { return __spread(new Set(item)); });
    var items_idx = items.map(function (item, idx) { return [item, idx]; });
    var axisData = getExpressionVector(data.expression, table, {
        expression: groupByExpression,
    }).map(function (item, idx) { return [item, idx]; });
    var isNumberValueType = Array.isArray(items_idx[0][0])
        ? typeof items_idx[0][0][0] === "number"
        : typeof items_idx[0][0] === "number";
    var onResetAxisCategories = utils_1.transformOnResetCategories(items_idx);
    var sortedCategories = utils_1.getSortedCategories(items_idx);
    var onConfirm = function (items) {
        try {
            utils_1.getOnConfirmFunction(axisData, items, items_idx, data);
        }
        catch (e) {
            console.log(e);
        }
    };
    var onChange = function () {
        var vectorData = getExpressionVector(data.orderByExpression, table, {
            expression: groupByExpression,
        });
        var items = vectorData.map(function (item) { return __spread(new Set(item)); });
        var newData = utils_1.updateWidgetCategoriesByExpression(items);
        data.orderByCategories = __spread(new Set(newData));
    };
    // eslint-disable-next-line no-constant-condition
    if (orderChanged) {
        columnsDisplayNames = columnsDisplayNames.map(function (name) {
            if (isOriginalColumn && name == data.orderByExpression) {
                return "Custom";
            }
            else {
                return name;
            }
        });
    }
    widgets.push(manager.searchWrapper({
        searchPattern: [
            strings_1.strings.objects.axes.orderBy,
            strings_1.strings.objects.general,
            mainCollapsePanelHeader,
        ],
    }, [
        manager.label(strings_1.strings.objects.axes.orderBy, {
            addMargins: false,
            ignoreSearch: true,
        }),
        manager.horizontal([1, 0], manager.inputSelect({ property: axisProperty, field: "orderByExpression" }, {
            type: "dropdown",
            showLabel: true,
            labels: columnsDisplayNames,
            options: columnsNames,
            onChange: onChange,
            ignoreSearch: true,
        }), manager.reorderByAnotherColumnWidget({ property: axisProperty, field: "orderByCategories" }, {
            allowReset: isNumberValueType == false,
            onConfirmClick: onConfirm,
            onResetCategories: onResetAxisCategories,
            sortedCategories: sortedCategories,
            allowDragItems: isNumberValueType == false,
            onReorderHandler: isOriginalColumn
                ? function () {
                    orderChanged = true;
                }
                : undefined,
            onButtonHandler: isOriginalColumn
                ? function () {
                    orderChanged = false;
                }
                : undefined,
        })),
    ]));
    return widgets;
}
function getTickDataAndTickFormatFields(data, axisProperty, manager, mainCollapsePanelHeader) {
    var showInputFormat = utils_1.shouldShowTickFormatForTickExpression(data, manager);
    var widgets = [];
    widgets.push(
    // manager.label(strings.objects.axes.tickData),
    manager.styledHorizontal({
        alignItems: "start",
    }, [1, 0], manager.inputExpression({
        property: axisProperty,
        field: "tickDataExpression",
    }, {
        allowNull: true,
        placeholder: strings_1.strings.core.default,
        dropzone: {
            type: "tick-data-binding",
            prompt: strings_1.strings.objects.dropTickData,
        },
        noLineHeight: true,
        label: strings_1.strings.objects.axes.tickData,
        searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
    })));
    if (showInputFormat) {
        widgets.push(manager.inputFormat({
            property: axisProperty,
            field: "tickFormat",
        }, {
            blank: strings_1.strings.core.auto,
            label: strings_1.strings.objects.axes.tickFormat,
            isDateField: data.numericalMode === types_1.NumericalMode.Temporal ||
                data.valueType === specification_1.DataType.Date,
            allowNull: true,
            searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
        }));
    }
    if (!data.tickDataExpression) {
        widgets.push(manager.inputBoolean({
            property: axisProperty,
            field: "autoNumberOfTicks",
        }, {
            type: "checkbox",
            label: strings_1.strings.objects.axes.autoNumberOfTicks,
            styles: {
                marginTop: "0.5rem",
            },
            searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
        }));
        if (!data.autoNumberOfTicks) {
            widgets.push(manager.inputNumber({
                property: axisProperty,
                field: "numberOfTicks",
            }, {
                label: strings_1.strings.objects.axes.numberOfTicks,
                showUpdown: true,
                updownTick: 1,
                minimum: 2,
                searchSection: [strings_1.strings.objects.general, mainCollapsePanelHeader],
            }));
        }
    }
    return widgets;
}
//# sourceMappingURL=axis.js.map