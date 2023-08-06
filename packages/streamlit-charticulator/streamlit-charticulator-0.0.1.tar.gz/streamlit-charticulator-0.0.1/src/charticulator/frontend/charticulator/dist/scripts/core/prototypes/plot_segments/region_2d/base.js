"use strict";
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
exports.Region2DConstraintBuilder = exports.SublayoutGroup = exports.DodgingFitters = exports.CrossFitter = exports.PlotSegmentAxisPropertyNames = exports.GridStartPosition = exports.GridDirection = exports.SublayoutAlignment = exports.Region2DSublayoutType = void 0;
var solver_1 = require("../../../solver");
var types_1 = require("../../../specification/types");
var axis_1 = require("../axis");
var strings_1 = require("./../../../../strings");
var Region2DSublayoutType;
(function (Region2DSublayoutType) {
    Region2DSublayoutType["Overlap"] = "overlap";
    Region2DSublayoutType["DodgeX"] = "dodge-x";
    Region2DSublayoutType["DodgeY"] = "dodge-y";
    Region2DSublayoutType["Grid"] = "grid";
    Region2DSublayoutType["Packing"] = "packing";
    Region2DSublayoutType["Jitter"] = "jitter";
})(Region2DSublayoutType = exports.Region2DSublayoutType || (exports.Region2DSublayoutType = {}));
var SublayoutAlignment;
(function (SublayoutAlignment) {
    SublayoutAlignment["Start"] = "start";
    SublayoutAlignment["Middle"] = "middle";
    SublayoutAlignment["End"] = "end";
})(SublayoutAlignment = exports.SublayoutAlignment || (exports.SublayoutAlignment = {}));
var GridDirection;
(function (GridDirection) {
    GridDirection["X"] = "x";
    GridDirection["Y"] = "y";
})(GridDirection = exports.GridDirection || (exports.GridDirection = {}));
var GridStartPosition;
(function (GridStartPosition) {
    GridStartPosition["LeftTop"] = "LT";
    GridStartPosition["RightTop"] = "RT";
    GridStartPosition["LeftBottom"] = "LB";
    GridStartPosition["RigtBottom"] = "RB";
})(GridStartPosition = exports.GridStartPosition || (exports.GridStartPosition = {}));
var PlotSegmentAxisPropertyNames;
(function (PlotSegmentAxisPropertyNames) {
    PlotSegmentAxisPropertyNames["xData"] = "xData";
    PlotSegmentAxisPropertyNames["yData"] = "yData";
    PlotSegmentAxisPropertyNames["axis"] = "axis";
})(PlotSegmentAxisPropertyNames = exports.PlotSegmentAxisPropertyNames || (exports.PlotSegmentAxisPropertyNames = {}));
var CrossFitter = /** @class */ (function () {
    function CrossFitter(solver, mode) {
        this.solver = solver;
        this.mode = mode;
        this.candidates = [];
    }
    CrossFitter.prototype.add = function (src, dst) {
        return this.addComplex(src, [[1, dst]]);
    };
    CrossFitter.prototype.addComplex = function (src, dst, dstBias) {
        if (dstBias === void 0) { dstBias = 0; }
        this.candidates.push([src, dst, dstBias]);
    };
    CrossFitter.prototype.addConstraint = function (w) {
        var e_1, _a;
        if (this.candidates.length == 0) {
            return;
        }
        try {
            for (var _b = __values(this.candidates), _c = _b.next(); !_c.done; _c = _b.next()) {
                var candidate = _c.value;
                if (this.mode == "min") {
                    this.solver.addSoftInequality(w, -candidate[2], [[1, candidate[0]]], candidate[1]);
                }
                else {
                    this.solver.addSoftInequality(w, candidate[2], candidate[1], [
                        [1, candidate[0]],
                    ]);
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
    return CrossFitter;
}());
exports.CrossFitter = CrossFitter;
var DodgingFitters = /** @class */ (function () {
    function DodgingFitters(solver) {
        this.xMin = new CrossFitter(solver, "min");
        this.yMin = new CrossFitter(solver, "min");
        this.xMax = new CrossFitter(solver, "max");
        this.yMax = new CrossFitter(solver, "max");
    }
    DodgingFitters.prototype.addConstraint = function (w) {
        this.xMin.addConstraint(w);
        this.xMax.addConstraint(w);
        this.yMin.addConstraint(w);
        this.yMax.addConstraint(w);
    };
    return DodgingFitters;
}());
exports.DodgingFitters = DodgingFitters;
/**
 * Describes variables for constraints group. Count of group matches with data cound
 */
var SublayoutGroup = /** @class */ (function () {
    function SublayoutGroup() {
    }
    return SublayoutGroup;
}());
exports.SublayoutGroup = SublayoutGroup;
/**
 * Class builds constrains for plot segments
 * The builder creates constraints depends on sublayout
 */
var Region2DConstraintBuilder = /** @class */ (function () {
    function Region2DConstraintBuilder(plotSegment, config, x1Name, x2Name, y1Name, y2Name, solver, solverContext, chartStateManager) {
        this.plotSegment = plotSegment;
        this.config = config;
        this.x1Name = x1Name;
        this.x2Name = x2Name;
        this.y1Name = y1Name;
        this.y2Name = y2Name;
        this.solver = solver;
        this.solverContext = solverContext;
        this.chartStateManager = chartStateManager;
    }
    Region2DConstraintBuilder.prototype.getTableContext = function () {
        return this.plotSegment.parent.dataflow.getTable(this.plotSegment.object.table);
    };
    Region2DConstraintBuilder.prototype.getExpression = function (expr) {
        return this.plotSegment.parent.dataflow.cache.parse(expr);
    };
    Region2DConstraintBuilder.prototype.groupMarksByCategories = function (categories) {
        var e_2, _a;
        var _this = this;
        // Prepare categories
        var categoriesParsed = categories.map(function (c) {
            var imap = new Map();
            for (var i = 0; i < c.categories.length; i++) {
                imap.set(c.categories[i], i);
            }
            return {
                categories: c.categories,
                indexMap: imap,
                stride: 0,
                expression: _this.getExpression(c.expression),
            };
        });
        var k = 1;
        for (var i = categoriesParsed.length - 1; i >= 0; i--) {
            var c = categoriesParsed[i];
            c.stride = k;
            k *= c.categories.length;
        }
        var totalLength = k;
        // Gather result
        var result = new Array(totalLength);
        for (var i = 0; i < totalLength; i++) {
            result[i] = [];
        }
        var dateRowIndices = this.plotSegment.state.dataRowIndices;
        var table = this.getTableContext();
        // Gather places
        for (var i = 0; i < dateRowIndices.length; i++) {
            var row = table.getGroupedContext(dateRowIndices[i]);
            var place = 0;
            try {
                for (var categoriesParsed_1 = (e_2 = void 0, __values(categoriesParsed)), categoriesParsed_1_1 = categoriesParsed_1.next(); !categoriesParsed_1_1.done; categoriesParsed_1_1 = categoriesParsed_1.next()) {
                    var c = categoriesParsed_1_1.value;
                    var value = c.expression.getStringValue(row);
                    place += c.indexMap.get(value) * c.stride;
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (categoriesParsed_1_1 && !categoriesParsed_1_1.done && (_a = categoriesParsed_1.return)) _a.call(categoriesParsed_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
            // Make sure the place is valid
            if (place == place) {
                result[place].push(i);
            }
        }
        return result;
    };
    Region2DConstraintBuilder.prototype.orderMarkGroups = function (groups) {
        var order = this.plotSegment.object.properties.sublayout.order;
        var dateRowIndices = this.plotSegment.state.dataRowIndices;
        var table = this.getTableContext();
        // debugger
        // Sort results
        if (order != null && order.expression) {
            var orderExpression_1 = this.getExpression(order.expression);
            var compare = function (i, j) {
                var vi = orderExpression_1.getValue(table.getGroupedContext(dateRowIndices[i]));
                var vj = orderExpression_1.getValue(table.getGroupedContext(dateRowIndices[j]));
                if (vi < vj) {
                    return -1;
                }
                else if (vi > vj) {
                    return 1;
                }
                else {
                    return 0;
                }
            };
            for (var i = 0; i < groups.length; i++) {
                groups[i].group.sort(compare);
            }
        }
        if (this.plotSegment.object.properties.sublayout.orderReversed) {
            for (var i = 0; i < groups.length; i++) {
                groups[i].group.reverse();
            }
        }
        return groups;
    };
    /** Make sure gapX correctly correspond to gapXRatio */
    Region2DConstraintBuilder.prototype.gapX = function (length, ratio) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var attrs = state.attributes;
        var _a = __read(solver.attrs(attrs, [
            "gapX",
            this.x1Name,
            this.x2Name,
        ]), 3), gapX = _a[0], x1 = _a[1], x2 = _a[2];
        solver.addLinear(solver_1.ConstraintStrength.HARD, ratio * (props.marginX2 + props.marginX2), [[length - 1, gapX]], [
            [ratio, x2],
            [-ratio, x1],
        ]);
    };
    /** Make sure gapY correctly correspond to gapYRatio */
    Region2DConstraintBuilder.prototype.gapY = function (length, ratio) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var attrs = state.attributes;
        var _a = __read(solver.attrs(attrs, [
            "gapY",
            this.y1Name,
            this.y2Name,
        ]), 3), gapY = _a[0], y1 = _a[1], y2 = _a[2];
        solver.addLinear(solver_1.ConstraintStrength.HARD, ratio * (props.marginX2 + props.marginX2), [[length - 1, gapY]], [
            [ratio, y2],
            [-ratio, y1],
        ]);
    };
    /**
     * Map elements according to numerical/categorical mapping
     */
    Region2DConstraintBuilder.prototype.numericalMapping = function (axis) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var attrs = state.attributes;
        var dataIndices = state.dataRowIndices;
        var table = this.getTableContext();
        switch (axis) {
            case "x":
                {
                    this.numericalMappingX(props, solver, attrs, state, table, dataIndices);
                    // solver.addEquals(ConstraintWeight.HARD, x, x1);
                }
                break;
            case "y": {
                this.numericalMappingY(props, solver, attrs, state, table, dataIndices);
                // solver.addEquals(ConstraintWeight.HARD, y, y2);
            }
        }
    };
    Region2DConstraintBuilder.prototype.numericalMappingY = function (props, solver, attrs, state, table, dataIndices) {
        var e_3, _a, e_4, _b;
        var data = props.yData;
        if (data.type == "numerical") {
            var _c = __read(solver.attrs(attrs, [this.y1Name, this.y2Name]), 2), y1 = _c[0], y2 = _c[1];
            var expr = this.getExpression(data.expression);
            var interp = axis_1.getNumericalInterpolate(data);
            try {
                for (var _d = __values(state.glyphs.entries()), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var _f = __read(_e.value, 2), index = _f[0], markState = _f[1];
                    var rowContext = table.getGroupedContext(dataIndices[index]);
                    var value = expr.getNumberValue(rowContext);
                    var t = interp(value);
                    solver.addLinear(solver_1.ConstraintStrength.HARD, (t - 1) * props.marginY2 + t * props.marginY1, [
                        [1 - t, y1],
                        [t, y2],
                    ], [[1, solver.attr(markState.attributes, "y")]]);
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_3) throw e_3.error; }
            }
        }
        if (data.type == "categorical") {
            var _g = __read(solver.attrs(attrs, [
                this.y1Name,
                this.y2Name,
                "gapY",
            ]), 3), y1 = _g[0], y2 = _g[1], gapY = _g[2];
            var expr = this.getExpression(data.expression);
            try {
                for (var _h = __values(state.glyphs.entries()), _j = _h.next(); !_j.done; _j = _h.next()) {
                    var _k = __read(_j.value, 2), index = _k[0], markState = _k[1];
                    var rowContext = table.getGroupedContext(dataIndices[index]);
                    var value = expr.getStringValue(rowContext);
                    this.gapY(data.categories.length, data.gapRatio);
                    var i = data.categories.indexOf(value);
                    solver.addLinear(solver_1.ConstraintStrength.HARD, (data.categories.length - i - 0.5) * props.marginY1 -
                        (i + 0.5) * props.marginY2, [
                        [i + 0.5, y2],
                        [data.categories.length - i - 0.5, y1],
                        [-data.categories.length / 2 + i + 0.5, gapY],
                    ], [[data.categories.length, solver.attr(markState.attributes, "y")]]);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
    };
    Region2DConstraintBuilder.prototype.numericalMappingX = function (props, solver, attrs, state, table, dataIndices) {
        var e_5, _a, e_6, _b;
        var data = props.xData;
        if (data.type == "numerical") {
            var _c = __read(solver.attrs(attrs, [this.x1Name, this.x2Name]), 2), x1 = _c[0], x2 = _c[1];
            var expr = this.getExpression(data.expression);
            var interp = axis_1.getNumericalInterpolate(data);
            try {
                for (var _d = __values(state.glyphs.entries()), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var _f = __read(_e.value, 2), index = _f[0], markState = _f[1];
                    var rowContext = table.getGroupedContext(dataIndices[index]);
                    var value = expr.getNumberValue(rowContext);
                    var t = interp(value);
                    solver.addLinear(solver_1.ConstraintStrength.HARD, (1 - t) * props.marginX1 - t * props.marginX2, [
                        [1 - t, x1],
                        [t, x2],
                    ], [[1, solver.attr(markState.attributes, "x")]]);
                }
            }
            catch (e_5_1) { e_5 = { error: e_5_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_5) throw e_5.error; }
            }
        }
        if (data.type == "categorical") {
            var _g = __read(solver.attrs(attrs, [
                this.x1Name,
                this.x2Name,
                "gapX",
            ]), 3), x1 = _g[0], x2 = _g[1], gapX = _g[2];
            var expr = this.getExpression(data.expression);
            try {
                for (var _h = __values(state.glyphs.entries()), _j = _h.next(); !_j.done; _j = _h.next()) {
                    var _k = __read(_j.value, 2), index = _k[0], markState = _k[1];
                    var rowContext = table.getGroupedContext(dataIndices[index]);
                    var value = expr.getStringValue(rowContext);
                    this.gapX(data.categories.length, data.gapRatio);
                    var i = data.categories.indexOf(value);
                    solver.addLinear(solver_1.ConstraintStrength.HARD, (data.categories.length - i - 0.5) * props.marginX1 -
                        (i + 0.5) * props.marginX2, [
                        [i + 0.5, x2],
                        [data.categories.length - i - 0.5, x1],
                        [-data.categories.length / 2 + i + 0.5, gapX],
                    ], [[data.categories.length, solver.attr(markState.attributes, "x")]]);
                }
            }
            catch (e_6_1) { e_6 = { error: e_6_1 }; }
            finally {
                try {
                    if (_j && !_j.done && (_b = _h.return)) _b.call(_h);
                }
                finally { if (e_6) throw e_6.error; }
            }
        }
    };
    Region2DConstraintBuilder.prototype.groupMarksByCategoricalMapping = function (axis) {
        var props = this.plotSegment.object.properties;
        switch (axis) {
            case "x": {
                var data = props.xData;
                return this.groupMarksByCategories([
                    { categories: data.categories, expression: data.expression },
                ]);
            }
            case "y": {
                var data = props.yData;
                return this.groupMarksByCategories([
                    { categories: data.categories, expression: data.expression },
                ]);
            }
            case "xy": {
                var xData = props.xData;
                var yData = props.yData;
                return this.groupMarksByCategories([
                    { categories: xData.categories, expression: xData.expression },
                    { categories: yData.categories, expression: yData.expression },
                ]);
            }
        }
    };
    Region2DConstraintBuilder.prototype.categoricalMapping = function (axis, sublayoutContext) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var attrs = state.attributes;
        var props = this.plotSegment.object.properties;
        var categoryMarks = this.groupMarksByCategoricalMapping(axis);
        switch (axis) {
            case "x":
                {
                    // take x axis data to determine count of groups
                    this.categoricalMappingX(props, solver, attrs, categoryMarks, sublayoutContext);
                }
                break;
            case "y":
                {
                    this.categoricalMappingY(props, solver, attrs, categoryMarks, sublayoutContext);
                }
                break;
            case "xy":
                {
                    this.categoricalMappingXY(props, solver, attrs, categoryMarks, sublayoutContext);
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.categoricalMappingXY = function (props, solver, attrs, categoryMarks, sublayoutContext) {
        var xData = props.xData;
        var yData = props.yData;
        var _a = __read(solver.attrs(attrs, [
            this.x1Name,
            this.x2Name,
            this.y1Name,
            this.y2Name,
        ]), 4), x1 = _a[0], x2 = _a[1], y1 = _a[2], y2 = _a[3];
        var xAxis = axis_1.getCategoricalAxis(xData, this.config.xAxisPrePostGap, false);
        var yAxis = axis_1.getCategoricalAxis(yData, this.config.yAxisPrePostGap, true);
        var sublayoutGroups = [];
        for (var yIndex = 0; yIndex < yData.categories.length; yIndex++) {
            var _b = __read(yAxis.ranges[yIndex], 2), ty1 = _b[0], ty2 = _b[1];
            for (var xIndex = 0; xIndex < xData.categories.length; xIndex++) {
                var _c = __read(xAxis.ranges[xIndex], 2), tx1 = _c[0], tx2 = _c[1];
                var vx1Expr = [
                    [tx1, x2],
                    [1 - tx1, x1],
                ];
                var vx2Expr = [
                    [tx2, x2],
                    [1 - tx2, x1],
                ];
                var vy1Expr = [
                    [ty1, y2],
                    [1 - ty1, y1],
                ];
                var vy2Expr = [
                    [ty2, y2],
                    [1 - ty2, y1],
                ];
                var vx1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx1Expr)) }, "value", { edit: true });
                var vx2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx2Expr)) }, "value", { edit: true });
                var vy1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy1Expr)) }, "value", { edit: true });
                var vy2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy2Expr)) }, "value", { edit: true });
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx1Expr, [[1, vx1]]);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx2Expr, [[1, vx2]]);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy1Expr, [[1, vy1]]);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy2Expr, [[1, vy2]]);
                sublayoutGroups.push({
                    group: categoryMarks[xIndex * yData.categories.length + yIndex],
                    x1: vx1,
                    y1: vy1,
                    x2: vx2,
                    y2: vy2,
                });
            }
        }
        this.applySublayout(sublayoutGroups, "xy", sublayoutContext);
    };
    Region2DConstraintBuilder.prototype.categoricalMappingY = function (props, solver, attrs, categoryMarks, sublayoutContext) {
        var data = props.yData;
        var _a = __read(solver.attrs(attrs, [
            this.x1Name,
            this.x2Name,
            this.y1Name,
            this.y2Name,
        ]), 4), x1 = _a[0], x2 = _a[1], y1 = _a[2], y2 = _a[3];
        var axis = axis_1.getCategoricalAxis(data, this.config.yAxisPrePostGap, true);
        var sublayoutGroups = [];
        for (var cindex = 0; cindex < data.categories.length; cindex++) {
            var _b = __read(axis.ranges[cindex], 2), t1 = _b[0], t2 = _b[1];
            var vy1Expr = [
                [t1, y2],
                [1 - t1, y1],
            ];
            var vy2Expr = [
                [t2, y2],
                [1 - t2, y1],
            ];
            var vy1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy1Expr)) }, "value", { edit: true });
            var vy2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy2Expr)) }, "value", { edit: true });
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy1Expr, [[1, vy1]]);
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy2Expr, [[1, vy2]]);
            sublayoutGroups.push({
                group: categoryMarks[cindex],
                x1: x1,
                y1: vy1,
                x2: x2,
                y2: vy2,
            });
        }
        this.applySublayout(sublayoutGroups, "y", sublayoutContext);
    };
    Region2DConstraintBuilder.prototype.categoricalMappingX = function (props, solver, attrs, categoryMarks, sublayoutContext) {
        var data = props.xData;
        var _a = __read(solver.attrs(attrs, [
            this.x1Name,
            this.x2Name,
            this.y1Name,
            this.y2Name,
        ]), 4), x1 = _a[0], x2 = _a[1], y1 = _a[2], y2 = _a[3];
        var axis = axis_1.getCategoricalAxis(data, this.config.xAxisPrePostGap, false);
        var sublayoutGroups = [];
        for (var cindex = 0; cindex < data.categories.length; cindex++) {
            var _b = __read(axis.ranges[cindex], 2), t1 = _b[0], t2 = _b[1];
            // t1 * x2 = (1 - t1) * x1
            var vx1Expr = [
                [t1, x2],
                [1 - t1, x1],
            ];
            // t2 * x2 = (1 - t2) * x1
            var vx2Expr = [
                [t2, x2],
                [1 - t2, x1],
            ];
            var vx1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx1Expr)) }, "value", { edit: true });
            var vx2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx2Expr)) }, "value", { edit: true });
            // t1 * x2 = (1 - t1) * x2 = 1 * vx1
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx1Expr, [[1, vx1]]);
            // t2 * x2 = (1 - t2) * x2 = 1 * vx2
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx2Expr, [[1, vx2]]);
            // save group of constraints
            sublayoutGroups.push({
                group: categoryMarks[cindex],
                x1: vx1,
                y1: y1,
                x2: vx2,
                y2: y2,
            });
        }
        this.applySublayout(sublayoutGroups, "x", sublayoutContext);
    };
    Region2DConstraintBuilder.prototype.categoricalHandles = function (axis, sublayout) {
        var handles = [];
        var props = this.plotSegment.object.properties;
        var x1 = this.plotSegment.state.attributes[this.x1Name];
        var y1 = this.plotSegment.state.attributes[this.y1Name];
        var x2 = this.plotSegment.state.attributes[this.x2Name];
        var y2 = this.plotSegment.state.attributes[this.y2Name];
        // We are using sublayouts here
        if (sublayout) {
            var categoryMarks = this.groupMarksByCategoricalMapping(axis);
            var xAxis_1 = axis == "x" || axis == "xy"
                ? axis_1.getCategoricalAxis(props.xData, this.config.xAxisPrePostGap, false)
                : null;
            var yAxis_1 = axis == "y" || axis == "xy"
                ? axis_1.getCategoricalAxis(props.yData, this.config.yAxisPrePostGap, true)
                : null;
            handles = handles.concat(this.sublayoutHandles(categoryMarks.map(function (x, i) {
                var ix = i, iy = i;
                if (axis == "xy") {
                    ix = i % xAxis_1.ranges.length;
                    iy = Math.floor(i / xAxis_1.ranges.length);
                }
                return {
                    group: x,
                    x1: xAxis_1 ? xAxis_1.ranges[ix][0] * (x2 - x1) + x1 : x1,
                    y1: yAxis_1 ? yAxis_1.ranges[iy][0] * (y2 - y1) + y1 : y1,
                    x2: xAxis_1 ? xAxis_1.ranges[ix][1] * (x2 - x1) + x1 : x2,
                    y2: yAxis_1 ? yAxis_1.ranges[iy][1] * (y2 - y1) + y1 : y2,
                };
            }), false, false));
        }
        if (axis == "x" || axis == "xy") {
            var data = props.xData;
            var axis_2 = axis_1.getCategoricalAxis(data, this.config.xAxisPrePostGap, false);
            for (var i = 0; i < axis_2.ranges.length - 1; i++) {
                var p1 = axis_2.ranges[i][1];
                handles.push({
                    type: "gap",
                    gap: {
                        property: {
                            property: PlotSegmentAxisPropertyNames.xData,
                            field: "gapRatio",
                        },
                        axis: axis_1.AxisMode.X,
                        reference: p1 * (x2 - x1) + x1,
                        value: data.gapRatio,
                        scale: axis_2.gapScale * (x2 - x1),
                        span: [y1, y2],
                    },
                });
            }
        }
        if (axis == "y" || axis == "xy") {
            var data = props.yData;
            var axis_3 = axis_1.getCategoricalAxis(data, this.config.yAxisPrePostGap, true);
            for (var i = 0; i < axis_3.ranges.length - 1; i++) {
                var p1 = axis_3.ranges[i][1];
                handles.push({
                    type: "gap",
                    gap: {
                        property: {
                            property: PlotSegmentAxisPropertyNames.yData,
                            field: "gapRatio",
                        },
                        axis: axis_1.AxisMode.Y,
                        reference: p1 * (y2 - y1) + y1,
                        value: data.gapRatio,
                        scale: axis_3.gapScale * (y2 - y1),
                        span: [x1, x2],
                    },
                });
            }
        }
        return handles;
    };
    Region2DConstraintBuilder.prototype.stacking = function (axis) {
        var e_7, _a;
        var solver = this.solver;
        var state = this.plotSegment.state;
        var attrs = state.attributes;
        var dataIndices = state.dataRowIndices;
        var _b = __read(solver.attrs(attrs, [
            this.x1Name,
            this.x2Name,
            this.y1Name,
            this.y2Name,
        ]), 4), x1 = _b[0], x2 = _b[1], y1 = _b[2], y2 = _b[3];
        var count = dataIndices.length;
        var doStack = count <= 36;
        try {
            for (var _c = __values(state.glyphs.entries()), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), index = _e[0], markState = _e[1];
                switch (axis) {
                    case "x":
                        {
                            this.stackingX(solver, attrs, doStack, index, state, x1, x2, count, markState);
                        }
                        break;
                    case "y":
                        {
                            this.stackingY(solver, attrs, doStack, index, state, y1, y2, count, markState);
                        }
                        break;
                }
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_7) throw e_7.error; }
        }
        switch (axis) {
            case "x":
                {
                    this.gapX(count, this.plotSegment.object.properties.xData.gapRatio);
                }
                break;
            case "y":
                {
                    this.gapY(count, this.plotSegment.object.properties.yData.gapRatio);
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.stackingY = function (solver, attrs, doStack, index, state, y1, y2, count, markState) {
        var _a = __read(solver.attrs(attrs, ["gapY"]), 1), gapY = _a[0];
        if (doStack) {
            if (index > 0) {
                var y2Prev = solver.attr(state.glyphs[index - 1].attributes, "y2");
                var y1This = solver.attr(state.glyphs[index].attributes, "y1");
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [1, y2Prev],
                    [-1, y1This],
                    [1, gapY],
                ]);
            }
            if (index == 0) {
                var y1This = solver.attr(state.glyphs[index].attributes, "y1");
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, y1]], [[1, y1This]]);
            }
            if (index == state.glyphs.length - 1) {
                var y2This = solver.attr(state.glyphs[index].attributes, "y2");
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, y2]], [[1, y2This]]);
            }
        }
        else {
            var t = (index + 0.5) / count;
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [1 - t, y2],
                [t, y1],
            ], [[1, solver.attr(markState.attributes, "y")]]);
            solver.addLinear(solver_1.ConstraintStrength.WEAK, 0, [
                [1, y2],
                [-1, y1],
            ], [
                [count, solver.attr(markState.attributes, "height")],
                [count - 1, gapY],
            ]);
        }
    };
    Region2DConstraintBuilder.prototype.stackingX = function (solver, attrs, doStack, index, state, x1, x2, count, markState) {
        var _a = __read(solver.attrs(attrs, ["gapX"]), 1), gapX = _a[0];
        if (doStack) {
            if (index > 0) {
                var x2Prev = solver.attr(state.glyphs[index - 1].attributes, "x2");
                var x1This = solver.attr(state.glyphs[index].attributes, "x1");
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [1, x2Prev],
                    [-1, x1This],
                    [1, gapX],
                ]);
            }
            if (index == 0) {
                var x1This = solver.attr(state.glyphs[index].attributes, "x1");
                // solver.addEquals(ConstraintWeight.HARD, x1, x1This);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, x1]], [[1, x1This]]);
            }
            if (index == state.glyphs.length - 1) {
                var x2This = solver.attr(state.glyphs[index].attributes, "x2");
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, x2]], [[1, x2This]]);
            }
        }
        else {
            var t = (index + 0.5) / count;
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [1 - t, x1],
                [t, x2],
            ], [[1, solver.attr(markState.attributes, "x")]]);
            solver.addLinear(solver_1.ConstraintStrength.WEAK, 0, [
                [1, x2],
                [-1, x1],
            ], [
                [count, solver.attr(markState.attributes, "width")],
                [count - 1, gapX],
            ]);
        }
    };
    Region2DConstraintBuilder.prototype.fitGroups = function (groups, axis) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var fitters = new DodgingFitters(solver);
        var alignment = props.sublayout.align;
        groups.forEach(function (group) {
            var markStates = group.group.map(function (index) { return state.glyphs[index]; });
            var x1 = group.x1, y1 = group.y1, x2 = group.x2, y2 = group.y2;
            for (var index = 0; index < markStates.length; index++) {
                var m1 = markStates[index];
                if (axis == "x" || axis == "xy") {
                    if (alignment.x == SublayoutAlignment.Start) {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "x1"), x1);
                    }
                    else {
                        fitters.xMin.add(solver.attr(m1.attributes, "x1"), x1);
                    }
                    if (alignment.x == SublayoutAlignment.End) {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "x2"), x2);
                    }
                    else {
                        fitters.xMax.add(solver.attr(m1.attributes, "x2"), x2);
                    }
                    if (alignment.x == SublayoutAlignment.Middle) {
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [1, solver.attr(m1.attributes, "x1")],
                            [1, solver.attr(m1.attributes, "x2")],
                        ], [
                            [1, x1],
                            [1, x2],
                        ]);
                    }
                }
                if (axis == "y" || axis == "xy") {
                    if (alignment.y == SublayoutAlignment.Start) {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "y1"), y1);
                    }
                    else {
                        fitters.yMin.add(solver.attr(m1.attributes, "y1"), y1);
                    }
                    if (alignment.y == SublayoutAlignment.End) {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "y2"), y2);
                    }
                    else {
                        fitters.yMax.add(solver.attr(m1.attributes, "y2"), y2);
                    }
                    if (alignment.y == SublayoutAlignment.Middle) {
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [1, solver.attr(m1.attributes, "y1")],
                            [1, solver.attr(m1.attributes, "y2")],
                        ], [
                            [1, y1],
                            [1, y2],
                        ]);
                    }
                }
            }
        });
        fitters.addConstraint(solver_1.ConstraintStrength.MEDIUM);
    };
    Region2DConstraintBuilder.prototype.applySublayout = function (groups, axis, context) {
        if (!context || context.mode == "disabled") {
            this.fitGroups(groups, axis);
        }
        else {
            this.orderMarkGroups(groups);
            var props = this.plotSegment.object.properties;
            if (context.mode == "x-only" || context.mode == "y-only") {
                if (props.sublayout.type == Region2DSublayoutType.Packing) {
                    this.sublayoutPacking(groups, context.mode == "x-only" ? axis_1.AxisMode.X : axis_1.AxisMode.Y);
                }
                else if (props.sublayout.type == Region2DSublayoutType.Jitter) {
                    this.sublayoutJitter(groups, context.mode == "x-only" ? axis_1.AxisMode.X : axis_1.AxisMode.Y);
                }
                else {
                    this.fitGroups(groups, axis);
                }
            }
            else {
                if (props.sublayout.type == Region2DSublayoutType.Overlap) {
                    this.fitGroups(groups, "xy");
                }
                // Stack X
                if (props.sublayout.type == Region2DSublayoutType.DodgeX) {
                    this.sublayoutDodging(groups, GridDirection.X, context.xAxisPrePostGap);
                }
                // Stack Y
                if (props.sublayout.type == Region2DSublayoutType.DodgeY) {
                    this.sublayoutDodging(groups, GridDirection.Y, context.yAxisPrePostGap);
                }
                // Grid layout
                if (props.sublayout.type == Region2DSublayoutType.Grid) {
                    this.sublayoutGrid(groups);
                }
                // Force layout
                if (props.sublayout.type == Region2DSublayoutType.Packing) {
                    this.sublayoutPacking(groups);
                }
                // Jitter layout
                if (props.sublayout.type == Region2DSublayoutType.Jitter) {
                    this.sublayoutJitter(groups);
                }
            }
        }
    };
    // eslint-disable-next-line
    Region2DConstraintBuilder.prototype.sublayoutDodging = function (groups, direction, enablePrePostGap) {
        var e_8, _a;
        var _this = this;
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var fitters = new DodgingFitters(solver);
        var alignment = props.sublayout.align;
        var maxCount = 0;
        try {
            for (var groups_1 = __values(groups), groups_1_1 = groups_1.next(); !groups_1_1.done; groups_1_1 = groups_1.next()) {
                var g = groups_1_1.value;
                maxCount = Math.max(maxCount, g.group.length);
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (groups_1_1 && !groups_1_1.done && (_a = groups_1.return)) _a.call(groups_1);
            }
            finally { if (e_8) throw e_8.error; }
        }
        var dodgeGapRatio = 0;
        var dodgeGapOffset = 0;
        if (!enablePrePostGap) {
            dodgeGapRatio =
                direction == "x"
                    ? props.sublayout.ratioX / (maxCount - 1)
                    : props.sublayout.ratioY / (maxCount - 1);
            dodgeGapOffset = 0;
        }
        else {
            dodgeGapRatio =
                direction == "x"
                    ? props.sublayout.ratioX / maxCount
                    : props.sublayout.ratioY / maxCount;
            dodgeGapOffset = dodgeGapRatio / 2;
        }
        groups.forEach(function (group) {
            var markStates = group.group.map(function (index) { return state.glyphs[index]; });
            var x1 = group.x1, y1 = group.y1, x2 = group.x2, y2 = group.y2;
            var count = markStates.length;
            // If nothing there, skip
            if (count == 0) {
                return;
            }
            for (var index = 0; index < markStates.length; index++) {
                var m1_1 = markStates[index];
                if (index > 0) {
                    var m0 = markStates[index - 1];
                    switch (direction) {
                        case "x":
                            {
                                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                                    [dodgeGapRatio, x2],
                                    [-dodgeGapRatio, x1],
                                    [1, solver.attr(m0.attributes, "x2")],
                                    [-1, solver.attr(m1_1.attributes, "x1")],
                                ]);
                            }
                            break;
                        case "y":
                            {
                                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                                    [dodgeGapRatio, y2],
                                    [-dodgeGapRatio, y1],
                                    [1, solver.attr(m0.attributes, "y2")],
                                    [-1, solver.attr(m1_1.attributes, "y1")],
                                ]);
                            }
                            break;
                    }
                }
                _this.setFirstSublayoutDodgingDirection(direction, alignment, solver, m1_1, y1, fitters, y2, x1, x2);
            }
            var m1 = markStates[0];
            var mN = markStates[markStates.length - 1];
            switch (direction) {
                case "x":
                    {
                        _this.setSublayoutDodgingDirectionX(x1, dodgeGapOffset, x2, alignment, solver, m1, fitters, mN);
                    }
                    break;
                case "y":
                    {
                        _this.setSublayoutDodgingDirectionY(y1, dodgeGapOffset, y2, alignment, solver, m1, fitters, mN);
                    }
                    break;
            }
        });
        fitters.addConstraint(solver_1.ConstraintStrength.MEDIUM);
    };
    Region2DConstraintBuilder.prototype.setSublayoutDodgingDirectionY = function (y1, dodgeGapOffset, y2, alignment, solver, m1, fitters, mN) {
        var y1WithGap = [
            [1, y1],
            [dodgeGapOffset, y2],
            [-dodgeGapOffset, y1],
        ];
        var y2WithGap = [
            [1, y2],
            [dodgeGapOffset, y1],
            [-dodgeGapOffset, y2],
        ];
        if (alignment.y == "start") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(m1.attributes, "y1")]], y1WithGap);
        }
        else {
            fitters.yMin.addComplex(solver.attr(m1.attributes, "y1"), y1WithGap);
        }
        if (alignment.y == "end") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(mN.attributes, "y2")]], y2WithGap);
        }
        else {
            fitters.yMax.addComplex(solver.attr(mN.attributes, "y2"), y2WithGap);
        }
        if (alignment.y == "middle") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [1, solver.attr(m1.attributes, "y1")],
                [1, solver.attr(mN.attributes, "y2")],
            ], [
                [1, y1],
                [1, y2],
            ]);
        }
    };
    Region2DConstraintBuilder.prototype.setSublayoutDodgingDirectionX = function (x1, dodgeGapOffset, x2, alignment, solver, m1, fitters, mN) {
        var x1WithGap = [
            [1, x1],
            [dodgeGapOffset, x2],
            [-dodgeGapOffset, x1],
        ];
        var x2WithGap = [
            [1, x2],
            [dodgeGapOffset, x1],
            [-dodgeGapOffset, x2],
        ];
        if (alignment.x == "start") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(m1.attributes, "x1")]], x1WithGap);
        }
        else {
            fitters.xMin.addComplex(solver.attr(m1.attributes, "x1"), x1WithGap);
        }
        if (alignment.x == "end") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(mN.attributes, "x2")]], x2WithGap);
        }
        else {
            fitters.xMax.addComplex(solver.attr(mN.attributes, "x2"), x2WithGap);
        }
        if (alignment.x == "middle") {
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [1, solver.attr(m1.attributes, "x1")],
                [1, solver.attr(mN.attributes, "x2")],
            ], [
                [1, x1],
                [1, x2],
            ]);
        }
    };
    Region2DConstraintBuilder.prototype.setFirstSublayoutDodgingDirection = function (direction, alignment, solver, m1, y1, fitters, y2, x1, x2) {
        switch (direction) {
            case "x":
                {
                    if (alignment.y == "start") {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "y1"), y1);
                    }
                    else {
                        fitters.yMin.add(solver.attr(m1.attributes, "y1"), y1);
                    }
                    if (alignment.y == "end") {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "y2"), y2);
                    }
                    else {
                        fitters.yMax.add(solver.attr(m1.attributes, "y2"), y2);
                    }
                    if (alignment.y == "middle") {
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [1, solver.attr(m1.attributes, "y1")],
                            [1, solver.attr(m1.attributes, "y2")],
                        ], [
                            [1, y1],
                            [1, y2],
                        ]);
                    }
                }
                break;
            case "y":
                {
                    if (alignment.x == "start") {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "x1"), x1);
                    }
                    else {
                        fitters.xMin.add(solver.attr(m1.attributes, "x1"), x1);
                    }
                    if (alignment.x == "end") {
                        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(m1.attributes, "x2"), x2);
                    }
                    else {
                        fitters.xMax.add(solver.attr(m1.attributes, "x2"), x2);
                    }
                    if (alignment.x == "middle") {
                        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                            [1, solver.attr(m1.attributes, "x1")],
                            [1, solver.attr(m1.attributes, "x2")],
                        ], [
                            [1, x1],
                            [1, x2],
                        ]);
                    }
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.getGlyphPreSolveAttributes = function (rowIndices) {
        var attrs = this.solverContext.getGlyphAttributes(this.plotSegment.object.glyph, this.plotSegment.object.table, rowIndices);
        return attrs;
    };
    Region2DConstraintBuilder.prototype.sublayoutGrid = function (groups, directionOverride) {
        var _this = this;
        var solver = this.solver;
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var direction = props.sublayout.grid.direction;
        if (directionOverride != null) {
            direction = directionOverride;
        }
        var alignX = props.sublayout.align.x;
        var alignY = props.sublayout.align.y;
        var xMinFitter = new CrossFitter(solver, "min");
        var xMaxFitter = new CrossFitter(solver, "max");
        var yMinFitter = new CrossFitter(solver, "min");
        var yMaxFitter = new CrossFitter(solver, "max");
        var maxCount = 0;
        groups.forEach(function (group) {
            if (maxCount < group.group.length) {
                maxCount = group.group.length;
            }
        });
        var xCount, yCount;
        // Determine xCount and yCount, aka., the number of divisions on each axis
        switch (direction) {
            case "x":
                {
                    if (props.sublayout.grid.xCount != null) {
                        xCount = props.sublayout.grid.xCount;
                        yCount = Math.ceil(maxCount / xCount);
                    }
                    else {
                        xCount = Math.ceil(Math.sqrt(maxCount));
                        yCount = Math.ceil(maxCount / xCount);
                    }
                }
                break;
            case "y":
                {
                    if (props.sublayout.grid.yCount != null) {
                        yCount = props.sublayout.grid.yCount;
                        xCount = Math.ceil(maxCount / yCount);
                    }
                    else {
                        yCount = Math.ceil(Math.sqrt(maxCount));
                        xCount = Math.ceil(maxCount / yCount);
                    }
                }
                break;
            case "x1":
                {
                    xCount = maxCount;
                    yCount = 1;
                }
                break;
            case "y1":
                {
                    yCount = maxCount;
                    xCount = 1;
                }
                break;
        }
        var gapRatioX = xCount > 1 ? props.sublayout.ratioX / (xCount - 1) : 0;
        var gapRatioY = yCount > 1 ? props.sublayout.ratioY / (yCount - 1) : 0;
        var gridStartPosition = props.sublayout.grid.gridStartPosition;
        groups.forEach(function (group) {
            var markStates = group.group.map(function (index) { return state.glyphs[index]; });
            var x1 = group.x1, y1 = group.y1, x2 = group.x2, y2 = group.y2;
            var xMax, yMax;
            if (direction == "x" || direction == "x1") {
                xMax = Math.min(markStates.length, xCount);
                yMax = Math.ceil(markStates.length / xCount);
            }
            else {
                yMax = Math.min(markStates.length, yCount);
                xMax = Math.ceil(markStates.length / yCount);
            }
            // Constraint glyphs
            _this.addGlyphConstraints(markStates, direction, xCount, alignY, xMax, yMax, yCount, alignX, gapRatioX, x2, x1, gapRatioY, y2, y1, solver, xMinFitter, xMaxFitter, yMinFitter, yMaxFitter, gridStartPosition);
        });
        xMinFitter.addConstraint(solver_1.ConstraintStrength.MEDIUM);
        xMaxFitter.addConstraint(solver_1.ConstraintStrength.MEDIUM);
        yMinFitter.addConstraint(solver_1.ConstraintStrength.MEDIUM);
        yMaxFitter.addConstraint(solver_1.ConstraintStrength.MEDIUM);
    };
    // eslint-disable-next-line
    Region2DConstraintBuilder.prototype.addGlyphConstraints = function (markStates, direction, xCount, alignY, xMax, yMax, yCount, alignX, gapRatioX, x2, x1, gapRatioY, y2, y1, solver, xMinFitter, xMaxFitter, yMinFitter, yMaxFitter, gridStartPosition) {
        if (gridStartPosition === GridStartPosition.LeftBottom ||
            gridStartPosition === GridStartPosition.RigtBottom) {
            markStates = markStates.reverse();
        }
        for (var i = 0; i < markStates.length; i++) {
            var xi = void 0, yi = void 0;
            if (direction == "x" || direction == "x1") {
                xi = i % xCount;
                if (alignY == "start") {
                    xi = xMax - 1 - ((markStates.length - 1 - i) % xCount);
                    yi = Math.floor((markStates.length - 1 - i) / xCount);
                }
                else {
                    yi = yMax - 1 - Math.floor(i / xCount);
                }
                if (gridStartPosition === GridStartPosition.RightTop ||
                    gridStartPosition === GridStartPosition.RigtBottom) {
                    xi = xCount - 1 - xi; // flip X
                }
            }
            else {
                yi = yMax - 1 - (i % yCount);
                xi = Math.floor(i / yCount);
                if (alignX == "end") {
                    yi = (markStates.length - 1 - i) % yCount;
                    xi = xMax - 1 - Math.floor((markStates.length - 1 - i) / yCount);
                }
                if (gridStartPosition === GridStartPosition.LeftTop ||
                    gridStartPosition === GridStartPosition.LeftBottom) {
                    yi = yCount - 1 - yi; // flip Y
                }
            }
            // Adjust xi, yi based on alignment settings
            if (alignX == "end") {
                xi = xi + xCount - xMax;
            }
            if (alignX == "middle") {
                xi = xi + (xCount - xMax) / 2;
            }
            if (alignY == "end") {
                yi = yi + yCount - yMax;
            }
            if (alignY == "middle") {
                yi = yi + (yCount - yMax) / 2;
            }
            var cellX1 = [
                [(xi / xCount) * (1 + gapRatioX), x2],
                [1 - (xi / xCount) * (1 + gapRatioX), x1],
            ];
            var cellX2 = [
                [((xi + 1) / xCount) * (1 + gapRatioX) - gapRatioX, x2],
                [1 - ((xi + 1) / xCount) * (1 + gapRatioX) + gapRatioX, x1],
            ];
            var cellY1 = [
                [(yi / yCount) * (1 + gapRatioY), y2],
                [1 - (yi / yCount) * (1 + gapRatioY), y1],
            ];
            var cellY2 = [
                [((yi + 1) / yCount) * (1 + gapRatioY) - gapRatioY, y2],
                [1 - ((yi + 1) / yCount) * (1 + gapRatioY) + gapRatioY, y1],
            ];
            var state = markStates[i];
            if (alignX == "start") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(state.attributes, "x1")]], cellX1);
            }
            else {
                xMinFitter.addComplex(solver.attr(state.attributes, "x1"), cellX1);
            }
            if (alignX == "end") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(state.attributes, "x2")]], cellX2);
            }
            else {
                xMaxFitter.addComplex(solver.attr(state.attributes, "x2"), cellX2);
            }
            if (alignX == "middle") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [1, solver.attr(state.attributes, "x1")],
                    [1, solver.attr(state.attributes, "x2")],
                ], cellX1.concat(cellX2));
            }
            if (alignY == "start") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(state.attributes, "y1")]], cellY1);
            }
            else {
                yMinFitter.addComplex(solver.attr(state.attributes, "y1"), cellY1);
            }
            if (alignY == "end") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, solver.attr(state.attributes, "y2")]], cellY2);
            }
            else {
                yMaxFitter.addComplex(solver.attr(state.attributes, "y2"), cellY2);
            }
            if (alignY == "middle") {
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                    [1, solver.attr(state.attributes, "y1")],
                    [1, solver.attr(state.attributes, "y2")],
                ], cellY1.concat(cellY2));
            }
        }
    };
    Region2DConstraintBuilder.prototype.sublayoutHandles = function (groups, enablePrePostGapX, enablePrePostGapY) {
        var e_9, _a, e_10, _b, e_11, _c;
        this.orderMarkGroups(groups);
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var handles = [];
        var maxCount = 0;
        try {
            for (var groups_2 = __values(groups), groups_2_1 = groups_2.next(); !groups_2_1.done; groups_2_1 = groups_2.next()) {
                var g = groups_2_1.value;
                maxCount = Math.max(maxCount, g.group.length);
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (groups_2_1 && !groups_2_1.done && (_a = groups_2.return)) _a.call(groups_2);
            }
            finally { if (e_9) throw e_9.error; }
        }
        if (props.sublayout.type == Region2DSublayoutType.DodgeX) {
            try {
                for (var groups_3 = __values(groups), groups_3_1 = groups_3.next(); !groups_3_1.done; groups_3_1 = groups_3.next()) {
                    var group = groups_3_1.value;
                    for (var i = 0; i < group.group.length - 1; i++) {
                        var state1 = state.glyphs[group.group[i]];
                        var state2 = state.glyphs[group.group[i + 1]];
                        var p1 = state1.attributes.x2;
                        var minY = Math.min(state1.attributes.y1, state1.attributes.y2, state2.attributes.y1, state2.attributes.y2);
                        var maxY = Math.max(state1.attributes.y1, state1.attributes.y2, state2.attributes.y1, state2.attributes.y2);
                        handles.push({
                            type: "gap",
                            gap: {
                                axis: axis_1.AxisMode.X,
                                property: { property: "sublayout", field: "ratioX" },
                                reference: p1,
                                value: props.sublayout.ratioX,
                                scale: (1 / (enablePrePostGapX ? maxCount : maxCount - 1)) *
                                    (group.x2 - group.x1),
                                span: [minY, maxY],
                            },
                        });
                    }
                }
            }
            catch (e_10_1) { e_10 = { error: e_10_1 }; }
            finally {
                try {
                    if (groups_3_1 && !groups_3_1.done && (_b = groups_3.return)) _b.call(groups_3);
                }
                finally { if (e_10) throw e_10.error; }
            }
        }
        if (props.sublayout.type == Region2DSublayoutType.DodgeY) {
            try {
                for (var groups_4 = __values(groups), groups_4_1 = groups_4.next(); !groups_4_1.done; groups_4_1 = groups_4.next()) {
                    var group = groups_4_1.value;
                    for (var i = 0; i < group.group.length - 1; i++) {
                        var state1 = state.glyphs[group.group[i]];
                        var state2 = state.glyphs[group.group[i + 1]];
                        var p1 = state1.attributes.y2;
                        var minX = Math.min(state1.attributes.x1, state1.attributes.x2, state2.attributes.x1, state2.attributes.x2);
                        var maxX = Math.max(state1.attributes.x1, state1.attributes.x2, state2.attributes.x1, state2.attributes.x2);
                        handles.push({
                            type: "gap",
                            gap: {
                                axis: axis_1.AxisMode.Y,
                                property: { property: "sublayout", field: "ratioY" },
                                reference: p1,
                                value: props.sublayout.ratioY,
                                scale: (1 / (enablePrePostGapY ? maxCount : maxCount - 1)) *
                                    (group.y2 - group.y1),
                                span: [minX, maxX],
                            },
                        });
                    }
                }
            }
            catch (e_11_1) { e_11 = { error: e_11_1 }; }
            finally {
                try {
                    if (groups_4_1 && !groups_4_1.done && (_c = groups_4.return)) _c.call(groups_4);
                }
                finally { if (e_11) throw e_11.error; }
            }
        }
        if (props.sublayout.type == Region2DSublayoutType.Grid) {
            // TODO: implement grid sublayout handles
        }
        return handles;
    };
    Region2DConstraintBuilder.prototype.sublayoutPacking = function (groups, axisOnly) {
        var _this = this;
        var solver = this.solver;
        var state = this.plotSegment.state;
        var packingProps = this.plotSegment.object.properties.sublayout.packing;
        groups.forEach(function (group) {
            var markStates = group.group.map(function (index) { return state.glyphs[index]; });
            var x1 = group.x1, y1 = group.y1, x2 = group.x2, y2 = group.y2;
            var centerState = {
                cx: 0,
                cy: 0,
            };
            var cx = solver.attr(centerState, "cx", {
                edit: true,
            });
            var cy = solver.attr(centerState, "cy", {
                edit: true,
            });
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cx]], [
                [1, x1],
                [1, x2],
            ]);
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, cy]], [
                [1, y1],
                [1, y2],
            ]);
            var points = markStates.map(function (state) {
                var e_12, _a;
                var radius = 0;
                try {
                    for (var _b = __values(state.marks), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var e = _c.value;
                        if (e.attributes.size != null) {
                            radius = Math.max(radius, Math.sqrt(e.attributes.size / Math.PI));
                        }
                        else {
                            var w = e.attributes.width;
                            var h = e.attributes.height;
                            if (w != null && h != null) {
                                radius = Math.max(radius, Math.sqrt(w * w + h * h) / 2);
                            }
                        }
                    }
                }
                catch (e_12_1) { e_12 = { error: e_12_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_12) throw e_12.error; }
                }
                if (radius == 0) {
                    radius = Region2DConstraintBuilder.defaultJitterPackingRadius;
                }
                return [
                    solver.attr(state.attributes, "x"),
                    solver.attr(state.attributes, "y"),
                    radius,
                ];
            });
            solver.addPlugin(new solver_1.ConstraintPlugins.PackingPlugin(solver, cx, cy, points, axisOnly, _this.config.getXYScale, {
                gravityX: packingProps && packingProps.gravityX,
                gravityY: packingProps && packingProps.gravityY,
                boxed: packingProps.boxedX || packingProps.boxedY
                    ? {
                        x1: packingProps.boxedX ? solver.getValue(group.x1) : null,
                        x2: packingProps.boxedX ? solver.getValue(group.x2) : null,
                        y1: packingProps.boxedY ? solver.getValue(group.y1) : null,
                        y2: packingProps.boxedY ? solver.getValue(group.y2) : null,
                    }
                    : null,
            }));
        });
    };
    Region2DConstraintBuilder.prototype.sublayoutJitter = function (groups, axisOnly) {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var jitterProps = this.plotSegment.object.properties.sublayout.jitter;
        groups.forEach(function (group) {
            var markStates = group.group.map(function (index) { return state.glyphs[index]; });
            var x1 = group.x1, y1 = group.y1, x2 = group.x2, y2 = group.y2;
            var points = markStates.map(function (state) {
                var e_13, _a;
                var radius = 0;
                try {
                    for (var _b = __values(state.marks), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var e = _c.value;
                        if (e.attributes.size != null) {
                            radius = Math.max(radius, Math.sqrt(e.attributes.size / Math.PI));
                        }
                        else {
                            var w = e.attributes.width;
                            var h = e.attributes.height;
                            if (w != null && h != null) {
                                radius = Math.max(radius, Math.sqrt(w * w + h * h) / 2);
                            }
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
                if (radius == 0) {
                    radius = Region2DConstraintBuilder.defaultJitterPackingRadius;
                }
                return [
                    solver.attr(state.attributes, "x"),
                    solver.attr(state.attributes, "y"),
                    radius,
                ];
            });
            solver.addPlugin(new solver_1.ConstraintPlugins.JitterPlugin(solver, x1, y1, x2, y2, points, axisOnly, jitterProps
                ? jitterProps
                : {
                    horizontal: true,
                    vertical: true,
                }));
        });
    };
    Region2DConstraintBuilder.prototype.getHandles = function () {
        var state = this.plotSegment.state;
        var props = this.plotSegment.object.properties;
        var xMode = props.xData ? props.xData.type : "null";
        var yMode = props.yData ? props.yData.type : "null";
        var handles = [];
        switch (xMode) {
            case "null":
                {
                    switch (yMode) {
                        case "null":
                            {
                                handles = handles.concat(this.sublayoutHandles([
                                    {
                                        x1: state.attributes[this.x1Name],
                                        y1: state.attributes[this.y1Name],
                                        x2: state.attributes[this.x2Name],
                                        y2: state.attributes[this.y2Name],
                                        group: state.dataRowIndices.map(function (x, i) { return i; }),
                                    },
                                ], this.config.xAxisPrePostGap, this.config.yAxisPrePostGap));
                            }
                            break;
                        // case "numerical":
                        //   {
                        //   }
                        //   break;
                        case "categorical":
                            {
                                handles = handles.concat(this.categoricalHandles("y", true));
                            }
                            break;
                    }
                }
                break;
            case "numerical":
                {
                    switch (yMode) {
                        // case "null":
                        //   {
                        //   }
                        //   break;
                        // case "numerical":
                        //   {
                        //   }
                        //   break;
                        case "categorical":
                            {
                                handles = handles.concat(this.categoricalHandles("y", false));
                            }
                            break;
                    }
                }
                break;
            case "categorical":
                {
                    switch (yMode) {
                        case "null":
                            {
                                handles = handles.concat(this.categoricalHandles("x", true));
                            }
                            break;
                        case "numerical":
                            {
                                handles = handles.concat(this.categoricalHandles("x", false));
                            }
                            break;
                        case "categorical":
                            {
                                handles = handles.concat(this.categoricalHandles("xy", true));
                            }
                            break;
                    }
                }
                break;
        }
        return handles;
    };
    Region2DConstraintBuilder.prototype.build = function () {
        var solver = this.solver;
        var state = this.plotSegment.state;
        var attrs = state.attributes;
        var props = this.plotSegment.object.properties;
        var xMode = props.xData ? props.xData.type : "null";
        var yMode = props.yData ? props.yData.type : "null";
        switch (xMode) {
            case "null":
                {
                    this.buildXNullMode(yMode, solver, attrs, state);
                }
                break;
            case "default":
                {
                    this.buildXDefaultMode(yMode, solver, attrs, state);
                }
                break;
            case "numerical":
                {
                    this.buildXNumericalMode(yMode, solver, attrs, state);
                }
                break;
            case "categorical":
                {
                    this.buildXCategoricalMode(yMode);
                }
                break;
        }
        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(attrs, "x"), solver.attr(attrs, this.x1Name));
        solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(attrs, "y"), solver.attr(attrs, this.y1Name));
    };
    Region2DConstraintBuilder.prototype.buildXCategoricalMode = function (yMode) {
        switch (yMode) {
            case "null":
                {
                    this.categoricalMapping("x", { mode: "default" });
                }
                break;
            case "default":
                {
                    this.stacking(axis_1.AxisMode.Y);
                    this.categoricalMapping("x", { mode: "disabled" });
                }
                break;
            case "numerical":
                {
                    this.numericalMapping(axis_1.AxisMode.Y);
                    this.categoricalMapping("x", { mode: "x-only" });
                }
                break;
            case "categorical":
                {
                    this.categoricalMapping("xy", { mode: "default" });
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.buildXNumericalMode = function (yMode, solver, attrs, state) {
        switch (yMode) {
            case "null":
                {
                    // numerical, null
                    this.numericalMapping(axis_1.AxisMode.X);
                    this.applySublayout([
                        {
                            x1: solver.attr(attrs, this.x1Name),
                            y1: solver.attr(attrs, this.y1Name),
                            x2: solver.attr(attrs, this.x2Name),
                            y2: solver.attr(attrs, this.y2Name),
                            group: state.dataRowIndices.map(function (x, i) { return i; }),
                        },
                    ], "y", {
                        mode: "y-only",
                    });
                }
                break;
            case "default":
                {
                    this.stacking(axis_1.AxisMode.Y);
                    this.numericalMapping(axis_1.AxisMode.X);
                }
                break;
            case "numerical":
                {
                    // numerical, numerical
                    this.numericalMapping(axis_1.AxisMode.X);
                    this.numericalMapping(axis_1.AxisMode.Y);
                }
                break;
            case "categorical":
                {
                    // numerical, categorical
                    this.numericalMapping(axis_1.AxisMode.X);
                    this.categoricalMapping("y", { mode: "y-only" });
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.buildXDefaultMode = function (yMode, solver, attrs, state) {
        switch (yMode) {
            case "null":
                {
                    this.stacking(axis_1.AxisMode.X);
                    this.applySublayout([
                        {
                            x1: solver.attr(attrs, this.x1Name),
                            y1: solver.attr(attrs, this.y1Name),
                            x2: solver.attr(attrs, this.x2Name),
                            y2: solver.attr(attrs, this.y2Name),
                            group: state.dataRowIndices.map(function (x, i) { return i; }),
                        },
                    ], "y", {
                        mode: "y-only",
                    });
                }
                break;
            case "default":
                {
                    this.stacking(axis_1.AxisMode.X);
                    this.stacking(axis_1.AxisMode.Y);
                }
                break;
            case "numerical":
                {
                    this.stacking(axis_1.AxisMode.X);
                    this.numericalMapping(axis_1.AxisMode.Y);
                }
                break;
            case "categorical":
                {
                    this.stacking(axis_1.AxisMode.X);
                    this.categoricalMapping("y", { mode: "disabled" });
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.buildXNullMode = function (yMode, solver, attrs, state) {
        switch (yMode) {
            case "null":
                {
                    // null, null
                    this.applySublayout([
                        {
                            x1: solver.attr(attrs, this.x1Name),
                            y1: solver.attr(attrs, this.y1Name),
                            x2: solver.attr(attrs, this.x2Name),
                            y2: solver.attr(attrs, this.y2Name),
                            group: state.dataRowIndices.map(function (x, i) { return i; }),
                        },
                    ], "xy", {
                        mode: "default",
                        xAxisPrePostGap: this.config.xAxisPrePostGap,
                        yAxisPrePostGap: this.config.yAxisPrePostGap,
                    });
                }
                break;
            case "default":
                {
                    this.stacking(axis_1.AxisMode.Y);
                    this.applySublayout([
                        {
                            x1: solver.attr(attrs, this.x1Name),
                            y1: solver.attr(attrs, this.y1Name),
                            x2: solver.attr(attrs, this.x2Name),
                            y2: solver.attr(attrs, this.y2Name),
                            group: state.dataRowIndices.map(function (x, i) { return i; }),
                        },
                    ], "x", {
                        mode: "x-only",
                    });
                }
                break;
            case "numerical":
                {
                    // null, numerical
                    this.numericalMapping(axis_1.AxisMode.Y);
                    this.applySublayout([
                        {
                            x1: solver.attr(attrs, this.x1Name),
                            y1: solver.attr(attrs, this.y1Name),
                            x2: solver.attr(attrs, this.x2Name),
                            y2: solver.attr(attrs, this.y2Name),
                            group: state.dataRowIndices.map(function (x, i) { return i; }),
                        },
                    ], "x", {
                        mode: "x-only",
                    });
                }
                break;
            case "categorical":
                {
                    // null, categorical
                    this.categoricalMapping("y", { mode: "default" });
                }
                break;
        }
    };
    Region2DConstraintBuilder.prototype.applicableSublayoutOptions = function () {
        var _a = this.config, icons = _a.icons, terminology = _a.terminology;
        var overlapOption = {
            value: Region2DSublayoutType.Overlap,
            label: terminology.overlap,
            icon: icons.overlapIcon,
        };
        var packingOption = {
            value: Region2DSublayoutType.Packing,
            label: terminology.packing,
            icon: icons.packingIcon,
        };
        var dodgeXOption = {
            value: Region2DSublayoutType.DodgeX,
            label: terminology.dodgeX,
            icon: icons.dodgeXIcon,
        };
        var dodgeYOption = {
            value: Region2DSublayoutType.DodgeY,
            label: terminology.dodgeY,
            icon: icons.dodgeYIcon,
        };
        var gridOption = {
            value: Region2DSublayoutType.Grid,
            label: terminology.grid,
            icon: icons.gridIcon,
        };
        var jitterOption = {
            value: Region2DSublayoutType.Jitter,
            label: terminology.jitter,
            icon: icons.jitterIcon,
        };
        var props = this.plotSegment.object.properties;
        var xMode = props.xData ? props.xData.type : "null";
        var yMode = props.yData ? props.yData.type : "null";
        if ((xMode == "null" || xMode == "categorical") &&
            (yMode == "null" || yMode == "categorical")) {
            return [
                dodgeXOption,
                dodgeYOption,
                gridOption,
                packingOption,
                jitterOption,
                overlapOption,
            ];
        }
        return [packingOption, jitterOption, overlapOption];
    };
    Region2DConstraintBuilder.prototype.isSublayoutApplicable = function () {
        var props = this.plotSegment.object.properties;
        var xMode = props.xData ? props.xData.type : "null";
        var yMode = props.yData ? props.yData.type : "null";
        // Sublayout is not applicable when one of x, y is scaffold ("default"), or both of them are numerical
        return (xMode != "default" &&
            yMode != "default" &&
            (xMode != "numerical" || yMode != "numerical"));
    };
    // eslint-disable-next-line
    Region2DConstraintBuilder.prototype.buildSublayoutWidgets = function (m) {
        var extra = [];
        var props = this.plotSegment.object.properties;
        var type = props.sublayout.type;
        if (type == Region2DSublayoutType.DodgeX ||
            type == Region2DSublayoutType.DodgeY ||
            type == Region2DSublayoutType.Grid ||
            type == Region2DSublayoutType.Overlap) {
            var isXFixed = props.xData && props.xData.type == "numerical";
            var isYFixed = props.yData && props.yData.type == "numerical";
            var alignmentWidgets = [];
            if (!isYFixed) {
                alignmentWidgets.push(m.inputSelect({ property: "sublayout", field: ["align", "y"] }, {
                    type: "radio",
                    options: ["start", "middle", "end"],
                    icons: [
                        "AlignVerticalBottom",
                        "AlignVerticalCenter",
                        "AlignVerticalTop",
                    ],
                    labels: [
                        strings_1.strings.alignment.bottom,
                        strings_1.strings.alignment.middle,
                        strings_1.strings.alignment.top,
                    ],
                    tooltip: strings_1.strings.canvas.alignItemsOnY,
                    ignoreSearch: true,
                }));
            }
            if (!isXFixed) {
                alignmentWidgets.push(m.inputSelect({ property: "sublayout", field: ["align", "x"] }, {
                    type: "radio",
                    options: ["start", "middle", "end"],
                    icons: [
                        "AlignHorizontalLeft",
                        "AlignHorizontalCenter",
                        "AlignHorizontalRight",
                    ],
                    labels: [
                        strings_1.strings.alignment.left,
                        strings_1.strings.alignment.middle,
                        strings_1.strings.alignment.right,
                    ],
                    tooltip: strings_1.strings.canvas.alignItemsOnX,
                    ignoreSearch: true,
                }));
            }
            extra.push(m.searchWrapper({
                searchPattern: [
                    strings_1.strings.alignment.alignment,
                    strings_1.strings.objects.plotSegment.subLayout,
                ],
            }, [
                m.vertical(m.label(strings_1.strings.alignment.alignment, {
                    ignoreSearch: true,
                    addMargins: false,
                }), m.horizontal.apply(m, __spread([[0, 0, 0]], alignmentWidgets.reverse(), [null]))),
            ]));
            if (type == Region2DSublayoutType.Grid) {
                extra.push(m.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.axes.gap,
                        strings_1.strings.objects.plotSegment.subLayout,
                        strings_1.strings.coordinateSystem.x,
                        strings_1.strings.coordinateSystem.y,
                    ],
                }, [
                    m.label(strings_1.strings.objects.axes.gap, { ignoreSearch: true }),
                    m.searchWrapper({
                        searchPattern: [
                            strings_1.strings.coordinateSystem.x,
                            strings_1.strings.objects.axes.gap,
                            strings_1.strings.objects.plotSegment.subLayout,
                        ],
                    }, [
                        m.inputNumber({ property: "sublayout", field: "ratioX" }, {
                            minimum: 0,
                            maximum: 1,
                            percentage: true,
                            showSlider: true,
                            label: strings_1.strings.coordinateSystem.x,
                            ignoreSearch: true,
                        }),
                    ]),
                    m.searchWrapper({
                        searchPattern: [
                            strings_1.strings.coordinateSystem.y,
                            strings_1.strings.objects.axes.gap,
                            strings_1.strings.objects.plotSegment.subLayout,
                        ],
                    }, [
                        m.inputNumber({ property: "sublayout", field: "ratioY" }, {
                            minimum: 0,
                            maximum: 1,
                            percentage: true,
                            showSlider: true,
                            label: strings_1.strings.coordinateSystem.y,
                            ignoreSearch: true,
                        }),
                    ]),
                ]));
            }
            else {
                extra.push(m.inputNumber({
                    property: "sublayout",
                    field: type == Region2DSublayoutType.DodgeX ? "ratioX" : "ratioY",
                }, {
                    minimum: 0,
                    maximum: 1,
                    percentage: true,
                    showSlider: true,
                    label: strings_1.strings.objects.axes.gap,
                    searchSection: strings_1.strings.objects.plotSegment.subLayout,
                }));
            }
            if (type == Region2DSublayoutType.Grid) {
                var terminology = this.config.terminology;
                extra.push(m.inputSelect({ property: "sublayout", field: ["grid", "direction"] }, {
                    type: "radio",
                    options: [GridDirection.X, GridDirection.Y],
                    icons: ["GripperBarHorizontal", "GripperBarVertical"],
                    labels: [terminology.gridDirectionX, terminology.gridDirectionY],
                    label: strings_1.strings.objects.plotSegment.orientation,
                    searchSection: strings_1.strings.objects.plotSegment.subLayout,
                }), m.inputSelect({
                    property: "sublayout",
                    field: ["grid", "gridStartPosition"],
                }, {
                    type: "radio",
                    icons: [
                        "ArrowTallDownRight",
                        "ArrowTallDownLeft",
                        "ArrowTallUpLeft",
                        "ArrowTallUpRight",
                    ],
                    options: [
                        GridStartPosition.LeftTop,
                        GridStartPosition.RightTop,
                        GridStartPosition.LeftBottom,
                        GridStartPosition.RigtBottom,
                    ],
                    labels: [
                        strings_1.strings.objects.plotSegment.directionDownRight,
                        strings_1.strings.objects.plotSegment.directionDownLeft,
                        strings_1.strings.objects.plotSegment.directionUpLeft,
                        strings_1.strings.objects.plotSegment.directionUpRight,
                    ],
                    label: strings_1.strings.objects.plotSegment.direction,
                    searchSection: strings_1.strings.objects.plotSegment.subLayout,
                }), m.inputNumber({
                    property: "sublayout",
                    field: props.sublayout.grid.direction == "x"
                        ? ["grid", "xCount"]
                        : ["grid", "yCount"],
                }, {
                    label: strings_1.strings.objects.axes.count,
                    searchSection: strings_1.strings.objects.plotSegment.subLayout,
                    placeholder: strings_1.strings.core.auto,
                }));
            }
            if (type != Region2DSublayoutType.Overlap) {
                extra.push(m.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.plotSegment.order,
                        strings_1.strings.objects.plotSegment.subLayout,
                    ],
                }, [
                    m.label(strings_1.strings.objects.plotSegment.order, {
                        ignoreSearch: true,
                        addMargins: false,
                    }),
                    m.horizontal([0, 0], m.orderByWidget({ property: "sublayout", field: "order" }, { table: this.plotSegment.object.table, shiftCallout: 15 }), m.inputBoolean({ property: "sublayout", field: "orderReversed" }, { type: "highlight", icon: "Sort", ignoreSearch: true })),
                ]));
            }
        }
        if (type == Region2DSublayoutType.Packing) {
            extra.push(m.searchWrapper({
                searchPattern: [
                    strings_1.strings.objects.plotSegment.subLayout,
                    strings_1.strings.objects.plotSegment.gravity,
                    strings_1.strings.coordinateSystem.x,
                    strings_1.strings.coordinateSystem.y,
                ],
            }, [
                m.label(strings_1.strings.objects.plotSegment.gravity, {
                    ignoreSearch: true,
                }),
                m.inputNumber({ property: "sublayout", field: ["packing", "gravityX"] }, {
                    minimum: 0.1,
                    maximum: 15,
                    label: strings_1.strings.coordinateSystem.x,
                    ignoreSearch: true,
                }),
                m.inputNumber({ property: "sublayout", field: ["packing", "gravityY"] }, {
                    minimum: 0.1,
                    maximum: 15,
                    label: strings_1.strings.coordinateSystem.y,
                    ignoreSearch: true,
                }),
                m.label(strings_1.strings.objects.plotSegment.packingInContainer, {
                    ignoreSearch: true,
                }),
                m.inputBoolean({ property: "sublayout", field: ["packing", "boxedX"] }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.plotSegment.packingX,
                    ignoreSearch: false,
                }),
                m.inputBoolean({ property: "sublayout", field: ["packing", "boxedY"] }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.plotSegment.packingY,
                    ignoreSearch: false,
                }),
            ]));
        }
        if (type == Region2DSublayoutType.Jitter) {
            extra.push(m.searchWrapper({
                searchPattern: [
                    strings_1.strings.objects.plotSegment.distribution,
                    strings_1.strings.objects.plotSegment.subLayout,
                ],
            }, [
                m.label(strings_1.strings.objects.plotSegment.distribution, {
                    ignoreSearch: true,
                }),
                m.inputBoolean({ property: "sublayout", field: ["jitter", "horizontal"] }, {
                    type: "highlight",
                    icon: "HorizontalDistributeCenter",
                    ignoreSearch: true,
                }),
                m.inputBoolean({ property: "sublayout", field: ["jitter", "vertical"] }, {
                    type: "highlight",
                    icon: "VerticalDistributeCenter",
                    ignoreSearch: true,
                }),
            ]));
        }
        var options = this.applicableSublayoutOptions();
        return [
            m.verticalGroup({
                header: strings_1.strings.objects.plotSegment.subLayout,
            }, __spread([
                m.inputSelect({ property: "sublayout", field: "type" }, {
                    type: "radio",
                    options: options.map(function (x) { return x.value; }),
                    icons: options.map(function (x) { return x.icon; }),
                    labels: options.map(function (x) { return x.label; }),
                    label: strings_1.strings.objects.plotSegment.type,
                    searchSection: strings_1.strings.objects.plotSegment.subLayout,
                })
            ], extra)),
        ];
    };
    Region2DConstraintBuilder.prototype.buildAxisWidgets = function (manager, axisName, axis) {
        var props = this.plotSegment.object.properties;
        var data = axis == "x" ? props.xData : props.yData;
        var axisProperty = axis == "x"
            ? PlotSegmentAxisPropertyNames.xData
            : PlotSegmentAxisPropertyNames.yData;
        var axisType = "";
        if (data) {
            switch (data.type) {
                case types_1.AxisDataBindingType.Categorical:
                    axisType = strings_1.strings.objects.axes.categoricalSuffix;
                    break;
                case types_1.AxisDataBindingType.Numerical:
                    axisType = strings_1.strings.objects.axes.numericalSuffix;
                    break;
            }
        }
        var mainCollapsePanelHeader = axisName + axisType;
        return [
            manager.customCollapsiblePanel(__spread(axis_1.buildAxisWidgets(data, axisProperty, manager, axisName, {
                showOffset: true,
                showScrolling: true,
                showOnTop: true,
            }, this.updatePlotSegment.bind(this)), this.plotSegment.buildGridLineWidgets(data, manager, axisProperty, mainCollapsePanelHeader)), {
                header: mainCollapsePanelHeader,
                styles: {
                    marginLeft: 5,
                },
            }),
        ];
    };
    Region2DConstraintBuilder.prototype.updatePlotSegment = function () {
        if (this.chartStateManager && this.plotSegment) {
            this.chartStateManager.remapPlotSegmentGlyphs(this.plotSegment.object);
        }
    };
    Region2DConstraintBuilder.prototype.buildPanelWidgets = function (m) {
        var terminology = this.config.terminology;
        if (this.isSublayoutApplicable()) {
            return __spread(this.buildAxisWidgets(m, terminology.xAxis, "x"), this.buildAxisWidgets(m, terminology.yAxis, "y"), this.buildSublayoutWidgets(m));
        }
        else {
            return __spread(this.buildAxisWidgets(m, terminology.xAxis, "x"), this.buildAxisWidgets(m, terminology.yAxis, "y"));
        }
    };
    // eslint-disable-next-line
    Region2DConstraintBuilder.prototype.buildPopupWidgets = function (m) {
        var props = this.plotSegment.object.properties;
        var _a = this.config, icons = _a.icons, terminology = _a.terminology;
        var sublayout = [];
        if (this.isSublayoutApplicable()) {
            var extra = [];
            var isXFixed = props.xData && props.xData.type == "numerical";
            var isYFixed = props.yData && props.yData.type == "numerical";
            var type = props.sublayout.type;
            if (type == Region2DSublayoutType.DodgeX ||
                type == Region2DSublayoutType.DodgeY ||
                type == Region2DSublayoutType.Grid ||
                type == Region2DSublayoutType.Overlap) {
                if (!isXFixed) {
                    extra.push(m.inputSelect({ property: "sublayout", field: ["align", "x"] }, {
                        type: "dropdown",
                        showLabel: true,
                        labelPosition: 1 /* Bottom */,
                        options: ["start", "middle", "end"],
                        icons: [icons.xMinIcon, icons.xMiddleIcon, icons.xMaxIcon],
                        labels: [
                            terminology.xMin,
                            terminology.xMiddle,
                            terminology.xMax,
                        ],
                        tooltip: strings_1.strings.canvas.alignItemsOnX,
                        hideBorder: true,
                        shiftCallout: 15,
                    }));
                }
                if (!isYFixed) {
                    extra.push(m.inputSelect({ property: "sublayout", field: ["align", "y"] }, {
                        type: "dropdown",
                        showLabel: true,
                        labelPosition: 1 /* Bottom */,
                        options: ["start", "middle", "end"],
                        icons: [icons.yMinIcon, icons.yMiddleIcon, icons.yMaxIcon],
                        labels: [
                            terminology.yMin,
                            terminology.yMiddle,
                            terminology.yMax,
                        ],
                        tooltip: strings_1.strings.canvas.alignItemsOnY,
                        hideBorder: true,
                        shiftCallout: 15,
                    }));
                }
                if (type == "grid") {
                    extra.push(m.sep());
                    extra.push(m.inputSelect({ property: "sublayout", field: ["grid", "direction"] }, {
                        type: "dropdown",
                        showLabel: true,
                        labelPosition: 1 /* Bottom */,
                        options: [GridDirection.X, GridDirection.Y],
                        icons: ["GripperBarHorizontal", "GripperBarVertical"],
                        labels: [
                            terminology.gridDirectionX,
                            terminology.gridDirectionY,
                        ],
                        tooltip: strings_1.strings.canvas.gridDirection,
                        hideBorder: true,
                        shiftCallout: 15,
                    }));
                    extra.push(m.inputSelect({
                        property: "sublayout",
                        field: ["grid", "gridStartPosition"],
                    }, {
                        type: "dropdown",
                        icons: [
                            "ArrowTallDownRight",
                            "ArrowTallDownLeft",
                            "ArrowTallUpLeft",
                            "ArrowTallUpRight",
                        ],
                        options: [
                            GridStartPosition.LeftTop,
                            GridStartPosition.RightTop,
                            GridStartPosition.LeftBottom,
                            GridStartPosition.RigtBottom,
                        ],
                        labels: [
                            strings_1.strings.objects.plotSegment.directionDownRight,
                            strings_1.strings.objects.plotSegment.directionDownLeft,
                            strings_1.strings.objects.plotSegment.directionUpLeft,
                            strings_1.strings.objects.plotSegment.directionUpRight,
                        ],
                        hideBorder: true,
                    }));
                }
                if (type != Region2DSublayoutType.Overlap) {
                    extra.push(m.sep());
                    extra.push(m.orderByWidget({ property: "sublayout", field: "order" }, {
                        table: this.plotSegment.object.table,
                        displayLabel: true,
                        tooltip: strings_1.strings.canvas.elementOrders,
                        shiftCallout: 15,
                    }), m.inputBoolean({ property: "sublayout", field: "orderReversed" }, { type: "highlight", icon: "Sort" }));
                }
            }
            var options = this.applicableSublayoutOptions();
            sublayout = __spread([
                m.inputSelect({ property: "sublayout", field: "type" }, {
                    type: "dropdown",
                    showLabel: true,
                    labelPosition: 1 /* Bottom */,
                    options: options.map(function (x) { return x.value; }),
                    icons: options.map(function (x) { return x.icon; }),
                    labels: options.map(function (x) { return x.label; }),
                    tooltip: strings_1.strings.canvas.sublayoutType,
                    hideBorder: true,
                    shiftCallout: 15,
                })
            ], extra);
        }
        var isXStacking = props.xData && props.xData.type == "default";
        var isYStacking = props.yData && props.yData.type == "default";
        if (isXStacking && !isYStacking) {
            if (props.xData.type == "default") {
                sublayout.push(m.label(terminology.xAxis + ": Stacking"));
            }
            sublayout.push(m.inputSelect({ property: "sublayout", field: ["align", "y"] }, {
                type: "dropdown",
                showLabel: true,
                labelPosition: 1 /* Bottom */,
                options: ["start", "middle", "end"],
                icons: [icons.yMinIcon, icons.yMiddleIcon, icons.yMaxIcon],
                labels: [terminology.yMin, terminology.yMiddle, terminology.yMax],
                hideBorder: true,
                shiftCallout: 15,
            }));
        }
        if (isYStacking && !isXStacking) {
            if (props.yData.type == "default") {
                sublayout.push(m.label(terminology.yAxis + ": Stacking"));
            }
            sublayout.push(m.inputSelect({ property: "sublayout", field: ["align", "x"] }, {
                type: "dropdown",
                showLabel: true,
                labelPosition: 1 /* Bottom */,
                options: ["start", "middle", "end"],
                icons: [icons.xMinIcon, icons.xMiddleIcon, icons.xMaxIcon],
                labels: [terminology.xMin, terminology.xMiddle, terminology.xMax],
                hideBorder: true,
                shiftCallout: 15,
            }));
        }
        if (isXStacking && isYStacking) {
            if (props.yData.type == "default") {
                sublayout.push(m.label(terminology.xAxis + " & " + terminology.yAxis + ": Stacking"));
            }
        }
        return __spread(sublayout);
    };
    Region2DConstraintBuilder.defaultJitterPackingRadius = 5;
    return Region2DConstraintBuilder;
}());
exports.Region2DConstraintBuilder = Region2DConstraintBuilder;
//# sourceMappingURL=base.js.map