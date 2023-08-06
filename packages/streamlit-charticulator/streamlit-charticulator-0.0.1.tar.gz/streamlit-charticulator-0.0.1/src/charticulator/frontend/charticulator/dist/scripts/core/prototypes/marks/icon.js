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
Object.defineProperty(exports, "__esModule", { value: true });
exports.IconElementClass = void 0;
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var types_1 = require("../../specification/types");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var icon_attrs_1 = require("./icon.attrs");
var image_1 = require("./image");
var IconElementClass = /** @class */ (function (_super) {
    __extends(IconElementClass, _super);
    function IconElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = icon_attrs_1.iconAttributes;
        _this.attributeNames = Object.keys(icon_attrs_1.iconAttributes);
        return _this;
    }
    IconElementClass.prototype.initializeState = function () {
        _super.prototype.initializeState.call(this);
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
        attrs.size = 400;
        attrs.opacity = 1;
        attrs.visible = true;
        attrs.image = null;
    };
    /** Get link anchors for this mark */
    IconElementClass.prototype.getLinkAnchors = function (mode) {
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
    IconElementClass.prototype.getLayoutProps = function () {
        var attrs = this.state.attributes;
        var image = attrs.image || image_1.imagePlaceholder;
        if (typeof image == "string") {
            // Be compatible with old version
            image = { src: image, width: 100, height: 100 };
        }
        if (attrs.size <= 0) {
            return { width: 0, height: 0, dx: 0, dy: 0 };
        }
        var h = Math.sqrt((attrs.size * image.height) / image.width);
        var w = (h * image.width) / image.height;
        var offsets = this.getCenterOffset(this.object.properties.alignment, w, h);
        return {
            width: w,
            height: h,
            dx: offsets[0],
            dy: offsets[1],
        };
    };
    IconElementClass.prototype.getCenterOffset = function (alignment, width, height) {
        var cx = width / 2, cy = height / 2;
        if (alignment.x == "left") {
            cx = -alignment.xMargin;
        }
        if (alignment.x == "right") {
            cx = width + alignment.xMargin;
        }
        if (alignment.y == "bottom") {
            cy = -alignment.yMargin;
        }
        if (alignment.y == "top") {
            cy = height + alignment.yMargin;
        }
        return [cx, cy];
    };
    /** Get the graphical element from the element */
    IconElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, 
    // eslint-disable-next-line
    emphasize) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        if (attrs.size <= 0) {
            return null;
        }
        var image = attrs.image || image_1.imagePlaceholder;
        if (typeof image == "string") {
            // Be compatible with old version
            image = { src: image, width: 100, height: 100 };
        }
        // Compute w, h to resize the image to the desired size
        var layout = this.getLayoutProps();
        var gImage = Graphics.makeGroup([
            {
                type: "image",
                src: image.src,
                x: -layout.dx,
                y: -layout.dy,
                width: layout.width,
                height: layout.height,
                mode: "stretch",
            },
        ]);
        gImage.transform = cs.getLocalTransform(attrs.x + offset.x, attrs.y + offset.y);
        gImage.transform.angle += this.object.properties.rotation;
        // Apply the opacity
        gImage.style = {
            opacity: attrs.opacity,
        };
        return gImage;
    };
    /** Get DropZones given current state */
    IconElementClass.prototype.getDropZones = function () {
        return [
            __assign(__assign({ type: "rectangle" }, this.getBoundingRectangle()), { title: "size", dropAction: {
                    scaleInference: {
                        attribute: "size",
                        attributeType: Specification.AttributeType.Number,
                    },
                }, accept: {
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                } }),
        ];
    };
    /** Get bounding rectangle given current state */
    IconElementClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y;
        var bbox = this.getBoundingRectangle();
        var props = this.object.properties;
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
                text: null,
                alignment: props.alignment,
                rotation: props.rotation,
            },
        ];
    };
    IconElementClass.prototype.getBoundingRectangle = function () {
        var attrs = this.state.attributes;
        var rotation = this.object.properties.rotation;
        var layout = this.getLayoutProps();
        var cos = Math.cos(common_1.Geometry.degreesToRadians(rotation));
        var sin = Math.sin(common_1.Geometry.degreesToRadians(rotation));
        var dx = layout.dx - layout.width / 2;
        var dy = layout.dy - layout.height / 2;
        return {
            cx: attrs.x - dx * cos + dy * sin,
            cy: attrs.y - dx * sin - dy * cos,
            width: layout.width,
            height: layout.height,
            rotation: rotation,
        };
    };
    IconElementClass.prototype.getBoundingBox = function () {
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
    IconElementClass.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y;
        return [
            { type: "x", value: x, attribute: "x" },
            { type: "y", value: y, attribute: "y" },
        ];
    };
    IconElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var props = this.object.properties;
        var widgets = [
            manager.verticalGroup({
                header: strings_1.strings.toolbar.icon,
            }, [
                manager.mappingEditor(strings_1.strings.objects.icon.image, "image", {
                    searchSection: strings_1.strings.toolbar.icon,
                }),
                manager.mappingEditor(strings_1.strings.objects.size, "size", {
                    acceptKinds: [Specification.DataKind.Numerical],
                    hints: { rangeNumber: [0, 100] },
                    defaultValue: 400,
                    numberOptions: {
                        showSlider: true,
                        minimum: 0,
                        sliderRange: [0, 3600],
                        sliderFunction: "sqrt",
                    },
                    searchSection: strings_1.strings.toolbar.icon,
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
                    searchSection: strings_1.strings.toolbar.icon,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.toolbar.icon,
                }),
            ]),
        ];
        widgets = widgets.concat([
            manager.verticalGroup({
                header: strings_1.strings.objects.anchorAndRotation,
            }, [
                manager.horizontal([0, 1], manager.inputSelect({ property: "alignment", field: "x" }, {
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
                    options: ["left", "middle", "right"],
                    label: strings_1.strings.objects.anchorX,
                    searchSection: strings_1.strings.objects.anchorAndRotation,
                }), props.alignment.x != "middle"
                    ? manager.inputNumber({ property: "alignment", field: "xMargin" }, {
                        label: strings_1.strings.margins.margin,
                        searchSection: strings_1.strings.objects.anchorAndRotation,
                    })
                    : null),
                manager.horizontal([0, 1], manager.inputSelect({ property: "alignment", field: "y" }, {
                    type: "radio",
                    icons: [
                        "AlignVerticalTop",
                        "AlignVerticalCenter",
                        "AlignVerticalBottom",
                    ],
                    labels: [
                        strings_1.strings.alignment.top,
                        strings_1.strings.alignment.middle,
                        strings_1.strings.alignment.bottom,
                    ],
                    options: ["top", "middle", "bottom"],
                    label: strings_1.strings.objects.anchorY,
                    searchSection: strings_1.strings.objects.anchorAndRotation,
                }), props.alignment.y != "middle"
                    ? manager.inputNumber({ property: "alignment", field: "yMargin" }, {
                        label: strings_1.strings.margins.margin,
                        searchSection: strings_1.strings.objects.anchorAndRotation,
                    })
                    : null),
            ]),
        ]);
        return widgets.concat(parentWidgets);
    };
    IconElementClass.prototype.getTemplateParameters = function () {
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
        return {
            properties: properties,
        };
    };
    IconElementClass.classID = "mark.icon";
    IconElementClass.type = "mark";
    IconElementClass.metadata = {
        displayName: "Icon",
        iconPath: "ImagePixel",
        creatingInteraction: {
            type: "point",
            mapping: { x: "x", y: "y" },
        },
    };
    IconElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { alignment: {
            x: types_1.TextAlignmentHorizontal.Middle,
            y: types_1.TextAlignmentVertical.Top,
            xMargin: 5,
            yMargin: 5,
        }, rotation: 0, visible: true });
    IconElementClass.defaultMappingValues = {
        opacity: 1,
        size: 400,
        visible: true,
    };
    return IconElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.IconElementClass = IconElementClass;
//# sourceMappingURL=icon.js.map