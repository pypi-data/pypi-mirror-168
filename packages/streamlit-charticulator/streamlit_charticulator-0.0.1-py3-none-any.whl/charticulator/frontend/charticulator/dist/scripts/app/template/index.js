"use strict";
/**
 * The {@link ChartTemplateBuilder} creates tempate ({@link ChartTemplate}) from the current chart.
 * {@link ChartTemplate} contains simplified version of {@link Chart} object in {@link ChartTemplate.specification} property.
 * Tempate can be exported as *.tmplt file (JSON format). It also uses on export to HTML file or on export as Power BI visual.
 *
 * Template can be loaded into container outside of Charticulator app to visualize with custom dataset.
 *
 * @packageDocumentation
 * @preferred
 */
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
exports.ChartTemplateBuilder = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var core_1 = require("../../core");
var dataset_1 = require("../../core/dataset");
var prototypes_1 = require("../../core/prototypes");
var specification_1 = require("../../core/specification");
/** Class builds the template from given {@link Specification.Chart} object  */
var ChartTemplateBuilder = /** @class */ (function () {
    function ChartTemplateBuilder(chart, dataset, manager, version) {
        this.chart = chart;
        this.dataset = dataset;
        this.manager = manager;
        this.version = version;
        this.usedColumns = {};
    }
    ChartTemplateBuilder.prototype.reset = function () {
        this.template = {
            specification: core_1.deepClone(this.chart),
            defaultAttributes: {},
            tables: [],
            inference: [],
            properties: [],
            version: this.version,
        };
        this.tableColumns = {};
        this.objectVisited = {};
    };
    ChartTemplateBuilder.prototype.addTable = function (table) {
        if (!Object.prototype.hasOwnProperty.call(this.tableColumns, table)) {
            this.tableColumns[table] = new Set();
        }
    };
    ChartTemplateBuilder.prototype.addColumn = function (table, columnName) {
        if (table == null) {
            table = this.dataset.tables[0].name;
        }
        var tableObject = core_1.getByName(this.dataset.tables, table);
        if (tableObject) {
            var column_1 = core_1.getByName(tableObject.columns, columnName);
            if (column_1) {
                if (column_1.metadata.isRaw) {
                    var notRawColumn = tableObject.columns.find(function (col) { return col.metadata.rawColumnName === column_1.name; });
                    if (Object.prototype.hasOwnProperty.call(this.tableColumns, table)) {
                        this.tableColumns[table].add(notRawColumn.name);
                    }
                    else {
                        this.tableColumns[table] = new Set([notRawColumn.name]);
                    }
                }
                // eslint-disable-next-line
                if (Object.prototype.hasOwnProperty.call(this.tableColumns, table)) {
                    this.tableColumns[table].add(columnName);
                }
                else {
                    this.tableColumns[table] = new Set([columnName]);
                }
            }
        }
    };
    ChartTemplateBuilder.prototype.addColumnsFromExpression = function (table, expr, textExpression) {
        var _this = this;
        if (expr) {
            var ex = void 0;
            if (textExpression) {
                ex = core_1.Expression.parseTextExpression(expr);
            }
            else {
                ex = core_1.Expression.parse(expr);
            }
            ex.replace(function (e) {
                if (e instanceof core_1.Expression.Variable) {
                    _this.addColumn(table, e.name);
                }
            });
        }
    };
    ChartTemplateBuilder.prototype.propertyToString = function (property) {
        var pn;
        if (typeof property == "string" || typeof property == "number") {
            pn = property.toString();
        }
        else {
            pn = property.property;
            if (property.field) {
                if (typeof property.field == "string" ||
                    typeof property.field == "number") {
                    pn += "." + property.field.toString();
                }
                else {
                    pn += "." + property.field.join(".");
                }
            }
            if (property.subfield) {
                if (typeof property.subfield == "string" ||
                    typeof property.subfield == "number") {
                    pn += "." + property.subfield.toString();
                }
                else {
                    pn += "." + property.subfield.join(".");
                }
            }
        }
        return pn;
    };
    // eslint-disable-next-line
    ChartTemplateBuilder.prototype.addObject = function (table, objectClass) {
        var e_1, _a, e_2, _b, e_3, _c;
        var _this = this;
        // Visit a object only once
        if (this.objectVisited[objectClass.object._id]) {
            return;
        }
        this.objectVisited[objectClass.object._id] = true;
        var template = this.template;
        // Get template inference data
        var params = objectClass.getTemplateParameters();
        if (params && params.inferences) {
            var _loop_1 = function (inference) {
                var e_4, _a, e_5, _b, e_6, _c;
                if (inference.axis) {
                    this_1.addColumnsFromExpression(inference.dataSource.table, inference.axis.expression);
                }
                if (inference.scale) {
                    // Find all objects that use the scale
                    var expressions = new Set();
                    var table_1 = null;
                    var groupBy = null;
                    try {
                        for (var _d = (e_4 = void 0, __values(core_1.Prototypes.forEachObject(this_1.template.specification))), _e = _d.next(); !_e.done; _e = _d.next()) {
                            var item = _e.value;
                            try {
                                for (var _f = (e_5 = void 0, __values(core_1.Prototypes.forEachMapping(item.object.mappings))), _g = _f.next(); !_g.done; _g = _f.next()) {
                                    var _h = __read(_g.value, 2), mapping = _h[1];
                                    if (mapping.type == specification_1.MappingType.scale) {
                                        var scaleMapping = mapping;
                                        if (scaleMapping.scale == inference.objectID) {
                                            expressions.add(scaleMapping.expression);
                                            if (item.kind == "glyph" || item.kind == "mark") {
                                                table_1 = item.glyph.table;
                                                try {
                                                    // Find the plot segment
                                                    for (var _j = (e_6 = void 0, __values(core_1.Prototypes.forEachObject(this_1.template.specification))), _k = _j.next(); !_k.done; _k = _j.next()) {
                                                        var ps = _k.value;
                                                        if (ps.kind == "chart-element" &&
                                                            core_1.Prototypes.isType(ps.object.classID, "plot-segment") &&
                                                            item.glyph._id === ps.chartElement.glyph) {
                                                            groupBy = ps.chartElement
                                                                .groupBy;
                                                            break; // TODO: for now, we assume it's the first one
                                                        }
                                                    }
                                                }
                                                catch (e_6_1) { e_6 = { error: e_6_1 }; }
                                                finally {
                                                    try {
                                                        if (_k && !_k.done && (_c = _j.return)) _c.call(_j);
                                                    }
                                                    finally { if (e_6) throw e_6.error; }
                                                }
                                            }
                                            else if (item.kind == "chart-element" &&
                                                core_1.Prototypes.isType(item.chartElement.classID, "legend.custom")) {
                                                // don't add column names legend expression into inferences
                                                expressions.delete(scaleMapping.expression);
                                            }
                                            else if (item.kind == "chart-element" &&
                                                core_1.Prototypes.isType(item.chartElement.classID, "links")) {
                                                var linkTable = item.object.properties.linkTable;
                                                var defaultTable = this_1.dataset.tables[0];
                                                table_1 = (linkTable && linkTable.table) || defaultTable.name;
                                            }
                                            else {
                                                table_1 = this_1.dataset.tables.find(function (table) { return table.type === dataset_1.TableType.Main; }).name;
                                            }
                                        }
                                    }
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
                    }
                    catch (e_4_1) { e_4 = { error: e_4_1 }; }
                    finally {
                        try {
                            if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                        }
                        finally { if (e_4) throw e_4.error; }
                    }
                    if (expressions.size == 0) {
                        return "continue";
                    }
                    inference.scale.expressions = Array.from(expressions);
                    if (!inference.dataSource) {
                        inference.dataSource = {
                            table: table_1,
                            groupBy: groupBy,
                        };
                    }
                }
                if (inference.expression) {
                    this_1.addColumnsFromExpression(inference.dataSource.table, inference.expression.expression);
                }
                if (inference.nestedChart) {
                    var nestedChart = inference.nestedChart;
                    Object.keys(nestedChart.columnNameMap).forEach(function (key) {
                        _this.addColumn(inference.dataSource.table, key);
                    });
                }
                if (inference.axis) {
                    var templateObject = core_1.Prototypes.findObjectById(this_1.chart, inference.objectID);
                    if (templateObject.properties[inference.axis.property].autoDomainMin !== "undefined") {
                        inference.autoDomainMin = templateObject.properties[inference.axis.property].autoDomainMin;
                    }
                    if (templateObject.properties[inference.axis.property].autoDomainMax !== "undefined") {
                        inference.autoDomainMax = templateObject.properties[inference.axis.property].autoDomainMax;
                    }
                    if (inference.autoDomainMax === undefined) {
                        inference.autoDomainMax = true;
                    }
                    if (inference.autoDomainMax === undefined) {
                        inference.autoDomainMax = true;
                    }
                }
                template.inference.push(inference);
            };
            var this_1 = this;
            try {
                for (var _d = __values(params.inferences), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var inference = _e.value;
                    _loop_1(inference);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        if (params && params.properties) {
            try {
                for (var _f = __values(params.properties), _g = _f.next(); !_g.done; _g = _f.next()) {
                    var property = _g.value;
                    // Make a default display name
                    var pn = "";
                    if (property.target.property) {
                        pn = this.propertyToString(property.target.property);
                    }
                    else if (property.target.attribute) {
                        pn = property.target.attribute;
                    }
                    property.displayName = objectClass.object.properties.name + "/" + pn;
                    template.properties.push(property);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
        // Add filter
        var plotSegmentObj = objectClass.object;
        if (core_1.Prototypes.isType(plotSegmentObj.classID, "plot-segment")) {
            this.addTable(plotSegmentObj.table);
            var filter = plotSegmentObj.filter;
            if (filter) {
                var categories = filter.categories, expression = filter.expression;
                if (expression) {
                    this.addColumnsFromExpression(table, expression);
                }
                if (categories) {
                    this.addColumnsFromExpression(table, categories.expression);
                }
            }
            var groupBy = plotSegmentObj.groupBy;
            if (groupBy && groupBy.expression) {
                this.addColumnsFromExpression(table, groupBy.expression);
            }
        }
        try {
            // Get mappings
            for (var _h = __values(core_1.Prototypes.forEachMapping(objectClass.object.mappings)), _j = _h.next(); !_j.done; _j = _h.next()) {
                var _k = __read(_j.value, 2), mapping = _k[1];
                if (mapping.type == specification_1.MappingType.scale) {
                    var scaleMapping = mapping;
                    this.addColumnsFromExpression(scaleMapping.table, scaleMapping.expression);
                }
                if (mapping.type == specification_1.MappingType.text) {
                    var textMapping = mapping;
                    this.addColumnsFromExpression(textMapping.table, textMapping.textExpression, true);
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
            }
            finally { if (e_3) throw e_3.error; }
        }
    };
    /**
     * Builds template.
     * All exposed objects should be initialized in {@link ChartTemplate} class
     * @returns JSON structure of template
     */
    // eslint-disable-next-line
    ChartTemplateBuilder.prototype.build = function () {
        var e_7, _a, e_8, _b, e_9, _c;
        var _this = this;
        var _d, _e, _f, _g, _h;
        this.reset();
        var template = this.template;
        var _loop_2 = function (elementClass) {
            var e_10, _a, e_11, _b, e_12, _c;
            var table = null;
            if (core_1.Prototypes.isType(elementClass.object.classID, "plot-segment")) {
                var plotSegment = elementClass.object;
                table = plotSegment.table;
            }
            if (core_1.Prototypes.isType(elementClass.object.classID, "links")) {
                if (core_1.Prototypes.isType(elementClass.object.classID, "links.through")) {
                    var facetExpressions = elementClass.object.properties
                        .linkThrough.facetExpressions;
                    var mainTable = this_2.dataset.tables.find(function (table) { return table.type === dataset_1.TableType.Main; });
                    this_2.addTable(mainTable.name);
                    try {
                        for (var facetExpressions_1 = (e_10 = void 0, __values(facetExpressions)), facetExpressions_1_1 = facetExpressions_1.next(); !facetExpressions_1_1.done; facetExpressions_1_1 = facetExpressions_1.next()) {
                            var expression = facetExpressions_1_1.value;
                            this_2.addColumn(mainTable.name, expression);
                        }
                    }
                    catch (e_10_1) { e_10 = { error: e_10_1 }; }
                    finally {
                        try {
                            if (facetExpressions_1_1 && !facetExpressions_1_1.done && (_a = facetExpressions_1.return)) _a.call(facetExpressions_1);
                        }
                        finally { if (e_10) throw e_10.error; }
                    }
                }
                var linkTable = elementClass.object.properties
                    .linkTable;
                if (linkTable) {
                    var linksTableName_1 = linkTable.table;
                    this_2.addTable(linksTableName_1); // TODO get table by type
                    var linksTable = this_2.dataset.tables.find(function (table) { return table.name === linksTableName_1; });
                    linksTable.columns.forEach(function (linksColumn) {
                        return _this.addColumn(linksTableName_1, linksColumn.name);
                    });
                    var table_2 = this_2.dataset.tables[0];
                    var idColumn = table_2 && table_2.columns.find(function (column) { return column.name === "id"; });
                    if (idColumn) {
                        this_2.addColumn(table_2.name, idColumn.name);
                    }
                }
            }
            this_2.addObject(table, elementClass);
            if (core_1.Prototypes.isType(elementClass.object.classID, "plot-segment")) {
                var plotSegmentState = elementClass.state;
                try {
                    for (var _d = (e_11 = void 0, __values(plotSegmentState.glyphs)), _e = _d.next(); !_e.done; _e = _d.next()) {
                        var glyph = _e.value;
                        this_2.addObject(table, this_2.manager.getClass(glyph));
                        try {
                            for (var _f = (e_12 = void 0, __values(glyph.marks)), _g = _f.next(); !_g.done; _g = _f.next()) {
                                var mark = _g.value;
                                this_2.addObject(table, this_2.manager.getClass(mark));
                            }
                        }
                        catch (e_12_1) { e_12 = { error: e_12_1 }; }
                        finally {
                            try {
                                if (_g && !_g.done && (_c = _f.return)) _c.call(_f);
                            }
                            finally { if (e_12) throw e_12.error; }
                        }
                        // Only one glyph is enough.
                        break;
                    }
                }
                catch (e_11_1) { e_11 = { error: e_11_1 }; }
                finally {
                    try {
                        if (_e && !_e.done && (_b = _d.return)) _b.call(_d);
                    }
                    finally { if (e_11) throw e_11.error; }
                }
            }
        };
        var this_2 = this;
        try {
            for (var _j = __values(this.manager.getElements()), _k = _j.next(); !_k.done; _k = _j.next()) {
                var elementClass = _k.value;
                _loop_2(elementClass);
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_k && !_k.done && (_a = _j.return)) _a.call(_j);
            }
            finally { if (e_7) throw e_7.error; }
        }
        try {
            for (var _l = __values(this.manager.chartState.scales), _m = _l.next(); !_m.done; _m = _l.next()) {
                var scaleState = _m.value;
                this.addObject(null, this.manager.getClass(scaleState));
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_m && !_m.done && (_b = _l.return)) _b.call(_l);
            }
            finally { if (e_8) throw e_8.error; }
        }
        this.addObject(null, this.manager.getChartClass(this.manager.chartState));
        // need to foreach objects to find all used columns
        try {
            var _loop_3 = function (item) {
                var e_13, _a;
                if (item.kind == prototypes_1.ObjectItemKind.ChartElement) {
                    if (core_1.Prototypes.isType(item.chartElement.classID, "legend.custom")) {
                        var scaleMapping = item.chartElement.mappings
                            .mappingOptions;
                        scaleMapping.expression = this_3.trackColumnFromExpression(scaleMapping.expression, scaleMapping.table);
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "plot-segment")) {
                        var plotSegment = item.chartElement;
                        // need to parse all expression to get column name
                        var originalTable = plotSegment.table;
                        var filter = plotSegment.filter;
                        if (filter && filter.expression) {
                            this_3.trackColumnFromExpression(filter.expression, originalTable);
                        }
                        var groupBy = plotSegment.groupBy;
                        if (groupBy && groupBy.expression) {
                            this_3.trackColumnFromExpression(groupBy.expression, originalTable);
                        }
                        var xAxisExpression = (_d = plotSegment.properties.xData) === null || _d === void 0 ? void 0 : _d.expression;
                        if (xAxisExpression) {
                            this_3.trackColumnFromExpression(xAxisExpression, originalTable);
                        }
                        var yAxisExpression = (_e = plotSegment.properties.yData) === null || _e === void 0 ? void 0 : _e.expression;
                        if (yAxisExpression) {
                            this_3.trackColumnFromExpression(yAxisExpression, originalTable);
                        }
                        var axisExpression = (_f = plotSegment.properties.axis) === null || _f === void 0 ? void 0 : _f.expression;
                        if (axisExpression) {
                            this_3.trackColumnFromExpression(axisExpression, originalTable);
                        }
                        var sublayout = (_h = (_g = plotSegment.properties
                            .sublayout) === null || _g === void 0 ? void 0 : _g.order) === null || _h === void 0 ? void 0 : _h.expression;
                        if (sublayout) {
                            this_3.trackColumnFromExpression(sublayout, originalTable);
                        }
                    }
                    if (core_1.Prototypes.isType(item.chartElement.classID, "links")) {
                        if (item.chartElement.classID == "links.through") {
                            var props_1 = item.chartElement
                                .properties;
                            if (props_1.linkThrough.facetExpressions) {
                                props_1.linkThrough.facetExpressions = props_1.linkThrough.facetExpressions.map(function (x) {
                                    return _this.trackColumnFromExpression(x, core_1.getById(_this.template.specification.elements, props_1.linkThrough.plotSegment).table);
                                });
                            }
                        }
                        if (item.chartElement.classID == "links.table") {
                            var props = item.chartElement
                                .properties;
                            if (!this_3.usedColumns[props.linkTable.table]) {
                                this_3.trackTable(props.linkTable.table);
                            }
                        }
                    }
                }
                if (item.kind == "glyph") {
                    if (!this_3.usedColumns[item.glyph.table]) {
                        this_3.trackTable(item.glyph.table);
                    }
                }
                if (item.kind === prototypes_1.ObjectItemKind.Mark) {
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.nested-chart")) {
                        var nestedChart = item.mark;
                        var columnNameMap = Object.keys(nestedChart.properties.columnNameMap);
                        var mainTable_1 = this_3.usedColumns[this_3.manager.dataset.tables.find(function (t) { return t.type === dataset_1.TableType.Main; })
                            .name];
                        columnNameMap.forEach(function (columnNames) { return (mainTable_1[columnNames] = columnNames); });
                    }
                    if (core_1.Prototypes.isType(item.mark.classID, "mark.data-axis")) {
                        try {
                            var glyphId_1 = item.glyph._id;
                            var glyphPlotSegment = __spread(prototypes_1.forEachObject(this_3.manager.chart)).find(function (item) {
                                return item.kind == prototypes_1.ObjectItemKind.ChartElement &&
                                    core_1.Prototypes.isType(item.chartElement.classID, "plot-segment") &&
                                    item.chartElement.glyph === glyphId_1;
                            });
                            var dataExpressions = item.mark.properties
                                .dataExpressions;
                            var table_3 = glyphPlotSegment.chartElement.table;
                            dataExpressions.forEach(function (expression) {
                                expression.expression = _this.trackColumnFromExpression(expression.expression, table_3);
                            });
                        }
                        catch (ex) {
                            console.error(ex);
                        }
                    }
                }
                var mappings = item.object.mappings;
                try {
                    for (var _b = (e_13 = void 0, __values(prototypes_1.forEachMapping(mappings))), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var _d = __read(_c.value, 2), mapping = _d[1];
                        if (mapping.type == specification_1.MappingType.scale) {
                            var scaleMapping = mapping;
                            scaleMapping.expression = this_3.trackColumnFromExpression(scaleMapping.expression, scaleMapping.table);
                            if (!this_3.usedColumns[scaleMapping.table]) {
                                this_3.trackTable(scaleMapping.table);
                            }
                        }
                        if (mapping.type == specification_1.MappingType.text) {
                            var textMapping = mapping;
                            if (!this_3.usedColumns[textMapping.table]) {
                                this_3.trackTable(textMapping.table);
                            }
                            textMapping.textExpression = this_3.trackColumnFromExpression(textMapping.textExpression, textMapping.table, true);
                        }
                    }
                }
                catch (e_13_1) { e_13 = { error: e_13_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_13) throw e_13.error; }
                }
            };
            var this_3 = this;
            try {
                for (var _o = __values(prototypes_1.forEachObject(this.manager.chart)), _p = _o.next(); !_p.done; _p = _o.next()) {
                    var item = _p.value;
                    _loop_3(item);
                }
            }
            catch (e_9_1) { e_9 = { error: e_9_1 }; }
            finally {
                try {
                    if (_p && !_p.done && (_c = _o.return)) _c.call(_o);
                }
                finally { if (e_9) throw e_9.error; }
            }
        }
        catch (ex) {
            console.error(ex);
        }
        // Extract data tables
        // if usedColumns count is 0, error was happened, add all columns as used
        var noUsedColumns = Object.keys(this.usedColumns).length === 0;
        template.tables = this.dataset.tables
            .map(function (table) {
            if (Object.prototype.hasOwnProperty.call(_this.tableColumns, table.name) &&
                (_this.usedColumns[table.name] || noUsedColumns)) {
                return {
                    name: table.name,
                    type: table.type,
                    columns: table.columns
                        .filter(function (x) {
                        var _a;
                        return ((_this.tableColumns[table.name].has(x.name) && ((_a = _this.usedColumns[table.name]) === null || _a === void 0 ? void 0 : _a[x.name])) ||
                            core_1.isReservedColumnName(x.name));
                    })
                        .map(function (x) { return ({
                        displayName: x.displayName || x.name,
                        name: x.name,
                        type: x.type,
                        metadata: x.metadata,
                    }); }),
                };
            }
            else {
                return null;
            }
        })
            .filter(function (x) { return x != null; });
        this.computeDefaultAttributes();
        return template;
    };
    ChartTemplateBuilder.prototype.trackColumnFromExpression = function (expr, table, isText) {
        if (isText === void 0) { isText = false; }
        if (isText) {
            return core_1.Expression.parseTextExpression(expr)
                .replace(core_1.Expression.variableReplacer(this.trackTable(table)))
                .toString();
        }
        return core_1.Expression.parse(expr)
            .replace(core_1.Expression.variableReplacer(this.trackTable(table)))
            .toString();
    };
    ChartTemplateBuilder.prototype.trackTable = function (table) {
        var _this = this;
        if (!this.usedColumns[table]) {
            this.usedColumns[table] = {
                hasOwnProperty: function (v) {
                    _this.usedColumns[table][v] = v;
                    return true;
                },
            };
        }
        return this.usedColumns[table];
    };
    /**
     * Computes the default attributes
     */
    ChartTemplateBuilder.prototype.computeDefaultAttributes = function () {
        var _this = this;
        var counts = {};
        // Go through all the mark instances
        this.manager.enumerateClassesByType("mark", function (cls, state) {
            var _id = cls.object._id;
            // Basic idea is sum up the attributes for each mark object, and then average them at the end
            var totals = (_this.template.defaultAttributes[_id] =
                _this.template.defaultAttributes[_id] || {});
            Object.keys(state.attributes).forEach(function (attribute) {
                // Only support numbers for now
                if (cls.attributes[attribute] &&
                    cls.attributes[attribute].type === "number") {
                    totals[attribute] = totals[attribute] || 0;
                    totals[attribute] += state.attributes[attribute] || 0;
                    counts[_id] = (counts[_id] || 0) + 1;
                }
            });
        });
        // The default attributes are currently totals, now divide each attribute by the count to average them
        Object.keys(this.template.defaultAttributes).forEach(function (objId) {
            var attribs = _this.template.defaultAttributes[objId];
            Object.keys(attribs).forEach(function (attribute) {
                attribs[attribute] = attribs[attribute] / counts[objId];
            });
        });
    };
    return ChartTemplateBuilder;
}());
exports.ChartTemplateBuilder = ChartTemplateBuilder;
//# sourceMappingURL=index.js.map