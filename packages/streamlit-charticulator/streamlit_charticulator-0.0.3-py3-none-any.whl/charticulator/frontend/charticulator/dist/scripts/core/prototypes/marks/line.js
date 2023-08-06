"use strict";
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
exports.LineElementClass = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../../common");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var line_attrs_1 = require("./line.attrs");
var common_2 = require("../common");
var Graphics = require("../../graphics");
var emphasis_1 = require("./emphasis");
var strings_1 = require("../../../strings");
var LineElementClass = /** @class */ (function (_super) {
    __extends(LineElementClass, _super);
    function LineElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = line_attrs_1.lineAttributes;
        _this.attributeNames = Object.keys(line_attrs_1.lineAttributes);
        return _this;
    }
    // Initialize the state of an element so that everything has a valid value
    LineElementClass.prototype.initializeState = function () {
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
        attrs.dx = 0;
        attrs.dy = 0;
        attrs.stroke = { r: 0, g: 0, b: 0 };
        attrs.strokeWidth = 1;
        attrs.opacity = 1;
        attrs.visible = true;
    };
    /** Get link anchors for this mark */
    LineElementClass.prototype.getLinkAnchors = function (mode) {
        var attrs = this.state.attributes;
        return [
            {
                element: this.object._id,
                points: [
                    {
                        x: attrs.cx,
                        y: attrs.cy,
                        xAttribute: "cx",
                        yAttribute: "cy",
                        direction: { x: mode == "begin" ? 1 : -1, y: 0 },
                    },
                ],
            },
            {
                element: this.object._id,
                points: [
                    {
                        x: attrs.x1,
                        y: attrs.y1,
                        xAttribute: "x1",
                        yAttribute: "y1",
                        direction: { x: mode == "begin" ? 1 : -1, y: 0 },
                    },
                ],
            },
            {
                element: this.object._id,
                points: [
                    {
                        x: attrs.x2,
                        y: attrs.y2,
                        xAttribute: "x2",
                        yAttribute: "y2",
                        direction: { x: mode == "begin" ? 1 : -1, y: 0 },
                    },
                ],
            },
        ];
    };
    /** Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    LineElementClass.prototype.buildConstraints = function (solver) {
        var _a = __read(solver.attrs(this.state.attributes, ["x1", "y1", "x2", "y2", "cx", "cy", "dx", "dy"]), 8), x1 = _a[0], y1 = _a[1], x2 = _a[2], y2 = _a[3], cx = _a[4], cy = _a[5], dx = _a[6], dy = _a[7];
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cx]], [
            [1, x1],
            [1, x2],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cy]], [
            [1, y1],
            [1, y2],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, dx]], [
            [1, x2],
            [-1, x1],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, dy]], [
            [1, y2],
            [-1, y1],
        ]);
    };
    /** Get the graphical element from the element */
    LineElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager, emphasize) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        var helper = new Graphics.CoordinateSystemHelper(cs);
        return helper.line(attrs.x1 + offset.x, attrs.y1 + offset.y, attrs.x2 + offset.x, attrs.y2 + offset.y, __assign({ strokeColor: attrs.stroke, strokeOpacity: attrs.opacity, strokeWidth: attrs.strokeWidth, strokeDasharray: common_2.strokeStyleToDashArray(this.object.properties.strokeStyle) }, this.generateEmphasisStyle(emphasize)));
    };
    /** Get DropZones given current state */
    LineElementClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var cx = x1;
        var cy = y1;
        return [
            {
                type: "line",
                p1: { x: x2, y: cy },
                p2: { x: x1, y: cy },
                title: "dx",
                accept: {
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "dx",
                        attributeType: "number",
                        hints: { autoRange: true, startWithZero: "always" },
                    },
                },
            },
            {
                type: "line",
                p1: { x: cx, y: y1 },
                p2: { x: cx, y: y2 },
                title: "dy",
                accept: {
                    kind: specification_1.DataKind.Numerical,
                    table: this.parent.object.table,
                },
                dropAction: {
                    scaleInference: {
                        attribute: "dy",
                        attributeType: "number",
                        hints: { autoRange: true, startWithZero: "always" },
                    },
                },
            },
        ];
    };
    /** Get bounding rectangle given current state */
    LineElementClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2, cx = attrs.cx, cy = attrs.cy;
        return [
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
                x: x2,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
            {
                type: "point",
                x: cx,
                y: cy,
                actions: [
                    { type: "attribute", source: "x", attribute: "cx" },
                    { type: "attribute", source: "y", attribute: "cy" },
                ],
            },
        ];
    };
    LineElementClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return {
            type: "line",
            morphing: true,
            x1: x1,
            y1: y1,
            x2: x2,
            y2: y2,
        };
    };
    LineElementClass.prototype.getSnappingGuides = function () {
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
    LineElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var parentWidgets = _super.prototype.getAttributePanelWidgets.call(this, manager);
        return [
            manager.verticalGroup({
                header: strings_1.strings.toolbar.line,
            }, [
                manager.mappingEditor(strings_1.strings.objects.line.xSpan, "dx", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.toolbar.line,
                }),
                manager.mappingEditor(strings_1.strings.objects.line.ySpan, "dy", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.toolbar.line,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.toolbar.line,
                }),
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.style,
            }, [
                manager.mappingEditor(strings_1.strings.objects.stroke, "stroke", {
                    searchSection: strings_1.strings.objects.style,
                }),
                manager.mappingEditor(strings_1.strings.objects.strokeWidth, "strokeWidth", {
                    hints: { rangeNumber: [0, 5] },
                    defaultValue: 1,
                    numberOptions: {
                        showSlider: true,
                        sliderRange: [0, 10],
                        minimum: 0,
                    },
                    searchSection: strings_1.strings.objects.style,
                }),
                manager.inputSelect({ property: "strokeStyle" }, {
                    type: "dropdown",
                    showLabel: true,
                    icons: ["stroke/solid", "stroke/dashed", "stroke/dotted"],
                    isLocalIcons: true,
                    labels: [
                        strings_1.strings.objects.links.solid,
                        strings_1.strings.objects.links.dashed,
                        strings_1.strings.objects.links.dotted,
                    ],
                    options: ["solid", "dashed", "dotted"],
                    label: strings_1.strings.objects.line.lineStyle,
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
    LineElementClass.prototype.getTemplateParameters = function () {
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
        if (this.object.mappings.stroke &&
            this.object.mappings.stroke.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "stroke",
                },
                type: Specification.AttributeType.Color,
                default: this.state.attributes.stroke &&
                    common_1.rgbToHex(this.state.attributes.stroke),
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
        return {
            properties: properties,
        };
    };
    LineElementClass.classID = "mark.line";
    LineElementClass.type = "mark";
    LineElementClass.metadata = {
        displayName: "Line",
        iconPath: "Line",
        creatingInteraction: {
            type: "line-segment",
            mapping: { x1: "x1", y1: "y1", x2: "x2", y2: "y2" },
        },
    };
    LineElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { strokeStyle: "solid", visible: true });
    LineElementClass.defaultMappingValues = {
        stroke: { r: 0, g: 0, b: 0 },
        strokeWidth: 1,
        opacity: 1,
        visible: true,
    };
    return LineElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.LineElementClass = LineElementClass;
//# sourceMappingURL=line.js.map