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
exports.RectElementClass = exports.ShapeType = void 0;
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var rect_attrs_1 = require("./rect.attrs");
var strings_1 = require("../../../strings");
var types_1 = require("../legends/types");
var graphics_1 = require("../../graphics");
var ShapeType;
(function (ShapeType) {
    ShapeType["Rectangle"] = "rectangle";
    ShapeType["Triangle"] = "triangle";
    ShapeType["Ellips"] = "ellipse";
})(ShapeType = exports.ShapeType || (exports.ShapeType = {}));
var RectElementClass = /** @class */ (function (_super) {
    __extends(RectElementClass, _super);
    function RectElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = rect_attrs_1.rectAttributes;
        _this.attributeNames = Object.keys(rect_attrs_1.rectAttributes);
        return _this;
    }
    // Initialize the state of an element so that everything has a valid value
    RectElementClass.prototype.initializeState = function () {
        _super.prototype.initializeState.call(this);
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
        attrs.fill = { r: 200, g: 200, b: 200 };
        attrs.strokeWidth = 1;
        attrs.opacity = 1;
        attrs.visible = true;
    };
    RectElementClass.prototype.getTemplateParameters = function () {
        var properties = [];
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
            properties.push({
                objectID: this.object._id,
                target: {
                    property: "strokeStyle",
                },
                type: Specification.AttributeType.Enum,
                default: this.object.properties.strokeStyle,
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
        properties.push({
            objectID: this.object._id,
            target: {
                property: "rx",
            },
            type: Specification.AttributeType.Number,
            default: 0,
        });
        properties.push({
            objectID: this.object._id,
            target: {
                property: "ry",
            },
            type: Specification.AttributeType.Number,
            default: 0,
        });
        return {
            properties: properties,
        };
    };
    RectElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var widgets = [
            manager.verticalGroup({
                header: strings_1.strings.objects.general,
            }, [
                manager.mappingEditor(strings_1.strings.objects.width, "width", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [specification_1.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.mappingEditor(strings_1.strings.objects.height, "height", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [specification_1.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.inputSelect({ property: "shape" }, {
                    type: "dropdown",
                    showLabel: true,
                    label: strings_1.strings.objects.rect.shape,
                    icons: ["RectangleShape", "TriangleShape", "Ellipse"],
                    labels: [
                        strings_1.strings.objects.rect.shapes.rectangle,
                        strings_1.strings.objects.rect.shapes.triangle,
                        strings_1.strings.objects.rect.shapes.ellipse,
                    ],
                    options: [
                        ShapeType.Rectangle,
                        ShapeType.Triangle,
                        ShapeType.Ellips,
                    ],
                    searchSection: strings_1.strings.objects.general,
                }),
                manager.inputBoolean({ property: "allowFlipping" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.rect.flipping,
                    searchSection: strings_1.strings.objects.general,
                    styles: {
                        marginTop: 5,
                    },
                }),
                this.object.properties.shape === ShapeType.Triangle
                    ? manager.inputBoolean({ property: "cometMark" }, {
                        type: "checkbox",
                        label: strings_1.strings.objects.rect.shapes.comet,
                        styles: {
                            marginTop: 5,
                        },
                        searchSection: strings_1.strings.objects.general,
                    })
                    : null,
                this.object.properties.shape === ShapeType.Triangle
                    ? manager.inputSelect({ property: "orientation" }, {
                        type: "radio",
                        showLabel: false,
                        icons: ["GripperBarVertical", "GripperBarHorizontal"],
                        labels: [
                            strings_1.strings.objects.legend.vertical,
                            strings_1.strings.objects.legend.horizontal,
                        ],
                        options: [
                            types_1.OrientationType.VERTICAL,
                            types_1.OrientationType.HORIZONTAL,
                        ],
                        label: strings_1.strings.objects.legend.orientation,
                        searchSection: strings_1.strings.objects.general,
                    })
                    : null,
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
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
                this.object.mappings.stroke != null
                    ? manager.inputSelect({ property: "strokeStyle" }, {
                        type: "dropdown",
                        showLabel: true,
                        label: strings_1.strings.objects.line.lineStyle,
                        icons: ["line", "stroke/dashed", "stroke/dotted"],
                        isLocalIcons: true,
                        labels: [
                            strings_1.strings.objects.links.solid,
                            strings_1.strings.objects.links.dashed,
                            strings_1.strings.objects.links.dotted,
                        ],
                        options: ["solid", "dashed", "dotted"],
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
                this.object.properties.shape === ShapeType.Rectangle
                    ? manager.inputNumber({
                        property: "rx",
                    }, {
                        label: strings_1.strings.objects.roundX,
                        showUpdown: true,
                        updownTick: 1,
                        minimum: 0,
                        searchSection: strings_1.strings.objects.style,
                    })
                    : null,
                this.object.properties.shape === ShapeType.Rectangle
                    ? manager.inputNumber({
                        property: "ry",
                    }, {
                        label: strings_1.strings.objects.roundY,
                        showUpdown: true,
                        updownTick: 1,
                        minimum: 0,
                        searchSection: strings_1.strings.objects.style,
                    })
                    : null,
            ]),
        ];
        widgets = widgets.concat(parentWidgets);
        return widgets;
    };
    /**
     * Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
     *   -------------- y1
     *   |            |     |
     *   |      *     | yc  height
     *   |            |     |
     *   -------------- y2
     *  x1     xc     x2
     *  <----width---->
     */
    RectElementClass.prototype.buildConstraints = function (solver) {
        // take variables for attributes
        var _a = __read(solver.attrs(this.state.attributes, ["x1", "y1", "x2", "y2", "cx", "cy", "width", "height"]), 8), x1 = _a[0], y1 = _a[1], x2 = _a[2], y2 = _a[3], cx = _a[4], cy = _a[5], width = _a[6], height = _a[7];
        // Describes intrinsic relations of reactangle
        // add constraint x2 - x1 = width
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, x2],
            [-1, x1],
        ], [[1, width]]);
        // add constraint y2 - y1 = height
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, y2],
            [-1, y1],
        ], [[1, height]]);
        // add constraint x1 + x2 = 2 * xc
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cx]], [
            [1, x1],
            [1, x2],
        ]);
        // add constraint y1 + y2 = 2 * yc
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cy]], [
            [1, y1],
            [1, y2],
        ]);
        if (!this.object.properties.allowFlipping &&
            this.object.properties.allowFlipping !== undefined) {
            // Additional constraint to prevent flipping mark objects
            // add constraint x2 >= x1
            solver.addSoftInequality(solver_1.ConstraintStrength.WEAKER, 0, [[1, x2]], [[1, x1]]);
            // add constraint y2 >= y1
            solver.addSoftInequality(solver_1.ConstraintStrength.WEAKER, 0, [[1, y2]], [[1, y1]]);
        }
    };
    // Get the graphical element from the element
    RectElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, empasized) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        var properties = this.object.properties;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        var helper = new Graphics.CoordinateSystemHelper(cs);
        switch (this.object.properties.shape) {
            case ShapeType.Ellips: {
                return helper.ellipse(attrs.x1 + offset.x, attrs.y1 + offset.y, attrs.x2 + offset.x, attrs.y2 + offset.y, __assign({ strokeColor: attrs.stroke, strokeWidth: attrs.strokeWidth, strokeLinejoin: "miter", strokeDasharray: common_2.strokeStyleToDashArray(this.object.properties.strokeStyle), fillColor: attrs.fill, opacity: attrs.opacity }, this.generateEmphasisStyle(empasized)));
            }
            case ShapeType.Triangle: {
                var path = this.drawTriangleOrCometMarks(helper, offset, empasized);
                return path;
            }
            case ShapeType.Rectangle:
            default: {
                return helper.rect(attrs.x1 + offset.x, attrs.y1 + offset.y, attrs.x2 + offset.x, attrs.y2 + offset.y, __assign({ strokeColor: attrs.stroke, strokeWidth: attrs.strokeWidth, strokeLinejoin: "miter", strokeDasharray: common_2.strokeStyleToDashArray(this.object.properties.strokeStyle), fillColor: attrs.fill, opacity: attrs.opacity }, this.generateEmphasisStyle(empasized)), properties.rx, properties.ry);
            }
        }
    };
    /** Get link anchors for this mark */
    // eslint-disable-next-line
    RectElementClass.prototype.getLinkAnchors = function () {
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
    RectElementClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                p1: { x: x2, y: y1 },
                p2: { x: x1, y: y1 },
                title: "width",
                accept: {
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "width",
                        attributeType: specification_1.AttributeType.Number,
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
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "height",
                        attributeType: specification_1.AttributeType.Number,
                        hints: { autoRange: true, startWithZero: "always" },
                    },
                },
            },
        ];
    };
    // Get bounding rectangle given current state
    RectElementClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "x1" }],
                value: x1,
                span: [y1, y2],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "x2" }],
                value: x2,
                span: [y1, y2],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "y1" }],
                value: y1,
                span: [x1, x2],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "y2" }],
                value: y2,
                span: [x1, x2],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "point",
                x: x1,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "point",
                x: x1,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
                options: {
                    snapToClosestPoint: true,
                },
            },
            {
                type: "point",
                x: x2,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y1" },
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
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
                options: {
                    snapToClosestPoint: true,
                },
            },
        ];
    };
    RectElementClass.prototype.getBoundingBox = function () {
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
    RectElementClass.prototype.getSnappingGuides = function () {
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
    RectElementClass.prototype.drawTriangleOrCometMarks = function (helper, offset, empasized) {
        var pathMaker = new Graphics.PathMaker();
        var properties = this.object.properties;
        var attrs = this.state.attributes;
        // normalized coordinates
        var x1 = attrs.x1 + offset.x;
        var x2 = attrs.x2 + offset.x;
        var y1 = attrs.y1 + offset.y;
        var y2 = attrs.y2 + offset.y;
        var halfYWidth = Math.abs(y1 - y2) / 2;
        var halfXWidth = Math.abs(x1 - x2) / 2;
        var minHalfWidth = Math.min(halfYWidth, halfXWidth);
        if (properties.orientation == types_1.OrientationType.HORIZONTAL &&
            helper.coordinateSystem instanceof graphics_1.CartesianCoordinates) {
            var xPosition = x1;
            if (properties.cometMark == true) {
                pathMaker.moveTo(xPosition, Math.max(y1, y2));
                helper.arcTo(pathMaker, minHalfWidth, halfYWidth, xPosition, Math.max(y1, y2), xPosition, Math.min(y1, y2), x2 > x1 ? 0 : 1);
                helper.lineTo(pathMaker, xPosition, Math.max(y1, y2), x2, (y1 + y2) / 2, false);
            }
            else {
                helper.lineTo(pathMaker, x1, y1, x1, y2, true);
                helper.lineTo(pathMaker, x1, y2, x2, (y1 + y2) / 2, false);
            }
        }
        else {
            if (properties.cometMark == true &&
                helper.coordinateSystem instanceof graphics_1.CartesianCoordinates) {
                var yPosition = y1;
                pathMaker.moveTo(Math.max(x1, x2), yPosition);
                helper.arcTo(pathMaker, halfXWidth, minHalfWidth, Math.max(x1, x2), yPosition, Math.min(x1, x2), yPosition, y2 > y1 ? 1 : 0);
                helper.lineTo(pathMaker, Math.max(x1, x2), yPosition, (x1 + x2) / 2, y2, false);
            }
            else {
                helper.lineTo(pathMaker, x1, y1, (x1 + x2) / 2, y2, true);
                helper.lineTo(pathMaker, (x1 + x2) / 2, y2, x2, y1, false);
            }
        }
        pathMaker.closePath();
        var path = pathMaker.path;
        path.style = __assign({ strokeColor: attrs.stroke, strokeWidth: attrs.strokeWidth, strokeLinejoin: "miter", strokeDasharray: common_2.strokeStyleToDashArray(properties.strokeStyle), fillColor: attrs.fill, opacity: attrs.opacity }, this.generateEmphasisStyle(empasized));
        return path;
    };
    RectElementClass.classID = "mark.rect";
    RectElementClass.type = "mark";
    RectElementClass.metadata = {
        displayName: "Shape",
        iconPath: "RectangleShape",
        creatingInteraction: {
            type: ShapeType.Rectangle,
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    RectElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { visible: true, strokeStyle: "solid", shape: ShapeType.Rectangle, allowFlipping: true, rx: 0, ry: 0, orientation: types_1.OrientationType.VERTICAL, cometMark: false });
    RectElementClass.defaultMappingValues = {
        fill: { r: 17, g: 141, b: 255 },
        strokeWidth: 1,
        opacity: 1,
        visible: true,
    };
    return RectElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.RectElementClass = RectElementClass;
//# sourceMappingURL=rect.js.map