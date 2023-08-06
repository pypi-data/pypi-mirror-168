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
exports.LegendCreationPanel = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../core");
var context_component_1 = require("../../context_component");
var data_field_selector_1 = require("../dataset/data_field_selector");
var radio_control_1 = require("./radio_control");
var dataset_1 = require("../../../core/dataset");
var specification_1 = require("../../../core/specification");
var react_1 = require("@fluentui/react");
var strings_1 = require("../../../strings");
var LegendCreationPanel = /** @class */ (function (_super) {
    __extends(LegendCreationPanel, _super);
    function LegendCreationPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        return _this;
    }
    LegendCreationPanel.prototype.getDefaultState = function () {
        return {
            legendDataSource: "columnValues",
            errorReport: null,
            legendType: "color",
        };
    };
    // eslint-disable-next-line
    LegendCreationPanel.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__link-type-table" },
            React.createElement("div", { className: "el-row" },
                React.createElement(react_1.Label, null, strings_1.strings.legendCreator.legendType),
                React.createElement(radio_control_1.PanelRadioControl, { options: ["columnValues", "columnNames"], labels: ["Column values", "Column names"], value: this.state.legendDataSource, onChange: function (newValue) {
                        return _this.setState({ legendDataSource: newValue });
                    }, showText: true })),
            this.state.legendDataSource == "columnValues" ? (React.createElement("div", null,
                React.createElement(react_1.Label, null, strings_1.strings.legendCreator.connectBy),
                React.createElement("div", { className: "el-row" },
                    React.createElement(data_field_selector_1.DataFieldSelector, { multiSelect: false, ref: function (e) { return (_this.groupBySelector = e); }, kinds: [
                            core_1.Specification.DataKind.Categorical,
                            core_1.Specification.DataKind.Numerical,
                            core_1.Specification.DataKind.Temporal,
                            core_1.Specification.DataKind.Ordinal,
                        ], datasetStore: this.store, nullDescription: "(select column to create legend)" })))) : (React.createElement("div", null,
                React.createElement(react_1.Label, null, strings_1.strings.legendCreator.connectBy),
                React.createElement("div", { className: "el-row" },
                    React.createElement(data_field_selector_1.DataFieldSelector, { multiSelect: true, ref: function (e) { return (_this.groupBySelector = e); }, kinds: [
                            core_1.Specification.DataKind.Categorical,
                            core_1.Specification.DataKind.Numerical,
                            core_1.Specification.DataKind.Temporal,
                            core_1.Specification.DataKind.Ordinal,
                        ], datasetStore: this.store, nullDescription: "(select column names to create legend)" })))),
            React.createElement("div", { className: "el-row" },
                React.createElement(react_1.PrimaryButton, { text: strings_1.strings.legendCreator.createLegend, title: strings_1.strings.legendCreator.createLegend, 
                    // eslint-disable-next-line
                    onClick: function () {
                        var _a;
                        var columns = _this.groupBySelector
                            ? _this.groupBySelector.value
                                ? _this.groupBySelector.props.multiSelect
                                    ? _this.groupBySelector.value
                                    : [_this.groupBySelector.value]
                                : []
                            : [];
                        var attributeType = specification_1.AttributeType.Color;
                        if (_this.state.legendDataSource === "columnNames") {
                            var valueType = core_1.Specification.DataType.String;
                            var valueKind = core_1.Specification.DataKind.Categorical;
                            var outputType = core_1.Specification.AttributeType.Color;
                            var scaleClassID = core_1.Prototypes.Scales.inferScaleType(valueType, valueKind, outputType);
                            var tableName = _this.store.dataset.tables.find(function (t) { return t.type === dataset_1.TableType.Main; }).name;
                            var table_1 = _this.store.chartManager.dataflow.getTable(tableName);
                            var data = columns
                                .map(function (ex) {
                                var index = table_1.columns.findIndex(function (col) { return col.name == ex.columnName; });
                                return "get(get(" + ex.table + ".columns, " + index + "), \"displayName\")";
                            })
                                .filter(function (v) { return v != null; });
                            var expression = "list(" + data
                                .map(function (ex) {
                                return "" + ex;
                            })
                                .join(",") + ")";
                            var parsedExpression = _this.store.chartManager.dataflow.cache.parse(expression);
                            var expressionData = parsedExpression.getValue(table_1);
                            var newScale = _this.store.chartManager.createObject(scaleClassID);
                            newScale.properties.name = _this.store.chartManager.findUnusedName("Scale");
                            newScale.inputType = valueType;
                            newScale.outputType = outputType;
                            _this.store.chartManager.addScale(newScale);
                            var scaleClass = _this.store.chartManager.getClassById(newScale._id);
                            scaleClass.inferParameters(expressionData, {});
                            var newLegend = _this.store.chartManager.createObject("legend.custom");
                            newLegend.properties.scale = newScale._id;
                            newLegend.mappings.x = {
                                type: specification_1.MappingType.parent,
                                parentAttribute: "x2",
                            };
                            newLegend.mappings.y = {
                                type: specification_1.MappingType.parent,
                                parentAttribute: "y2",
                            };
                            _this.store.chartManager.addChartElement(newLegend);
                            _this.store.chartManager.chart.mappings.marginRight = {
                                type: specification_1.MappingType.value,
                                value: 100,
                            };
                            var mappingOptions = {
                                type: specification_1.MappingType.scale,
                                table: tableName,
                                expression: expression,
                                valueType: valueType,
                                scale: newScale._id,
                                allowSelectValue: true,
                            };
                            if (!newLegend.mappings) {
                                newLegend.mappings = {};
                            }
                            newLegend.mappings.mappingOptions = mappingOptions;
                        }
                        else {
                            var kind = _this.groupBySelector
                                .value.metadata.kind;
                            switch (kind) {
                                case dataset_1.DataKind.Numerical:
                                case dataset_1.DataKind.Temporal:
                                    attributeType = specification_1.AttributeType.Number;
                                    break;
                                case dataset_1.DataKind.Ordinal:
                                    attributeType = specification_1.AttributeType.Text;
                                    break;
                            }
                        }
                        if (_this.state.legendDataSource === "columnValues") {
                            var aggregation = core_1.Expression.getDefaultAggregationFunction(columns[0].type, (_a = columns[0].metadata) === null || _a === void 0 ? void 0 : _a.kind);
                            var aggregatedExpression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(columns[0].expression)).toString();
                            var table = columns[0].table;
                            var inferred = _this.store.scaleInference({ chart: { table: table } }, {
                                expression: aggregatedExpression,
                                valueType: columns[0].type,
                                valueKind: columns[0].metadata.kind,
                                outputType: attributeType,
                                hints: {},
                            });
                            var scaleObject = core_1.getById(_this.store.chartManager.chart.scales, inferred);
                            var newLegend = null;
                            switch (scaleObject.classID) {
                                case "scale.categorical<string,color>":
                                    newLegend = _this.store.chartManager.createObject("legend.categorical");
                                    newLegend.properties.scale = inferred;
                                    newLegend.mappings.x = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "x2",
                                    };
                                    newLegend.mappings.y = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "y2",
                                    };
                                    _this.store.chartManager.addChartElement(newLegend);
                                    _this.store.chartManager.chart.mappings.marginRight = {
                                        type: specification_1.MappingType.value,
                                        value: 100,
                                    };
                                    break;
                                case "scale.linear<number,color>":
                                case "scale.linear<integer,color>":
                                    newLegend = _this.store.chartManager.createObject("legend.numerical-color");
                                    newLegend.properties.scale = inferred;
                                    newLegend.mappings.x = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "x2",
                                    };
                                    newLegend.mappings.y = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "y2",
                                    };
                                    _this.store.chartManager.addChartElement(newLegend);
                                    _this.store.chartManager.chart.mappings.marginRight = {
                                        type: specification_1.MappingType.value,
                                        value: 100,
                                    };
                                    break;
                                case "scale.linear<number,number>":
                                case "scale.linear<integer,number>":
                                    newLegend = _this.store.chartManager.createObject("legend.numerical-number");
                                    newLegend.properties.scale = inferred;
                                    newLegend.mappings.x1 = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "x1",
                                    };
                                    newLegend.mappings.y1 = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "y1",
                                    };
                                    newLegend.mappings.x2 = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "x1",
                                    };
                                    newLegend.mappings.y2 = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: "y2",
                                    };
                                    _this.store.chartManager.addChartElement(newLegend);
                            }
                            newLegend.mappings.mappingOptions = {
                                type: specification_1.MappingType.scale,
                                table: table,
                                expression: aggregatedExpression,
                                valueType: columns[0].type,
                                scale: inferred,
                            };
                        }
                        _this.store.solveConstraintsAndUpdateGraphics();
                        _this.props.onFinish();
                    } }),
                this.state.errorReport ? (React.createElement("span", null, this.state.errorReport)) : null)));
    };
    return LegendCreationPanel;
}(context_component_1.ContextedComponent));
exports.LegendCreationPanel = LegendCreationPanel;
//# sourceMappingURL=legend_creator.js.map