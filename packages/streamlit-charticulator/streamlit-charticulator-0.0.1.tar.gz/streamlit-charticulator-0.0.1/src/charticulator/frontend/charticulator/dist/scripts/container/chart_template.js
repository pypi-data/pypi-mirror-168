"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChartTemplate = void 0;
var core_1 = require("../core");
var prototypes_1 = require("../core/prototypes");
var group_by_1 = require("../core/prototypes/group_by");
var types_1 = require("../core/specification/types");
var specification_1 = require("../core/specification");
var guides_1 = require("../core/prototypes/guides");
var d3_scale_1 = require("d3-scale");
/** Represents a chart template */
var ChartTemplate = /** @class */ (function () {
    /** Create a chart template */
    function ChartTemplate(template) {
        this.template = template;
        this.columnAssignment = {};
        this.tableAssignment = {};
    }
    ChartTemplate.prototype.getDatasetSchema = function () {
        return this.template.tables;
    };
    /** Reset slot assignments */
    ChartTemplate.prototype.reset = function () {
        this.columnAssignment = {};
        this.tableAssignment = {};
    };
    /** Assign a table */
    ChartTemplate.prototype.assignTable = function (tableName, table) {
        this.tableAssignment[tableName] = table;
    };
    /** Assign an expression to a data mapping slot */
    ChartTemplate.prototype.assignColumn = function (tableName, columnName, column) {
        if (!Object.prototype.hasOwnProperty.call(this.columnAssignment, tableName)) {
            this.columnAssignment[tableName] = {};
        }
        this.columnAssignment[tableName][columnName] = column;
    };
    /** Get variable map for a given table */
    ChartTemplate.prototype.getVariableMap = function (table) {
        var variableMap = {};
        if (this.columnAssignment[table]) {
            variableMap = __assign({}, this.columnAssignment[table]);
        }
        if (this.tableAssignment) {
            variableMap = __assign(__assign({}, variableMap), this.tableAssignment);
        }
        return variableMap;
    };
    ChartTemplate.prototype.transformExpression = function (expr, table) {
        return core_1.Expression.parse(expr)
            .replace(core_1.Expression.variableReplacer(this.getVariableMap(table)))
            .toString();
    };
    ChartTemplate.prototype.transformTextExpression = function (expr, table) {
        return core_1.Expression.parseTextExpression(expr)
            .replace(core_1.Expression.variableReplacer(this.getVariableMap(table)))
            .toString();
    };
    ChartTemplate.prototype.transformGroupBy = function (groupBy, table) {
        if (!groupBy) {
            return null;
        }
        if (groupBy.expression) {
            return {
                expression: this.transformExpression(groupBy.expression, table),
            };
        }
    };
    /**
     * Creates instance of chart object from template. Chart objecty can be loaded into container to display it in canvas
     * On editing this method ensure that you made correspond changes in template builder ({@link ChartTemplateBuilder}).
     * Any exposed into template objects should be initialized here
     */
    // eslint-disable-next-line
    ChartTemplate.prototype.instantiate = function (dataset, inference) {
        var e_1, _a, e_2, _b;
        var _this = this;
        var _c, _d, _e;
        if (inference === void 0) { inference = true; }
        // Make a copy of the chart spec so we won't touch the original template data
        var chart = core_1.deepClone(this.template.specification);
        var _loop_1 = function (item) {
            var e_3, _a;
            // Replace table with assigned table
            if (item.kind == "chart-element") {
                // legend with column names
                if (core_1.Prototypes.isType(item.chartElement.classID, "legend.custom")) {
                    var scaleMapping = item.chartElement.mappings
                        .mappingOptions;
                    scaleMapping.expression = this_1.transformExpression(scaleMapping.expression, scaleMapping.table);
                }
                // Guide
                if (core_1.Prototypes.isType(item.chartElement.classID, "guide.guide")) {
                    var valueProp = this_1.template.properties.filter(function (p) {
                        return p.objectID === item.chartElement._id &&
                            p.target.attribute === guides_1.GuideAttributeNames.value;
                    })[0];
                    if (valueProp) {
                        var valueMapping = {
                            type: specification_1.MappingType.value,
                            value: valueProp.default,
                        };
                        item.chartElement.mappings.value = valueMapping;
                    }
                }
                // PlotSegment
                if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment")) {
                    var plotSegment = item.chartElement;
                    var originalTable = plotSegment.table;
                    plotSegment.table = this_1.tableAssignment[originalTable];
                    // Also fix filter and gropyBy expressions
                    if (plotSegment.filter) {
                        if (plotSegment.filter.categories) {
                            plotSegment.filter.categories.expression = this_1.transformExpression(plotSegment.filter.categories.expression, originalTable);
                        }
                        if (plotSegment.filter.expression) {
                            plotSegment.filter.expression = this_1.transformExpression(plotSegment.filter.expression, originalTable);
                        }
                    }
                    if (plotSegment.groupBy) {
                        if (plotSegment.groupBy.expression) {
                            plotSegment.groupBy.expression = this_1.transformExpression(plotSegment.groupBy.expression, originalTable);
                        }
                    }
                    if (plotSegment.properties.xData) {
                        if (plotSegment.properties.xData.expression) {
                            plotSegment.properties
                                .xData.expression = this_1.transformExpression(plotSegment.properties.xData.expression, originalTable);
                        }
                        if (plotSegment.properties.xData.rawExpression) {
                            plotSegment.properties
                                .xData.rawExpression = this_1.transformExpression(plotSegment.properties.xData.rawExpression, originalTable);
                        }
                    }
                    if (plotSegment.properties.yData) {
                        if (plotSegment.properties.yData.expression) {
                            plotSegment.properties
                                .yData.expression = this_1.transformExpression(plotSegment.properties.yData.expression, originalTable);
                        }
                        if (plotSegment.properties.yData.rawExpression) {
                            plotSegment.properties
                                .yData.rawExpression = this_1.transformExpression(plotSegment.properties.yData.rawExpression, originalTable);
                        }
                    }
                    if (plotSegment.properties.axis) {
                        if (plotSegment.properties.axis.expression) {
                            plotSegment.properties
                                .axis.expression = this_1.transformExpression(plotSegment.properties.axis.expression, originalTable);
                        }
                        if (plotSegment.properties.axis.rawExpression) {
                            plotSegment.properties
                                .axis.rawExpression = this_1.transformExpression(plotSegment.properties.axis.rawExpression, originalTable);
                        }
                    }
                    if (plotSegment.properties.sublayout) {
                        var expression = (_c = plotSegment.properties
                            .sublayout.order) === null || _c === void 0 ? void 0 : _c.expression;
                        if (expression) {
                            plotSegment.properties
                                .sublayout.order.expression = this_1.transformExpression(expression, originalTable);
                        }
                    }
                }
                // Links
                if (core_1.Prototypes.isType(item.chartElement.classID, "links")) {
                    if (item.chartElement.classID == "links.through") {
                        var props_1 = item.chartElement
                            .properties;
                        if (props_1.linkThrough.facetExpressions) {
                            props_1.linkThrough.facetExpressions = props_1.linkThrough.facetExpressions.map(function (x) {
                                return _this.transformExpression(x, core_1.getById(_this.template.specification.elements, props_1.linkThrough.plotSegment).table);
                            });
                        }
                    }
                    if (item.chartElement.classID == "links.table") {
                        var props = item.chartElement
                            .properties;
                        props.linkTable.table = this_1.tableAssignment[props.linkTable.table];
                    }
                }
            }
            // Glyphs
            if (item.kind == "glyph") {
                item.glyph.table = this_1.tableAssignment[item.glyph.table];
            }
            if (item.kind == "mark") {
                if (core_1.Prototypes.isType(item.mark.classID, "mark.data-axis")) {
                    try {
                        var glyphId_1 = item.glyph._id;
                        var glyphPlotSegment_1 = __spread(prototypes_1.forEachObject(chart)).find(function (item) {
                            return item.kind == "chart-element" &&
                                core_1.Prototypes.isType(item.chartElement.classID, "plot-segment") &&
                                item.chartElement.glyph === glyphId_1;
                        });
                        var dataExpressions = item.mark.properties
                            .dataExpressions;
                        // table name in plotSegment can be replaced already
                        var table_1 = Object.keys(this_1.tableAssignment).find(function (key) {
                            return _this.tableAssignment[key] ===
                                glyphPlotSegment_1.chartElement.table;
                        }) || glyphPlotSegment_1.chartElement.table;
                        dataExpressions.forEach(function (expression) {
                            expression.expression = _this.transformExpression(expression.expression, table_1);
                        });
                    }
                    catch (ex) {
                        console.error(ex);
                    }
                }
            }
            // Replace data-mapping expressions with assigned columns
            var mappings = item.object.mappings;
            try {
                for (var _b = (e_3 = void 0, __values(prototypes_1.forEachMapping(mappings))), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), mapping = _d[1];
                    if (mapping.type == specification_1.MappingType.scale) {
                        var scaleMapping = mapping;
                        scaleMapping.expression = this_1.transformExpression(scaleMapping.expression, scaleMapping.table);
                        scaleMapping.table = this_1.tableAssignment[scaleMapping.table];
                    }
                    if (mapping.type == specification_1.MappingType.text) {
                        var textMapping = mapping;
                        textMapping.textExpression = this_1.transformTextExpression(textMapping.textExpression, textMapping.table);
                        textMapping.table = this_1.tableAssignment[textMapping.table];
                    }
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_3) throw e_3.error; }
            }
        };
        var this_1 = this;
        try {
            // Transform table and expressions with current assignments
            for (var _f = __values(prototypes_1.forEachObject(chart)), _g = _f.next(); !_g.done; _g = _f.next()) {
                var item = _g.value;
                _loop_1(item);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_a = _f.return)) _a.call(_f);
            }
            finally { if (e_1) throw e_1.error; }
        }
        if (!inference) {
            return {
                chart: chart,
                defaultAttributes: this.template.defaultAttributes,
            };
        }
        var df = new core_1.Prototypes.Dataflow.DataflowManager(dataset);
        var getExpressionVector = function (expression, table, groupBy) {
            var expr = core_1.Expression.parse(expression);
            var tableContext = df.getTable(table);
            var indices = groupBy
                ? new group_by_1.CompiledGroupBy(groupBy, df.cache).groupBy(tableContext)
                : core_1.makeRange(0, tableContext.rows.length).map(function (x) { return [x]; });
            return indices.map(function (is) {
                return expr.getValue(tableContext.getGroupedContext(is));
            });
        };
        var _loop_2 = function (inference_1) {
            var e_4, _a;
            var object = prototypes_1.findObjectById(chart, inference_1.objectID);
            if (inference_1.expression) {
                var expr = this_2.transformExpression(inference_1.expression.expression, inference_1.dataSource.table);
                prototypes_1.setProperty(object, inference_1.expression.property, expr);
            }
            if (inference_1.axis) {
                var axis = inference_1.axis;
                if (axis.type == "default") {
                    return "continue";
                }
                var expression = this_2.transformExpression(inference_1.axis.expression, inference_1.dataSource.table);
                var axisDataBinding_1 = prototypes_1.getProperty(object, axis.property);
                axisDataBinding_1.expression = expression;
                if (inference_1.autoDomainMin || inference_1.autoDomainMax) {
                    // disableAuto flag responsible for disabling/enabling configulration scale domains when new data is coming
                    // If disableAuto is true, the same scales will be used for data
                    // Example: If disableAuto is true, axis values will be same for all new data sets.
                    var vector = getExpressionVector(expression, this_2.tableAssignment[inference_1.dataSource.table], this_2.transformGroupBy(inference_1.dataSource.groupBy, inference_1.dataSource.table));
                    if (inference_1.axis.additionalExpressions) {
                        try {
                            for (var _b = (e_4 = void 0, __values(inference_1.axis.additionalExpressions)), _c = _b.next(); !_c.done; _c = _b.next()) {
                                var item = _c.value;
                                var expr = this_2.transformExpression(item, inference_1.dataSource.table);
                                vector = vector.concat(getExpressionVector(expr, this_2.tableAssignment[inference_1.dataSource.table], this_2.transformGroupBy(inference_1.dataSource.groupBy, inference_1.dataSource.table)));
                            }
                        }
                        catch (e_4_1) { e_4 = { error: e_4_1 }; }
                        finally {
                            try {
                                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                            }
                            finally { if (e_4) throw e_4.error; }
                        }
                    }
                    if (axis.type == "categorical") {
                        var scale_1 = new core_1.Scale.CategoricalScale();
                        scale_1.inferParameters(vector, inference_1.axis.orderMode || types_1.OrderMode.order);
                        axisDataBinding_1.categories = new Array(scale_1.domain.size);
                        var newData_1 = new Array(scale_1.domain.size);
                        scale_1.domain.forEach(function (index, key) {
                            newData_1[index] = key;
                        });
                        // try to save given order from template
                        if (axisDataBinding_1.order &&
                            axisDataBinding_1.orderMode === types_1.OrderMode.order) {
                            axisDataBinding_1.order = axisDataBinding_1.order.filter(function (value) {
                                return scale_1.domain.has(value);
                            });
                            var newItems = newData_1.filter(function (category) {
                                return !axisDataBinding_1.order.find(function (order) { return order === category; });
                            });
                            axisDataBinding_1.categories = new Array(axisDataBinding_1.order.length);
                            axisDataBinding_1.order.forEach(function (value, index) {
                                axisDataBinding_1.categories[index] = value;
                            });
                            axisDataBinding_1.categories = axisDataBinding_1.categories.concat(newItems);
                            axisDataBinding_1.order = axisDataBinding_1.order.concat(newItems);
                        }
                        else {
                            axisDataBinding_1.categories = new Array(scale_1.domain.size);
                            scale_1.domain.forEach(function (index, key) {
                                axisDataBinding_1.categories[index] = key;
                            });
                        }
                        axisDataBinding_1.allCategories = core_1.deepClone(axisDataBinding_1.categories);
                        if (axisDataBinding_1.allowScrolling) {
                            var start = Math.floor(((axisDataBinding_1.categories.length -
                                axisDataBinding_1.windowSize) /
                                100) *
                                axisDataBinding_1.scrollPosition);
                            axisDataBinding_1.categories = axisDataBinding_1.categories.slice(start, start + axisDataBinding_1.windowSize);
                        }
                    }
                    else if (axis.type == "numerical") {
                        var scale = new core_1.Scale.LinearScale();
                        scale.inferParameters(vector);
                        if (inference_1.autoDomainMin) {
                            axisDataBinding_1.dataDomainMin = scale.domainMin;
                            axisDataBinding_1.domainMin = scale.domainMin;
                        }
                        if (inference_1.autoDomainMax) {
                            axisDataBinding_1.dataDomainMax = scale.domainMax;
                            axisDataBinding_1.domainMax = scale.domainMax;
                        }
                        if (axisDataBinding_1.allowScrolling) {
                            var scrollScale = d3_scale_1.scaleLinear()
                                .domain([0, 100])
                                .range([
                                axisDataBinding_1.dataDomainMin,
                                axisDataBinding_1.dataDomainMax,
                            ]);
                            var start = scrollScale(axisDataBinding_1.scrollPosition);
                            axisDataBinding_1.domainMin = start;
                            axisDataBinding_1.domainMax = start + axisDataBinding_1.windowSize;
                        }
                        else {
                            if (inference_1.autoDomainMin) {
                                axisDataBinding_1.dataDomainMin = scale.domainMin;
                            }
                            if (inference_1.autoDomainMax) {
                                axisDataBinding_1.dataDomainMax = scale.domainMax;
                            }
                        }
                        if (axis.defineCategories) {
                            axisDataBinding_1.categories = core_1.defineCategories(vector);
                        }
                    }
                }
            }
            if (inference_1.scale) {
                // uses disableAutoMin disableAutoMax for handle old templates
                // copy old parameters to new
                if (inference_1.autoDomainMin == null &&
                    inference_1.disableAutoMin != null) {
                    inference_1.autoDomainMin = !inference_1.disableAutoMin;
                }
                // copy old parameters to new
                if (inference_1.autoDomainMax == null &&
                    inference_1.disableAutoMax != null) {
                    inference_1.autoDomainMax = !inference_1.disableAutoMax;
                }
                if (inference_1.autoDomainMin || inference_1.autoDomainMax) {
                    var scale = inference_1.scale;
                    var expressions = scale.expressions.map(function (x) {
                        return _this.transformExpression(x, inference_1.dataSource.table);
                    });
                    var vectors = expressions.map(function (x) {
                        return getExpressionVector(x, _this.tableAssignment[inference_1.dataSource.table], _this.transformGroupBy(inference_1.dataSource.groupBy, inference_1.dataSource.table));
                    });
                    var vector = vectors.reduce(function (a, b) { return a.concat(b); }, []);
                    var scaleClass = core_1.Prototypes.ObjectClasses.Create(null, object, {
                        attributes: {},
                    });
                    if (object.classID === "scale.categorical<string,color>") {
                        scaleClass.inferParameters(vector, {
                            reuseRange: true,
                            extendScaleMin: true,
                            extendScaleMax: true,
                        });
                    }
                    else {
                        scaleClass.inferParameters(vector, {
                            extendScaleMax: inference_1.autoDomainMax,
                            extendScaleMin: inference_1.autoDomainMin,
                            reuseRange: true,
                            rangeNumber: [
                                (_d = object.mappings.rangeMin) === null || _d === void 0 ? void 0 : _d.value,
                                (_e = object.mappings.rangeMax) === null || _e === void 0 ? void 0 : _e.value,
                            ],
                        });
                    }
                }
            }
            if (inference_1.nestedChart) {
                var nestedChart_1 = inference_1.nestedChart;
                var columnNameMap_1 = {};
                Object.keys(nestedChart_1.columnNameMap).forEach(function (key) {
                    var newKey = _this.columnAssignment[inference_1.dataSource.table][key];
                    columnNameMap_1[newKey] = nestedChart_1.columnNameMap[key];
                });
                prototypes_1.setProperty(object, "columnNameMap", columnNameMap_1);
            }
        };
        var this_2 = this;
        try {
            // Perform inferences
            for (var _h = __values(this.template.inference), _j = _h.next(); !_j.done; _j = _h.next()) {
                var inference_1 = _j.value;
                _loop_2(inference_1);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return {
            chart: chart,
            defaultAttributes: this.template.defaultAttributes,
        };
    };
    ChartTemplate.SetChartProperty = function (chart, objectID, property, value) {
        var obj = core_1.Prototypes.findObjectById(chart, objectID);
        if (!obj) {
            return;
        }
        core_1.Prototypes.setProperty(obj, property, value);
    };
    ChartTemplate.GetChartProperty = function (chart, objectID, property) {
        var obj = core_1.Prototypes.findObjectById(chart, objectID);
        if (!obj) {
            return null;
        }
        return core_1.Prototypes.getProperty(obj, property);
    };
    ChartTemplate.SetChartAttributeMapping = function (chart, objectID, attribute, value) {
        var obj = core_1.Prototypes.findObjectById(chart, objectID);
        if (!obj) {
            return;
        }
        obj.mappings[attribute] = value;
    };
    ChartTemplate.GetChartAttributeMapping = function (chart, objectID, attribute) {
        var obj = core_1.Prototypes.findObjectById(chart, objectID);
        if (!obj) {
            return null;
        }
        return obj.mappings[attribute];
    };
    return ChartTemplate;
}());
exports.ChartTemplate = ChartTemplate;
//# sourceMappingURL=chart_template.js.map