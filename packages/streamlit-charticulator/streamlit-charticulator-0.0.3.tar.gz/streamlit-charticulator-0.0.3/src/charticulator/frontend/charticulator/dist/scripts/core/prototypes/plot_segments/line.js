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
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.LineGuide = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Graphics = require("../../graphics");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var axis_1 = require("./axis");
var plot_segment_1 = require("./plot_segment");
var __1 = require("../..");
var LineGuide = /** @class */ (function (_super) {
    __extends(LineGuide, _super);
    function LineGuide() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["x1", "x2", "y1", "y2"];
        _this.attributes = {
            x1: {
                name: "x1",
                type: Specification.AttributeType.Number,
            },
            y1: {
                name: "y1",
                type: Specification.AttributeType.Number,
            },
            x2: {
                name: "x2",
                type: Specification.AttributeType.Number,
            },
            y2: {
                name: "y2",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    LineGuide.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x1 = -100;
        attrs.x2 = 100;
        attrs.y1 = -100;
        attrs.y2 = 100;
    };
    /**
     * Creates constraints for elements on the line plot segment
     * Line plot segment distributes the elements on the line
     *  (y1 and y2 can have different values, so line can have some angle between line and axis lines)
     *  *
     *  y1 *------#------#------* y2
     *    x1      t      t      x2
     *
     * # - some element on line
     * t - position of the element on line
     */
    LineGuide.prototype.buildGlyphConstraints = function (solver) {
        var e_1, _a;
        var props = this.object.properties;
        var rows = this.parent.dataflow.getTable(this.object.table);
        // take variables for attributes
        var _b = __read(solver.attrs(this.state.attributes, [
            "x1",
            "y1",
            "x2",
            "y2",
        ]), 4), x1 = _b[0], y1 = _b[1], x2 = _b[2], y2 = _b[3];
        var count = this.state.dataRowIndices.length;
        var dataIndices = this.state.dataRowIndices;
        try {
            for (var _c = __values(this.state.glyphs.entries()), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), index = _e[0], markState = _e[1];
                // describes position of points on line (proportions)
                var t = (0.5 + index) / count;
                if (props.axis == null) {
                    t = (0.5 + index) / count;
                }
                else {
                    var data = props.axis;
                    switch (data.type) {
                        case "numerical":
                            {
                                var row = rows.getGroupedContext(dataIndices[index]);
                                var expr = this.parent.dataflow.cache.parse(data.expression);
                                var value = expr.getNumberValue(row);
                                var interp = axis_1.getNumericalInterpolate(data);
                                t = interp(value);
                            }
                            break;
                        case "categorical":
                            {
                                var axis = axis_1.getCategoricalAxis(props.axis, false, false);
                                var row = rows.getGroupedContext(dataIndices[index]);
                                var expr = this.parent.dataflow.cache.parse(data.expression);
                                var value = expr.getStringValue(row);
                                var i = data.categories.indexOf(value);
                                t = (axis.ranges[i][0] + axis.ranges[i][1]) / 2;
                            }
                            break;
                        case "default":
                            {
                                t = (0.5 + index) / count;
                            }
                            break;
                    }
                }
                // t is position of elements on line
                // add constraint t*x2 + (1 - t) * x1 = x
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [t, x2],
                    [1 - t, x1],
                ], [[1, solver.attr(markState.attributes, "x")]]);
                // add constraint t*y2 + (1 - t) * y1 = y
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [t, y2],
                    [1 - t, y1],
                ], [[1, solver.attr(markState.attributes, "y")]]);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    LineGuide.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var zones = [];
        zones.push({
            type: "line",
            p1: { x: x1, y: y1 },
            p2: { x: x2, y: y2 },
            title: "Axis",
            dropAction: {
                axisInference: { property: "axis" },
            },
            accept: {
                table: this.object.table,
            },
        });
        return zones;
    };
    LineGuide.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
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
        ];
    };
    LineGuide.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        return {
            type: "line",
            x1: x1,
            y1: y1,
            x2: x2,
            y2: y2,
        };
    };
    LineGuide.prototype.getGraphics = function (manager) {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var props = this.object.properties;
        var length = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
        if (props.axis == null) {
            return Graphics.makeLine(x1, y1, x2, y2, {
                strokeColor: { r: 0, g: 0, b: 0 },
                fillColor: null,
            });
        }
        if (props.axis && props.axis.visible) {
            var renderer = new axis_1.AxisRenderer();
            renderer.setAxisDataBinding(props.axis, 0, length, false, false, this.getDisplayFormat(props.axis, props.axis.tickFormat, manager));
            var g = renderer.renderLine(x1, y1, (Math.atan2(y2 - y1, x2 - x1) / Math.PI) * 180, 1);
            return g;
        }
    };
    LineGuide.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        return __spread(_super.prototype.getAttributePanelWidgets.call(this, manager), axis_1.buildAxisWidgets(props.axis, "axis", manager, "Axis", {
            showScrolling: false,
            showOffset: false,
            showOnTop: false,
        }));
    };
    /**
     * Renders gridlines for axis. Returns empty array to diable widgets for line plot segment.
     * Not implemented yet
     * @param data axis data binding
     * @param manager widgets manager
     * @param axisProperty property name of plotsegment with axis properties (xData, yData, axis)
     */
    LineGuide.prototype.buildGridLineWidgets = function () {
        return [];
    };
    LineGuide.prototype.getTemplateParameters = function () {
        var r = [];
        var p = [];
        if (this.object.properties.axis) {
            r.push(axis_1.buildAxisInference(this.object, "axis"));
            p = p.concat(axis_1.buildAxisProperties(this.object, "axis"));
        }
        if (this.object.properties.axis &&
            (this.object.properties.axis.autoDomainMin ||
                this.object.properties.axis.autoDomainMax)) {
            var values = this.object.properties.axis.categories;
            var defaultValue = __1.getSortDirection(values);
            p.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: "axis",
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: defaultValue,
            });
        }
        return { inferences: r, properties: p };
    };
    LineGuide.classID = "plot-segment.line";
    LineGuide.type = "plot-segment";
    LineGuide.metadata = {
        displayName: "PlotSegment",
        iconPath: "plot-segment/line",
        creatingInteraction: {
            type: "line-segment",
            mapping: { x1: "x1", y1: "y1", x2: "x2", y2: "y2" },
        },
    };
    LineGuide.defaultProperties = {
        visible: true,
    };
    return LineGuide;
}(plot_segment_1.PlotSegmentClass));
exports.LineGuide = LineGuide;
//# sourceMappingURL=line.js.map