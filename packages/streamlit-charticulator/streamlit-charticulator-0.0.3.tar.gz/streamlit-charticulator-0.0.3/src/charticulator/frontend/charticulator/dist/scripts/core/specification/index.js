"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmphasisMethod = exports.MappingType = exports.AttributeType = exports.DataKind = exports.DataType = exports.Template = exports.Types = void 0;
var Template = require("./template");
exports.Template = Template;
var Types = require("./types");
exports.Types = Types;
/** Data type in memory */
var DataType;
(function (DataType) {
    /** String data type, stored as string */
    DataType["String"] = "string";
    /** Number data type, stored as number */
    DataType["Number"] = "number";
    /** Boolean data type, stored as boolean */
    DataType["Boolean"] = "boolean";
    /** Date data type, stored as unix timestamps (ms) */
    DataType["Date"] = "date";
    /** Image data as base64 string */
    DataType["Image"] = "image";
})(DataType = exports.DataType || (exports.DataType = {}));
/** Abstract data kind */
var DataKind;
(function (DataKind) {
    /** Ordinal data kind */
    DataKind["Ordinal"] = "ordinal";
    /** Categorical data kind */
    DataKind["Categorical"] = "categorical";
    /** Numerical data kind */
    DataKind["Numerical"] = "numerical";
    /** Temporal data kind */
    DataKind["Temporal"] = "temporal";
})(DataKind = exports.DataKind || (exports.DataKind = {}));
// ===========================================================================
// Attributes
// ===========================================================================
var AttributeType;
(function (AttributeType) {
    AttributeType["Number"] = "number";
    AttributeType["Enum"] = "enum";
    AttributeType["Text"] = "text";
    AttributeType["Boolean"] = "boolean";
    AttributeType["FontFamily"] = "font-family";
    AttributeType["Color"] = "color";
    AttributeType["Image"] = "image";
    AttributeType["Point"] = "point";
    AttributeType["Object"] = "object";
})(AttributeType = exports.AttributeType || (exports.AttributeType = {}));
var MappingType;
(function (MappingType) {
    MappingType["_element"] = "_element";
    MappingType["parent"] = "parent";
    MappingType["scale"] = "scale";
    MappingType["expressionScale"] = "expressionScale";
    MappingType["text"] = "text";
    MappingType["value"] = "value";
})(MappingType = exports.MappingType || (exports.MappingType = {}));
/**
 * Represents the type of method to use when emphasizing an element
 */
var EmphasisMethod;
(function (EmphasisMethod) {
    EmphasisMethod["Saturation"] = "saturation";
    EmphasisMethod["Outline"] = "outline";
})(EmphasisMethod = exports.EmphasisMethod || (exports.EmphasisMethod = {}));
//# sourceMappingURL=index.js.map