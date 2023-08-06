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
exports.PolarPlotSegment = exports.icons = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Graphics = require("../../../graphics");
var solver_1 = require("../../../solver");
var Specification = require("../../../specification");
var axis_1 = require("../axis");
var base_1 = require("./base");
var plot_segment_1 = require("../plot_segment");
var __1 = require("../../..");
var strings_1 = require("../../../../strings");
var utils_1 = require("./utils");
exports.icons = {
    xMinIcon: "AlignHorizontalLeft",
    xMiddleIcon: "AlignHorizontalCenter",
    xMaxIcon: "AlignHorizontalRight",
    yMiddleIcon: "AlignHorizontalRight",
    yMinIcon: "AlignVerticalBottom",
    yMaxIcon: "AlignVerticalTop",
    dodgeXIcon: "CharticulatorArrangePolar",
    dodgeYIcon: "CharticulatorStackRadial",
    gridIcon: "sublayout/polar-grid",
    packingIcon: "sublayout/packing",
    overlapIcon: "Stack",
    jitterIcon: "sublayout/jitter",
};
var PolarPlotSegment = /** @class */ (function (_super) {
    __extends(PolarPlotSegment, _super);
    function PolarPlotSegment() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [
            "x1",
            "x2",
            "y1",
            "y2",
            "angle1",
            "angle2",
            "radial1",
            "radial2",
            "gapX",
            "gapY",
            "x",
            "y",
            "cx",
            "cy",
            "a1r1x",
            "a1r1y",
            "a1r2x",
            "a1r2y",
            "a2r1x",
            "a2r1y",
            "a2r2x",
            "a2r2y",
        ];
        _this.attributes = {
            x1: {
                name: "x1",
                type: Specification.AttributeType.Number,
            },
            x2: {
                name: "x2",
                type: Specification.AttributeType.Number,
            },
            y1: {
                name: "y1",
                type: Specification.AttributeType.Number,
            },
            y2: {
                name: "y2",
                type: Specification.AttributeType.Number,
            },
            angle1: {
                name: "angle1",
                type: Specification.AttributeType.Number,
                defaultValue: -90,
            },
            angle2: {
                name: "angle2",
                type: Specification.AttributeType.Number,
                defaultValue: 90,
            },
            radial1: {
                name: "radial1",
                type: Specification.AttributeType.Number,
            },
            radial2: {
                name: "radial2",
                type: Specification.AttributeType.Number,
            },
            x: {
                name: "x",
                type: Specification.AttributeType.Number,
            },
            y: {
                name: "y",
                type: Specification.AttributeType.Number,
            },
            gapX: {
                name: "gapX",
                type: Specification.AttributeType.Number,
                editableInGlyphStage: true,
            },
            gapY: {
                name: "gapY",
                type: Specification.AttributeType.Number,
                editableInGlyphStage: true,
            },
            cx: {
                name: "cx",
                type: Specification.AttributeType.Number,
            },
            cy: {
                name: "cy",
                type: Specification.AttributeType.Number,
            },
            a1r1x: {
                name: "a1r1x",
                type: Specification.AttributeType.Number,
            },
            a1r1y: {
                name: "a1r1y",
                type: Specification.AttributeType.Number,
            },
            a1r2x: {
                name: "a1r2x",
                type: Specification.AttributeType.Number,
            },
            a1r2y: {
                name: "a1r2y",
                type: Specification.AttributeType.Number,
            },
            a2r1x: {
                name: "a2r1x",
                type: Specification.AttributeType.Number,
            },
            a2r1y: {
                name: "a2r1y",
                type: Specification.AttributeType.Number,
            },
            a2r2x: {
                name: "a2r2x",
                type: Specification.AttributeType.Number,
            },
            a2r2y: {
                name: "a2r2y",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    PolarPlotSegment.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.angle1 = 0;
        attrs.angle2 = 360;
        attrs.radial1 = 10;
        attrs.radial2 = 100;
        attrs.x1 = -100;
        attrs.x2 = 100;
        attrs.y1 = -100;
        attrs.y2 = 100;
        attrs.x = attrs.x1;
        attrs.y = attrs.y2;
        attrs.gapX = 4;
        attrs.gapY = 4;
        attrs.cx = 0;
        attrs.cy = 0;
        attrs.a1r1x = 0;
        attrs.a1r1y = 0;
        attrs.a1r2x = 0;
        attrs.a1r2y = 0;
        attrs.a2r1x = 0;
        attrs.a2r1y = 0;
        attrs.a2r2x = 0;
        attrs.a2r2y = 0;
    };
    PolarPlotSegment.prototype.createBuilder = function (solver, context) {
        var _this = this;
        var props = this.object.properties;
        var config = {
            terminology: strings_1.strings.polarTerminology,
            icons: exports.icons,
            xAxisPrePostGap: (props.endAngle - props.startAngle) % 360 == 0,
            yAxisPrePostGap: false,
            getXYScale: function () {
                var radiusMiddle = (_this.state.attributes.radial1 + _this.state.attributes.radial2) / 2;
                return { x: 57.29577951308232 / radiusMiddle, y: 1 };
            },
        };
        var builder = new base_1.Region2DConstraintBuilder(this, config, "angle1", "angle2", "radial1", "radial2", solver, context);
        return builder;
    };
    PolarPlotSegment.prototype.buildConstraints = function (solver, context, manager) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var _a = __read(solver.attrs(attrs, [
            "x1",
            "y1",
            "x2",
            "y2",
            "radial1",
            "radial2",
        ]), 6), x1 = _a[0], y1 = _a[1], x2 = _a[2], y2 = _a[3], innerRadius = _a[4], outerRadius = _a[5];
        attrs.angle1 = props.startAngle;
        attrs.angle2 = props.endAngle;
        solver.makeConstant(attrs, "angle1");
        solver.makeConstant(attrs, "angle2");
        var center = utils_1.getCenterByAngle(props, attrs);
        //update radii
        utils_1.setRadiiByCenter(props, attrs, center);
        if (attrs.x2 - attrs.x1 < attrs.y2 - attrs.y1) {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.innerRatio, x2],
                [-props.innerRatio, x1],
            ], [[2, innerRadius]]);
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.outerRatio, x2],
                [-props.outerRatio, x1],
            ], [[2, outerRadius]]);
        }
        else {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.innerRatio, y2],
                [-props.innerRatio, y1],
            ], [[2, innerRadius]]);
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.outerRatio, y2],
                [-props.outerRatio, y1],
            ], [[2, outerRadius]]);
        }
        solver.makeConstant(attrs, "cx");
        solver.makeConstant(attrs, "cy");
        solver.makeConstant(attrs, "a1r1x");
        solver.makeConstant(attrs, "a1r1y");
        solver.makeConstant(attrs, "a1r2x");
        solver.makeConstant(attrs, "a1r2y");
        solver.makeConstant(attrs, "a2r1x");
        solver.makeConstant(attrs, "a2r1y");
        solver.makeConstant(attrs, "a2r2x");
        solver.makeConstant(attrs, "a2r2y");
        solver.addPlugin(new solver_1.ConstraintPlugins.PolarPlotSegmentPlugin(attrs, this.parent.object.constraints, this.object._id, manager, this.object.properties));
    };
    PolarPlotSegment.prototype.buildGlyphConstraints = function (solver, context) {
        var builder = this.createBuilder(solver, context);
        builder.build();
    };
    PolarPlotSegment.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2, cx = attrs.cx, cy = attrs.cy;
        return {
            type: "rectangle",
            cx: cx,
            cy: cy,
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            rotation: 0,
        };
    };
    PolarPlotSegment.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2, cx = attrs.cx, cy = attrs.cy;
        return [
            { type: "x", value: x1, attribute: "x1" },
            { type: "x", value: x2, attribute: "x2" },
            { type: "y", value: y1, attribute: "y1" },
            { type: "y", value: y2, attribute: "y2" },
            { type: "x", value: cx, attribute: "cx" },
            { type: "y", value: cy, attribute: "cy" },
        ];
    };
    PolarPlotSegment.prototype.getGraphics = function (manager) {
        var builder = this.createBuilder();
        var g = Graphics.makeGroup([]);
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var radialData = props.yData;
        var angularData = props.xData;
        var angleStart = props.startAngle;
        var angleEnd = props.endAngle;
        var innerRadius = attrs.radial1;
        var outerRadius = attrs.radial2;
        var center = utils_1.getCenterByAngle(props, attrs);
        if (radialData && radialData.visible) {
            var axisRenderer = new axis_1.AxisRenderer();
            axisRenderer.setAxisDataBinding(radialData, innerRadius, outerRadius, false, true, this.getDisplayFormat(props.yData, props.yData.tickFormat, manager));
            g.elements.push(axisRenderer.renderLine(center.cx, center.cy, 90 - (radialData.side == "opposite" ? angleEnd : angleStart), -1));
        }
        if (angularData && angularData.visible) {
            var axisRenderer = new axis_1.AxisRenderer().setAxisDataBinding(angularData, angleStart, angleEnd, builder.config.xAxisPrePostGap, false, this.getDisplayFormat(props.xData, props.xData.tickFormat, manager));
            g.elements.push(axisRenderer.renderPolar(center.cx, center.cy, angularData.side == "opposite" ? innerRadius : outerRadius, angularData.side == "opposite" ? -1 : 1));
        }
        return g;
    };
    PolarPlotSegment.prototype.getPlotSegmentBackgroundGraphics = function (manager) {
        var g = Graphics.makeGroup([]);
        var builder = this.createBuilder();
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var radialData = props.yData;
        var angularData = props.xData;
        var angleStart = props.startAngle;
        var angleEnd = props.endAngle;
        var innerRadius = attrs.radial1;
        var outerRadius = attrs.radial2;
        var center = utils_1.getCenterByAngle(props, attrs);
        if (radialData && radialData.visible) {
            var axisRenderer = new axis_1.AxisRenderer();
            axisRenderer.setAxisDataBinding(radialData, innerRadius, outerRadius, false, true, this.getDisplayFormat(props.yData, props.yData.tickFormat, manager));
            g.elements.push(axisRenderer.renderPolarArcGridLine(center.cx, center.cy, innerRadius, outerRadius, angleStart, angleEnd));
        }
        if (angularData && angularData.visible) {
            var axisRenderer = new axis_1.AxisRenderer().setAxisDataBinding(angularData, angleStart, angleEnd, builder.config.xAxisPrePostGap, false, this.getDisplayFormat(props.xData, props.xData.tickFormat, manager));
            g.elements.push(axisRenderer.renderPolarRadialGridLine(center.cx, center.cy, innerRadius, outerRadius));
        }
        return g;
    };
    PolarPlotSegment.prototype.getCoordinateSystem = function () {
        var attrs = this.state.attributes;
        var center = utils_1.getCenterByAngle(this.object.properties, attrs);
        return new Graphics.PolarCoordinates({
            x: center.cx,
            y: center.cy,
        }, attrs.radial1, attrs.radial2, this.object.properties.equalizeArea);
    };
    PolarPlotSegment.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2, radial1 = attrs.radial1, radial2 = attrs.radial2;
        var center = utils_1.getCenterByAngle(props, attrs);
        var zones = [];
        zones.push({
            type: "region",
            accept: { scaffolds: ["polar"] },
            dropAction: { extendPlotSegment: {} },
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Add Angular Scaffold",
        });
        zones.push({
            type: "region",
            accept: { scaffolds: ["curve"] },
            dropAction: { extendPlotSegment: {} },
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Convert to Curve Coordinates",
        });
        zones.push({
            type: "region",
            accept: { scaffolds: ["cartesian-x", "cartesian-y"] },
            dropAction: { extendPlotSegment: {} },
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Convert to Cartesian Coordinates",
        });
        //update drop zone for right side
        var points = utils_1.getRadialAxisDropZoneLineCenter(center, radial1, radial2);
        zones.push({
            type: "line",
            p1: points.p1,
            p2: points.p2,
            title: "Radial Axis",
            dropAction: {
                axisInference: { property: base_1.PlotSegmentAxisPropertyNames.yData },
            },
            accept: {
                table: this.object.table,
            },
        });
        zones.push({
            type: "arc",
            center: { x: center.cx, y: center.cy },
            radius: radial2,
            angleStart: attrs.angle1,
            angleEnd: attrs.angle2,
            title: "Angular Axis",
            dropAction: {
                axisInference: { property: base_1.PlotSegmentAxisPropertyNames.xData },
            },
            accept: {
                table: this.object.table,
            },
        });
        return zones;
    };
    PolarPlotSegment.prototype.getAxisModes = function () {
        var props = this.object.properties;
        return [
            props.xData ? props.xData.type : "null",
            props.yData ? props.yData.type : "null",
        ];
    };
    // eslint-disable-next-line
    PolarPlotSegment.prototype.getHandles = function () {
        var _this = this;
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        var center = utils_1.getCenterByAngle(props, attrs);
        var radius = utils_1.getHandlesRadius(props, attrs, center);
        var builder = this.createBuilder();
        return __spread([
            {
                type: "line",
                axis: "y",
                value: y1,
                span: [x1, x2],
                actions: [{ type: "attribute", attribute: "y1" }],
            },
            {
                type: "line",
                axis: "y",
                value: y2,
                span: [x1, x2],
                actions: [{ type: "attribute", attribute: "y2" }],
            },
            {
                type: "line",
                axis: "x",
                value: x1,
                span: [y1, y2],
                actions: [{ type: "attribute", attribute: "x1" }],
            },
            {
                type: "line",
                axis: "x",
                value: x2,
                span: [y1, y2],
                actions: [{ type: "attribute", attribute: "x2" }],
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
                x: x2,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
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
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            }
        ], builder.getHandles().map(function (handle) {
            return {
                type: "gap-ratio",
                axis: handle.gap.axis,
                reference: handle.gap.reference,
                value: handle.gap.value,
                scale: handle.gap.scale,
                span: handle.gap.span,
                range: [0, 1],
                coordinateSystem: _this.getCoordinateSystem(),
                actions: [
                    {
                        type: "property",
                        property: handle.gap.property.property,
                        field: handle.gap.property.field,
                    },
                ],
            };
        }), [
            {
                type: "angle",
                actions: [{ type: "property", property: "endAngle" }],
                cx: center.cx,
                cy: center.cy,
                radius: radius * Math.max(props.innerRatio, props.outerRatio),
                value: props.endAngle,
                clipAngles: [props.startAngle, null],
                icon: "<",
            },
            {
                type: "angle",
                actions: [{ type: "property", property: "startAngle" }],
                cx: center.cx,
                cy: center.cy,
                radius: radius * Math.max(props.innerRatio, props.outerRatio),
                value: props.startAngle,
                clipAngles: [null, props.endAngle],
                icon: ">",
            },
            {
                type: "distance-ratio",
                actions: [{ type: "property", property: "outerRatio" }],
                cx: center.cx,
                cy: center.cy,
                value: props.outerRatio,
                startDistance: 0,
                endDistance: radius,
                startAngle: props.startAngle,
                endAngle: props.endAngle,
                clipRange: [props.innerRatio + 0.01, 1],
            },
            {
                type: "distance-ratio",
                actions: [{ type: "property", property: "innerRatio" }],
                cx: center.cx,
                cy: center.cy,
                value: props.innerRatio,
                startDistance: 0,
                endDistance: radius,
                startAngle: props.startAngle,
                endAngle: props.endAngle,
                clipRange: [0, props.outerRatio - 0.01],
            },
        ]);
    };
    PolarPlotSegment.prototype.getPopupEditor = function (manager) {
        var builder = this.createBuilder();
        var widgets = builder.buildPopupWidgets(manager);
        if (widgets.length == 0) {
            return null;
        }
        var attrs = this.state.attributes;
        var anchor = { x: attrs.x1, y: attrs.y2 };
        return {
            anchor: anchor,
            widgets: __spread(widgets),
        };
    };
    PolarPlotSegment.prototype.getAttributePanelWidgets = function (manager) {
        var builder = this.createBuilder();
        return __spread(_super.prototype.getAttributePanelWidgets.call(this, manager), [
            manager.verticalGroup({
                header: strings_1.strings.objects.plotSegment.polarCoordinates,
            }, [
                manager.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.plotSegment.polarCoordinates,
                        strings_1.strings.objects.plotSegment.angle,
                    ],
                }, [
                    manager.label(strings_1.strings.objects.plotSegment.angle, {
                        ignoreSearch: true,
                    }),
                    manager.horizontal([1, 0, 1], manager.inputNumber({ property: "startAngle" }, { ignoreSearch: true }), manager.label("-", { ignoreSearch: true }), manager.inputNumber({ property: "endAngle" }, { ignoreSearch: true })),
                ]),
                manager.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.plotSegment.polarCoordinates,
                        strings_1.strings.objects.plotSegment.radius,
                        strings_1.strings.objects.plotSegment.inner,
                        strings_1.strings.objects.plotSegment.outer,
                    ],
                }, [
                    manager.label(strings_1.strings.objects.plotSegment.radius, {
                        ignoreSearch: true,
                    }),
                    manager.horizontal([0, 1, 0, 1], manager.label(strings_1.strings.objects.plotSegment.inner, {
                        ignoreSearch: true,
                    }), manager.inputNumber({ property: "innerRatio" }, { ignoreSearch: true }), manager.label(strings_1.strings.objects.plotSegment.outer, {
                        ignoreSearch: true,
                    }), manager.inputNumber({ property: "outerRatio" }, { maximum: 1, ignoreSearch: true })),
                ]),
                manager.inputBoolean({ property: "autoAlignment" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.plotSegment.autoAlignment,
                    headerLabel: strings_1.strings.objects.plotSegment.origin,
                    searchSection: strings_1.strings.objects.plotSegment.polarCoordinates,
                }),
                manager.inputBoolean({ property: "equalizeArea" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.plotSegment.heightToArea,
                    headerLabel: strings_1.strings.objects.plotSegment.equalizeArea,
                    searchSection: strings_1.strings.objects.plotSegment.polarCoordinates,
                }),
            ])
        ], builder.buildPanelWidgets(manager));
    };
    PolarPlotSegment.prototype.getTemplateParameters = function () {
        var r = [];
        var p = [];
        if (this.object.properties.xData) {
            r.push(axis_1.buildAxisInference(this.object, base_1.PlotSegmentAxisPropertyNames.xData));
            p = p.concat(axis_1.buildAxisProperties(this.object, base_1.PlotSegmentAxisPropertyNames.xData));
        }
        if (this.object.properties.yData) {
            r.push(axis_1.buildAxisInference(this.object, base_1.PlotSegmentAxisPropertyNames.yData));
            p = p.concat(axis_1.buildAxisProperties(this.object, base_1.PlotSegmentAxisPropertyNames.yData));
        }
        if (this.object.properties.sublayout.order &&
            this.object.properties.sublayout.order.expression) {
            r.push({
                objectID: this.object._id,
                dataSource: {
                    table: this.object.table,
                    groupBy: this.object.groupBy,
                },
                expression: {
                    expression: this.object.properties.sublayout.order.expression,
                    property: { property: "sublayout", field: ["order", "expression"] },
                },
            });
        }
        if (this.object.properties.xData &&
            (this.object.properties.xData.autoDomainMin ||
                this.object.properties.xData.autoDomainMax)) {
            var values = this.object.properties.xData.categories;
            var defaultValue = __1.getSortDirection(values);
            p.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: base_1.PlotSegmentAxisPropertyNames.xData,
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: defaultValue,
            });
        }
        if (this.object.properties.yData &&
            (this.object.properties.yData.autoDomainMin ||
                this.object.properties.yData.autoDomainMax)) {
            var values = this.object.properties.yData.categories;
            var defaultValue = __1.getSortDirection(values);
            p.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: base_1.PlotSegmentAxisPropertyNames.yData,
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: defaultValue,
            });
        }
        return { inferences: r, properties: p };
    };
    PolarPlotSegment.classID = "plot-segment.polar";
    PolarPlotSegment.type = "plot-segment";
    PolarPlotSegment.metadata = {
        displayName: "PlotSegment",
        iconPath: "plot-segment/polar",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    PolarPlotSegment.defaultProperties = {
        marginX1: 0,
        marginY1: 0,
        marginX2: 0,
        marginY2: 0,
        visible: true,
        sublayout: {
            type: base_1.Region2DSublayoutType.DodgeX,
            order: null,
            ratioX: 0.1,
            ratioY: 0.1,
            align: {
                x: "start",
                y: "start",
            },
            grid: {
                direction: base_1.GridDirection.X,
                xCount: null,
                yCount: null,
                gridStartPosition: base_1.GridStartPosition.LeftTop,
            },
        },
        startAngle: 0,
        endAngle: 360,
        innerRatio: 0.5,
        outerRatio: 0.9,
        autoAlignment: false,
    };
    return PolarPlotSegment;
}(plot_segment_1.PlotSegmentClass));
exports.PolarPlotSegment = PolarPlotSegment;
//# sourceMappingURL=polar.js.map