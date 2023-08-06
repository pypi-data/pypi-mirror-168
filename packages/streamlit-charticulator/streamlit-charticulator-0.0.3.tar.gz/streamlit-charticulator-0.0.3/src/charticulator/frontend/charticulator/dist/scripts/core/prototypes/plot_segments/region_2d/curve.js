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
exports.CurvePlotSegment = exports.icons = void 0;
var Graphics = require("../../../graphics");
var solver_1 = require("../../../solver");
var Specification = require("../../../specification");
var axis_1 = require("../axis");
var base_1 = require("./base");
var plot_segment_1 = require("../plot_segment");
var strings_1 = require("../../../../strings");
exports.icons = {
    xMinIcon: "AlignHorizontalLeft",
    xMiddleIcon: "AlignHorizontalCenter",
    xMaxIcon: "AlignHorizontalRight",
    yMiddleIcon: "align/y-middle",
    yMinIcon: "Bottom",
    yMaxIcon: "Top",
    dodgeXIcon: "HorizontalDistributeCenter",
    dodgeYIcon: "VerticalDistributeCenter",
    gridIcon: "GridViewSmall",
    packingIcon: "sublayout/packing",
    jitterIcon: "sublayout/jitter",
    overlapIcon: "Stack",
};
var CurvePlotSegment = /** @class */ (function (_super) {
    __extends(CurvePlotSegment, _super);
    function CurvePlotSegment() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [
            "x1",
            "x2",
            "y1",
            "y2",
            "tangent1",
            "tangent2",
            "normal1",
            "normal2",
            "gapX",
            "gapY",
            "x",
            "y",
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
            tangent1: {
                name: "tangent1",
                type: Specification.AttributeType.Number,
            },
            tangent2: {
                name: "tangent2",
                type: Specification.AttributeType.Number,
            },
            normal1: {
                name: "normal1",
                type: Specification.AttributeType.Number,
            },
            normal2: {
                name: "normal2",
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
        };
        return _this;
    }
    CurvePlotSegment.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.tangent1 = 0;
        attrs.tangent2 = 360;
        attrs.normal1 = 10;
        attrs.normal2 = 100;
        attrs.x1 = -100;
        attrs.x2 = 100;
        attrs.y1 = -100;
        attrs.y2 = 100;
        attrs.x = attrs.x1;
        attrs.y = attrs.y2;
        attrs.gapX = 4;
        attrs.gapY = 4;
    };
    CurvePlotSegment.prototype.createBuilder = function (solver, context) {
        var config = {
            terminology: strings_1.strings.curveTerminology,
            icons: exports.icons,
            xAxisPrePostGap: false,
            yAxisPrePostGap: false,
        };
        var builder = new base_1.Region2DConstraintBuilder(this, config, "tangent1", "tangent2", "normal1", "normal2", solver, context);
        return builder;
    };
    CurvePlotSegment.prototype.getCurveArcLength = function () {
        return new Graphics.MultiCurveParametrization(this.object.properties.curve.map(function (c) { return new Graphics.BezierCurveParameterization(c[0], c[1], c[2], c[3]); })).getLength();
    };
    CurvePlotSegment.prototype.buildConstraints = function (solver, 
    // eslint-disable-next-line
    context) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var _a = __read(solver.attrs(attrs, [
            "x1",
            "y1",
            "x2",
            "y2",
            "tangent1",
            "tangent2",
            "normal1",
            "normal2",
        ]), 8), x1 = _a[0], 
        // eslint-disable-next-line
        y1 = _a[1], x2 = _a[2], 
        // eslint-disable-next-line
        y2 = _a[3], 
        // eslint-disable-next-line
        tangent1 = _a[4], tangent2 = _a[5], normal1 = _a[6], normal2 = _a[7];
        var arcLength = this.getCurveArcLength();
        attrs.tangent1 = 0;
        solver.makeConstant(attrs, "tangent1");
        // tangent2 = arcLength * (x2 - x1) / 2
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, tangent2]], [
            [arcLength / 2, x2],
            [-arcLength / 2, x1],
        ]);
        // normal1 = normalStart * (x2 - x1) / 2
        // normal2 = normalEnd * (x2 - x1) / 2
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, normal1]], [
            [props.normalStart / 2, x2],
            [-props.normalStart / 2, x1],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, normal2]], [
            [props.normalEnd / 2, x2],
            [-props.normalEnd / 2, x1],
        ]);
    };
    CurvePlotSegment.prototype.buildGlyphConstraints = function (solver, context) {
        var builder = this.createBuilder(solver, context);
        builder.build();
    };
    CurvePlotSegment.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        return {
            type: "rectangle",
            cx: (x1 + x2) / 2,
            cy: (y1 + y2) / 2,
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            rotation: 0,
        };
    };
    CurvePlotSegment.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            { type: "x", value: x1, attribute: "x1" },
            { type: "x", value: x2, attribute: "x2" },
            { type: "y", value: y1, attribute: "y1" },
            { type: "y", value: y2, attribute: "y2" },
        ];
    };
    CurvePlotSegment.prototype.getGraphics = function (manager) {
        var _a = this.state.attributes, tangent1 = _a.tangent1, tangent2 = _a.tangent2, normal1 = _a.normal1, normal2 = _a.normal2;
        var g = Graphics.makeGroup([]);
        var props = this.object.properties;
        var cs = this.getCoordinateSystem();
        if (props.xData && props.xData.visible) {
            g.elements.push(new axis_1.AxisRenderer()
                .setAxisDataBinding(props.xData, tangent1, tangent2, false, false, this.getDisplayFormat(props.xData, props.xData.tickFormat, manager))
                .renderCurve(cs, props.xData.side == "opposite" ? normal2 : normal1, props.xData.side == "opposite" ? -1 : 1));
        }
        if (props.yData && props.yData.visible) {
            var tr = cs.getLocalTransform(props.yData.side == "opposite" ? tangent2 : tangent1, 0);
            tr = Graphics.concatTransform(cs.getBaseTransform(), tr);
            g.elements.push(new axis_1.AxisRenderer()
                .setAxisDataBinding(props.yData, normal1, normal2, false, true, this.getDisplayFormat(props.yData, props.yData.tickFormat, manager))
                .renderLine(tr.x, tr.y, tr.angle + 90, props.yData.side == "opposite" ? 1 : -1));
        }
        return g;
    };
    CurvePlotSegment.prototype.getCoordinateSystem = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var cx = (x1 + x2) / 2, cy = (y1 + y2) / 2;
        var scaler = (x2 - x1) / 2;
        return new Graphics.BezierCurveCoordinates({ x: cx, y: cy }, new Graphics.MultiCurveParametrization(this.object.properties.curve.map(function (ps) {
            var p = ps.map(function (p) { return ({ x: p.x * scaler, y: p.y * scaler }); });
            return new Graphics.BezierCurveParameterization(p[0], p[1], p[2], p[3]);
        })));
    };
    CurvePlotSegment.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var zones = [];
        zones.push({
            type: "region",
            accept: { scaffolds: ["polar"] },
            dropAction: { extendPlotSegment: {} },
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Convert to Polar Coordinates",
        });
        zones.push({
            type: "region",
            accept: { scaffolds: ["cartesian-x", "cartesian-y"] },
            dropAction: { extendPlotSegment: {} },
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Convert to Cartesian Coordinates",
        });
        // zones.push(
        //     <DropZones.Line>{
        //         type: "line",
        //         p1: { x: cx + radial1, y: cy }, p2: { x: cx + radial2, y: cy },
        //         title: "Radial Axis",
        //         dropAction: {
        //             axisInference: { property: AxisPropertiesNames.yData }
        //         }
        //     }
        // );
        // zones.push(
        //     <DropZones.Arc>{
        //         type: "arc",
        //         center: { x: cx, y: cy },
        //         radius: radial2,
        //         angleStart: attrs.angle1, angleEnd: attrs.angle2,
        //         title: "Angular Axis",
        //         dropAction: {
        //             axisInference: { property: AxisPropertiesNames.xData }
        //         }
        //     }
        // );
        return zones;
    };
    CurvePlotSegment.prototype.getAxisModes = function () {
        var props = this.object.properties;
        return [
            props.xData ? props.xData.type : "null",
            props.yData ? props.yData.type : "null",
        ];
    };
    CurvePlotSegment.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        var h = [
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
            },
            {
                type: "input-curve",
                x1: x1,
                y1: y1,
                x2: x2,
                y2: y2,
                actions: [{ type: "property", property: "curve" }],
            },
        ];
        return h;
    };
    CurvePlotSegment.prototype.getPopupEditor = function (manager) {
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
    /**
     * Renders gridlines for axis. Returns empty array to diable widgets for curve plot segment.
     * Not implemented yet
     * @param data axis data binding
     * @param manager widgets manager
     * @param axisProperty property name of plotsegment with axis properties (xData, yData, axis)
     */
    CurvePlotSegment.prototype.buildGridLineWidgets = function () {
        return [];
    };
    CurvePlotSegment.prototype.getAttributePanelWidgets = function (manager) {
        var builder = this.createBuilder();
        return __spread(_super.prototype.getAttributePanelWidgets.call(this, manager), [
            manager.verticalGroup({
                header: strings_1.strings.objects.plotSegment.curveCoordinates,
            }, [
                manager.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.plotSegment.normal,
                        strings_1.strings.objects.plotSegment.curveCoordinates,
                    ],
                }, [
                    manager.label(strings_1.strings.objects.plotSegment.normal, {
                        ignoreSearch: true,
                    }),
                    manager.horizontal([1, 0, 1], manager.inputNumber({ property: "normalStart" }, { ignoreSearch: true }), manager.label("-", { ignoreSearch: true }), manager.inputNumber({ property: "normalEnd" }, { ignoreSearch: true })),
                ]),
            ])
        ], builder.buildPanelWidgets(manager));
    };
    CurvePlotSegment.prototype.getTemplateParameters = function () {
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
            p.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: base_1.PlotSegmentAxisPropertyNames.xData,
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: "ascending",
            });
        }
        if (this.object.properties.yData &&
            (this.object.properties.yData.autoDomainMin ||
                this.object.properties.yData.autoDomainMax)) {
            p.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: base_1.PlotSegmentAxisPropertyNames.yData,
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: "ascending",
            });
        }
        return { inferences: r, properties: p };
    };
    CurvePlotSegment.classID = "plot-segment.curve";
    CurvePlotSegment.type = "plot-segment";
    CurvePlotSegment.metadata = {
        displayName: "PlotSegment",
        iconPath: "plot-segment/curve",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    CurvePlotSegment.defaultProperties = {
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
        curve: [
            [
                { x: -1, y: 0 },
                { x: -0.25, y: -0.5 },
                { x: 0.25, y: 0.5 },
                { x: 1, y: 0 },
            ],
        ],
        normalStart: -0.2,
        normalEnd: 0.2,
    };
    return CurvePlotSegment;
}(plot_segment_1.PlotSegmentClass));
exports.CurvePlotSegment = CurvePlotSegment;
//# sourceMappingURL=curve.js.map