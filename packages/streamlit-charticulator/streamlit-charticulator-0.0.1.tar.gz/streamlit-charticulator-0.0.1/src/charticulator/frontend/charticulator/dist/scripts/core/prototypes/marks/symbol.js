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
Object.defineProperty(exports, "__esModule", { value: true });
exports.SymbolElementClass = exports.symbolTypesList = void 0;
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var graphics_1 = require("../../graphics");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var symbol_attrs_1 = require("./symbol.attrs");
exports.symbolTypesList = symbol_attrs_1.symbolTypes;
var SymbolElementClass = /** @class */ (function (_super) {
    __extends(SymbolElementClass, _super);
    function SymbolElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = symbol_attrs_1.symbolAttributes;
        _this.attributeNames = Object.keys(symbol_attrs_1.symbolAttributes);
        return _this;
    }
    SymbolElementClass.prototype.initializeState = function () {
        _super.prototype.initializeState.call(this);
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
        attrs.size = 60;
        attrs.fill = { r: 128, g: 128, b: 128 };
        attrs.strokeWidth = 1;
        attrs.opacity = 1;
        attrs.visible = true;
        attrs.symbol = "circle";
    };
    /** Get link anchors for this mark */
    SymbolElementClass.prototype.getLinkAnchors = function (mode) {
        var attrs = this.state.attributes;
        return [
            {
                element: this.object._id,
                points: [
                    {
                        x: attrs.x,
                        y: attrs.y,
                        xAttribute: "x",
                        yAttribute: "y",
                        direction: { x: mode == "begin" ? 1 : -1, y: 0 },
                    },
                ],
            },
        ];
    };
    // Get the graphical element from the element
    // eslint-disable-next-line
    SymbolElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, emphasize) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        if (attrs.size <= 0) {
            return null;
        }
        var pc = cs.transformPoint(attrs.x + offset.x, attrs.y + offset.y);
        var rotation = this.object.properties.rotation;
        var style = __assign({ strokeColor: attrs.stroke, strokeWidth: attrs.strokeWidth, fillColor: attrs.fill, opacity: attrs.opacity }, this.generateEmphasisStyle(emphasize));
        switch (attrs.symbol) {
            case "square": {
                var w = Math.sqrt(attrs.size);
                var elem = {
                    type: "rect",
                    style: style,
                    x1: -w / 2,
                    y1: -w / 2,
                    x2: w / 2,
                    y2: w / 2,
                    rotation: rotation,
                };
                var gr = graphics_1.makeGroup([elem]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            case "cross": {
                var r = Math.sqrt(attrs.size / 5) / 2;
                var path = Graphics.makePath(style);
                path.moveTo(-3 * r, -r);
                path.lineTo(-r, -r);
                path.lineTo(-r, -3 * r);
                path.lineTo(-r, -3 * r);
                path.lineTo(+r, -3 * r);
                path.lineTo(+r, -r);
                path.lineTo(+3 * r, -r);
                path.lineTo(+3 * r, +r);
                path.lineTo(+r, +r);
                path.lineTo(+r, +3 * r);
                path.lineTo(-r, +3 * r);
                path.lineTo(-r, +r);
                path.lineTo(-3 * r, +r);
                path.transformRotation(rotation);
                path.closePath();
                var gr = graphics_1.makeGroup([path.path]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            case "diamond": {
                var tan30 = 0.5773502691896257; // Math.sqrt(1 / 3);
                var tan30_2 = 1.1547005383792515; // tan30 * 2;
                var y = Math.sqrt(attrs.size / tan30_2), x = y * tan30;
                var path = Graphics.makePath(style);
                path.moveTo(0, -y);
                path.lineTo(x, 0);
                path.lineTo(0, y);
                path.lineTo(-x, 0);
                path.transformRotation(rotation);
                path.closePath();
                var gr = graphics_1.makeGroup([path.path]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            case "star": {
                var ka = 0.8908130915292852281;
                // const kr = 0.3819660112501051; // Math.sin(Math.PI / 10) / Math.sin(7 * Math.PI / 10),
                var kx = 0.22451398828979266; // Math.sin(2 * Math.PI / 10) * kr;
                var ky = -0.3090169943749474; // -Math.cos(2 * Math.PI / 10) * kr;
                var r = Math.sqrt(attrs.size * ka), x = kx * r, y = ky * r;
                var path = Graphics.makePath(style);
                path.moveTo(0, -r);
                path.lineTo(x, y);
                for (var i = 1; i < 5; ++i) {
                    var a = (Math.PI * 2 * i) / 5, c = Math.cos(a), s = Math.sin(a);
                    path.lineTo(s * r, -c * r);
                    path.lineTo(c * x - s * y, s * x + c * y);
                }
                path.transformRotation(rotation);
                path.closePath();
                var gr = graphics_1.makeGroup([path.path]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            case "triangle": {
                var sqrt3 = Math.sqrt(3);
                var y = -Math.sqrt(attrs.size / (sqrt3 * 3));
                var path = Graphics.makePath(style);
                path.moveTo(0, y * 2);
                path.lineTo(-sqrt3 * y, -y);
                path.lineTo(sqrt3 * y, -y);
                path.transformRotation(rotation);
                path.closePath();
                var gr = graphics_1.makeGroup([path.path]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            case "wye": {
                var c = -0.5, s = Math.sqrt(3) / 2, k = 1 / Math.sqrt(12), a = (k / 2 + 1) * 3;
                var r = Math.sqrt(attrs.size / a), x0 = r / 2, y0 = r * k, x1 = x0, y1 = r * k + r, x2 = -x1, y2 = y1;
                var path = Graphics.makePath(style);
                path.moveTo(x0, y0);
                path.lineTo(x1, y1);
                path.lineTo(x2, y2);
                path.lineTo(c * x0 - s * y0, s * x0 + c * y0);
                path.lineTo(c * x1 - s * y1, s * x1 + c * y1);
                path.lineTo(c * x2 - s * y2, s * x2 + c * y2);
                path.lineTo(c * x0 + s * y0, c * y0 - s * x0);
                path.lineTo(c * x1 + s * y1, c * y1 - s * x1);
                path.lineTo(c * x2 + s * y2, c * y2 - s * x2);
                path.transformRotation(rotation);
                path.closePath();
                var gr = graphics_1.makeGroup([path.path]);
                gr.transform.x = pc.x;
                gr.transform.y = pc.y;
                return gr;
            }
            default: {
                return {
                    type: "circle",
                    style: style,
                    cx: pc.x,
                    cy: pc.y,
                    r: Math.sqrt(attrs.size / Math.PI),
                };
            }
        }
    };
    // Get DropZones given current state
    SymbolElementClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y, size = attrs.size;
        var r = Math.sqrt(size);
        return [
            {
                type: "line",
                p1: { x: x + r, y: y },
                p2: { x: x - r, y: y },
                title: "size",
                dropAction: {
                    scaleInference: {
                        attribute: "size",
                        attributeType: Specification.AttributeType.Number,
                        hints: { rangeNumber: [0, 200 * Math.PI] },
                    },
                },
                accept: {
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                },
            },
        ];
    };
    // Get bounding rectangle given current state
    SymbolElementClass.prototype.getHandles = function () {
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
            },
        ];
    };
    SymbolElementClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y, size = attrs.size;
        return {
            type: "circle",
            cx: x,
            cy: y,
            radius: Math.sqrt(size / Math.PI),
        };
    };
    SymbolElementClass.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y;
        return [
            { type: "x", value: x, attribute: "x" },
            { type: "y", value: y, attribute: "y" },
        ];
    };
    SymbolElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var widgets = [
            manager.verticalGroup({
                header: strings_1.strings.objects.general,
            }, [
                manager.mappingEditor(strings_1.strings.objects.rect.shape, "symbol", {
                    acceptKinds: [Specification.DataKind.Categorical],
                    hints: { rangeEnum: symbol_attrs_1.symbolTypes },
                    defaultValue: "circle",
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.size, "size", {
                    acceptKinds: [Specification.DataKind.Numerical],
                    hints: { rangeNumber: [0, 200 * Math.PI] },
                    defaultValue: 60,
                    numberOptions: {
                        showSlider: true,
                        minimum: 0,
                        sliderRange: [0, 3600],
                        sliderFunction: "sqrt",
                    },
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.inputNumber({ property: "rotation" }, {
                    label: strings_1.strings.objects.rotation,
                    showUpdown: true,
                    updownTick: 5,
                    searchSection: strings_1.strings.objects.general,
                }),
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.style,
            }, [
                manager.mappingEditor(strings_1.strings.objects.fill, "fill", {
                    searchSection: strings_1.strings.objects.style,
                }),
                manager.mappingEditor(strings_1.strings.objects.stroke, "stroke", {
                    searchSection: strings_1.strings.objects.style,
                }),
                this.object.mappings.stroke != null
                    ? manager.mappingEditor(strings_1.strings.objects.strokeWidth, "strokeWidth", {
                        hints: { rangeNumber: [0, 5] },
                        defaultValue: 1,
                        numberOptions: {
                            showSlider: true,
                            sliderRange: [0, 5],
                            minimum: 0,
                        },
                        searchSection: strings_1.strings.objects.style,
                    })
                    : null,
                manager.mappingEditor(strings_1.strings.objects.opacity, "opacity", {
                    hints: { rangeNumber: [0, 1] },
                    defaultValue: 1,
                    numberOptions: {
                        showSlider: true,
                        minimum: 0,
                        maximum: 1,
                        step: 0.1,
                    },
                    searchSection: strings_1.strings.objects.style,
                }),
            ]),
        ];
        widgets = widgets.concat([]);
        return widgets.concat(parentWidgets);
    };
    SymbolElementClass.prototype.getTemplateParameters = function () {
        var properties = [];
        if (this.object.mappings.visible &&
            this.object.mappings.visible.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "visible",
                },
                type: Specification.AttributeType.Boolean,
                default: this.state.attributes.visible,
            });
        }
        if (this.object.mappings.fill &&
            this.object.mappings.fill.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "fill",
                },
                type: Specification.AttributeType.Color,
                default: common_1.rgbToHex(this.state.attributes.fill),
            });
        }
        if (this.object.mappings.strokeWidth &&
            this.object.mappings.strokeWidth.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "strokeWidth",
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.strokeWidth,
            });
        }
        if (this.object.mappings.stroke &&
            this.object.mappings.stroke.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "stroke",
                },
                type: Specification.AttributeType.Color,
                default: common_1.rgbToHex(this.state.attributes.stroke),
            });
        }
        if (this.object.mappings.size &&
            this.object.mappings.size.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "size",
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.size,
            });
        }
        if (this.object.mappings.opacity &&
            this.object.mappings.opacity.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "opacity",
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.opacity,
            });
        }
        if (this.object.mappings.symbol &&
            this.object.mappings.symbol.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "symbol",
                },
                type: Specification.AttributeType.Enum,
                default: this.state.attributes.symbol,
            });
        }
        return {
            properties: properties,
        };
    };
    SymbolElementClass.classID = "mark.symbol";
    SymbolElementClass.type = "mark";
    SymbolElementClass.metadata = {
        displayName: "Symbol",
        iconPath: "Shapes",
        creatingInteraction: {
            type: "point",
            mapping: { x: "x", y: "y" },
        },
    };
    SymbolElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { visible: true, rotation: 0 });
    SymbolElementClass.defaultMappingValues = {
        fill: { r: 17, g: 141, b: 255 },
        strokeWidth: 1,
        opacity: 1,
        size: 60,
        visible: true,
    };
    return SymbolElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.SymbolElementClass = SymbolElementClass;
//# sourceMappingURL=symbol.js.map