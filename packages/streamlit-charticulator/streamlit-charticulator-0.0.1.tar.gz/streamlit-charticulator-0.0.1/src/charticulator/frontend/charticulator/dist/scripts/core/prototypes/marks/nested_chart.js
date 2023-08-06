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
exports.NestedChartElementClass = void 0;
var common_1 = require("../../common");
var dataset_1 = require("../../dataset");
var Graphics = require("../../graphics");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var emphasis_1 = require("./emphasis");
var nested_chart_attrs_1 = require("./nested_chart.attrs");
var base_1 = require("../plot_segments/region_2d/base");
var strings_1 = require("../../../strings");
var NestedChartElementClass = /** @class */ (function (_super) {
    __extends(NestedChartElementClass, _super);
    function NestedChartElementClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributes = nested_chart_attrs_1.nestedChartAttributes;
        _this.attributeNames = Object.keys(nested_chart_attrs_1.nestedChartAttributes);
        return _this;
    }
    // Initialize the state of an element so that everything has a valid value
    NestedChartElementClass.prototype.initializeState = function () {
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
        attrs.visible = true;
    };
    NestedChartElementClass.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.verticalGroup({ header: strings_1.strings.objects.nestedChart.sizeAndShape }, [
                manager.mappingEditor(strings_1.strings.objects.width, "width", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.nestedChart.sizeAndShape,
                }),
                manager.mappingEditor(strings_1.strings.objects.height, "height", {
                    hints: { autoRange: true, startWithZero: "always" },
                    acceptKinds: [Specification.DataKind.Numerical],
                    defaultAuto: true,
                    searchSection: strings_1.strings.objects.nestedChart.sizeAndShape,
                }),
                manager.mappingEditor(strings_1.strings.objects.visibleOn.visibility, "visible", {
                    defaultValue: true,
                    searchSection: strings_1.strings.objects.nestedChart.sizeAndShape,
                }),
                manager.nestedChartEditor({ property: "specification" }, {
                    specification: this.object.properties.specification,
                    dataset: this.getDataset(0),
                    // filterCondition: this.getFilterCondition(),
                    width: this.state.attributes.width,
                    height: this.state.attributes.height,
                    searchSection: strings_1.strings.objects.nestedChart.sizeAndShape,
                }),
            ]),
        ];
    };
    // Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
    NestedChartElementClass.prototype.buildConstraints = function (solver) {
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
    NestedChartElementClass.prototype.getFilterCondition = function () {
        var glyphIndex = 0;
        var manager = this.getChartClass().manager;
        var plotSegmentClass = this.getPlotSegmentClass();
        var table = common_1.getByName(manager.dataset.tables, plotSegmentClass.object.table);
        var rowIndex = plotSegmentClass.state.dataRowIndices[glyphIndex][0];
        var data = table.rows[rowIndex];
        return plotSegmentClass.object.groupBy
            ? {
                column: plotSegmentClass.object.groupBy.expression,
                value: data[plotSegmentClass.object.groupBy.expression],
            }
            : null;
    };
    NestedChartElementClass.prototype.getDataset = function (glyphIndex) {
        var e_1, _a, e_2, _b;
        var manager = this.getChartClass().manager;
        var plotSegmentClass = this.getPlotSegmentClass();
        var table = common_1.getByName(manager.dataset.tables, plotSegmentClass.object.table);
        var columnNameMap = this.object.properties.columnNameMap;
        if (table.columns.length === Object.keys(columnNameMap).length) {
            if (columnNameMap == null) {
                columnNameMap = {};
                try {
                    for (var _c = __values(table.columns), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var c = _d.value;
                        columnNameMap[c.name] = c.name;
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
                this.object.properties.columnNameMap = columnNameMap;
            }
        }
        else {
            //update columns
            columnNameMap = {};
            try {
                for (var _e = __values(table.columns), _f = _e.next(); !_f.done; _f = _e.next()) {
                    var c = _f.value;
                    columnNameMap[c.name] = c.name;
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                }
                finally { if (e_2) throw e_2.error; }
            }
            this.object.properties.columnNameMap = columnNameMap;
        }
        var dataRowIndices = plotSegmentClass.state.dataRowIndices[glyphIndex];
        var mapToRows = function (dataRowIndices) {
            return dataRowIndices.map(function (i) {
                var data = table.rows[i];
                var r = { _id: data._id };
                for (var col in columnNameMap) {
                    r[columnNameMap[col]] = data[col];
                }
                return r;
            });
        };
        return {
            name: "NestedData",
            tables: [
                {
                    name: "MainTable",
                    displayName: "MainTable",
                    columns: table.columns.map(function (x) {
                        return {
                            name: columnNameMap[x.name],
                            displayName: columnNameMap[x.name],
                            type: x.type,
                            metadata: x.metadata,
                        };
                    }),
                    rows: mapToRows(dataRowIndices),
                    type: dataset_1.TableType.Main,
                    localeNumberFormat: table.localeNumberFormat,
                },
            ],
        };
    };
    // Get the graphical element from the element
    NestedChartElementClass.prototype.getGraphics = function (cs, offset, glyphIndex, 
    // eslint-disable-next-line
    manager, 
    // eslint-disable-next-line
    empasized) {
        if (glyphIndex === void 0) { glyphIndex = 0; }
        var attrs = this.state.attributes;
        if (!attrs.visible || !this.object.properties.visible) {
            return null;
        }
        var g = Graphics.makeGroup([
            {
                type: "chart-container",
                dataset: this.getDataset(glyphIndex),
                chart: common_1.deepClone(this.object.properties.specification),
                selectable: {
                    plotSegment: this.getPlotSegmentClass().object,
                    glyphIndex: glyphIndex,
                    rowIndices: this.getPlotSegmentClass().state.dataRowIndices[glyphIndex],
                },
                width: attrs.width,
                height: attrs.height,
            },
        ]);
        g.transform = { angle: 0, x: -attrs.width / 2, y: attrs.height / 2 };
        var gContainer = Graphics.makeGroup([g]);
        gContainer.transform = cs.getLocalTransform(attrs.cx + offset.x, attrs.cy + offset.y);
        return gContainer;
    };
    // Get DropZones given current state
    NestedChartElementClass.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            {
                type: "line",
                p1: { x: x2, y: y1 },
                p2: { x: x1, y: y1 },
                title: "width",
                accept: { kind: Specification.DataKind.Numerical },
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
                accept: { kind: Specification.DataKind.Numerical },
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
    NestedChartElementClass.prototype.getHandles = function () {
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
    NestedChartElementClass.prototype.getBoundingBox = function () {
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
    NestedChartElementClass.prototype.getSnappingGuides = function () {
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
    NestedChartElementClass.createDefault = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var obj = (_super.createDefault.apply(this, __spread(args)));
        var myGlyphID = common_1.uniqueID();
        var tableName = "MainTable";
        obj.properties.specification = {
            _id: common_1.uniqueID(),
            classID: "chart.rectangle",
            properties: {
                name: "Nested Chart",
                backgroundColor: null,
                backgroundOpacity: 1,
            },
            mappings: {
                marginTop: {
                    type: specification_1.MappingType.value,
                    value: 25,
                },
                marginBottom: {
                    type: specification_1.MappingType.value,
                    value: 10,
                },
                marginLeft: {
                    type: specification_1.MappingType.value,
                    value: 10,
                },
                marginRight: {
                    type: specification_1.MappingType.value,
                    value: 10,
                },
            },
            glyphs: [
                {
                    _id: myGlyphID,
                    classID: "glyph.rectangle",
                    properties: { name: "Glyph" },
                    table: tableName,
                    marks: [
                        {
                            _id: common_1.uniqueID(),
                            classID: "mark.anchor",
                            properties: { name: "Anchor" },
                            mappings: {
                                x: {
                                    type: specification_1.MappingType.parent,
                                    parentAttribute: "icx",
                                },
                                y: {
                                    type: specification_1.MappingType.parent,
                                    parentAttribute: "icy",
                                },
                            },
                        },
                    ],
                    mappings: {},
                    constraints: [],
                },
            ],
            elements: [
                {
                    _id: common_1.uniqueID(),
                    classID: "plot-segment.cartesian",
                    glyph: myGlyphID,
                    table: tableName,
                    filter: null,
                    mappings: {
                        x1: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "x1",
                        },
                        y1: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "y1",
                        },
                        x2: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "x2",
                        },
                        y2: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "y2",
                        },
                    },
                    properties: {
                        name: "PlotSegment1",
                        visible: true,
                        marginX1: 0,
                        marginY1: 0,
                        marginX2: 0,
                        marginY2: 0,
                        sublayout: {
                            type: base_1.Region2DSublayoutType.DodgeX,
                            order: null,
                            ratioX: 0.1,
                            ratioY: 0.1,
                            align: {
                                x: base_1.SublayoutAlignment.Start,
                                y: base_1.SublayoutAlignment.Start,
                            },
                            grid: {
                                direction: base_1.GridDirection.X,
                                xCount: null,
                                yCount: null,
                                gridStartPosition: base_1.GridStartPosition.LeftTop,
                            },
                        },
                    },
                },
                {
                    _id: common_1.uniqueID(),
                    classID: "mark.text",
                    properties: {
                        name: "Title",
                        visible: true,
                        alignment: { x: "middle", y: "top", xMargin: 0, yMargin: 5 },
                        rotation: 0,
                    },
                    mappings: {
                        x: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "cx",
                        },
                        y: {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "oy2",
                        },
                        text: {
                            type: specification_1.MappingType.value,
                            value: "Nested Chart",
                        },
                        fontSize: {
                            type: specification_1.MappingType.value,
                            value: 12,
                        },
                        color: {
                            type: specification_1.MappingType.value,
                            value: { r: 0, g: 0, b: 0 },
                        },
                    },
                },
            ],
            scales: [],
            scaleMappings: [],
            constraints: [],
            resources: [],
        };
        return obj;
    };
    NestedChartElementClass.prototype.getTemplateParameters = function () {
        return {
            inferences: [
                {
                    objectID: this.object._id,
                    dataSource: {
                        table: this.getGlyphClass().object.table,
                    },
                    nestedChart: {
                        columnNameMap: this.object.properties.columnNameMap,
                    },
                },
            ],
        };
    };
    NestedChartElementClass.classID = "mark.nested-chart";
    NestedChartElementClass.type = "mark";
    NestedChartElementClass.metadata = {
        displayName: "NestedChart",
        iconPath: "BarChartVerticalFilter",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    NestedChartElementClass.defaultProperties = {
        visible: true,
    };
    NestedChartElementClass.defaultMappingValues = {
        visible: true,
    };
    return NestedChartElementClass;
}(emphasis_1.EmphasizableMarkClass));
exports.NestedChartElementClass = NestedChartElementClass;
//# sourceMappingURL=nested_chart.js.map