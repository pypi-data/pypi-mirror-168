"use strict";
/**
 * Expressions
 *
 * The module of exressions responsible for data binding or data fetching
 * Grammar of expression described in [parser.pegjs file](\src\core\expression\index.ts)
 *
 * @packageDocumentation
 * @preferred
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseTextExpression = exports.parse = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var classes_1 = require("./classes");
var classes_2 = require("./classes");
Object.defineProperty(exports, "Expression", { enumerable: true, get: function () { return classes_2.Expression; } });
Object.defineProperty(exports, "TextExpression", { enumerable: true, get: function () { return classes_2.TextExpression; } });
Object.defineProperty(exports, "ShadowContext", { enumerable: true, get: function () { return classes_2.ShadowContext; } });
Object.defineProperty(exports, "LambdaFunction", { enumerable: true, get: function () { return classes_2.LambdaFunction; } });
Object.defineProperty(exports, "SimpleContext", { enumerable: true, get: function () { return classes_2.SimpleContext; } });
Object.defineProperty(exports, "FieldAccess", { enumerable: true, get: function () { return classes_2.FieldAccess; } });
Object.defineProperty(exports, "FunctionCall", { enumerable: true, get: function () { return classes_2.FunctionCall; } });
Object.defineProperty(exports, "Variable", { enumerable: true, get: function () { return classes_2.Variable; } });
Object.defineProperty(exports, "Value", { enumerable: true, get: function () { return classes_2.Value; } });
Object.defineProperty(exports, "NumberValue", { enumerable: true, get: function () { return classes_2.NumberValue; } });
Object.defineProperty(exports, "BooleanValue", { enumerable: true, get: function () { return classes_2.BooleanValue; } });
Object.defineProperty(exports, "StringValue", { enumerable: true, get: function () { return classes_2.StringValue; } });
Object.defineProperty(exports, "DateValue", { enumerable: true, get: function () { return classes_2.DateValue; } });
Object.defineProperty(exports, "variableReplacer", { enumerable: true, get: function () { return classes_2.variableReplacer; } });
/** Shortcut to Expression.Parse */
function parse(str) {
    return classes_1.Expression.Parse(str);
}
exports.parse = parse;
/** Shortcut to TextExpression.Parse */
function parseTextExpression(str) {
    return classes_1.TextExpression.Parse(str);
}
exports.parseTextExpression = parseTextExpression;
var helpers_1 = require("./helpers");
Object.defineProperty(exports, "variable", { enumerable: true, get: function () { return helpers_1.variable; } });
Object.defineProperty(exports, "functionCall", { enumerable: true, get: function () { return helpers_1.functionCall; } });
Object.defineProperty(exports, "lambda", { enumerable: true, get: function () { return helpers_1.lambda; } });
Object.defineProperty(exports, "fields", { enumerable: true, get: function () { return helpers_1.fields; } });
Object.defineProperty(exports, "add", { enumerable: true, get: function () { return helpers_1.add; } });
Object.defineProperty(exports, "sub", { enumerable: true, get: function () { return helpers_1.sub; } });
Object.defineProperty(exports, "mul", { enumerable: true, get: function () { return helpers_1.mul; } });
Object.defineProperty(exports, "div", { enumerable: true, get: function () { return helpers_1.div; } });
Object.defineProperty(exports, "number", { enumerable: true, get: function () { return helpers_1.number; } });
Object.defineProperty(exports, "string", { enumerable: true, get: function () { return helpers_1.string; } });
Object.defineProperty(exports, "date", { enumerable: true, get: function () { return helpers_1.date; } });
Object.defineProperty(exports, "boolean", { enumerable: true, get: function () { return helpers_1.boolean; } });
Object.defineProperty(exports, "ExpressionCache", { enumerable: true, get: function () { return helpers_1.ExpressionCache; } });
Object.defineProperty(exports, "getDefaultAggregationFunction", { enumerable: true, get: function () { return helpers_1.getDefaultAggregationFunction; } });
Object.defineProperty(exports, "getCompatibleAggregationFunctionsByDataType", { enumerable: true, get: function () { return helpers_1.getCompatibleAggregationFunctionsByDataType; } });
Object.defineProperty(exports, "getCompatibleAggregationFunctionsByDataKind", { enumerable: true, get: function () { return helpers_1.getCompatibleAggregationFunctionsByDataKind; } });
Object.defineProperty(exports, "aggregationFunctions", { enumerable: true, get: function () { return helpers_1.aggregationFunctions; } });
Object.defineProperty(exports, "verifyUserExpression", { enumerable: true, get: function () { return helpers_1.verifyUserExpression; } });
//# sourceMappingURL=index.js.map