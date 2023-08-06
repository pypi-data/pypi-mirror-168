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
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.WASMSolver = exports.Matrix = exports.initialize = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var LSCGSolver = require("lscg-solver");
var common_1 = require("../common");
var abstract_1 = require("./abstract");
function initialize() {
    return LSCGSolver.initialize();
}
exports.initialize = initialize;
exports.Matrix = LSCGSolver.Matrix;
var strengthMap = (_a = {},
    _a[abstract_1.ConstraintStrength.HARD] = LSCGSolver.ConstraintSolver.STRENGTH_HARD,
    _a[abstract_1.ConstraintStrength.STRONG] = LSCGSolver.ConstraintSolver.STRENGTH_STRONG,
    _a[abstract_1.ConstraintStrength.MEDIUM] = LSCGSolver.ConstraintSolver.STRENGTH_MEDIUM,
    _a[abstract_1.ConstraintStrength.WEAK] = LSCGSolver.ConstraintSolver.STRENGTH_WEAK,
    _a[abstract_1.ConstraintStrength.WEAKER] = LSCGSolver.ConstraintSolver.STRENGTH_WEAKER,
    _a);
var WASMSolver = /** @class */ (function (_super) {
    __extends(WASMSolver, _super);
    function WASMSolver() {
        var _this = _super.call(this) || this;
        _this.currentIndex = 0;
        _this.softInequalities = [];
        _this.variables = new common_1.KeyNameMap();
        _this.solver = new LSCGSolver.ConstraintSolver();
        _this.solver.flags = LSCGSolver.ConstraintSolver.FLAG_REDUCE; // | LSCGSolver.ConstraintSolver.FLAG_LAGRANGE;
        _this.solver.tolerance = 1e-8;
        return _this;
    }
    WASMSolver.prototype.makeConstant = function (map, name) {
        this.solver.makeConstant(this.attr(map, name).index);
    };
    /** Get the variable of an attribute */
    WASMSolver.prototype.attr = function (map, name, options) {
        if (this.variables.has(map, name)) {
            return this.variables.get(map, name);
        }
        else {
            this.currentIndex++;
            var item = { index: this.currentIndex, map: map, name: name };
            this.variables.add(map, name, item);
            var value = +map[name];
            // Safety check: the solver won't like NaNs
            if (isNaN(value)) {
                value = 0;
            }
            this.solver.addVariable(this.currentIndex, value, options ? options.edit : false);
            if (!options) {
                console.warn("Creating new attr " + name + " without options");
            }
            return item;
        }
    };
    /** Get the value of a variable */
    WASMSolver.prototype.getValue = function (attr) {
        return attr.map[attr.name];
    };
    /** Set the value of a variable */
    WASMSolver.prototype.setValue = function (attr, value) {
        attr.map[attr.name] = value;
    };
    /**
     * Add a linear constraint
     * @param lhs - left-hand side of equation
     * @param rhs - left-hand side of equation
     */
    WASMSolver.prototype.addLinear = function (strength, bias, lhs, rhs) {
        var e_1, _a, e_2, _b;
        var st = strengthMap[strength];
        var weights = [];
        var variable_names = [];
        try {
            for (var lhs_1 = __values(lhs), lhs_1_1 = lhs_1.next(); !lhs_1_1.done; lhs_1_1 = lhs_1.next()) {
                var item = lhs_1_1.value;
                weights.push(item[0]);
                variable_names.push(item[1].index);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (lhs_1_1 && !lhs_1_1.done && (_a = lhs_1.return)) _a.call(lhs_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        if (rhs) {
            try {
                for (var rhs_1 = __values(rhs), rhs_1_1 = rhs_1.next(); !rhs_1_1.done; rhs_1_1 = rhs_1.next()) {
                    var item = rhs_1_1.value;
                    weights.push(-item[0]);
                    variable_names.push(item[1].index);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (rhs_1_1 && !rhs_1_1.done && (_b = rhs_1.return)) _b.call(rhs_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
        this.solver.addConstraint(st, bias, variable_names, weights);
    };
    /** Add a soft inequality constraint: bias + linear(lhs) >= linear(rhs) */
    WASMSolver.prototype.addSoftInequality = function (strength, bias, lhs, rhs) {
        var e_3, _a, e_4, _b;
        var st = strengthMap[strength];
        var weights = [];
        var variable_names = [];
        try {
            for (var lhs_2 = __values(lhs), lhs_2_1 = lhs_2.next(); !lhs_2_1.done; lhs_2_1 = lhs_2.next()) {
                var item = lhs_2_1.value;
                weights.push(item[0]);
                variable_names.push(item[1].index);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (lhs_2_1 && !lhs_2_1.done && (_a = lhs_2.return)) _a.call(lhs_2);
            }
            finally { if (e_3) throw e_3.error; }
        }
        if (rhs) {
            try {
                for (var rhs_2 = __values(rhs), rhs_2_1 = rhs_2.next(); !rhs_2_1.done; rhs_2_1 = rhs_2.next()) {
                    var item = rhs_2_1.value;
                    weights.push(-item[0]);
                    variable_names.push(item[1].index);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (rhs_2_1 && !rhs_2_1.done && (_b = rhs_2.return)) _b.call(rhs_2);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
        var id = this.solver.addConstraint(st, bias, variable_names, weights);
        this.softInequalities.push({
            id: id,
            bias: bias,
            variable_names: variable_names,
            weights: weights,
        });
    };
    /** Solve the constraints */
    WASMSolver.prototype.solve = function () {
        var e_5, _a;
        var _this = this;
        this.variables.forEach(function (value, map, key) {
            _this.solver.setValue(value.index, map[key]);
        });
        this.solver.regularizerWeight = 0.001;
        var maxIters = 20;
        for (var iter = 0; iter < maxIters; iter++) {
            this.solver.solve();
            var shouldReiterate = false;
            try {
                for (var _b = (e_5 = void 0, __values(this.softInequalities)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var soft = _c.value;
                    var value = soft.bias;
                    for (var i = 0; i < soft.variable_names.length; i++) {
                        value +=
                            this.solver.getValue(soft.variable_names[i]) * soft.weights[i];
                    }
                    if (value >= -1e-6) {
                        this.solver.setConstraintStrength(soft.id, LSCGSolver.ConstraintSolver.STRENGTH_DISABLED);
                    }
                    else {
                        shouldReiterate = true;
                    }
                }
            }
            catch (e_5_1) { e_5 = { error: e_5_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_5) throw e_5.error; }
            }
            if (!shouldReiterate) {
                break;
            }
            if (iter == maxIters - 1) {
                console.warn("Soft inequalities didn't converge within " + maxIters + " iterations");
            }
        }
        this.variables.forEach(function (value, map, key) {
            map[key] = _this.solver.getValue(value.index);
        });
        return [0, this.solver.error];
    };
    WASMSolver.prototype.destroy = function () {
        this.solver.destroy();
    };
    return WASMSolver;
}(abstract_1.ConstraintSolver));
exports.WASMSolver = WASMSolver;
//# sourceMappingURL=wasm_solver.js.map