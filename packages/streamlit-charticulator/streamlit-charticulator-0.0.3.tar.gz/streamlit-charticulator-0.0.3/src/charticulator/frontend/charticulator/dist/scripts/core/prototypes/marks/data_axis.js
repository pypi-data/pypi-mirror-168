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
exports.DataAxisClass = void 0;
// This implements Data-Driven Guides (straight line guide).
var mark_1 = require("./mark");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var attrs_1 = require("../attrs");
var common_1 = require("../common");
var axis_1 = require("../plot_segments/axis");
var React = require("react");
var strings_1 = require("../../../strings");
var DataAxisClass = /** @class */ (function (_super) {
    __extends(DataAxisClass, _super);
    function DataAxisClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getTickData = function (axis, manager) {
            var _a, _b;
            var table = manager.getTable((_b = (_a = _this.getPlotSegmentClass()) === null || _a === void 0 ? void 0 : _a.object) === null || _b === void 0 ? void 0 : _b.table);
            var axisExpression = manager.dataflow.cache.parse(axis.expression);
            var tickDataExpression = manager.dataflow.cache.parse(axis.tickDataExpression);
            var result = [];
            for (var i = 0; i < table.rows.length; i++) {
                var c = table.getRowContext(i);
                var axisValue = axisExpression.getValue(c);
                var tickData = tickDataExpression.getValue(c);
                result.push({ value: axisValue, tick: tickData });
            }
            return result;
        };
        return _this;
    }
    DataAxisClass.prototype.getAttributeNames = function (expr) {
        return ["anchorX" + expr.name, "anchorY" + expr.name];
    };
    Object.defineProperty(DataAxisClass.prototype, "attributeNames", {
        get: function () {
            var e_1, _a;
            var r = ["x1", "y1", "x2", "y2"];
            try {
                for (var _b = __values(this.object.properties.dataExpressions), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    var _d = __read(this.getAttributeNames(item), 2), xName = _d[0], yName = _d[1];
                    r.push(xName);
                    r.push(yName);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return r;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DataAxisClass.prototype, "attributes", {
        get: function () {
            var e_2, _a;
            var r = __assign({}, attrs_1.AttrBuilder.line());
            try {
                for (var _b = __values(this.object.properties.dataExpressions), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    var _d = __read(this.getAttributeNames(item), 2), xName = _d[0], yName = _d[1];
                    r[xName] = {
                        name: xName,
                        type: Specification.AttributeType.Number,
                    };
                    r[yName] = {
                        name: yName,
                        type: Specification.AttributeType.Number,
                    };
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_2) throw e_2.error; }
            }
            return r;
        },
        enumerable: false,
        configurable: true
    });
    DataAxisClass.prototype.buildConstraints = function (solver, context) {
        var e_3, _a;
        if (context == null) {
            return;
        }
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var _b = __read(solver.attrs(attrs, ["x1", "y1", "x2", "y2"]), 4), x1 = _b[0], y1 = _b[1], x2 = _b[2], y2 = _b[3];
        if (props.axis) {
            if (props.axis.type == "numerical") {
                try {
                    for (var _c = __values(props.dataExpressions), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var item = _d.value;
                        var _e = __read(this.getAttributeNames(item), 2), attrX = _e[0], attrY = _e[1];
                        var expr = (context.getExpressionValue(item.expression, context.rowContext));
                        var interp = axis_1.getNumericalInterpolate(props.axis);
                        var t = interp(expr);
                        if (attrs[attrX] == null) {
                            attrs[attrX] = attrs.x1;
                        }
                        if (attrs[attrY] == null) {
                            attrs[attrY] = attrs.y1;
                        }
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [t, x2],
                            [1 - t, x1],
                        ], [[1, solver.attr(attrs, attrX)]]);
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [t, y2],
                            [1 - t, y1],
                        ], [[1, solver.attr(attrs, attrY)]]);
                    }
                }
                catch (e_3_1) { e_3 = { error: e_3_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                    }
                    finally { if (e_3) throw e_3.error; }
                }
            }
        }
    };
    /** Initialize the state of an element so that everything has a valid value */
    DataAxisClass.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x1 = -10;
        attrs.y1 = -10;
        attrs.x2 = 10;
        attrs.y2 = 10;
    };
    /** Get bounding rectangle given current state */
    DataAxisClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        return [
            {
                type: "point",
                x: attrs.x1,
                y: attrs.y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
            },
            {
                type: "point",
                x: attrs.x2,
                y: attrs.y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
        ];
    };
    DataAxisClass.prototype.getGraphics = function (cs, offset, glyphIndex, manager) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var ps = this.getPlotSegmentClass();
        switch (props.visibleOn) {
            case "all":
                break;
            case "last":
                {
                    var index = ps === null || ps === void 0 ? void 0 : ps.getLastGlyphIndex();
                    if (glyphIndex != index) {
                        return null;
                    }
                }
                break;
            case "first":
            default:
                {
                    var index = ps === null || ps === void 0 ? void 0 : ps.getFirstGlyphIndex();
                    if (glyphIndex != index) {
                        return null;
                    }
                }
                break;
        }
        if (props.axis) {
            if (props.axis.visible) {
                var renderer = new axis_1.AxisRenderer();
                renderer.setAxisDataBinding(props.axis, 0, Math.sqrt((attrs.x2 - attrs.x1) * (attrs.x2 - attrs.x1) +
                    (attrs.y2 - attrs.y1) * (attrs.y2 - attrs.y1)), false, false);
                if (props.axis.tickDataExpression) {
                    try {
                        renderer.setTicksByData(this.getTickData(props.axis, manager), props.axis.tickFormat);
                    }
                    catch (ex) {
                        console.log(ex);
                    }
                }
                var g = renderer.renderLine(0, 0, (Math.atan2(attrs.y2 - attrs.y1, attrs.x2 - attrs.x1) / Math.PI) *
                    180, -1);
                g.transform = cs.getLocalTransform(attrs.x1 + offset.x, attrs.y1 + offset.y);
                return g;
            }
            else {
                return null;
            }
        }
        else {
            var renderer = new axis_1.AxisRenderer();
            renderer.setAxisDataBinding(null, 0, Math.sqrt((attrs.x2 - attrs.x1) * (attrs.x2 - attrs.x1) +
                (attrs.y2 - attrs.y1) * (attrs.y2 - attrs.y1)), false, false);
            var g = renderer.renderLine(0, 0, (Math.atan2(attrs.y2 - attrs.y1, attrs.x2 - attrs.x1) / Math.PI) * 180, -1);
            g.transform = cs.getLocalTransform(attrs.x1 + offset.x, attrs.y1 + offset.y);
            return g;
        }
    };
    DataAxisClass.prototype.getSnappingGuides = function () {
        var e_4, _a, e_5, _b, e_6, _c;
        var attrs = this.state.attributes;
        var guides = [];
        if (attrs.x1 != attrs.x2) {
            try {
                for (var _d = __values(this.object.properties.dataExpressions), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var item = _e.value;
                    var attr = this.getAttributeNames(item)[0];
                    guides.push({
                        type: "x",
                        value: attrs[attr],
                        attribute: attr,
                    });
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
        if (attrs.y1 != attrs.y2) {
            try {
                for (var _f = __values(this.object.properties.dataExpressions), _g = _f.next(); !_g.done; _g = _f.next()) {
                    var item = _g.value;
                    var attr = this.getAttributeNames(item)[1];
                    guides.push({
                        type: "y",
                        value: attrs[attr],
                        attribute: attr,
                    });
                }
            }
            catch (e_5_1) { e_5 = { error: e_5_1 }; }
            finally {
                try {
                    if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                }
                finally { if (e_5) throw e_5.error; }
            }
        }
        try {
            for (var _h = __values(this.object.properties.dataExpressions), _j = _h.next(); !_j.done; _j = _h.next()) {
                var item = _j.value;
                var _k = __read(this.getAttributeNames(item), 2), attrX = _k[0], attrY = _k[1];
                guides.push({
                    type: "label",
                    x: attrs[attrX],
                    y: attrs[attrY],
                    text: item.expression,
                });
            }
        }
        catch (e_6_1) { e_6 = { error: e_6_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
            }
            finally { if (e_6) throw e_6.error; }
        }
        return guides;
    };
    DataAxisClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        return {
            type: "line",
            x1: attrs.x1,
            y1: attrs.y1,
            x2: attrs.x2,
            y2: attrs.y2,
        };
    };
    // Get DropZones given current state
    DataAxisClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                p1: { x: x1, y: y1 },
                p2: { x: x2, y: y2 },
                title: "Data Axis",
                dropAction: {
                    axisInference: {
                        property: "axis",
                        appendToProperty: "dataExpressions",
                    },
                },
            },
        ];
    };
    DataAxisClass.prototype.getAttributePanelWidgets = function (manager) {
        var _this = this;
        var props = this.object.properties;
        var axisWidgets = axis_1.buildAxisWidgets(props.axis, "axis", manager, strings_1.strings.toolbar.dataAxis, {
            showOffset: false,
            showScrolling: false,
            showOnTop: false,
        });
        var r = __spread([
            manager.verticalGroup({
                header: strings_1.strings.objects.general,
            }, [
                manager.inputSelect({ property: "visibleOn" }, {
                    labels: [
                        strings_1.strings.objects.visibleOn.all,
                        strings_1.strings.objects.visibleOn.first,
                        strings_1.strings.objects.visibleOn.last,
                    ],
                    showLabel: true,
                    options: ["all", "first", "last"],
                    type: "dropdown",
                    label: strings_1.strings.objects.visibleOn.label,
                }),
            ])
        ], axisWidgets);
        if (props.dataExpressions.length > 0) {
            r.push(manager.verticalGroup({
                header: strings_1.strings.objects.axes.dataExpressions,
            }, [
                manager.arrayWidget({ property: "dataExpressions" }, function (item, index) {
                    var expressionInput = manager.inputExpression({
                        property: "dataExpressions",
                        field: item.field instanceof Array
                            ? __spread(item.field, ["expression"]) : [item.field, "expression"],
                    }, { table: _this.getGlyphClass().object.table });
                    return React.createElement("Fragment", { key: index }, expressionInput);
                }, {
                    allowDelete: true,
                    allowReorder: true,
                }),
            ]));
        }
        return r;
    };
    DataAxisClass.prototype.getTemplateParameters = function () {
        var _this = this;
        var props = this.object.properties;
        var dataSource = {
            table: this.getGlyphClass().object.table,
            groupBy: null,
        };
        var properties = [];
        if (this.object.properties.axis) {
            properties = properties.concat(axis_1.buildAxisProperties(this.object, "axis"));
            properties.push({
                objectID: this.object._id,
                target: {
                    property: {
                        property: "axis",
                        field: "categories",
                    },
                },
                type: Specification.AttributeType.Enum,
                default: "ascending",
            });
        }
        if (props.dataExpressions && props.dataExpressions.length > 0) {
            return {
                inferences: __spread([
                    {
                        objectID: this.object._id,
                        dataSource: dataSource,
                        axis: {
                            expression: props.dataExpressions[0].expression,
                            additionalExpressions: props.dataExpressions.map(function (x) { return x.expression; }),
                            type: props.axis.type,
                            property: "axis",
                            defineCategories: false,
                        },
                    }
                ], props.dataExpressions.map(function (x, i) {
                    return {
                        objectID: _this.object._id,
                        dataSource: dataSource,
                        expression: {
                            expression: x.expression,
                            property: {
                                property: "dataExpressions",
                                field: [i, "expression"],
                            },
                        },
                    };
                })),
                properties: properties,
            };
        }
    };
    DataAxisClass.classID = "mark.data-axis";
    DataAxisClass.type = "mark";
    DataAxisClass.metadata = {
        displayName: "DataAxis",
        iconPath: "mark/data-axis",
        creatingInteraction: {
            type: "line-segment",
            mapping: { x1: "x1", y1: "y1", x2: "x2", y2: "y2" },
        },
    };
    DataAxisClass.defaultProperties = __assign(__assign({}, common_1.ObjectClass.defaultProperties), { dataExpressions: [], axis: null, visible: true, visibleOn: "first" });
    return DataAxisClass;
}(mark_1.MarkClass));
exports.DataAxisClass = DataAxisClass;
//# sourceMappingURL=data_axis.js.map