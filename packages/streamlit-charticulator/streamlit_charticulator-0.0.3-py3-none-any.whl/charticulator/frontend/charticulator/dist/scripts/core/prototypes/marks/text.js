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
Object.defineProperty(exports, "__esModule", { value: true });
exports.TextElementClass = void 0;
var defaults_1 = require("../../../app/stores/defaults");
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var types_1 = require("../../specification/types");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var text_attrs_1 = require("./text.attrs");
var TextElementClass = /** @class */ (function (_super) {
    __extends(TextElementClass, _super);
    function TextElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = text_attrs_1.textAttributes;
        _this.attributeNames = Object.keys(text_attrs_1.textAttributes);
        return _this;
    }
    // Initialize the state of an element so that everything has a valid value
    TextElementClass.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
        attrs.text = "Text";
        attrs.fontFamily = defaults_1.defaultFont;
        attrs.fontSize = defaults_1.defaultFontSize;
        attrs.color = {
            r: 0,
            g: 0,
            b: 0,
        };
        attrs.backgroundColor = null;
        attrs.backgroundColorFilterId = "text-color-filter-" + common_1.getRandomNumber();
        attrs.visible = true;
        attrs.outline = null;
        attrs.opacity = 1;
    };
    // Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
    // eslint-disable-next-line
    TextElementClass.prototype.buildConstraints = function (solver) { };
    // Get the graphical element from the element
    TextElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, empasized) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        var props = this.object.properties;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        if (!attrs.backgroundColorFilterId) {
            attrs.backgroundColorFilterId = "text-color-filter-" + common_1.getRandomNumber();
        }
        var metrics = Graphics.TextMeasurer.Measure(attrs.text, attrs.fontFamily, attrs.fontSize);
        var _a = __read(Graphics.TextMeasurer.ComputeTextPosition(0, 0, metrics, props.alignment.x, props.alignment.y, props.alignment.xMargin, props.alignment.yMargin), 2), dx = _a[0], dy = _a[1];
        var p = cs.getLocalTransform(attrs.x + offset.x, attrs.y + offset.y);
        p.angle += props.rotation;
        var text = null;
        var textContent = attrs.text && common_1.splitStringByNewLine(common_1.replaceNewLineBySymbol(attrs.text));
        if (textContent && textContent.length > 1) {
            var height = attrs.fontSize;
            var lines = [];
            for (var index = 0; index < textContent.length; index++) {
                lines.push(Graphics.makeText(dx, dy - height * index, textContent[index], attrs.fontFamily, attrs.fontSize, __assign({ strokeColor: attrs.outline, fillColor: attrs.color, backgroundColor: attrs.backgroundColor, backgroundColorId: attrs.backgroundColorFilterId, opacity: attrs.opacity }, this.generateEmphasisStyle(empasized))));
            }
            text = Graphics.makeGroup(lines);
        }
        else {
            text = Graphics.makeText(dx, dy, attrs.text, attrs.fontFamily, attrs.fontSize, __assign({ strokeColor: attrs.outline, fillColor: attrs.color, backgroundColor: attrs.backgroundColor, backgroundColorId: attrs.backgroundColorFilterId, opacity: attrs.opacity }, this.generateEmphasisStyle(empasized)));
        }
        var g = Graphics.makeGroup([text]);
        g.transform = p;
        return g;
    };
    // Get DropZones given current state
    TextElementClass.prototype.getDropZones = function () {
        return [
            __assign(__assign({ type: "rectangle" }, this.getBoundingRectangle()), { title: "text", dropAction: {
                    scaleInference: {
                        attribute: "text",
                        attributeType: Specification.AttributeType.Text,
                    },
                }, accept: {
                    table: this.parent.object.table,
                } }),
        ];
    };
    // Get bounding rectangle given current state
    TextElementClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var x = attrs.x, y = attrs.y;
        var bbox = this.getBoundingRectangle();
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
            {
                type: "text-alignment",
                actions: [
                    { type: "property", source: "alignment", property: "alignment" },
                    { type: "property", source: "rotation", property: "rotation" },
                    {
                        type: "attribute-value-mapping",
                        source: "text",
                        attribute: "text",
                    },
                ],
                textWidth: bbox.width,
                textHeight: bbox.height,
                anchorX: x,
                anchorY: y,
                text: attrs.text,
                alignment: props.alignment,
                rotation: props.rotation,
            },
        ];
    };
    TextElementClass.prototype.getBoundingRectangle = function () {
        var props = this.object.properties;
        var attrs = this.state.attributes;
        var metrics = Graphics.TextMeasurer.Measure(attrs.text, attrs.fontFamily, attrs.fontSize);
        var _a = __read(Graphics.TextMeasurer.ComputeTextPosition(0, 0, metrics, props.alignment.x, props.alignment.y, props.alignment.xMargin, props.alignment.yMargin), 2), dx = _a[0], dy = _a[1];
        var cx = dx + metrics.width / 2;
        var cy = dy + metrics.middle;
        var rotation = this.object.properties.rotation;
        var cos = Math.cos(common_1.Geometry.degreesToRadians(rotation));
        var sin = Math.sin(common_1.Geometry.degreesToRadians(rotation));
        return {
            cx: attrs.x + cx * cos - cy * sin,
            cy: attrs.y + cx * sin + cy * cos,
            width: metrics.width,
            height: (metrics.middle - metrics.ideographicBaseline) * 2,
            rotation: rotation,
        };
    };
    TextElementClass.prototype.getBoundingBox = function () {
        var rect = this.getBoundingRectangle();
        var attrs = this.state.attributes;
        return {
            type: "anchored-rectangle",
            anchorX: attrs.x,
            anchorY: attrs.y,
            cx: rect.cx - attrs.x,
            cy: rect.cy - attrs.y,
            width: rect.width,
            height: rect.height,
            rotation: rect.rotation,
        };
    };
    TextElementClass.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y;
        return [
            { type: "x", value: x, attribute: "x" },
            { type: "y", value: y, attribute: "y" },
        ];
    };
    TextElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var props = this.object.properties;
        return [
            manager.verticalGroup({
                header: strings_1.strings.objects.general,
            }, [
                manager.mappingEditor(strings_1.strings.toolbar.text, "text", {
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.font, "fontFamily", {
                    defaultValue: defaults_1.defaultFont,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.size, "fontSize", {
                    hints: { rangeNumber: [0, 36] },
                    defaultValue: defaults_1.defaultFontSize,
                    numberOptions: {
                        showUpdown: true,
                        updownStyle: "font",
                        minimum: 0,
                        updownTick: 2,
                    },
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.objects.general,
                }),
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.anchorAndRotation,
            }, [
                manager.inputSelect({ property: "alignment", field: "x" }, {
                    type: "radio",
                    icons: [
                        "AlignHorizontalLeft",
                        "AlignHorizontalCenter",
                        "AlignHorizontalRight",
                    ],
                    labels: ["Left", "Middle", "Right"],
                    options: ["left", "middle", "right"],
                    label: strings_1.strings.objects.anchorX,
                    searchSection: strings_1.strings.objects.anchorAndRotation,
                }),
                props.alignment.x != "middle"
                    ? manager.inputNumber({ property: "alignment", field: "xMargin" }, {
                        updownTick: 1,
                        showUpdown: true,
                        label: "Margin",
                        searchSection: strings_1.strings.objects.anchorAndRotation,
                    })
                    : null,
                manager.inputSelect({ property: "alignment", field: "y" }, {
                    type: "radio",
                    icons: [
                        "AlignVerticalTop",
                        "AlignVerticalCenter",
                        "AlignVerticalBottom",
                    ],
                    labels: ["Top", "Middle", "Bottom"],
                    options: ["top", "middle", "bottom"],
                    label: strings_1.strings.objects.anchorY,
                    searchSection: strings_1.strings.objects.anchorAndRotation,
                }),
                props.alignment.y != "middle"
                    ? manager.inputNumber({ property: "alignment", field: "yMargin" }, {
                        updownTick: 1,
                        showUpdown: true,
                        label: strings_1.strings.objects.text.margin,
                        searchSection: strings_1.strings.objects.anchorAndRotation,
                    })
                    : null,
                manager.inputNumber({ property: "rotation" }, {
                    label: strings_1.strings.objects.rotation,
                    showUpdown: true,
                    updownTick: 1,
                    searchSection: strings_1.strings.objects.anchorAndRotation,
                }),
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.style,
            }, [
                manager.mappingEditor(strings_1.strings.objects.color, "color", {
                    searchSection: strings_1.strings.objects.style,
                }),
                manager.mappingEditor(strings_1.strings.objects.outline, "outline", {
                    searchSection: strings_1.strings.objects.style,
                }),
                manager.mappingEditor(strings_1.strings.objects.background, "backgroundColor", {
                    defaultValue: null,
                    searchSection: strings_1.strings.objects.style,
                }),
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
        ].concat(parentWidgets);
    };
    TextElementClass.prototype.getTemplateParameters = function () {
        var properties = [];
        if (this.object.mappings.fontFamily &&
            this.object.mappings.fontFamily.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "fontFamily",
                },
                type: Specification.AttributeType.FontFamily,
                default: this.state.attributes.fontFamily,
            });
        }
        if (this.object.mappings.fontSize &&
            this.object.mappings.fontSize.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "fontSize",
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.fontSize,
            });
        }
        if (this.object.mappings.color &&
            this.object.mappings.color.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "color",
                },
                type: Specification.AttributeType.Color,
                default: common_1.rgbToHex(this.state.attributes.color),
            });
        }
        if (this.object.mappings.backgroundColor &&
            this.object.mappings.backgroundColor.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "backgroundColor",
                },
                type: Specification.AttributeType.Color,
                default: null,
            });
        }
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
        if (this.object.mappings.text &&
            this.object.mappings.text.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "text",
                },
                type: Specification.AttributeType.Text,
                default: this.state.attributes.text,
            });
        }
        return {
            properties: properties,
        };
    };
    TextElementClass.classID = "mark.text";
    TextElementClass.type = "mark";
    TextElementClass.metadata = {
        displayName: "Text",
        iconPath: "FontColorA",
        creatingInteraction: {
            type: "point",
            mapping: { x: "x", y: "y" },
        },
    };
    TextElementClass.defaultMappingValues = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { text: "Text", fontFamily: defaults_1.defaultFont, fontSize: defaults_1.defaultFontSize, color: { r: 0, g: 0, b: 0 }, opacity: 1, visible: true });
    TextElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { alignment: {
            x: types_1.TextAlignmentHorizontal.Middle,
            y: types_1.TextAlignmentVertical.Top,
            xMargin: 5,
            yMargin: 5,
        }, rotation: 0, visible: true });
    return TextElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.TextElementClass = TextElementClass;
//# sourceMappingURL=text.js.map