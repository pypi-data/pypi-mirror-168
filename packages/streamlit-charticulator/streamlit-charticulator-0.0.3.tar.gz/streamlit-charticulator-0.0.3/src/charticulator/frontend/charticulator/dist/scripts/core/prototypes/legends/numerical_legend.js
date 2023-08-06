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
exports.NumericalNumberLegendClass = exports.NumericalNumberLegendAttributeNames = void 0;
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
var axis_1 = require("../plot_segments/axis");
var plot_segments_1 = require("../plot_segments");
var NumericalNumberLegendAttributeNames;
(function (NumericalNumberLegendAttributeNames) {
    NumericalNumberLegendAttributeNames["x1"] = "x1";
    NumericalNumberLegendAttributeNames["y1"] = "y1";
    NumericalNumberLegendAttributeNames["x2"] = "x2";
    NumericalNumberLegendAttributeNames["y2"] = "y2";
    NumericalNumberLegendAttributeNames["cx"] = "cx";
    NumericalNumberLegendAttributeNames["cy"] = "cy";
    NumericalNumberLegendAttributeNames["radius"] = "radius";
    NumericalNumberLegendAttributeNames["startAngle"] = "startAngle";
    NumericalNumberLegendAttributeNames["endAngle"] = "endAngle";
})(NumericalNumberLegendAttributeNames = exports.NumericalNumberLegendAttributeNames || (exports.NumericalNumberLegendAttributeNames = {}));
var PRECISION = 1e-3;
var NumericalNumberLegendClass = /** @class */ (function (_super) {
    __extends(NumericalNumberLegendClass, _super);
    function NumericalNumberLegendClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [
            NumericalNumberLegendAttributeNames.x1,
            NumericalNumberLegendAttributeNames.y1,
            NumericalNumberLegendAttributeNames.x2,
            NumericalNumberLegendAttributeNames.y2,
            NumericalNumberLegendAttributeNames.cx,
            NumericalNumberLegendAttributeNames.cy,
            NumericalNumberLegendAttributeNames.radius,
            NumericalNumberLegendAttributeNames.startAngle,
            NumericalNumberLegendAttributeNames.endAngle,
        ];
        _this.attributes = {
            x1: {
                name: NumericalNumberLegendAttributeNames.x1,
                type: Specification.AttributeType.Number,
            },
            y1: {
                name: NumericalNumberLegendAttributeNames.y1,
                type: Specification.AttributeType.Number,
            },
            x2: {
                name: NumericalNumberLegendAttributeNames.x2,
                type: Specification.AttributeType.Number,
            },
            y2: {
                name: NumericalNumberLegendAttributeNames.y2,
                type: Specification.AttributeType.Number,
            },
            cx: {
                name: NumericalNumberLegendAttributeNames.cx,
                type: Specification.AttributeType.Number,
            },
            cy: {
                name: NumericalNumberLegendAttributeNames.cx,
                type: Specification.AttributeType.Number,
            },
            radius: {
                name: NumericalNumberLegendAttributeNames.radius,
                type: Specification.AttributeType.Number,
            },
            startAngle: {
                name: NumericalNumberLegendAttributeNames.startAngle,
                type: Specification.AttributeType.Number,
            },
            endAngle: {
                name: NumericalNumberLegendAttributeNames.endAngle,
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    NumericalNumberLegendClass.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x1 = 0;
        attrs.y1 = 0;
        attrs.x2 = 0;
        attrs.y2 = 0;
        attrs.cx = 0;
        attrs.cy = 0;
        attrs.radius = 0;
        attrs.startAngle = 0;
        attrs.endAngle = 0;
    };
    NumericalNumberLegendClass.prototype.getScale = function () {
        var scale = this.object.properties.scale;
        var scaleIndex = common_1.indexOf(this.parent.object.scales, function (x) { return x._id == scale; });
        if (scaleIndex >= 0) {
            return [
                this.parent.object.scales[scaleIndex],
                this.parent.state.scales[scaleIndex],
            ];
        }
        else {
            return null;
        }
    };
    NumericalNumberLegendClass.prototype.getBoundingBox = function () {
        if (this.object.properties.polarAngularMode) {
            var _a = this.state.attributes, cx = _a.cx, cy = _a.cy, radius = _a.radius;
            var bbox = {
                type: "circle",
                cx: cx,
                cy: cy,
                radius: radius,
            };
            return bbox;
        }
        else {
            var _b = this.state.attributes, x1 = _b.x1, y1 = _b.y1, x2 = _b.x2, y2 = _b.y2;
            var bbox = {
                type: "line",
                x1: x1,
                y1: y1,
                x2: x2,
                y2: y2,
            };
            return bbox;
        }
    };
    NumericalNumberLegendClass.prototype.getHandles = function () {
        var attributes = this.state.attributes;
        if (this.object.properties.polarAngularMode) {
            var cx = attributes.cx, cy = attributes.cy;
            // TODO is there a circle handle?????
            var points = [
                {
                    type: "point",
                    x: cx,
                    y: cy,
                    actions: [
                        {
                            type: "attribute",
                            source: "x",
                            attribute: NumericalNumberLegendAttributeNames.cx,
                        },
                        {
                            type: "attribute",
                            source: "y",
                            attribute: NumericalNumberLegendAttributeNames.cy,
                        },
                    ],
                    options: {
                        snapToClosestPoint: true,
                    },
                },
            ];
            return points;
        }
        else {
            var x1 = attributes.x1, y1 = attributes.y1, x2 = attributes.x2, y2 = attributes.y2;
            var points = [
                {
                    type: "point",
                    x: x1,
                    y: y1,
                    actions: [
                        {
                            type: "attribute",
                            source: "x",
                            attribute: NumericalNumberLegendAttributeNames.x1,
                        },
                        {
                            type: "attribute",
                            source: "y",
                            attribute: NumericalNumberLegendAttributeNames.y1,
                        },
                    ],
                    options: {
                        snapToClosestPoint: true,
                    },
                },
                {
                    type: "point",
                    x: x2,
                    y: y2,
                    actions: [
                        {
                            type: "attribute",
                            source: "x",
                            attribute: NumericalNumberLegendAttributeNames.x2,
                        },
                        {
                            type: "attribute",
                            source: "y",
                            attribute: NumericalNumberLegendAttributeNames.y2,
                        },
                    ],
                    options: {
                        snapToClosestPoint: true,
                    },
                },
            ];
            return points;
        }
    };
    NumericalNumberLegendClass.prototype.getGraphics = function () {
        var scale = this.getScale();
        if (!scale) {
            return null;
        }
        if (!this.object.properties.axis.visible) {
            return null;
        }
        var rangeMin = scale[1].attributes.rangeMin;
        var rangeMax = scale[1].attributes.rangeMax;
        var domainMin = scale[0].properties.domainMin;
        var domainMax = scale[0].properties.domainMax;
        if (this.object.properties.polarAngularMode) {
            return this.getPolarAxisGraphics(rangeMin, rangeMax, domainMin, domainMax);
        }
        else {
            return Graphics.makeGroup([
                this.getLineAxisGraphics(rangeMin, rangeMax, domainMin, domainMax),
                this.getGridLineGraphics(rangeMin, rangeMax, domainMin, domainMax),
            ]);
        }
    };
    NumericalNumberLegendClass.prototype.getPolarAxisGraphics = function (rangeMin, rangeMax, domainMin, domainMax) {
        var renderer = new axis_1.AxisRenderer();
        renderer.oppositeSide = this.object.properties.axis.side === "opposite";
        var _a = this.state.attributes, startAngle = _a.startAngle, endAngle = _a.endAngle;
        var length = endAngle - startAngle;
        var props = this.object.properties;
        var scaling = (rangeMax - rangeMin) / (domainMax - domainMin);
        renderer.setLinearScale(domainMin, domainMin + (length - rangeMin / 360) / scaling, startAngle, endAngle, props.axis.tickFormat);
        renderer.setStyle(this.object.properties.axis.style);
        return renderer.renderPolar(this.state.attributes.cx, this.state.attributes.cy, this.state.attributes.radius, renderer.oppositeSide ? -1 : 1);
    };
    NumericalNumberLegendClass.prototype.getLineAxisGraphics = function (rangeMin, rangeMax, domainMin, domainMax) {
        var dx = this.state.attributes.x2 - this.state.attributes.x1;
        var dy = this.state.attributes.y2 - this.state.attributes.y1;
        var length = Math.sqrt(dx * dx + dy * dy);
        var renderer = new axis_1.AxisRenderer();
        renderer.oppositeSide = this.object.properties.axis.side === "opposite";
        var props = this.object.properties;
        // Extend/shrink range, and update the domain accordingly. Keep the scaling factor.
        var scaling = (rangeMax - rangeMin) / (domainMax - domainMin);
        renderer.setLinearScale(domainMin, domainMin + (length - rangeMin) / scaling, rangeMin, length, props.axis.tickFormat);
        renderer.setStyle(this.object.properties.axis.style);
        return renderer.renderLine(this.state.attributes.x1, this.state.attributes.y1, (Math.atan2(dy, dx) / Math.PI) * 180, -1);
    };
    NumericalNumberLegendClass.prototype.getGridLineGraphics = function (rangeMin, rangeMax, domainMin, domainMax) {
        var _a, _b, _c, _d;
        var legendId = this.object._id;
        var chartConstrains = this.parent.object.constraints;
        if (chartConstrains.length > 0) {
            //x1, y1, x2, y2
            //check if 4 constrain for legend
            var amountLegendConstrain = chartConstrains.filter(function (elem) { var _a; return ((_a = elem.attributes) === null || _a === void 0 ? void 0 : _a.element) === legendId; });
            if (amountLegendConstrain.length === 4) {
                var targetConstrain = chartConstrains === null || chartConstrains === void 0 ? void 0 : chartConstrains.find(function (constant) { var _a; return ((_a = constant === null || constant === void 0 ? void 0 : constant.attributes) === null || _a === void 0 ? void 0 : _a.element) === legendId; });
                var targetId_1 = (_a = targetConstrain === null || targetConstrain === void 0 ? void 0 : targetConstrain.attributes) === null || _a === void 0 ? void 0 : _a.targetElement;
                var plotSIdx = this.parent.object.elements.findIndex(function (element) { return element._id === targetId_1; });
                var plotSAttributes = (_b = this.parent.state.elements[plotSIdx]) === null || _b === void 0 ? void 0 : _b.attributes;
                var x1 = this.state.attributes.x1;
                var x2 = this.state.attributes.x2;
                var y1 = this.state.attributes.y1;
                var y2 = this.state.attributes.y2;
                var isXEquals = Math.abs(x2 - x1) < PRECISION;
                var isYEquals = Math.abs(y2 - y1) < PRECISION;
                if (!isXEquals && !isYEquals) {
                    return null;
                }
                var angle = isYEquals ? 0 : 90;
                var dx = (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.x2) - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.x1);
                var dy = (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.y2) - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.y1);
                var length_1 = isYEquals ? dx : dy;
                var renderer = new axis_1.AxisRenderer();
                var props = this.object.properties;
                var scaling = (rangeMax - rangeMin) / (domainMax - domainMin);
                renderer.setLinearScale(domainMin, domainMin + (length_1 - rangeMin) / scaling, rangeMin, length_1, props.axis.tickFormat);
                renderer.setStyle(__assign(__assign({}, axis_1.defaultAxisStyle), (_d = (_c = this.object.properties) === null || _c === void 0 ? void 0 : _c.axis) === null || _d === void 0 ? void 0 : _d.style));
                //gridline should be in PlotSegment
                var side = 1;
                if (isXEquals) {
                    if (y1 > y2) {
                        if (Math.abs(x1 - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.x1)) < PRECISION) {
                            side = -1;
                        }
                        else {
                            side = 1;
                        }
                    }
                    else {
                        if (Math.abs(x1 - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.x1)) < PRECISION) {
                            side = -1;
                        }
                        else {
                            side = 1;
                        }
                    }
                }
                if (isYEquals) {
                    if (x1 > x2) {
                        if (Math.abs(y1 - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.y1)) < PRECISION) {
                            side = 1;
                        }
                        else {
                            side = -1;
                        }
                    }
                    else {
                        if (Math.abs(y1 - (plotSAttributes === null || plotSAttributes === void 0 ? void 0 : plotSAttributes.y1)) < PRECISION) {
                            side = 1;
                        }
                        else {
                            side = -1;
                        }
                    }
                }
                return renderer.renderGridLine(x1 > x2 ? x2 : x1, y1 > y2 ? y2 : y1, angle, side, isYEquals ? dy : dx);
            }
        }
        return null;
    };
    NumericalNumberLegendClass.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        return __spread([
            manager.sectionHeader(strings_1.strings.objects.axis),
            axis_1.buildAxisAppearanceWidgets("axis", manager, {
                isVisible: props.axis.visible,
                wordWrap: props.axis.style.wordWrap,
                isOffset: false,
                isOnTop: false,
            })
        ], plot_segments_1.PlotSegmentClass.getGridLineAttributePanelWidgets(manager, "axis"));
    };
    NumericalNumberLegendClass.classID = "legend.numerical-number";
    NumericalNumberLegendClass.type = "legend";
    NumericalNumberLegendClass.metadata = {
        displayName: "Legend",
        iconPath: "CharticulatorLegend",
    };
    NumericalNumberLegendClass.defaultProperties = {
        visible: true,
        axis: {
            side: "default",
            visible: true,
            style: common_1.deepClone(axis_1.defaultAxisStyle),
            tickFormat: "",
        },
    };
    return NumericalNumberLegendClass;
}(chart_element_1.ChartElementClass));
exports.NumericalNumberLegendClass = NumericalNumberLegendClass;
//# sourceMappingURL=numerical_legend.js.map