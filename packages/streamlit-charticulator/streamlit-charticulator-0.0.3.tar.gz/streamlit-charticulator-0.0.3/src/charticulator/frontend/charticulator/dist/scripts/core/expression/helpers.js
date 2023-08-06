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
exports.verifyUserExpression = exports.ExpressionCache = exports.getDefaultAggregationFunction = exports.getCompatibleAggregationFunctionsByDataKind = exports.getCompatibleAggregationFunctionsByDataType = exports.aggregationFunctions = exports.date = exports.boolean = exports.string = exports.number = exports.div = exports.mul = exports.sub = exports.add = exports.fields = exports.lambda = exports.functionCall = exports.variable = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var classes_1 = require("./classes");
var specification_1 = require("../specification");
function variable(name) {
    return new classes_1.Variable(name);
}
exports.variable = variable;
function functionCall(functionName) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    var fields = functionName.split(".");
    return new classes_1.FunctionCall(fields, args);
}
exports.functionCall = functionCall;
function lambda(names, expression) {
    return new classes_1.LambdaFunction(expression, names);
}
exports.lambda = lambda;
function fields(expr) {
    var fields = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        fields[_i - 1] = arguments[_i];
    }
    return new classes_1.FieldAccess(expr, fields);
}
exports.fields = fields;
function add(lhs, rhs) {
    return new classes_1.Operator("+", lhs, rhs);
}
exports.add = add;
function sub(lhs, rhs) {
    return new classes_1.Operator("-", lhs, rhs);
}
exports.sub = sub;
function mul(lhs, rhs) {
    return new classes_1.Operator("*", lhs, rhs);
}
exports.mul = mul;
function div(lhs, rhs) {
    return new classes_1.Operator("/", lhs, rhs);
}
exports.div = div;
function number(v) {
    return new classes_1.NumberValue(v);
}
exports.number = number;
function string(v) {
    return new classes_1.StringValue(v);
}
exports.string = string;
function boolean(v) {
    return new classes_1.BooleanValue(v);
}
exports.boolean = boolean;
function date(v) {
    return new classes_1.DateValue(v);
}
exports.date = date;
exports.aggregationFunctions = [
    {
        name: "avg",
        displayName: "Average",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "median",
        displayName: "Median",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "sum",
        displayName: "Sum",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "min",
        displayName: "Min",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "max",
        displayName: "Max",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "stdev",
        displayName: "Standard Deviation",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "variance",
        displayName: "Variance",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "first",
        displayName: "First",
        inputTypes: [specification_1.DataType.String, specification_1.DataType.Boolean],
        inputKind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
    },
    {
        name: "last",
        displayName: "Last",
        inputTypes: [specification_1.DataType.String, specification_1.DataType.Boolean],
        inputKind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
    },
    {
        name: "count",
        displayName: "Count",
        inputTypes: [specification_1.DataType.String, specification_1.DataType.Boolean],
        inputKind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
    },
    {
        name: "quartile1",
        displayName: "1st Quartile",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "quartile3",
        displayName: "3rd Quartile",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
    {
        name: "iqr",
        displayName: "Inter Quartile Range (IQR)",
        inputTypes: [specification_1.DataType.Number],
        inputKind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
    },
];
function getCompatibleAggregationFunctionsByDataType(inputType) {
    return exports.aggregationFunctions.filter(function (x) { return x.inputTypes == null || x.inputTypes.indexOf(inputType) >= 0; });
}
exports.getCompatibleAggregationFunctionsByDataType = getCompatibleAggregationFunctionsByDataType;
function getCompatibleAggregationFunctionsByDataKind(inputKind) {
    return exports.aggregationFunctions.filter(function (x) { return x.inputKind == null || x.inputKind.indexOf(inputKind) >= 0; });
}
exports.getCompatibleAggregationFunctionsByDataKind = getCompatibleAggregationFunctionsByDataKind;
function getDefaultAggregationFunction(inputType, kind) {
    if (inputType == specification_1.DataType.Number || inputType == specification_1.DataType.Date) {
        if (kind === specification_1.DataKind.Categorical || kind === specification_1.DataKind.Ordinal) {
            return "first";
        }
        else {
            return "avg";
        }
    }
    else {
        return "first";
    }
}
exports.getDefaultAggregationFunction = getDefaultAggregationFunction;
var ExpressionCache = /** @class */ (function () {
    function ExpressionCache() {
        this.items = new Map();
        this.textItems = new Map();
    }
    ExpressionCache.prototype.clear = function () {
        this.items.clear();
        this.textItems.clear();
    };
    ExpressionCache.prototype.parse = function (expr) {
        if (this.items.has(expr)) {
            return this.items.get(expr);
        }
        else {
            var result = classes_1.Expression.Parse(expr);
            this.items.set(expr, result);
            return result;
        }
    };
    ExpressionCache.prototype.parseTextExpression = function (expr) {
        if (this.textItems.has(expr)) {
            return this.textItems.get(expr);
        }
        else {
            var result = classes_1.TextExpression.Parse(expr);
            this.textItems.set(expr, result);
            return result;
        }
    };
    return ExpressionCache;
}());
exports.ExpressionCache = ExpressionCache;
/**
 * Verify user input expression
 * @param inputString The expression from user input
 * @param options Verification options
 */
function verifyUserExpression(inputString, options) {
    var e_1, _a, e_2, _b;
    var expr;
    // Try parse the expression
    try {
        if (options.textExpression) {
            expr = classes_1.TextExpression.Parse(inputString);
        }
        else {
            expr = classes_1.Expression.Parse(inputString);
        }
    }
    catch (error) {
        return {
            pass: false,
            error: "Parse Error: " + error.message,
        };
    }
    if (options.table) {
        try {
            expr.getValue(options.table);
        }
        catch (error) {
            return {
                pass: false,
                error: "Evaluate Error: " + error.message,
            };
        }
    }
    else if (options.data) {
        if (options.expectedTypes) {
            var expectedTypes = new Set(options.expectedTypes);
            try {
                try {
                    for (var _c = __values(options.data), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var ctx = _d.value;
                        var value = expr.getValue(ctx);
                        var valueType = typeof value;
                        if (value == null || valueType == "undefined") {
                            valueType = "null";
                        }
                        if (!expectedTypes.has(valueType)) {
                            return {
                                pass: false,
                                error: "Type Error: unexpected " + valueType + " returned",
                            };
                        }
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
            }
            catch (error) {
                return {
                    pass: false,
                    error: "Evaluate Error: " + error.message,
                };
            }
        }
        else {
            try {
                try {
                    for (var _e = __values(options.data), _f = _e.next(); !_f.done; _f = _e.next()) {
                        var ctx = _f.value;
                        expr.getValue(ctx);
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
            catch (error) {
                return {
                    pass: false,
                    error: "Evaluate Error: " + error.message,
                };
            }
        }
    }
    return {
        pass: true,
        formatted: expr.toString(),
    };
}
exports.verifyUserExpression = verifyUserExpression;
//# sourceMappingURL=helpers.js.map