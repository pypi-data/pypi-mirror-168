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
exports.ImageElementClass = exports.imagePlaceholder = void 0;
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var image_attrs_1 = require("./image.attrs");
exports.imagePlaceholder = {
    src: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHRpdGxlPmljb25zPC90aXRsZT48cmVjdCB4PSI1LjE1MTI0IiB5PSI2LjY4NDYyIiB3aWR0aD0iMjEuNjk3NTIiIGhlaWdodD0iMTguNjEyNSIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6IzAwMDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLXdpZHRoOjAuOTI2MTg0MTE3Nzk0MDM2OXB4Ii8+PHBvbHlnb24gcG9pbnRzPSIyMC4xNSAxMi45NDMgMTMuODExIDIxLjQwNCAxMC4xNTQgMTYuNDk4IDUuMTUxIDIzLjE3NiA1LjE1MSAyNS4zMDYgMTAuODg4IDI1LjMwNiAxNi43MTkgMjUuMzA2IDI2Ljg0OSAyNS4zMDYgMjYuODQ5IDIxLjkzIDIwLjE1IDEyLjk0MyIgc3R5bGU9ImZpbGwtb3BhY2l0eTowLjI7c3Ryb2tlOiMwMDA7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLWxpbmVqb2luOnJvdW5kO3N0cm9rZS13aWR0aDowLjcwMDAwMDAwMDAwMDAwMDFweCIvPjxjaXJjbGUgY3g9IjExLjkyMDI3IiBjeT0iMTIuMzk5MjMiIHI9IjEuOTAyMTYiIHN0eWxlPSJmaWxsLW9wYWNpdHk6MC4yO3N0cm9rZTojMDAwO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2Utd2lkdGg6MC43MDAwMDAwMDAwMDAwMDAxcHgiLz48L3N2Zz4=",
    width: 100,
    height: 100,
};
var ImageElementClass = /** @class */ (function (_super) {
    __extends(ImageElementClass, _super);
    function ImageElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = image_attrs_1.imageAttributes;
        _this.attributeNames = Object.keys(image_attrs_1.imageAttributes);
        return _this;
    }
    /** Initialize the state of an element so that everything has a valid value */
    ImageElementClass.prototype.initializeState = function () {
        var defaultWidth = 30;
        var defaultHeight = 50;
        var attrs = this.state.attributes;
        attrs.x1 = -defaultWidth / 2;
        attrs.y1 = -defaultHeight / 2;
        attrs.x2 = +defaultWidth / 2;
        attrs.y2 = +defaultHeight / 2;
        attrs.cx = 0;
        attrs.cy = 0;
        attrs.width = defaultWidth;
        attrs.height = defaultHeight;
        attrs.stroke = null;
        attrs.fill = null;
        attrs.strokeWidth = 1;
        attrs.opacity = 1;
        attrs.visible = true;
        attrs.image = null;
    };
    // eslint-disable-next-line
    ImageElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var widgets = [
            manager.verticalGroup({
                header: strings_1.strings.objects.general,
            }, [
                manager.mappingEditor(strings_1.strings.objects.width, "width", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.height, "height", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.objects.general,
                }),
            ]),
            // manager.sectionHeader(strings.objects.size),
            manager.verticalGroup({
                header: strings_1.strings.toolbar.image,
            }, __spread([
                manager.mappingEditor(strings_1.strings.objects.icon.image, "image", {
                    searchSection: strings_1.strings.toolbar.image,
                }),
                manager.inputSelect({ property: "imageMode" }, {
                    type: "dropdown",
                    showLabel: true,
                    labels: [
                        strings_1.strings.objects.image.letterbox,
                        strings_1.strings.objects.image.stretch,
                    ],
                    options: ["letterbox", "stretch"],
                    label: strings_1.strings.objects.image.imageMode,
                    searchSection: strings_1.strings.toolbar.image,
                })
            ], (this.object.properties.imageMode == "letterbox"
                ? [
                    manager.searchWrapper({
                        searchPattern: [
                            strings_1.strings.alignment.align,
                            strings_1.strings.objects.icon.image,
                        ],
                    }, manager.label(strings_1.strings.alignment.align), manager.horizontal([0, 1], manager.inputSelect({ property: "alignX" }, {
                        type: "radio",
                        options: ["start", "middle", "end"],
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
                    }))),
                ]
                : []))),
            manager.verticalGroup({
                header: strings_1.strings.alignment.padding,
            }, [
                // manager.label(strings.coordinateSystem.x),
                manager.inputNumber({ property: "paddingX" }, {
                    updownTick: 1,
                    showUpdown: true,
                    label: strings_1.strings.coordinateSystem.x,
                    searchSection: strings_1.strings.alignment.padding,
                }),
                // manager.label(strings.coordinateSystem.y),
                manager.inputNumber({ property: "paddingY" }, {
                    updownTick: 1,
                    showUpdown: true,
                    label: strings_1.strings.coordinateSystem.y,
                    searchSection: strings_1.strings.alignment.padding,
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
        return widgets.concat(parentWidgets);
    };
    /**
     * Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
     * See description of {@link RectElementClass.buildConstraints} method for details. Image has the same shape, except center point.
     */
    ImageElementClass.prototype.buildConstraints = function (solver) {
        var _a = __read(solver.attrs(this.state.attributes, ["x1", "y1", "x2", "y2", "cx", "cy", "width", "height"]), 8), x1 = _a[0], y1 = _a[1], x2 = _a[2], y2 = _a[3], cx = _a[4], cy = _a[5], width = _a[6], height = _a[7];
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, x2],
            [-1, x1],
        ], [[1, width]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, y2],
            [-1, y1],
        ], [[1, height]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cx]], [
            [1, x1],
            [1, x2],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cy]], [
            [1, y1],
            [1, y2],
        ]);
    };
    // Get the graphical element from the element
    // eslint-disable-next-line
    ImageElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, empasized) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        var paddingX = props.paddingX || 0;
        var paddingY = props.paddingY || 0;
        var alignX = props.alignX || "middle";
        var alignY = props.alignY || "middle";
        var image = attrs.image || exports.imagePlaceholder;
        if (typeof image == "string") {
            // Be compatible with old version
            image = { src: image, width: 100, height: 100 };
        }
        var helper = new Graphics.CoordinateSystemHelper(cs);
        var g = Graphics.makeGroup([]);
        // If fill color is specified, draw a background rect
        if (attrs.fill) {
            g.elements.push(helper.rect(attrs.x1 + offset.x, attrs.y1 + offset.y, attrs.x2 + offset.x, attrs.y2 + offset.y, {
                strokeColor: null,
                fillColor: attrs.fill,
            }));
        }
        // Center in local coordiantes
        var cx = (attrs.x1 + attrs.x2) / 2;
        var cy = (attrs.y1 + attrs.y2) / 2;
        // Decide the width/height of the image area
        // For special coordinate systems, use the middle lines' length as width/height
        var containerWidth = common_1.Geometry.pointDistance(cs.transformPoint(attrs.x1 + offset.x, cy + offset.y), cs.transformPoint(attrs.x2 + offset.x, cy + offset.y));
        var containerHeight = common_1.Geometry.pointDistance(cs.transformPoint(cx + offset.x, attrs.y1 + offset.y), cs.transformPoint(cx + offset.x, attrs.y2 + offset.y));
        var boxWidth = Math.max(0, containerWidth - paddingX * 2);
        var boxHeight = Math.max(0, containerHeight - paddingY * 2);
        // Fit image into boxWidth x boxHeight, based on the specified option
        var imageWidth;
        var imageHeight;
        switch (props.imageMode) {
            case "stretch":
                {
                    imageWidth = boxWidth;
                    imageHeight = boxHeight;
                }
                break;
            case "letterbox":
            default:
                {
                    if (image.width / image.height > boxWidth / boxHeight) {
                        imageWidth = boxWidth;
                        imageHeight = (image.height / image.width) * boxWidth;
                    }
                    else {
                        imageHeight = boxHeight;
                        imageWidth = (image.width / image.height) * boxHeight;
                    }
                }
                break;
        }
        // Decide the anchor position (px, py) in local coordinates
        var px = cx;
        var py = cy;
        var imgX = -imageWidth / 2;
        var imgY = -imageHeight / 2;
        if (alignX == "start") {
            px = attrs.x1;
            imgX = paddingX;
        }
        else if (alignX == "end") {
            px = attrs.x2;
            imgX = -imageWidth - paddingX;
        }
        if (alignY == "start") {
            py = attrs.y1;
            imgY = paddingY;
        }
        else if (alignY == "end") {
            py = attrs.y2;
            imgY = -imageHeight - paddingY;
        }
        // Create the image element
        var gImage = Graphics.makeGroup([
            {
                type: "image",
                src: image.src,
                x: imgX,
                y: imgY,
                width: imageWidth,
                height: imageHeight,
                mode: "stretch",
                style: __assign(__assign({}, this.generateEmphasisStyle(empasized)), { colorFilter: empasized
                        ? "alpha(opacity=" + emphasis_1.DEFAULT_POWER_BI_OPACITY * 100 + ")"
                        : null }),
            },
        ]);
        gImage.transform = cs.getLocalTransform(px + offset.x, py + offset.y);
        g.elements.push(gImage);
        // If stroke color is specified, stroke a foreground rect
        if (attrs.stroke) {
            g.elements.push(helper.rect(attrs.x1 + offset.x, attrs.y1 + offset.y, attrs.x2 + offset.x, attrs.y2 + offset.y, {
                strokeColor: attrs.stroke,
                strokeWidth: attrs.strokeWidth,
                strokeLinejoin: "miter",
                fillColor: null,
            }));
        }
        // Apply the opacity
        g.style = {
            opacity: attrs.opacity,
        };
        return g;
    };
    /** Get link anchors for this mark */
    // eslint-disable-next-line
    ImageElementClass.prototype.getLinkAnchors = function () {
        var attrs = this.state.attributes;
        var element = this.object._id;
        return [
            {
                element: element,
                points: [
                    {
                        x: attrs.x1,
                        y: attrs.y1,
                        xAttribute: "x1",
                        yAttribute: "y1",
                        direction: { x: -1, y: 0 },
                    },
                    {
                        x: attrs.x1,
                        y: attrs.y2,
                        xAttribute: "x1",
                        yAttribute: "y2",
                        direction: { x: -1, y: 0 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.x2,
                        y: attrs.y1,
                        xAttribute: "x2",
                        yAttribute: "y1",
                        direction: { x: 1, y: 0 },
                    },
                    {
                        x: attrs.x2,
                        y: attrs.y2,
                        xAttribute: "x2",
                        yAttribute: "y2",
                        direction: { x: 1, y: 0 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.x1,
                        y: attrs.y1,
                        xAttribute: "x1",
                        yAttribute: "y1",
                        direction: { x: 0, y: -1 },
                    },
                    {
                        x: attrs.x2,
                        y: attrs.y1,
                        xAttribute: "x2",
                        yAttribute: "y1",
                        direction: { x: 0, y: -1 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.x1,
                        y: attrs.y2,
                        xAttribute: "x1",
                        yAttribute: "y2",
                        direction: { x: 0, y: 1 },
                    },
                    {
                        x: attrs.x2,
                        y: attrs.y2,
                        xAttribute: "x2",
                        yAttribute: "y2",
                        direction: { x: 0, y: 1 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.cx,
                        y: attrs.y1,
                        xAttribute: "cx",
                        yAttribute: "y1",
                        direction: { x: 0, y: -1 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.cx,
                        y: attrs.y2,
                        xAttribute: "cx",
                        yAttribute: "y2",
                        direction: { x: 0, y: 1 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.x1,
                        y: attrs.cy,
                        xAttribute: "x1",
                        yAttribute: "cy",
                        direction: { x: -1, y: 0 },
                    },
                ],
            },
            {
                element: element,
                points: [
                    {
                        x: attrs.x2,
                        y: attrs.cy,
                        xAttribute: "x2",
                        yAttribute: "cy",
                        direction: { x: 1, y: 0 },
                    },
                ],
            },
        ];
    };
    // Get DropZones given current state
    ImageElementClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                p1: { x: x2, y: y1 },
                p2: { x: x1, y: y1 },
                title: "width",
                accept: {
                    kind: Specification.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "width",
                        attributeType: Specification.AttributeType.Number,
                        hints: { autoRange: true, startWithZero: "always" },
                    },
                },
            },
            {
                type: "line",
                p1: { x: x1, y: y1 },
                p2: { x: x1, y: y2 },
                title: "height",
                accept: {
                    kind: Specification.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "height",
                        attributeType: Specification.AttributeType.Number,
                        hints: { autoRange: true, startWithZero: "always" },
                    },
                },
            },
        ];
    };
    // Get bounding rectangle given current state
    ImageElementClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "x1" }],
                value: x1,
                span: [y1, y2],
            },
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "x2" }],
                value: x2,
                span: [y1, y2],
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "y1" }],
                value: y1,
                span: [x1, x2],
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "y2" }],
                value: y2,
                span: [x1, x2],
            },
            {
                type: "point",
                x: x1,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
            },
            {
                type: "point",
                x: x1,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
            {
                type: "point",
                x: x2,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
            },
            {
                type: "point",
                x: x2,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
        ];
    };
    ImageElementClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return {
            type: "rectangle",
            cx: (x1 + x2) / 2,
            cy: (y1 + y2) / 2,
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            rotation: 0,
        };
    };
    ImageElementClass.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2, cx = attrs.cx, cy = attrs.cy;
        return [
            { type: "x", value: x1, attribute: "x1" },
            { type: "x", value: x2, attribute: "x2" },
            { type: "x", value: cx, attribute: "cx" },
            { type: "y", value: y1, attribute: "y1" },
            { type: "y", value: y2, attribute: "y2" },
            { type: "y", value: cy, attribute: "cy" },
        ];
    };
    ImageElementClass.prototype.getTemplateParameters = function () {
        var _a;
        var properties = [];
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
        if (this.object.mappings.visible &&
            this.object.mappings.visible.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "visible",
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.visible,
            });
        }
        if (this.object.mappings.image &&
            this.object.mappings.image.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "image",
                },
                type: Specification.AttributeType.Image,
                default: (_a = this.state.attributes.image) === null || _a === void 0 ? void 0 : _a.src,
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
        return {
            properties: properties,
        };
    };
    ImageElementClass.classID = "mark.image";
    ImageElementClass.type = "mark";
    ImageElementClass.metadata = {
        displayName: "Image",
        iconPath: "FileImage",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    ImageElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { visible: true, imageMode: "letterbox", paddingX: 0, paddingY: 0, alignX: "middle", alignY: "middle" });
    ImageElementClass.defaultMappingValues = {
        strokeWidth: 1,
        opacity: 1,
        visible: true,
    };
    return ImageElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.ImageElementClass = ImageElementClass;
//# sourceMappingURL=image.js.map