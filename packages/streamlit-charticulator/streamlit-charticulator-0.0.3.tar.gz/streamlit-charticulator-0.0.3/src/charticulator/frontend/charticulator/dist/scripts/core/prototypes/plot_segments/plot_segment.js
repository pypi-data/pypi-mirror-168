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
Object.defineProperty(exports, "__esModule", { value: true });
exports.PlotSegmentClass = void 0;
var Graphics = require("../../graphics");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
var expression_1 = require("../../expression");
var __1 = require("../..");
var axis_1 = require("./axis");
var types_1 = require("../../specification/types");
var strings_1 = require("../../../strings");
var PlotSegmentClass = /** @class */ (function (_super) {
    __extends(PlotSegmentClass, _super);
    function PlotSegmentClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getDisplayFormat = function (binding, tickFormat, manager) {
            if (binding.numericalMode === types_1.NumericalMode.Temporal ||
                binding.valueType === Specification.DataType.Date) {
                if (tickFormat) {
                    return function (value) {
                        return __1.getTimeFormatFunction()(tickFormat.replace(__1.tickFormatParserExpression(), "$1"))(value);
                    };
                }
                else {
                    return function (value) {
                        return __1.getTimeFormatFunction()("%m/%d/%Y")(value);
                    };
                }
            }
            else {
                if (tickFormat) {
                    var resolvedFormat_1 = axis_1.AxisRenderer.getTickFormat(tickFormat, null);
                    return function (value) {
                        return resolvedFormat_1(value);
                    };
                }
                else {
                    if (binding.rawExpression && manager) {
                        var rawFormat = _this.getDisplayRawFormat(binding, manager);
                        if (rawFormat) {
                            return rawFormat;
                        }
                    }
                    return function (value) {
                        return value;
                    };
                }
            }
        };
        return _this;
    }
    /** Fill the layout's default state */
    // eslint-disable-next-line
    PlotSegmentClass.prototype.initializeState = function () { };
    /** Build intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    // eslint-disable-next-line
    PlotSegmentClass.prototype.buildConstraints = function (
    // eslint-disable-next-line
    solver, 
    // eslint-disable-next-line
    context, 
    // eslint-disable-next-line
    manager
    // eslint-disable-next-line
    ) { };
    /** Build constraints for glyphs within */
    // eslint-disable-next-line
    PlotSegmentClass.prototype.buildGlyphConstraints = function (
    // eslint-disable-next-line
    solver, 
    // eslint-disable-next-line
    context
    // eslint-disable-next-line
    ) { };
    /** Get the graphics that represent this layout */
    PlotSegmentClass.prototype.getPlotSegmentGraphics = function (glyphGraphics, manager) {
        return Graphics.makeGroup([glyphGraphics, this.getGraphics(manager)]);
    };
    /** Get the graphics that represent this layout of elements in background*/
    PlotSegmentClass.prototype.getPlotSegmentBackgroundGraphics = function (
    // eslint-disable-next-line
    manager) {
        return null;
    };
    // Renders interactable elements of plotsegment;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    PlotSegmentClass.prototype.renderControls = function (
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    _manager, 
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    _zoom) {
        return null;
    };
    PlotSegmentClass.prototype.getCoordinateSystem = function () {
        return new Graphics.CartesianCoordinates();
    };
    /** Get DropZones given current state */
    PlotSegmentClass.prototype.getDropZones = function () {
        return [];
    };
    /** Get handles given current state */
    PlotSegmentClass.prototype.getHandles = function () {
        return null;
    };
    PlotSegmentClass.prototype.getBoundingBox = function () {
        return null;
    };
    /**
     * Renders gridlines for axis
     * @param data axis data binding
     * @param manager widgets manager
     * @param axisProperty property name of plotsegment with axis properties (xData, yData, axis)
     */
    PlotSegmentClass.prototype.buildGridLineWidgets = function (data, manager, axisProperty, mainCollapsePanelHeader) {
        if (!data) {
            return [];
        }
        if (data.type === types_1.AxisDataBindingType.Default) {
            return [];
        }
        return PlotSegmentClass.getGridLineAttributePanelWidgets(manager, axisProperty, mainCollapsePanelHeader);
    };
    PlotSegmentClass.getGridLineAttributePanelWidgets = function (manager, axisProperty, mainCollapsePanelHeader) {
        return [
            manager.verticalGroup({
                header: strings_1.strings.objects.plotSegment.gridline,
            }, [
                manager.inputSelect({ property: axisProperty, field: ["style", "gridlineStyle"] }, {
                    type: "dropdown",
                    showLabel: true,
                    isLocalIcons: true,
                    icons: [
                        "ChromeClose",
                        "stroke/solid",
                        "stroke/dashed",
                        "stroke/dotted",
                    ],
                    options: ["none", "solid", "dashed", "dotted"],
                    labels: [
                        strings_1.strings.filter.none,
                        strings_1.strings.objects.links.solid,
                        strings_1.strings.objects.links.dashed,
                        strings_1.strings.objects.links.dotted,
                    ],
                    label: strings_1.strings.objects.style,
                    searchSection: [
                        strings_1.strings.objects.plotSegment.gridline,
                        mainCollapsePanelHeader,
                    ],
                }),
                manager.inputColor({
                    property: axisProperty,
                    field: ["style", "gridlineColor"],
                }, {
                    label: strings_1.strings.objects.color,
                    labelKey: "gridline-color-" + axisProperty,
                    searchSection: [
                        strings_1.strings.objects.plotSegment.gridline,
                        mainCollapsePanelHeader,
                    ],
                }),
                manager.inputNumber({
                    property: axisProperty,
                    field: ["style", "gridlineWidth"],
                }, {
                    minimum: 0,
                    maximum: 100,
                    showUpdown: true,
                    label: strings_1.strings.objects.width,
                    searchSection: [
                        strings_1.strings.objects.plotSegment.gridline,
                        mainCollapsePanelHeader,
                    ],
                }),
            ]),
        ];
    };
    PlotSegmentClass.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.horizontal([0, 1, 1], manager.label("Data", {
                addMargins: true,
                key: "Data",
                ignoreSearch: true,
            }), manager.horizontal([1], [
                manager.filterEditor({
                    table: this.object.table,
                    target: { plotSegment: this.object },
                    value: this.object.filter,
                    mode: "button" /* Button */,
                    key: "filterEditor",
                    ignoreSearch: true,
                }),
                manager.groupByEditor({
                    table: this.object.table,
                    target: { plotSegment: this.object },
                    value: this.object.groupBy,
                    mode: "button" /* Button */,
                    key: "groupByEditor",
                    ignoreSearch: true,
                }),
            ])),
        ];
    };
    PlotSegmentClass.createDefault = function (glyph) {
        var plotSegment = _super.createDefault.call(this);
        plotSegment.glyph = glyph._id;
        plotSegment.table = glyph.table;
        return plotSegment;
    };
    PlotSegmentClass.prototype.getDisplayRawFormat = function (binding, manager) {
        var tableName = this.object.table;
        var table = manager.dataset.tables.find(function (table) { return table.name === tableName; });
        var getColumnName = function (rawExpression) {
            // eslint-disable-next-line
            var expression = expression_1.TextExpression.Parse("${" + rawExpression + "}");
            var parsedExpression = expression.parts.find(function (part) {
                if (part.expression instanceof expression_1.FunctionCall) {
                    return (part.expression.args.find(function (arg) { return arg instanceof expression_1.Variable; }));
                }
            });
            var functionCallpart = parsedExpression && parsedExpression.expression;
            if (functionCallpart) {
                var variable = (functionCallpart.args.find(function (arg) { return arg instanceof expression_1.Variable; }));
                var columnName_1 = variable.name;
                var column = table.columns.find(function (column) { return column.name === columnName_1; });
                return column.name;
            }
            return null;
        };
        if (binding.valueType === Specification.DataType.Boolean) {
            var columnName_2 = getColumnName(binding.expression);
            var rawColumnName_1 = getColumnName(binding.rawExpression);
            if (columnName_2 && rawColumnName_1) {
                var dataMapping_1 = new Map();
                table.rows.forEach(function (row) {
                    var value = row[columnName_2];
                    var rawValue = row[rawColumnName_1];
                    if (value !== undefined && value !== null && rawValue !== undefined) {
                        var stringValue = value.toString();
                        var rawValueString = (rawValue || row[__1.refineColumnName(rawColumnName_1)]).toString();
                        dataMapping_1.set(stringValue, rawValueString);
                    }
                });
                return function (value) {
                    var rawValue = dataMapping_1.get(value);
                    return rawValue !== null ? rawValue : value;
                };
            }
        }
        return null;
    };
    PlotSegmentClass.prototype.buildGlyphOrderedList = function () {
        var groups = this.state.dataRowIndices.map(function (x, i) { return i; });
        if (!this.object.properties.sublayout) {
            return groups;
        }
        var order = this.object.properties.sublayout.order;
        var dateRowIndices = this.state.dataRowIndices;
        var table = this.parent.dataflow.getTable(this.object.table);
        if (order != null && order.expression) {
            var orderExpression_1 = this.parent.dataflow.cache.parse(order.expression);
            var compare = function (i, j) {
                var vi = orderExpression_1.getValue(table.getGroupedContext(dateRowIndices[i]));
                var vj = orderExpression_1.getValue(table.getGroupedContext(dateRowIndices[j]));
                return __1.getSortFunctionByData([vi + "", vj + ""])(vi, vj);
            };
            groups.sort(compare);
        }
        if (this.object.properties.sublayout.orderReversed) {
            groups.reverse();
        }
        return groups;
    };
    /**
     * Return the index of the first glyph after sorting glyphs according sublayout order parameter
     */
    PlotSegmentClass.prototype.getFirstGlyphIndex = function () {
        var glyphs = this.buildGlyphOrderedList();
        return glyphs.length > 0 ? glyphs[0] : -1;
    };
    /**
     * Return the index of the last glyph after sorting glyphs according sublayout order parameter
     */
    PlotSegmentClass.prototype.getLastGlyphIndex = function () {
        var glyphs = this.buildGlyphOrderedList();
        return glyphs.length > 0 ? glyphs[glyphs.length - 1] : -1;
    };
    return PlotSegmentClass;
}(chart_element_1.ChartElementClass));
exports.PlotSegmentClass = PlotSegmentClass;
//# sourceMappingURL=plot_segment.js.map