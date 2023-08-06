"use strict";
/* eslint-disable max-lines-per-function */
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
exports.LegendClass = void 0;
var defaults_1 = require("../../../app/stores/defaults");
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
var LegendClass = /** @class */ (function (_super) {
    __extends(LegendClass, _super);
    function LegendClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["x", "y"];
        _this.attributes = {
            x: {
                name: "x",
                type: Specification.AttributeType.Number,
            },
            y: {
                name: "y",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    LegendClass.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
    };
    LegendClass.prototype.getLayoutBox = function () {
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
    LegendClass.prototype.getBoundingBox = function () {
        var _a = this.getLayoutBox(), x1 = _a.x1, y1 = _a.y1, x2 = _a.x2, y2 = _a.y2;
        return {
            type: "rectangle",
            cx: (x1 + x2) / 2,
            cy: (y1 + y2) / 2,
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            rotation: 0,
        };
    };
    LegendClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y;
        return [
            {
                type: "point",
                x: x,
                y: y,
                actions: [
                    { type: "attribute", source: "x", attribute: "x" },
                    { type: "attribute", source: "y", attribute: "y" },
                ],
                options: {
                    snapToClosestPoint: true,
                },
            },
        ];
    };
    LegendClass.prototype.getScale = function () {
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
    LegendClass.prototype.getLegendSize = function () {
        return [10, 10];
    };
    LegendClass.prototype.getOrderingObjects = function () {
        var scale = this.getScale();
        if (scale) {
            var _a = __read(scale, 1), scaleObject = _a[0];
            var mapping = scaleObject.properties.mapping;
            return Object.keys(mapping);
        }
        return [];
    };
    LegendClass.prototype.getAttributePanelWidgets = function (manager) {
        var widget = [
            manager.verticalGroup({
                header: strings_1.strings.objects.legend.labels,
            }, [
                manager.inputFontFamily({ property: "fontFamily" }, {
                    label: strings_1.strings.objects.font,
                    searchSection: strings_1.strings.objects.legend.labels,
                }),
                manager.inputNumber({ property: "fontSize" }, {
                    showUpdown: true,
                    updownStyle: "font",
                    updownTick: 2,
                    label: strings_1.strings.objects.size,
                    searchSection: strings_1.strings.objects.legend.labels,
                }),
                manager.inputColor({ property: "textColor" }, {
                    label: strings_1.strings.objects.color,
                    labelKey: strings_1.strings.objects.color,
                    allowNull: true,
                    searchSection: strings_1.strings.objects.legend.labels,
                }),
                this.object.classID === "legend.categorical"
                    ? manager.inputSelect({ property: "markerShape" }, {
                        type: "dropdown",
                        showLabel: true,
                        icons: ["RectangleShape", "TriangleShape", "Ellipse"],
                        labels: [
                            strings_1.strings.toolbar.rectangle,
                            strings_1.strings.toolbar.triangle,
                            strings_1.strings.toolbar.ellipse,
                        ],
                        options: ["rectangle", "triangle", "circle"],
                        label: strings_1.strings.objects.legend.markerShape,
                        searchSection: strings_1.strings.objects.legend.labels,
                    })
                    : null,
                this.object.classID === "legend.categorical"
                    ? manager.searchWrapper({
                        searchPattern: [
                            strings_1.strings.objects.legend.ordering,
                            strings_1.strings.objects.legend.labels,
                        ],
                    }, [
                        manager.label(strings_1.strings.objects.legend.ordering),
                        manager.reorderWidget({
                            property: "order",
                        }, {
                            items: this.getOrderingObjects(),
                            onConfirm: function (items) {
                                manager.emitSetProperty({
                                    property: "order",
                                    field: null,
                                }, items);
                            },
                        }),
                    ])
                    : null,
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.legend.layout,
            }, [
                manager.searchWrapper({
                    searchPattern: [
                        strings_1.strings.alignment.align,
                        strings_1.strings.objects.legend.layout,
                    ],
                }, [
                    manager.label(strings_1.strings.alignment.alignment),
                    manager.horizontal([0, 0], manager.inputSelect({ property: "alignX" }, {
                        type: "radio",
                        icons: [
                            "AlignHorizontalLeft",
                            "AlignHorizontalCenter",
                            "AlignHorizontalRight",
                        ],
                        labels: [
                            strings_1.strings.alignment.left,
                            strings_1.strings.alignment.middle,
                            strings_1.strings.alignment.right,
                        ],
                        options: ["start", "middle", "end"],
                        ignoreSearch: true,
                    }), manager.inputSelect({ property: "alignY" }, {
                        type: "radio",
                        options: ["start", "middle", "end"],
                        icons: [
                            "AlignVerticalBottom",
                            "AlignVerticalCenter",
                            "AlignVerticalTop",
                        ],
                        labels: [
                            strings_1.strings.alignment.bottom,
                            strings_1.strings.alignment.middle,
                            strings_1.strings.alignment.top,
                        ],
                        ignoreSearch: true,
                    }), null),
                ]),
            ]),
        ];
        return widget;
    };
    LegendClass.prototype.getTemplateParameters = function () {
        var properties = [];
        if (this.object.properties.fontFamily) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "fontFamily",
                },
                type: Specification.AttributeType.FontFamily,
                default: this.object.properties.fontFamily,
            });
        }
        if (this.object.properties.fontSize) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "fontSize",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.fontSize,
            });
        }
        if (this.object.properties.textColor) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "textColor",
                },
                type: Specification.AttributeType.Color,
                default: common_1.rgbToHex(this.object.properties.textColor),
            });
        }
        if (this.object.properties.markerShape) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "markerShape",
                },
                type: Specification.AttributeType.Enum,
                default: this.object.properties.markerShape,
            });
        }
        if (this.object.properties.alignY) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "alignY",
                },
                type: Specification.AttributeType.Enum,
                default: this.object.properties.alignY,
            });
        }
        if (this.object.properties.alignX) {
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "alignX",
                },
                type: Specification.AttributeType.Enum,
                default: this.object.properties.alignX,
            });
        }
        return {
            properties: properties,
        };
    };
    LegendClass.metadata = {
        displayName: "Legend",
        iconPath: "CharticulatorLegend",
    };
    LegendClass.defaultProperties = {
        scale: null,
        visible: true,
        alignX: "start",
        alignY: "end",
        fontFamily: defaults_1.defaultFont,
        fontSize: defaults_1.defaultFontSizeLegend,
        textColor: { r: 0, g: 0, b: 0 },
        dataSource: "columnValues",
        dataExpressions: [],
        markerShape: "circle",
        order: null,
    };
    return LegendClass;
}(chart_element_1.ChartElementClass));
exports.LegendClass = LegendClass;
//# sourceMappingURL=legend.js.map