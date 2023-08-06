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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Variable = exports.LambdaFunction = exports.Operator = exports.FunctionCall = exports.FieldAccess = exports.DateValue = exports.BooleanValue = exports.NumberValue = exports.StringValue = exports.Value = exports.TextExpression = exports.Expression = exports.variableReplacer = exports.SimpleContext = exports.ShadowContext = void 0;
var pegjs = require("./parser.pegjs");
var ShadowContext = /** @class */ (function () {
    function ShadowContext(upstream, shadows) {
        if (upstream === void 0) { upstream = null; }
        if (shadows === void 0) { shadows = {}; }
        this.upstream = upstream;
        this.shadows = shadows;
    }
    ShadowContext.prototype.getVariable = function (name) {
        if (Object.prototype.hasOwnProperty.call(this.shadows, name)) {
            return this.shadows[name];
        }
        return this.upstream.getVariable(name);
    };
    return ShadowContext;
}());
exports.ShadowContext = ShadowContext;
var SimpleContext = /** @class */ (function () {
    function SimpleContext() {
        this.variables = {};
    }
    SimpleContext.prototype.getVariable = function (name) {
        return this.variables[name];
    };
    return SimpleContext;
}());
exports.SimpleContext = SimpleContext;
var intrinsics_1 = require("./intrinsics");
var dataflow_1 = require("../prototypes/dataflow");
var __1 = require("..");
function variableReplacer(map) {
    return function (expr) {
        if (expr instanceof Variable) {
            // DON'T CHANGE TO Object.prototype.hasOwnProperty.call !!!
            // Template builder overrides hasOwnProperty method
            // eslint-disable-next-line
            if (map.hasOwnProperty(expr.name)) {
                return new Variable(map[expr.name]);
            }
        }
    };
}
exports.variableReplacer = variableReplacer;
var Expression = /** @class */ (function () {
    function Expression() {
    }
    Expression.prototype.toStringPrecedence = function (parent) {
        if (this.getPrecedence() < parent) {
            return "(" + this.toString() + ")";
        }
        else {
            return this.toString();
        }
    };
    Expression.prototype.getNumberValue = function (c) {
        var v = this.getValue(c);
        return v;
    };
    Expression.prototype.getStringValue = function (c) {
        var v = this.getValue(c);
        return v !== null && v !== undefined ? v.toString() : "null";
    };
    Expression.Parse = function (expr) {
        return pegjs.parse(expr);
    };
    Expression.prototype.replace = function (replacer) {
        var r = replacer(this);
        if (r) {
            // If the expression matches the pattern, replace itself
            return r;
        }
        else {
            // Otherwise, replace any pattern found inside
            return this.replaceChildren(replacer);
        }
    };
    return Expression;
}());
exports.Expression = Expression;
/** Text expression is a special class, it cannot be used inside other expression */
var TextExpression = /** @class */ (function () {
    function TextExpression(parts) {
        if (parts === void 0) { parts = []; }
        this.parts = parts;
    }
    TextExpression.prototype.getValue = function (context) {
        return this.parts
            .map(function (part) {
            if (part.string) {
                return part.string;
            }
            else if (part.expression) {
                var val = part.expression.getValue(context);
                if (part.format) {
                    try {
                        return __1.getFormat()(part.format)(+val);
                    }
                    catch (ex) {
                        try {
                            return __1.applyDateFormat(new Date(+val), part.format);
                        }
                        catch (ex) {
                            // try to handle specific format
                            if (part.format.match(/^%raw$/).length > 0) {
                                return getFormattedValue(context, val, part.expression);
                            }
                            else {
                                throw ex;
                            }
                        }
                    }
                }
                else {
                    return val;
                }
            }
        })
            .join("");
    };
    TextExpression.prototype.isTrivialString = function () {
        return this.parts.every(function (x) { return x.string != null; });
    };
    TextExpression.prototype.toString = function () {
        return this.parts
            .map(function (part) {
            if (part.string) {
                return part.string.replace(/([$\\])/g, "\\$1");
            }
            else if (part.expression) {
                var str = part.expression.toString();
                if (part.format) {
                    return "${" + str + "}{" + part.format + "}";
                }
                else {
                    return "${" + str + "}";
                }
            }
        })
            .join("");
    };
    TextExpression.Parse = function (expr) {
        return pegjs.parse(expr, { startRule: "start_text" });
    };
    TextExpression.prototype.replace = function (r) {
        return new TextExpression(this.parts.map(function (part) {
            if (part.string) {
                return { string: part.string };
            }
            else if (part.expression) {
                if (part.format) {
                    return {
                        expression: part.expression.replace(r),
                        format: part.format,
                    };
                }
                else {
                    return { expression: part.expression.replace(r) };
                }
            }
        }));
    };
    return TextExpression;
}());
exports.TextExpression = TextExpression;
var Value = /** @class */ (function (_super) {
    __extends(Value, _super);
    function Value(value) {
        var _this = _super.call(this) || this;
        _this.value = value;
        return _this;
    }
    Value.prototype.getValue = function () {
        return this.value;
    };
    Value.prototype.toString = function () {
        return JSON.stringify(this.value);
    };
    Value.prototype.getPrecedence = function () {
        return intrinsics_1.precedences.VALUE;
    };
    // eslint-disable-next-line
    Value.prototype.replaceChildren = function (r) {
        return new Value(this.value);
    };
    return Value;
}(Expression));
exports.Value = Value;
var StringValue = /** @class */ (function (_super) {
    __extends(StringValue, _super);
    function StringValue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return StringValue;
}(Value));
exports.StringValue = StringValue;
var NumberValue = /** @class */ (function (_super) {
    __extends(NumberValue, _super);
    function NumberValue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return NumberValue;
}(Value));
exports.NumberValue = NumberValue;
var BooleanValue = /** @class */ (function (_super) {
    __extends(BooleanValue, _super);
    function BooleanValue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return BooleanValue;
}(Value));
exports.BooleanValue = BooleanValue;
var DateValue = /** @class */ (function (_super) {
    __extends(DateValue, _super);
    function DateValue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return DateValue;
}(Value));
exports.DateValue = DateValue;
var FieldAccess = /** @class */ (function (_super) {
    __extends(FieldAccess, _super);
    function FieldAccess(expr, fields) {
        var _this = _super.call(this) || this;
        _this.expr = expr;
        _this.fields = fields;
        return _this;
    }
    FieldAccess.prototype.getValue = function (c) {
        var e_1, _a;
        var v = this.expr.getValue(c);
        try {
            for (var _b = __values(this.fields), _c = _b.next(); !_c.done; _c = _b.next()) {
                var f = _c.value;
                v = v[f];
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return v;
    };
    FieldAccess.prototype.toString = function () {
        return this.expr.toStringPrecedence(intrinsics_1.precedences.FIELD_ACCESS) + "." + this.fields.map(Variable.VariableNameToString).join(".");
    };
    FieldAccess.prototype.getPrecedence = function () {
        return intrinsics_1.precedences.FIELD_ACCESS;
    };
    FieldAccess.prototype.replaceChildren = function (r) {
        return new FieldAccess(this.expr.replace(r), this.fields);
    };
    return FieldAccess;
}(Expression));
exports.FieldAccess = FieldAccess;
var FunctionCall = /** @class */ (function (_super) {
    __extends(FunctionCall, _super);
    function FunctionCall(parts, args) {
        var e_2, _a;
        var _this = _super.call(this) || this;
        _this.name = parts.join(".");
        _this.args = args;
        var v = intrinsics_1.functions;
        try {
            for (var parts_1 = __values(parts), parts_1_1 = parts_1.next(); !parts_1_1.done; parts_1_1 = parts_1.next()) {
                var part = parts_1_1.value;
                if (Object.prototype.hasOwnProperty.call(v, part) || v[part]) {
                    v = v[part];
                }
                else {
                    v = undefined;
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (parts_1_1 && !parts_1_1.done && (_a = parts_1.return)) _a.call(parts_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        if (v == undefined) {
            throw new SyntaxError("undefiend function " + _this.name);
        }
        else {
            _this.function = v;
        }
        return _this;
    }
    FunctionCall.prototype.getValue = function (c) {
        var _a;
        var data = (_a = this.args
            .map(function (arg) { return arg.getValue(c); })) === null || _a === void 0 ? void 0 : _a.filter(function (item) { return item !== undefined; });
        if (!data.length) {
            return null;
        }
        return this.function.apply(this, __spread(data));
    };
    FunctionCall.prototype.toString = function () {
        return this.name + "(" + this.args
            .map(function (arg) { return arg.toStringPrecedence(intrinsics_1.precedences.FUNCTION_ARGUMENT); })
            .join(", ") + ")";
    };
    FunctionCall.prototype.getPrecedence = function () {
        return intrinsics_1.precedences.FUNCTION_CALL;
    };
    FunctionCall.prototype.replaceChildren = function (r) {
        return new FunctionCall(this.name.split("."), this.args.map(function (x) { return x.replace(r); }));
    };
    return FunctionCall;
}(Expression));
exports.FunctionCall = FunctionCall;
var Operator = /** @class */ (function (_super) {
    __extends(Operator, _super);
    function Operator(name, lhs, rhs) {
        var _this = _super.call(this) || this;
        _this.name = name;
        _this.lhs = lhs;
        _this.rhs = rhs;
        if (rhs != undefined) {
            _this.op = intrinsics_1.operators[name];
        }
        else {
            _this.op = intrinsics_1.operators["unary:" + name];
        }
        return _this;
    }
    Operator.prototype.getValue = function (c) {
        var lhs = this.lhs.getValue(c);
        if (this.rhs != undefined) {
            var rhs = this.rhs.getValue(c);
            return this.op(lhs, rhs);
        }
        else {
            return this.op(lhs);
        }
    };
    Operator.prototype.toString = function () {
        var p = this.getMyPrecedence();
        if (this.rhs != undefined) {
            return this.lhs.toStringPrecedence(p[1]) + " " + this.name + " " + this.rhs.toStringPrecedence(p[2]);
        }
        else {
            return this.name + " " + this.lhs.toStringPrecedence(p[1]);
        }
    };
    Operator.prototype.getMyPrecedence = function () {
        if (this.rhs != undefined) {
            return intrinsics_1.precedences.OPERATORS[this.name];
        }
        else {
            return intrinsics_1.precedences.OPERATORS["unary:" + this.name];
        }
    };
    Operator.prototype.getPrecedence = function () {
        return this.getMyPrecedence()[0];
    };
    Operator.prototype.replaceChildren = function (r) {
        return new Operator(this.name, this.lhs.replace(r), this.rhs ? this.rhs.replace(r) : null);
    };
    return Operator;
}(Expression));
exports.Operator = Operator;
var LambdaFunction = /** @class */ (function (_super) {
    __extends(LambdaFunction, _super);
    function LambdaFunction(expr, argNames) {
        var _this = _super.call(this) || this;
        _this.expr = expr;
        _this.argNames = argNames;
        return _this;
    }
    LambdaFunction.prototype.getValue = function (c) {
        var _this = this;
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var lambdaContext = new ShadowContext(c);
            for (var i = 0; i < _this.argNames.length; i++) {
                lambdaContext.shadows[_this.argNames[i]] = args[i];
            }
            return _this.expr.getValue(lambdaContext);
        };
    };
    LambdaFunction.prototype.toString = function () {
        return "(" + this.argNames.join(", ") + ") => " + this.expr.toStringPrecedence(intrinsics_1.precedences.LAMBDA_EXPRESSION);
    };
    LambdaFunction.prototype.getPrecedence = function () {
        return intrinsics_1.precedences.LAMBDA_FUNCTION;
    };
    LambdaFunction.prototype.replaceChildren = function (r) {
        var _this = this;
        // Mask the argument variables in the lambda function
        var rMasked = function (expr) {
            if (expr instanceof Variable && _this.argNames.indexOf(expr.name) >= 0) {
                return undefined;
            }
            else {
                return r(expr);
            }
        };
        return new LambdaFunction(this.expr.replace(rMasked), this.argNames);
    };
    return LambdaFunction;
}(Expression));
exports.LambdaFunction = LambdaFunction;
var Variable = /** @class */ (function (_super) {
    __extends(Variable, _super);
    function Variable(name) {
        var _this = _super.call(this) || this;
        _this.name = name;
        return _this;
    }
    Variable.prototype.getValue = function (c) {
        var v = c.getVariable(this.name);
        if (v === undefined) {
            return intrinsics_1.constants[this.name];
        }
        else {
            return v;
        }
    };
    Variable.prototype.toString = function () {
        return Variable.VariableNameToString(this.name);
    };
    Variable.prototype.getPrecedence = function () {
        return intrinsics_1.precedences.VARIABLE;
    };
    Variable.isNonEnglishVariableName = function (name) {
        // eslint-disable-next-line no-control-regex
        if (name.match(/^[^\x00-\x7F]+$/)) {
            return true;
        }
        return false;
    };
    Variable.VariableNameToString = function (name) {
        if (name.match(/^[a-zA-Z_][a-zA-Z0-9_]*$/)) {
            return name;
        }
        else {
            return JSON.stringify(name).replace(/^"|"$/g, "`");
        }
    };
    // eslint-disable-next-line
    Variable.prototype.replaceChildren = function (r) {
        return new Variable(this.name);
    };
    return Variable;
}(Expression));
exports.Variable = Variable;
function getFormattedValue(context, val, expression) {
    if (val === undefined || val === null) {
        return val;
    }
    if (context instanceof ShadowContext) {
        if (expression instanceof FunctionCall &&
            expression.args[0] instanceof Variable) {
            var columnName_1 = expression.args[0].name;
            var column = (context.upstream).columns.find(function (col) { return col.name == columnName_1; });
            if (column.metadata.rawColumnName &&
                (column.metadata.kind === __1.Specification.DataKind.Temporal ||
                    column.type === __1.Specification.DataType.Boolean)) {
                return context.getVariable(column.metadata.rawColumnName);
            }
        }
    }
    if (context instanceof dataflow_1.DataflowTableGroupedContext) {
        if (expression instanceof FunctionCall &&
            expression.args[0] instanceof Variable) {
            var columnName_2 = expression.args[0].name;
            var rawColumnName = context
                .getTable()
                .columns.find(function (col) { return col.name == columnName_2; }).metadata.rawColumnName;
            if (rawColumnName) {
                return context.getVariable(rawColumnName);
            }
        }
    }
    return val;
}
//# sourceMappingURL=classes.js.map