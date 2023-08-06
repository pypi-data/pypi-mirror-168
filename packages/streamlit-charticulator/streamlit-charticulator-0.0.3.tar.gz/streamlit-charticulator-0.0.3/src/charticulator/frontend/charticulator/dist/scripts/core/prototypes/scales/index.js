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
exports.registerClasses = exports.inferScaleType = exports.ScaleClass = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var scale_1 = require("./scale");
Object.defineProperty(exports, "ScaleClass", { enumerable: true, get: function () { return scale_1.ScaleClass; } });
var specification_1 = require("../../specification");
var object_1 = require("../object");
var categorical_1 = require("./categorical");
var linear_1 = require("./linear");
var inferScaleTypeRules = [
    {
        input: {
            type: [specification_1.DataType.Number, specification_1.DataType.Date],
            kind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
        },
        output: specification_1.AttributeType.Number,
        scale: "scale.linear<number,number>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.Number, specification_1.DataType.Date],
            kind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
        },
        output: specification_1.AttributeType.Color,
        scale: "scale.linear<number,color>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.Number, specification_1.DataType.Date],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
        },
        output: specification_1.AttributeType.Color,
        scale: "scale.categorical<string,color>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.Number, specification_1.DataType.Date],
            kind: [specification_1.DataKind.Numerical, specification_1.DataKind.Temporal],
        },
        output: specification_1.AttributeType.Boolean,
        scale: "scale.linear<number,boolean>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.String, specification_1.DataType.Boolean],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
        },
        output: specification_1.AttributeType.Color,
        scale: "scale.categorical<string,color>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.String, specification_1.DataType.Boolean],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
        },
        output: specification_1.AttributeType.Image,
        scale: "scale.categorical<string,image>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.Image, specification_1.DataType.Image],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Categorical],
        },
        output: specification_1.AttributeType.Image,
        scale: "scale.categorical<image,image>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.String, specification_1.DataType.Boolean],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
        },
        output: specification_1.AttributeType.Enum,
        scale: "scale.categorical<string,enum>",
        priority: 1,
    },
    {
        input: {
            type: [specification_1.DataType.String, specification_1.DataType.Boolean],
            kind: [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal],
        },
        output: specification_1.AttributeType.Boolean,
        scale: "scale.categorical<string,boolean>",
        priority: 1,
    },
    {
        input: { type: specification_1.DataType.String, kind: [specification_1.DataKind.Ordinal] },
        output: specification_1.AttributeType.Number,
        scale: "scale.categorical<string,number>",
        priority: 1,
    },
];
function match(test, input) {
    if (test instanceof Array) {
        return test.indexOf(input) >= 0;
    }
    else {
        return test == input;
    }
}
// Return the scale class by matching dataType and attrType
function inferScaleType(dataType, dataKind, attrType) {
    var e_1, _a;
    // Match scale inference rules, find the matched one with top priority.
    var candidate = null;
    try {
        for (var inferScaleTypeRules_1 = __values(inferScaleTypeRules), inferScaleTypeRules_1_1 = inferScaleTypeRules_1.next(); !inferScaleTypeRules_1_1.done; inferScaleTypeRules_1_1 = inferScaleTypeRules_1.next()) {
            var rule = inferScaleTypeRules_1_1.value;
            // Filter non-matches
            if (!match(rule.input.type, dataType)) {
                continue;
            }
            if (!match(rule.output, attrType)) {
                continue;
            }
            if (!match(rule.input.kind, dataKind)) {
                continue;
            }
            if (!candidate || candidate.priority < rule.priority) {
                candidate = rule;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (inferScaleTypeRules_1_1 && !inferScaleTypeRules_1_1.done && (_a = inferScaleTypeRules_1.return)) _a.call(inferScaleTypeRules_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    if (candidate) {
        return candidate.scale;
    }
    else {
        return null;
    }
}
exports.inferScaleType = inferScaleType;
function registerClasses() {
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleNumber);
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleColor);
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleBoolean);
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleEnum);
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleImage);
    object_1.ObjectClasses.Register(categorical_1.CategoricalScaleBase64Image);
    object_1.ObjectClasses.Register(linear_1.LinearScale);
    object_1.ObjectClasses.Register(linear_1.LinearColorScale);
    object_1.ObjectClasses.Register(linear_1.LinearBooleanScale);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map