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
Object.defineProperty(exports, "__esModule", { value: true });
exports.GlyphConstraintAnalyzer = exports.ChartConstraintSolver = void 0;
var Dataset = require("../dataset");
var Expression = require("../expression");
var Prototypes = require("../prototypes");
var common_1 = require("../common");
var abstract_1 = require("./abstract");
var wasm_solver_1 = require("./wasm_solver");
var expression_1 = require("../expression");
var specification_1 = require("../specification");
/** Solves constraints in the scope of a chart */
var ChartConstraintSolver = /** @class */ (function () {
    /**
     * Create a ChartConstraintSolver
     * - stage == "chart": disregard glyphs, solve chart-level constraints
     * - stage == "glyphs": fix chart-level attributes, solve only glyphs
     * @param stage determines the scope of the variables to solve
     */
    function ChartConstraintSolver(stage) {
        this.supportVariables = new common_1.KeyNameMap();
        this.glyphAnalyzeResults = new WeakMap();
        this.solver = new wasm_solver_1.WASMSolver();
        this.stage = stage;
    }
    ChartConstraintSolver.prototype.setManager = function (manager) {
        this.chart = manager.chart;
        this.chartState = manager.chartState;
        this.manager = manager;
        this.dataset = manager.dataset;
        this.datasetContext = new Dataset.DatasetContext(this.dataset);
        this.expressionCache = new Expression.ExpressionCache();
    };
    ChartConstraintSolver.prototype.setDataset = function (dataset) {
        this.dataset = dataset;
        this.datasetContext = new Dataset.DatasetContext(this.dataset);
        this.expressionCache = new Expression.ExpressionCache();
    };
    ChartConstraintSolver.prototype.solve = function () {
        var loss = this.solver.solve();
        this.solver.applyPlugins();
        return { softLoss: loss[1], hardLoss: loss[0] };
    };
    ChartConstraintSolver.prototype.destroy = function () {
        if (this.solver) {
            this.solver.destroy();
        }
    };
    // eslint-disable-next-line max-lines-per-function
    ChartConstraintSolver.prototype.addMapping = function (attrs, parentAttrs, attr, info, mapping, rowContext, rowIndex) {
        var _a, _b;
        if (rowContext == null &&
            (mapping.type == specification_1.MappingType.scale || mapping.type == specification_1.MappingType.text)) {
            var xMapping = mapping ||
                mapping;
            rowContext = this.manager.getChartDataContext(xMapping.table);
        }
        switch (mapping.type) {
            case specification_1.MappingType.scale:
                {
                    var scaleMapping = mapping;
                    if (scaleMapping.scale != null) {
                        // Apply the scale
                        var expr = this.expressionCache.parse(scaleMapping.expression);
                        var dataValue = expr.getValue(rowContext);
                        var scaleClass = (this.manager.getClassById(scaleMapping.scale));
                        if (!info.solverExclude) {
                            scaleClass.buildConstraint(dataValue, this.solver.attr(attrs, attr), this.solver);
                        }
                        var value = scaleClass.mapDataToAttribute(dataValue);
                        attrs[attr] = value;
                        // this.registry.makeConstant(attrs, attr);
                        // this.hardBuilder.addLinear(value as number, [[-1, this.hardBuilder.attr(attrs, attr)]])
                    }
                    else {
                        // No scale, map the column value directly
                        var expr = this.expressionCache.parse(scaleMapping.expression);
                        var dataValue = expr.getValue(rowContext);
                        attrs[attr] = dataValue;
                        if (!info.solverExclude) {
                            this.solver.makeConstant(attrs, attr);
                        }
                        // this.hardBuilder.addLinear(attrs[attr] as number, [[-1, this.hardBuilder.attr(attrs, attr)]])
                    }
                }
                break;
            case specification_1.MappingType.expressionScale:
                {
                    var dataTable = this.manager.dataset.tables.filter(function (tb) { return tb.type === "Main"; });
                    var dataImageIndex_1 = (_a = dataTable === null || dataTable === void 0 ? void 0 : dataTable[0]) === null || _a === void 0 ? void 0 : _a.rows[rowIndex[0]][common_1.ImageKeyColumn];
                    var imageTable = this.manager.dataset.tables.filter(function (tb) { return tb.type === "Image"; });
                    var imageDataTableIndex = (_b = imageTable === null || imageTable === void 0 ? void 0 : imageTable[0]) === null || _b === void 0 ? void 0 : _b.rows.find(function (row) { return row[common_1.ImageKeyColumn] == dataImageIndex_1; });
                    // get table from scale mapping
                    var scaleMapping = (mapping);
                    var tableContext = this.manager.dataflow.getTable(scaleMapping.table);
                    rowContext = tableContext.getGroupedContext(rowIndex);
                    // const expr = this.expressionCache.parse(scaleMapping.expression);
                    // const dataValue = <Dataset.DataValue>expr.getValue(rowContext);
                    var dataValue = "";
                    var scaleClass = (this.manager.getClassById(scaleMapping.scale));
                    if (!info.solverExclude) {
                        scaleClass.buildConstraint(dataValue, this.solver.attr(attrs, attr), this.solver);
                    }
                    var value = scaleClass.mapDataToAttribute(imageDataTableIndex[common_1.ImageKeyColumn]);
                    attrs[attr] = value;
                }
                break;
            case specification_1.MappingType.text:
                {
                    var textMapping = mapping;
                    var expr = this.expressionCache.parseTextExpression(textMapping.textExpression);
                    if (expr.parts.find(function (part) {
                        return part.expression instanceof expression_1.FunctionCall &&
                            part.expression.name === "columnName";
                    })) {
                        attrs[attr] = expr.getValue(rowContext.getTable());
                    }
                    else {
                        attrs[attr] = expr.getValue(rowContext);
                    }
                }
                break;
            case specification_1.MappingType.value:
                {
                    var valueMapping = mapping;
                    attrs[attr] = valueMapping.value;
                    if (!info.solverExclude) {
                        this.solver.makeConstant(attrs, attr);
                    }
                    // this.registry.makeConstant(attrs, attr);
                }
                break;
            case specification_1.MappingType.parent:
                {
                    var parentMapping = mapping;
                    this.solver.addEquals(abstract_1.ConstraintStrength.HARD, this.solver.attr(attrs, attr), this.solver.attr(parentAttrs, parentMapping.parentAttribute));
                }
                break;
        }
    };
    ChartConstraintSolver.prototype.addObject = function (object, objectState, parentState, rowContext, solve, rowIndex) {
        var e_1, _a;
        var objectClass = this.manager.getClass(objectState);
        try {
            for (var _b = __values(objectClass.attributeNames), _c = _b.next(); !_c.done; _c = _b.next()) {
                var attr = _c.value;
                var info = objectClass.attributes[attr];
                if (!info.solverExclude) {
                    if (objectState.attributes[attr] == null) {
                        objectState.attributes[attr] = 0;
                    }
                    this.addAttribute(objectState.attributes, attr, solve || info.editableInGlyphStage);
                }
                if (!info.stateExclude) {
                    if (Object.prototype.hasOwnProperty.call(object.mappings, attr)) {
                        // If the attribute is mapped, apply the mapping, and do not compute gradient
                        var mapping = object.mappings[attr];
                        this.addMapping(objectState.attributes, parentState != null ? parentState.attributes : null, attr, info, mapping, rowContext, rowIndex);
                    }
                    else {
                        if (info.defaultValue !== undefined) {
                            objectState.attributes[attr] = info.defaultValue;
                        }
                    }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    ChartConstraintSolver.prototype.addScales = function (allowScaleParameterChange) {
        var e_2, _a;
        if (allowScaleParameterChange === void 0) { allowScaleParameterChange = true; }
        var _b = this, chart = _b.chart, chartState = _b.chartState;
        try {
            for (var _c = __values(common_1.zip(chart.scales, chartState.scales)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), scale = _e[0], scaleState = _e[1];
                this.addObject(scale, scaleState, null, null, allowScaleParameterChange, [
                    0,
                ]);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_2) throw e_2.error; }
        }
    };
    ChartConstraintSolver.prototype.getSupportVariable = function (key, name, defaultValue) {
        if (this.supportVariables.has(key, name)) {
            return this.solver.attr(this.supportVariables.get(key, name), "value");
        }
        else {
            var attr = {};
            attr.value = defaultValue;
            this.supportVariables.add(key, name, attr);
            var variable = this.solver.attr(attr, "value", {
                edit: true,
            });
            return variable;
        }
    };
    ChartConstraintSolver.prototype.addMark = function (layout, mark, rowContext, markState, element, elementState, rowIndex) {
        var _this = this;
        this.addObject(element, elementState, markState, rowContext, true, rowIndex);
        var elementClass = this.manager.getMarkClass(elementState);
        elementClass.buildConstraints(this.solver, {
            rowContext: rowContext,
            getExpressionValue: function (expr, context) {
                return _this.manager.dataflow.cache
                    .parse(expr)
                    .getNumberValue(context);
            },
        }, this.manager);
    };
    ChartConstraintSolver.prototype.getAttachedAttributes = function (mark) {
        var e_3, _a;
        var attached = new Set();
        try {
            for (var _b = __values(mark.marks), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (element.classID == "mark.anchor") {
                    continue;
                }
                for (var name_1 in element.mappings) {
                    var mapping = element.mappings[name_1];
                    if (mapping.type == specification_1.MappingType.parent) {
                        attached.add(mapping.parentAttribute);
                    }
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
        return attached;
    };
    ChartConstraintSolver.prototype.getGlyphAnalyzeResult = function (glyph) {
        if (this.glyphAnalyzeResults.has(glyph)) {
            return this.glyphAnalyzeResults.get(glyph);
        }
        var analyzer = new GlyphConstraintAnalyzer(glyph, this.manager);
        analyzer.solve();
        this.glyphAnalyzeResults.set(glyph, analyzer);
        return analyzer;
    };
    ChartConstraintSolver.prototype.addGlyph = function (layout, rowContext, glyph, glyphState, rowIndex) {
        var e_4, _a, e_5, _b, e_6, _c;
        // Mark attributes
        this.addObject(glyph, glyphState, null, rowContext, true, rowIndex);
        var glyphAnalyzed = this.getGlyphAnalyzeResult(glyph);
        var glyphClass = this.manager.getGlyphClass(glyphState);
        try {
            for (var _d = __values(glyphClass.attributeNames), _e = _d.next(); !_e.done; _e = _d.next()) {
                var attr = _e.value;
                // const info = glyphClass.attributes[attr];
                // if (info.solverExclude) {
                //   continue;
                // }
                // this.addAttribute(glyphState.attributes, attr, true);
                // If width/height are not constrained, make them constant
                if (attr == "width" && glyphAnalyzed.widthFree) {
                    var variable = this.getSupportVariable(layout, glyph._id + "/" + attr, glyphState.attributes[attr]);
                    this.solver.addEquals(abstract_1.ConstraintStrength.HARD, variable, this.solver.attr(glyphState.attributes, attr));
                }
                if (attr == "height" && glyphAnalyzed.heightFree) {
                    var variable = this.getSupportVariable(layout, glyph._id + "/" + attr, glyphState.attributes[attr]);
                    this.solver.addEquals(abstract_1.ConstraintStrength.HARD, variable, this.solver.attr(glyphState.attributes, attr));
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
        try {
            // Element attributes and intrinsic constraints
            for (var _f = __values(common_1.zip(glyph.marks, glyphState.marks)), _g = _f.next(); !_g.done; _g = _f.next()) {
                var _h = __read(_g.value, 2), element = _h[0], elementState = _h[1];
                this.addMark(layout, glyph, rowContext, glyphState, element, elementState, rowIndex);
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_5) throw e_5.error; }
        }
        // Mark-level constraints
        glyphClass.buildIntrinsicConstraints(this.solver);
        try {
            for (var _j = __values(glyph.constraints), _k = _j.next(); !_k.done; _k = _j.next()) {
                var constraint = _k.value;
                var cls = Prototypes.Constraints.ConstraintTypeClass.getClass(constraint.type);
                cls.buildConstraints(constraint, glyph.marks, glyphState.marks, this.solver);
            }
        }
        catch (e_6_1) { e_6 = { error: e_6_1 }; }
        finally {
            try {
                if (_k && !_k.done && (_c = _j.return)) _c.call(_j);
            }
            finally { if (e_6) throw e_6.error; }
        }
    };
    ChartConstraintSolver.prototype.addAttribute = function (attrs, attr, edit) {
        this.solver.attr(attrs, attr, { edit: edit });
    };
    ChartConstraintSolver.prototype.addChart = function () {
        var e_7, _a, e_8, _b, e_9, _c;
        var _this = this;
        var _d = this, chart = _d.chart, chartState = _d.chartState;
        this.addObject(chart, chartState, null, null, this.stage == "chart", [0]);
        var boundsClass = this.manager.getChartClass(chartState);
        boundsClass.buildIntrinsicConstraints(this.solver);
        try {
            for (var _e = __values(common_1.zip(chart.elements, chartState.elements)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var _g = __read(_f.value, 2), element = _g[0], elementState = _g[1];
                this.addObject(element, elementState, chartState, null, this.stage == "chart", [0]);
                var elementClass = this.manager.getChartElementClass(elementState);
                elementClass.buildConstraints(this.solver, {
                    getExpressionValue: function (expr, context) {
                        return _this.manager.dataflow.cache
                            .parse(expr)
                            .getNumberValue(context);
                    },
                    getGlyphAttributes: function (glyphID, table, rowIndex) {
                        var analyzed = _this.getGlyphAnalyzeResult(common_1.getById(_this.chart.glyphs, glyphID));
                        return analyzed.computeAttributes(_this.manager.dataflow.getTable(table).getGroupedContext(rowIndex));
                    },
                }, this.manager);
                if (this.stage == "glyphs") {
                    if (Prototypes.isType(element.classID, "plot-segment")) {
                        var layout = element;
                        var layoutState = elementState;
                        var mark = common_1.getById(chart.glyphs, layout.glyph);
                        var tableContext = this.manager.dataflow.getTable(layout.table);
                        try {
                            for (var _h = (e_8 = void 0, __values(common_1.zip(layoutState.dataRowIndices, layoutState.glyphs))), _j = _h.next(); !_j.done; _j = _h.next()) {
                                var _k = __read(_j.value, 2), dataRowIndex = _k[0], markState = _k[1];
                                this.addGlyph(layout, tableContext.getGroupedContext(dataRowIndex), mark, markState, dataRowIndex);
                            }
                        }
                        catch (e_8_1) { e_8 = { error: e_8_1 }; }
                        finally {
                            try {
                                if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
                            }
                            finally { if (e_8) throw e_8.error; }
                        }
                        elementClass.buildGlyphConstraints(this.solver, {
                            getExpressionValue: function (expr, context) {
                                return _this.manager.dataflow.cache
                                    .parse(expr)
                                    .getNumberValue(context);
                            },
                            getGlyphAttributes: function (glyphID, table, rowIndex) {
                                var analyzed = _this.getGlyphAnalyzeResult(common_1.getById(_this.chart.glyphs, glyphID));
                                return analyzed.computeAttributes(_this.manager.dataflow
                                    .getTable(table)
                                    .getGroupedContext(rowIndex));
                            },
                        });
                    }
                }
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
            }
            finally { if (e_7) throw e_7.error; }
        }
        try {
            for (var _l = __values(chart.constraints), _m = _l.next(); !_m.done; _m = _l.next()) {
                var constraint = _m.value;
                var cls = Prototypes.Constraints.ConstraintTypeClass.getClass(constraint.type);
                cls.buildConstraints(constraint, chart.elements, chartState.elements, this.solver);
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (_m && !_m.done && (_c = _l.return)) _c.call(_l);
            }
            finally { if (e_9) throw e_9.error; }
        }
    };
    ChartConstraintSolver.prototype.setup = function (manager) {
        this.setManager(manager);
        this.addScales(true);
        this.addChart();
    };
    return ChartConstraintSolver;
}());
exports.ChartConstraintSolver = ChartConstraintSolver;
var GlyphConstraintAnalyzer = /** @class */ (function (_super) {
    __extends(GlyphConstraintAnalyzer, _super);
    function GlyphConstraintAnalyzer(glyph, manager) {
        var e_10, _a, e_11, _b, e_12, _c, e_13, _d, e_14, _e;
        var _this = _super.call(this) || this;
        // Variable registry
        _this.variableRegistry = new common_1.KeyNameMap();
        _this.indexToAttribute = new Map();
        _this.currentVariableIndex = 0;
        _this.linears = [];
        _this.inputBiases = new Map();
        _this.indexToBias = new Map();
        _this.inputBiasesCount = 0;
        _this.dataInputList = new Map();
        _this.manager = manager;
        var glyphState = {
            attributes: {},
            marks: [],
        };
        var glyphClass = (Prototypes.ObjectClasses.Create(null, glyph, glyphState));
        glyphClass.initializeState();
        try {
            for (var _f = __values(glyph.marks), _g = _f.next(); !_g.done; _g = _f.next()) {
                var mark = _g.value;
                var markState = {
                    attributes: {},
                };
                glyphState.marks.push(markState);
                var markClass = Prototypes.ObjectClasses.Create(glyphClass, mark, markState);
                markClass.initializeState();
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_a = _f.return)) _a.call(_f);
            }
            finally { if (e_10) throw e_10.error; }
        }
        try {
            for (var _h = __values(glyphClass.attributeNames), _j = _h.next(); !_j.done; _j = _h.next()) {
                var attr = _j.value;
                var info = glyphClass.attributes[attr];
                if (info.solverExclude) {
                    continue;
                }
                _this.addAttribute(glyphState.attributes, attr, glyph._id);
                if (Object.prototype.hasOwnProperty.call(glyph.mappings, attr)) {
                    _this.addMapping(glyphState.attributes, attr, glyph.mappings[attr], null);
                }
            }
        }
        catch (e_11_1) { e_11 = { error: e_11_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
            }
            finally { if (e_11) throw e_11.error; }
        }
        try {
            for (var _k = __values(common_1.zip(glyph.marks, glyphState.marks)), _l = _k.next(); !_l.done; _l = _k.next()) {
                var _m = __read(_l.value, 2), mark = _m[0], markState = _m[1];
                var markClass = (Prototypes.ObjectClasses.Create(glyphClass, mark, markState));
                try {
                    for (var _o = (e_13 = void 0, __values(markClass.attributeNames)), _p = _o.next(); !_p.done; _p = _o.next()) {
                        var attr = _p.value;
                        var info = markClass.attributes[attr];
                        if (info.solverExclude) {
                            continue;
                        }
                        _this.addAttribute(markState.attributes, attr, mark._id);
                        if (Object.prototype.hasOwnProperty.call(mark.mappings, attr)) {
                            _this.addMapping(markState.attributes, attr, mark.mappings[attr], glyphState.attributes);
                        }
                    }
                }
                catch (e_13_1) { e_13 = { error: e_13_1 }; }
                finally {
                    try {
                        if (_p && !_p.done && (_d = _o.return)) _d.call(_o);
                    }
                    finally { if (e_13) throw e_13.error; }
                }
                markClass.buildConstraints(_this, {
                    getExpressionValue: function () { return 1; },
                }, _this.manager);
            }
        }
        catch (e_12_1) { e_12 = { error: e_12_1 }; }
        finally {
            try {
                if (_l && !_l.done && (_c = _k.return)) _c.call(_k);
            }
            finally { if (e_12) throw e_12.error; }
        }
        glyphClass.buildIntrinsicConstraints(_this);
        _this.addInputAttribute("x", _this.attr(glyphState.attributes, "x"));
        _this.addInputAttribute("y", _this.attr(glyphState.attributes, "y"));
        try {
            for (var _q = __values(glyph.constraints), _r = _q.next(); !_r.done; _r = _q.next()) {
                var constraint = _r.value;
                var cls = Prototypes.Constraints.ConstraintTypeClass.getClass(constraint.type);
                cls.buildConstraints(constraint, glyph.marks, glyphState.marks, _this);
            }
        }
        catch (e_14_1) { e_14 = { error: e_14_1 }; }
        finally {
            try {
                if (_r && !_r.done && (_e = _q.return)) _e.call(_q);
            }
            finally { if (e_14) throw e_14.error; }
        }
        _this.glyphState = glyphState;
        return _this;
    }
    GlyphConstraintAnalyzer.prototype.addAttribute = function (attrs, attr, id) {
        var attrInfo = {
            index: this.currentVariableIndex,
            type: "object",
            id: id,
            attribute: attr,
        };
        this.variableRegistry.add(attrs, attr, attrInfo);
        this.indexToAttribute.set(attrInfo.index, attrInfo);
        this.currentVariableIndex += 1;
        return attrInfo;
    };
    // Allocate or get attribute index
    GlyphConstraintAnalyzer.prototype.attr = function (attrs, attr) {
        if (this.variableRegistry.has(attrs, attr)) {
            return this.variableRegistry.get(attrs, attr);
        }
        else {
            var attrInfo = {
                index: this.currentVariableIndex,
                id: common_1.uniqueID(),
                type: "object",
                attribute: attr,
            };
            console.warn("Adding unnamed attribute", attr);
            this.variableRegistry.add(attrs, attr, attrInfo);
            this.indexToAttribute.set(attrInfo.index, attrInfo);
            this.currentVariableIndex += 1;
            return attrInfo;
        }
    };
    GlyphConstraintAnalyzer.prototype.addLinear = function (strength, bias, lhs, rhs) {
        if (rhs === void 0) { rhs = []; }
        this.linears.push([
            bias,
            lhs
                .map(function (_a) {
                var _b = __read(_a, 2), weight = _b[0], obj = _b[1];
                return ({ weight: weight, index: obj.index });
            })
                .concat(rhs.map(function (_a) {
                var _b = __read(_a, 2), weight = _b[0], obj = _b[1];
                return ({ weight: -weight, index: obj.index });
            })),
        ]);
    };
    GlyphConstraintAnalyzer.prototype.addSoftInequality = function (strength, bias, lhs, rhs) {
        if (rhs === void 0) { rhs = []; }
        this.linears.push([
            bias,
            lhs
                .map(function (_a) {
                var _b = __read(_a, 2), weight = _b[0], obj = _b[1];
                return ({ weight: weight, index: obj.index });
            })
                .concat(rhs.map(function (_a) {
                var _b = __read(_a, 2), weight = _b[0], obj = _b[1];
                return ({ weight: -weight, index: obj.index });
            })),
        ]);
    };
    GlyphConstraintAnalyzer.prototype.addInputAttribute = function (name, attr) {
        if (this.inputBiases.has(name)) {
            var idx = this.inputBiases.get(name).index;
            this.linears.push([
                0,
                [
                    { weight: 1, index: attr.index },
                    { weight: 1, biasIndex: idx },
                ],
            ]);
        }
        else {
            var idx = this.inputBiasesCount;
            this.inputBiasesCount++;
            var attrInfo = {
                index: idx,
                type: "input",
                id: null,
                attribute: name,
            };
            this.inputBiases.set(name, attrInfo);
            this.indexToBias.set(attrInfo.index, attrInfo);
            this.linears.push([
                0,
                [
                    { weight: 1, index: attr.index },
                    { weight: 1, biasIndex: idx },
                ],
            ]);
        }
    };
    GlyphConstraintAnalyzer.prototype.addDataInput = function (name, expression) {
        this.dataInputList.set(name, Expression.parse(expression));
    };
    GlyphConstraintAnalyzer.prototype.addMapping = function (attrs, attr, mapping, parentAttrs) {
        switch (mapping.type) {
            case specification_1.MappingType.scale:
                {
                    var scaleMapping = mapping;
                    this.addInputAttribute("scale/" + scaleMapping.scale + "/" + scaleMapping.expression, this.attr(attrs, attr));
                    this.addDataInput("scale/" + scaleMapping.scale + "/" + scaleMapping.expression, scaleMapping.expression);
                }
                break;
            case specification_1.MappingType.value:
                {
                    var valueMapping = mapping;
                    attrs[attr] = valueMapping.value;
                    this.addLinear(abstract_1.ConstraintStrength.HARD, valueMapping.value, [
                        [-1, this.attr(attrs, attr)],
                    ]);
                }
                break;
            case specification_1.MappingType.parent:
                {
                    var parentMapping = mapping;
                    this.addEquals(abstract_1.ConstraintStrength.HARD, this.attr(attrs, attr), this.attr(parentAttrs, parentMapping.parentAttribute));
                }
                break;
        }
    };
    // eslint-disable-next-line
    GlyphConstraintAnalyzer.prototype.setValue = function () { };
    GlyphConstraintAnalyzer.prototype.getValue = function () {
        return 0;
    };
    GlyphConstraintAnalyzer.prototype.makeConstant = function (attr) {
        console.warn("(unimplemented) Make Constant: ", attr);
    };
    // eslint-disable-next-line
    GlyphConstraintAnalyzer.prototype.destroy = function () { };
    GlyphConstraintAnalyzer.prototype.solve = function () {
        var e_15, _a;
        var N = this.currentVariableIndex;
        var linears = this.linears;
        // Formulate the problem as A * X = B
        var A = new wasm_solver_1.Matrix();
        A.init(linears.length, N);
        var B = new wasm_solver_1.Matrix();
        B.init(linears.length, this.inputBiasesCount + 1);
        var A_data = A.data(), A_rowStride = A.rowStride, A_colStride = A.colStride;
        var B_data = B.data(), B_rowStride = B.rowStride, B_colStride = B.colStride;
        for (var i = 0; i < linears.length; i++) {
            B_data[i * B_rowStride] = -linears[i][0];
            try {
                for (var _b = (e_15 = void 0, __values(linears[i][1])), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    if (item.index != null) {
                        A_data[i * A_rowStride + item.index * A_colStride] = item.weight;
                    }
                    if (item.biasIndex != null) {
                        B_data[i * B_rowStride + (1 + item.biasIndex) * B_colStride] =
                            item.weight;
                    }
                }
            }
            catch (e_15_1) { e_15 = { error: e_15_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_15) throw e_15.error; }
            }
        }
        var X = new wasm_solver_1.Matrix();
        var ker = new wasm_solver_1.Matrix();
        wasm_solver_1.Matrix.SolveLinearSystem(X, ker, A, B);
        this.X0 = [];
        this.ker = [];
        var X_data = X.data(), X_colStride = X.colStride, X_rowStride = X.rowStride;
        for (var i = 0; i < X.cols; i++) {
            var a = new Float64Array(N);
            for (var j = 0; j < N; j++) {
                a[j] = X_data[i * X_colStride + j * X_rowStride];
            }
            this.X0.push(a);
        }
        var ker_data = ker.data(), ker_colStride = ker.colStride, ker_rowStride = ker.rowStride;
        for (var i = 0; i < ker.cols; i++) {
            var a = new Float64Array(N);
            for (var j = 0; j < N; j++) {
                a[j] = ker_data[i * ker_colStride + j * ker_rowStride];
            }
            this.ker.push(a);
        }
        X.destroy();
        ker.destroy();
        A.destroy();
        B.destroy();
        return null;
    };
    GlyphConstraintAnalyzer.prototype.isAttributeFree = function (attr) {
        var e_16, _a;
        var isNonZero = false;
        try {
            for (var _b = __values(this.ker), _c = _b.next(); !_c.done; _c = _b.next()) {
                var x = _c.value;
                if (Math.abs(x[attr.index]) > 1e-8) {
                    isNonZero = true;
                }
            }
        }
        catch (e_16_1) { e_16 = { error: e_16_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_16) throw e_16.error; }
        }
        return isNonZero;
    };
    Object.defineProperty(GlyphConstraintAnalyzer.prototype, "widthFree", {
        get: function () {
            return this.isAttributeFree(this.attr(this.glyphState.attributes, "width"));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(GlyphConstraintAnalyzer.prototype, "heightFree", {
        get: function () {
            return this.isAttributeFree(this.attr(this.glyphState.attributes, "height"));
        },
        enumerable: false,
        configurable: true
    });
    GlyphConstraintAnalyzer.prototype.computeAttribute = function (attr, rowContext) {
        var result = 0;
        for (var i = 0; i < this.X0.length; i++) {
            var bi = this.X0[i][attr.index];
            if (i == 0) {
                result += bi;
            }
            else {
                var bias = this.indexToBias.get(i - 1);
                if (bias && this.dataInputList.has(bias.attribute)) {
                    result +=
                        bi *
                            this.dataInputList.get(bias.attribute).getNumberValue(rowContext);
                }
            }
        }
        return result;
    };
    GlyphConstraintAnalyzer.prototype.computeAttributes = function (rowContext) {
        return {
            width: this.computeAttribute(this.attr(this.glyphState.attributes, "width"), rowContext),
            height: this.computeAttribute(this.attr(this.glyphState.attributes, "height"), rowContext),
        };
    };
    return GlyphConstraintAnalyzer;
}(abstract_1.ConstraintSolver));
exports.GlyphConstraintAnalyzer = GlyphConstraintAnalyzer;
//# sourceMappingURL=solver.js.map