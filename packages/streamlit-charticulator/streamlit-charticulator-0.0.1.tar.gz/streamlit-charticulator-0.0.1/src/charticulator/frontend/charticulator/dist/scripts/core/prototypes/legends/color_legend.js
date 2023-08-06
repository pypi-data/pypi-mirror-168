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
exports.NumericalColorLegendClass = void 0;
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var axis_1 = require("../plot_segments/axis");
var legend_1 = require("./legend");
var strings_1 = require("../../../strings");
var types_1 = require("./types");
var NumericalColorLegendClass = /** @class */ (function (_super) {
    __extends(NumericalColorLegendClass, _super);
    function NumericalColorLegendClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.gradientWidth = 12;
        return _this;
    }
    NumericalColorLegendClass.prototype.getLineHeight = function () {
        return this.object.properties.fontSize + 25 + this.gradientWidth;
    };
    NumericalColorLegendClass.prototype.getLegendSize = function () {
        var props = this.object.properties;
        var length = props.length
            ? +props.length
            : NumericalColorLegendClass.defaultLegendLength;
        if (this.isHorizontalOrientation()) {
            return [length, this.getLineHeight()];
        }
        return [this.getLineHeight(), length];
    };
    NumericalColorLegendClass.prototype.isHorizontalOrientation = function () {
        var props = this.object.properties;
        return props.orientation === types_1.OrientationType.HORIZONTAL;
    };
    NumericalColorLegendClass.prototype.getGraphics = function () {
        var height = this.isHorizontalOrientation()
            ? this.getLegendSize()[0]
            : this.getLegendSize()[1];
        var marginLeft = 5;
        var gradientWidth = 12;
        var axisMargin = 2;
        var horizontalShift = this.getLegendSize()[1] - gradientWidth;
        var scale = this.getScale();
        if (!scale) {
            return null;
        }
        var range = scale[0].properties.range;
        var domainMin = scale[0].properties.domainMin;
        var domainMax = scale[0].properties.domainMax;
        var axisRenderer = new axis_1.AxisRenderer();
        axisRenderer.setLinearScale(domainMin, domainMax, 0, height, null);
        axisRenderer.setStyle({
            tickColor: this.object.properties.textColor,
            fontSize: this.object.properties.fontSize,
            fontFamily: this.object.properties.fontFamily,
            lineColor: this.object.properties.textColor,
        });
        var g = Graphics.makeGroup([]);
        if (this.isHorizontalOrientation()) {
            g.elements.push(axisRenderer.renderLine(0, -axisMargin, 0, 1));
        }
        else {
            g.elements.push(axisRenderer.renderLine(marginLeft + gradientWidth + axisMargin, 0, 90, 1));
        }
        var ticks = height * 2;
        var interp = common_1.interpolateColors(range.colors, range.colorspace);
        for (var i = 0; i < ticks; i++) {
            var t = (i + 0.5) / ticks;
            var color = interp(t);
            var y1_1 = (i / ticks) * height;
            var y2 = Math.min(height, ((i + 1.5) / ticks) * height);
            if (this.isHorizontalOrientation()) {
                g.elements.push(Graphics.makeRect(y1_1, 0, y2, gradientWidth, {
                    fillColor: color,
                }));
            }
            else {
                g.elements.push(Graphics.makeRect(marginLeft, y1_1, marginLeft + gradientWidth, y2, {
                    fillColor: color,
                }));
            }
        }
        var _a = this.getLayoutBox(), x1 = _a.x1, y1 = _a.y1;
        if (this.isHorizontalOrientation()) {
            g.transform = { x: x1, y: y1 + horizontalShift, angle: 0 };
        }
        else {
            g.transform = { x: x1, y: y1, angle: 0 };
        }
        return g;
    };
    NumericalColorLegendClass.prototype.getAttributePanelWidgets = function (manager) {
        var widgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        return __spread(widgets, [
            manager.verticalGroup({
                header: strings_1.strings.objects.legend.numericalColorLegend,
            }, [
                manager.inputNumber({ property: "length" }, {
                    label: this.isHorizontalOrientation()
                        ? strings_1.strings.objects.width
                        : strings_1.strings.objects.height,
                    updownTick: 10,
                    showUpdown: true,
                    searchSection: strings_1.strings.objects.legend.numericalColorLegend,
                }),
                manager.inputSelect({ property: "orientation" }, {
                    type: "radio",
                    showLabel: false,
                    icons: ["AlignHorizontalCenter", "AlignVerticalCenter"],
                    labels: [
                        strings_1.strings.objects.legend.vertical,
                        strings_1.strings.objects.legend.horizontal,
                    ],
                    options: [types_1.OrientationType.VERTICAL, types_1.OrientationType.HORIZONTAL],
                    label: strings_1.strings.objects.legend.orientation,
                    searchSection: strings_1.strings.objects.legend.numericalColorLegend,
                }),
            ]),
        ]);
    };
    NumericalColorLegendClass.classID = "legend.numerical-color";
    NumericalColorLegendClass.type = "legend";
    NumericalColorLegendClass.defaultLegendLength = 100;
    NumericalColorLegendClass.defaultProperties = __assign(__assign({}, legend_1.LegendClass.defaultProperties), { orientation: types_1.OrientationType.VERTICAL, length: NumericalColorLegendClass.defaultLegendLength });
    return NumericalColorLegendClass;
}(legend_1.LegendClass));
exports.NumericalColorLegendClass = NumericalColorLegendClass;
//# sourceMappingURL=color_legend.js.map