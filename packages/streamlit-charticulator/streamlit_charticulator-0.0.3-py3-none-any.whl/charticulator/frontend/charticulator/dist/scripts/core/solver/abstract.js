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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConstraintSolver = exports.ConstraintPlugin = exports.ConstraintStrength = void 0;
var ConstraintStrength;
(function (ConstraintStrength) {
    ConstraintStrength[ConstraintStrength["HARD"] = 1] = "HARD";
    ConstraintStrength[ConstraintStrength["STRONG"] = 2] = "STRONG";
    ConstraintStrength[ConstraintStrength["MEDIUM"] = 3] = "MEDIUM";
    ConstraintStrength[ConstraintStrength["WEAK"] = 4] = "WEAK";
    ConstraintStrength[ConstraintStrength["WEAKER"] = 5] = "WEAKER";
})(ConstraintStrength = exports.ConstraintStrength || (exports.ConstraintStrength = {}));
var ConstraintPlugin = /** @class */ (function () {
    function ConstraintPlugin() {
    }
    return ConstraintPlugin;
}());
exports.ConstraintPlugin = ConstraintPlugin;
var ConstraintSolver = /** @class */ (function () {
    function ConstraintSolver() {
        this.plugins = [];
    }
    // /** Solve the constraints asynchronously */
    // public abstract solveAsync(callback: (finish: boolean) => void): void;
    // /** Stop the async solve */
    // public abstract solveAsyncStop(): void;
    // Below are general helper functions
    /** Get attributes */
    ConstraintSolver.prototype.attrs = function (map, name) {
        var _this = this;
        return name.map(function (n) { return _this.attr(map, n); });
    };
    /** Get a linear value */
    ConstraintSolver.prototype.getLinear = function () {
        var e_1, _a;
        var items = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            items[_i] = arguments[_i];
        }
        var s = 0;
        try {
            for (var items_1 = __values(items), items_1_1 = items_1.next(); !items_1_1.done; items_1_1 = items_1.next()) {
                var v = items_1_1.value;
                s += v[0] * this.getValue(v[1]);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (items_1_1 && !items_1_1.done && (_a = items_1.return)) _a.call(items_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return s;
    };
    /** Add a constraint that enfoces a = b */
    ConstraintSolver.prototype.addEquals = function (strength, a, b) {
        this.addLinear(strength, 0, [
            [1, a],
            [-1, b],
        ]);
    };
    /** Add a constraint that enfoces a = value */
    ConstraintSolver.prototype.addEqualToConstant = function (strength, a, value) {
        this.addLinear(strength, value, [[-1, a]]);
    };
    ConstraintSolver.prototype.addPlugin = function (plugin) {
        this.plugins.push(plugin);
    };
    ConstraintSolver.prototype.applyPlugins = function () {
        this.plugins.forEach(function (p) { return p.apply(); });
    };
    return ConstraintSolver;
}());
exports.ConstraintSolver = ConstraintSolver;
//# sourceMappingURL=abstract.js.map