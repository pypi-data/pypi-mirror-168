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
Object.defineProperty(exports, "__esModule", { value: true });
exports.TextboxElementClass = void 0;
var defaults_1 = require("../../../app/stores/defaults");
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var graphics_1 = require("../../graphics");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var common_2 = require("../common");
var emphasis_1 = require("./emphasis");
var textbox_attrs_1 = require("./textbox.attrs");
var TextboxElementClass = /** @class */ (function (_super) {
    __extends(TextboxElementClass, _super);
    function TextboxElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = textbox_attrs_1.textboxAttributes;
        _this.attributeNames = Object.keys(textbox_attrs_1.textboxAttributes);
        return _this;
    }
    // Initialize the state of an element so that everything has a valid value
    TextboxElementClass.prototype.initializeState = function () {
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
        attrs.text = null;
        attrs.fontFamily = defaults_1.defaultFont;
        attrs.fontSize = defaults_1.defaultFontSize;
    };
    // eslint-disable-next-line
    TextboxElementClass.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
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
            manager.verticalGroup({
                header: strings_1.strings.toolbar.text,
            }, [
                manager.mappingEditor(strings_1.strings.toolbar.text, "text", {
                    searchSection: strings_1.strings.toolbar.text,
                }),
                manager.mappingEditor(strings_1.strings.objects.font, "fontFamily", {
                    defaultValue: defaults_1.defaultFont,
                    searchSection: strings_1.strings.toolbar.text,
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
                    searchSection: strings_1.strings.toolbar.text,
                }),
            ]),
            manager.verticalGroup({
                header: strings_1.strings.objects.layout,
            }, [
                manager.inputSelect({ property: "alignX" }, {
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
                    label: strings_1.strings.objects.alignX,
                    searchSection: strings_1.strings.objects.layout,
                }),
                props.alignX != "middle"
                    ? manager.inputNumber({ property: "paddingX" }, {
                        updownTick: 1,
                        showUpdown: true,
                        label: strings_1.strings.objects.text.margin,
                        searchSection: strings_1.strings.objects.layout,
                    })
                    : null,
                manager.inputSelect({ property: "alignY" }, {
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
                    label: strings_1.strings.objects.alignX,
                    searchSection: strings_1.strings.objects.layout,
                }),
                props.alignY != "middle"
                    ? manager.inputNumber({ property: "paddingY" }, {
                        updownTick: 1,
                        showUpdown: true,
                        label: strings_1.strings.objects.text.margin,
                        searchSection: strings_1.strings.objects.layout,
                    })
                    : null,
                manager.inputBoolean({ property: "wordWrap" }, {
                    type: "checkbox",
                    headerLabel: strings_1.strings.objects.text.textDisplaying,
                    label: strings_1.strings.objects.text.wrapText,
                    searchSection: strings_1.strings.objects.layout,
                }),
                props.wordWrap
                    ? manager.inputBoolean({ property: "overFlow" }, {
                        type: "checkbox",
                        label: strings_1.strings.objects.text.overflow,
                        searchSection: strings_1.strings.objects.layout,
                    })
                    : null,
                props.wordWrap
                    ? manager.inputSelect({ property: "alignText" }, {
                        type: "radio",
                        options: ["end", "middle", "start"],
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
                        label: strings_1.strings.alignment.alignment,
                        searchSection: strings_1.strings.objects.layout,
                    })
                    : null,
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
        ];
        return widgets.concat(parentWidgets);
    };
    // Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
    TextboxElementClass.prototype.buildConstraints = function (solver) {
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
    TextboxElementClass.prototype.getGraphics = function (cs, offset, 
    // eslint-disable-next-line
    glyphIndex, 
    // eslint-disable-next-line
    manager) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        if (!attrs.text ||
            (!attrs.color && !attrs.outline) ||
            !attrs.visible ||
            attrs.opacity == 0) {
            return Graphics.makeGroup([]);
        }
        if (!attrs.backgroundColorFilterId) {
            attrs.backgroundColorFilterId = "text-color-filter-" + common_1.getRandomNumber();
        }
        var metrics = Graphics.TextMeasurer.Measure(attrs.text, attrs.fontFamily, attrs.fontSize);
        var helper = new Graphics.CoordinateSystemHelper(cs);
        var cheight = (metrics.middle - metrics.ideographicBaseline) * 2;
        var y = 0;
        switch (props.alignY) {
            case "start":
                {
                    y = attrs.y1 - metrics.ideographicBaseline + props.paddingY;
                }
                break;
            case "middle":
                {
                    y = attrs.cy - cheight / 2 - metrics.ideographicBaseline;
                }
                break;
            case "end":
                {
                    y = attrs.y2 - cheight - metrics.ideographicBaseline - props.paddingY;
                }
                break;
        }
        var textElement;
        var applyStyles = function (textElement, attrs) {
            if (attrs.outline) {
                if (attrs.color) {
                    var g = Graphics.makeGroup([
                        __assign(__assign({}, textElement), { style: {
                                strokeColor: attrs.outline,
                            } }),
                        __assign(__assign({}, textElement), { style: {
                                fillColor: attrs.color,
                            } }),
                    ]);
                    g.style = { opacity: attrs.opacity };
                    return g;
                }
                else {
                    return __assign(__assign({}, textElement), { style: {
                            strokeColor: attrs.outline,
                            opacity: attrs.opacity,
                        } });
                }
            }
            else {
                return __assign(__assign({}, textElement), { style: {
                        fillColor: attrs.color,
                        opacity: attrs.opacity,
                    } });
            }
        };
        var textContent = common_1.replaceNewLineBySymbol(attrs.text);
        if ((textContent && common_1.splitStringByNewLine(textContent).length > 1) ||
            props.wordWrap) {
            var height = attrs.fontSize;
            // set limit of lines depends of height bounding box
            var maxLines = 1000;
            // if option enabled and no space for rest of text, set limit of lines count
            if (!props.overFlow) {
                maxLines = Math.floor(Math.abs(attrs.y2 - attrs.y1) / height);
            }
            var textContentList = [textContent];
            // auto wrap text content
            if (props.wordWrap) {
                textContentList = graphics_1.splitByWidth(common_1.replaceSymbolByTab(common_1.replaceSymbolByNewLine(attrs.text)), Math.abs(attrs.x2 - attrs.x1) - 10, maxLines, attrs.fontFamily, attrs.fontSize);
            }
            // add user input wrap
            textContentList = textContentList.flatMap(function (line) {
                return common_1.splitStringByNewLine(line);
            });
            var lines = [];
            var textBoxShift = 0;
            switch (props.alignY) {
                case "start":
                    {
                        switch (props.alignText) {
                            case "start":
                                textBoxShift = -height;
                                break;
                            case "middle":
                                textBoxShift = (textContentList.length * height) / 2 - height;
                                break;
                            case "end":
                                textBoxShift = textContentList.length * height - height;
                                break;
                        }
                    }
                    break;
                case "middle":
                    {
                        switch (props.alignText) {
                            case "start":
                                textBoxShift = -height / 2;
                                break;
                            case "middle":
                                textBoxShift =
                                    (textContentList.length * height) / 2 - height / 2;
                                break;
                            case "end":
                                textBoxShift = textContentList.length * height - height / 2;
                                break;
                        }
                    }
                    break;
                case "end":
                    {
                        switch (props.alignText) {
                            case "start":
                                textBoxShift = 0;
                                break;
                            case "middle":
                                textBoxShift = (textContentList.length * height) / 2;
                                break;
                            case "end":
                                textBoxShift = textContentList.length * height;
                                break;
                        }
                    }
                    break;
            }
            for (var index = 0; index < textContentList.length; index++) {
                var pathMaker = new Graphics.PathMaker();
                helper.lineTo(pathMaker, attrs.x1 + offset.x + props.paddingX, y + offset.y + textBoxShift - height * index, attrs.x2 + offset.x - props.paddingX, y + offset.y + textBoxShift - height * index, true);
                var cmds = pathMaker.path.cmds;
                var textElement_1 = applyStyles({
                    key: index,
                    type: "text-on-path",
                    pathCmds: cmds,
                    text: textContentList[index],
                    fontFamily: attrs.fontFamily,
                    fontSize: attrs.fontSize,
                    align: props.alignX,
                }, attrs);
                lines.push(textElement_1);
            }
            return Graphics.makeGroup(lines);
        }
        else {
            var pathMaker = new Graphics.PathMaker();
            helper.lineTo(pathMaker, attrs.x1 + offset.x + props.paddingX, y + offset.y, attrs.x2 + offset.x - props.paddingX, y + offset.y, true);
            var cmds = pathMaker.path.cmds;
            textElement = {
                type: "text-on-path",
                pathCmds: cmds,
                text: attrs.text,
                fontFamily: attrs.fontFamily,
                fontSize: attrs.fontSize,
                align: props.alignX,
            };
            var background = {
                type: "rect",
                x1: attrs.x1 + offset.x,
                y1: attrs.y1 + offset.y,
                x2: attrs.x2 + offset.x,
                y2: attrs.y2 + offset.y,
                style: {
                    fillColor: attrs.backgroundColor,
                },
            };
            return Graphics.makeGroup([
                background,
                applyStyles(textElement, attrs),
            ]);
        }
    };
    /** Get link anchors for this mark */
    // eslint-disable-next-line
    TextboxElementClass.prototype.getLinkAnchors = function () {
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
    TextboxElementClass.prototype.getDropZones = function () {
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
    TextboxElementClass.prototype.getHandles = function () {
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
    TextboxElementClass.prototype.getBoundingBox = function () {
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
    TextboxElementClass.prototype.getSnappingGuides = function () {
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
    // eslint-disable-next-line
    TextboxElementClass.prototype.getTemplateParameters = function () {
        var properties = [];
        if (this.object.mappings.vistextible &&
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
        if (this.object.properties.wordWrap !== undefined) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "wordWrap",
                },
                type: Specification.AttributeType.Boolean,
                default: this.object.properties.wordWrap,
            });
        }
        return {
            properties: properties,
        };
    };
    TextboxElementClass.classID = "mark.textbox";
    TextboxElementClass.type = "mark";
    TextboxElementClass.metadata = {
        displayName: "Textbox",
        iconPath: "TextField",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    TextboxElementClass.defaultProperties = __assign(__assign({}, common_2.ObjectClass.defaultProperties), { visible: true, paddingX: 0, paddingY: 0, alignX: "middle", alignY: "middle", wordWrap: false, overFlow: true, alignText: "start" });
    TextboxElementClass.defaultMappingValues = {
        text: "Text",
        fontFamily: defaults_1.defaultFont,
        fontSize: defaults_1.defaultFontSize,
        color: { r: 0, g: 0, b: 0 },
        opacity: 1,
        visible: true,
    };
    return TextboxElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.TextboxElementClass = TextboxElementClass;
//# sourceMappingURL=textbox.js.map