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
exports.CategoricalLegendClass = exports.ReservedMappingKeyNamePrefix = void 0;
var Graphics = require("../../graphics");
var legend_1 = require("./legend");
var strings_1 = require("../../../strings");
var types_1 = require("./types");
exports.ReservedMappingKeyNamePrefix = "reserved_";
var CategoricalLegendClass = /** @class */ (function (_super) {
    __extends(CategoricalLegendClass, _super);
    function CategoricalLegendClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.textMeasure = new Graphics.TextMeasurer();
        return _this;
        // private getScaleEditor(
        //   manager: Controls.WidgetManager & CharticulatorPropertyAccessors
        // ) {
        //   const scale = this?.getScale();
        //   if (scale) {
        //     return manager.vertical(
        //       manager.label(strings.objects.colors, {
        //         addMargins: true,
        //       }),
        //       manager.horizontal(
        //         [1],
        //         manager.scaleEditor(
        //           "mappingOptions",
        //           strings.objects.legend.editColors
        //         )
        //       )
        //     );
        //   }
        //   return null;
        // }
    }
    CategoricalLegendClass.prototype.getLegendItems = function () {
        var scale = this.getScale();
        if (scale) {
            var _a = __read(scale, 1), scaleObject = _a[0];
            var mapping_1 = scaleObject.properties.mapping;
            var items = [];
            for (var key in mapping_1) {
                if (Object.prototype.hasOwnProperty.call(mapping_1, key) &&
                    !key.startsWith(exports.ReservedMappingKeyNamePrefix)) {
                    switch (scaleObject.classID) {
                        case "scale.categorical<string,boolean>":
                            {
                                items.push({
                                    type: "boolean",
                                    label: key,
                                    value: mapping_1[key],
                                });
                            }
                            break;
                        case "scale.categorical<string,number>":
                            {
                                items.push({ type: "number", label: key, value: mapping_1[key] });
                            }
                            break;
                        case "scale.categorical<string,color>":
                            {
                                items.push({ type: "color", label: key, value: mapping_1[key] });
                            }
                            break;
                    }
                }
            }
            if (this.object.properties.order) {
                if (this.object.properties.order.length != items.length) {
                    return items;
                }
                else {
                    return this.object.properties.order.map(function (orderItem) {
                        return {
                            type: "color",
                            label: orderItem,
                            value: mapping_1[orderItem],
                        };
                    });
                }
            }
            else {
                return items;
            }
        }
        else {
            return [];
        }
    };
    CategoricalLegendClass.prototype.getLineHeight = function () {
        return this.object.properties.fontSize + 10;
    };
    CategoricalLegendClass.prototype.getLineWidth = function () {
        var width = 0;
        var items = this.getLegendItems();
        if (this.object.properties.orientation === types_1.OrientationType.HORIZONTAL) {
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var metrics = this.textMeasure.measure(item.label);
                width += 10 + metrics.width;
            }
        }
        else {
            width = (items[0] && this.textMeasure.measure(items[0].label).width) || 0;
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var metrics = this.textMeasure.measure(item.label);
                if (10 + metrics.width > width) {
                    width = 10 + metrics.width;
                }
            }
        }
        return width;
    };
    CategoricalLegendClass.prototype.getLegendSize = function () {
        var items = this.getLegendItems();
        if (this.object.properties.orientation === types_1.OrientationType.VERTICAL ||
            this.object.properties.orientation === undefined) {
            return [
                this.getLineWidth() + this.getLineHeight(),
                items.length * this.getLineHeight(),
            ];
        }
        else {
            return [
                this.getLineWidth() + items.length * this.getLineHeight(),
                this.getLineHeight(),
            ];
        }
    };
    // eslint-disable-next-line
    CategoricalLegendClass.prototype.getGraphics = function () {
        var fontFamily = this.object.properties.fontFamily;
        var fontSize = this.object.properties.fontSize;
        var lineHeight = this.getLineHeight();
        this.textMeasure.setFontFamily(fontFamily);
        this.textMeasure.setFontSize(fontSize);
        var g = Graphics.makeGroup([]);
        var items = this.getLegendItems();
        var horizontalGap = 10;
        var itemGroupOffset = 0;
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var metrics = this.textMeasure.measure(item.label);
            var offsets = Graphics.TextMeasurer.ComputeTextPosition(lineHeight, lineHeight / 2, metrics, "left", "middle", 5, 0);
            var textLabel = Graphics.makeText(offsets[0], offsets[1], item.label, fontFamily, fontSize, { fillColor: this.object.properties.textColor });
            var gItem = Graphics.makeGroup([textLabel]);
            switch (item.type) {
                case "color":
                    {
                        switch (this.object.properties.markerShape) {
                            case "rectangle":
                                gItem.elements.push(Graphics.makeRect(8, 4, lineHeight, lineHeight - 4, {
                                    fillColor: item.value,
                                }));
                                break;
                            case "triangle":
                                gItem.elements.push(Graphics.makePolygon([
                                    {
                                        x: lineHeight / 2 + 4,
                                        y: lineHeight - 4,
                                    },
                                    {
                                        x: 0 + 4 + 2,
                                        y: 0 + 4,
                                    },
                                    {
                                        x: lineHeight + 4 - 2,
                                        y: 0 + 4,
                                    },
                                ], {
                                    fillColor: item.value,
                                }));
                                break;
                            case "circle":
                            default:
                                gItem.elements.push(Graphics.makeCircle(lineHeight / 2, lineHeight / 2, lineHeight / 3, {
                                    fillColor: item.value,
                                }));
                        }
                    }
                    break;
            }
            if (this.object.properties.orientation === types_1.OrientationType.HORIZONTAL) {
                gItem.transform = {
                    x: itemGroupOffset,
                    y: 0,
                    angle: 0,
                };
                itemGroupOffset += metrics.width + lineHeight + horizontalGap;
            }
            else {
                gItem.transform = {
                    x: 0,
                    y: lineHeight * (items.length - 1 - i),
                    angle: 0,
                };
            }
            g.elements.push(gItem);
        }
        var _a = this.getLayoutBox(), x1 = _a.x1, y1 = _a.y1;
        g.transform = { x: x1, y: y1, angle: 0 };
        return g;
    };
    CategoricalLegendClass.prototype.getLayoutBox = function () {
        if (this.object.properties.orientation === types_1.OrientationType.VERTICAL ||
            this.object.properties.orientation === undefined) {
            return _super.prototype.getLayoutBox.call(this);
        }
        var _a = this.state.attributes, x = _a.x, y = _a.y;
        var _b = __read(this.getLegendSize(), 2), width = _b[0], height = _b[1];
        var x1, y1, x2, y2;
        switch (this.object.properties.alignX) {
            case "start":
                x1 = x;
                x2 = x + width;
                break;
            case "middle":
                x1 = x - width / 2;
                x2 = x + width / 2;
                break;
            case "end":
                x1 = x - width;
                x2 = x;
                break;
        }
        switch (this.object.properties.alignY) {
            case "start":
                y1 = y;
                y2 = y + height;
                break;
            case "middle":
                y1 = y - height / 2;
                y2 = y + height / 2;
                break;
            case "end":
                y1 = y - height;
                y2 = y;
                break;
        }
        return { x1: x1, y1: y1, x2: x2, y2: y2 };
    };
    CategoricalLegendClass.prototype.getAttributePanelWidgets = function (manager) {
        var widgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        return __spread(widgets, [
            manager.verticalGroup({
                header: strings_1.strings.objects.legend.categoricalLegend,
            }, [
                manager.inputSelect({ property: "orientation" }, {
                    type: "radio",
                    showLabel: false,
                    icons: ["GripperBarVertical", "GripperBarHorizontal"],
                    labels: [
                        strings_1.strings.objects.legend.vertical,
                        strings_1.strings.objects.legend.horizontal,
                    ],
                    options: [types_1.OrientationType.VERTICAL, types_1.OrientationType.HORIZONTAL],
                    label: strings_1.strings.objects.legend.orientation,
                    searchSection: strings_1.strings.objects.legend.categoricalLegend,
                }),
            ]),
        ]);
    };
    CategoricalLegendClass.classID = "legend.categorical";
    CategoricalLegendClass.type = "legend";
    CategoricalLegendClass.defaultProperties = __assign(__assign({}, legend_1.LegendClass.defaultProperties), { orientation: types_1.OrientationType.VERTICAL });
    return CategoricalLegendClass;
}(legend_1.LegendClass));
exports.CategoricalLegendClass = CategoricalLegendClass;
//# sourceMappingURL=categorical_legend.js.map