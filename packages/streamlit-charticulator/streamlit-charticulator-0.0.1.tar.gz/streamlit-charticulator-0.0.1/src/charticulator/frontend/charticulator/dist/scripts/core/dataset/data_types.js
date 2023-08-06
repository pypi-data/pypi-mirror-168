"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.isBase64Image = exports.convertColumnType = exports.inferAndConvertColumn = exports.getDistinctValues = exports.convertColumn = exports.inferColumnType = exports.dataTypes = void 0;
var types_1 = require("../specification/types");
var dataset_1 = require("./dataset");
var datetime_1 = require("./datetime");
function localeNumber(x, localeNumberFormat) {
    var reRemove = new RegExp("\\" + localeNumberFormat.remove, "g");
    x = x.replace(reRemove, "");
    if (localeNumberFormat.decimal !== ".") {
        var reReplace = new RegExp("\\" + localeNumberFormat.decimal, "g");
        x = x.replace(reReplace, ".");
    }
    return +x;
}
exports.dataTypes = {
    boolean: {
        test: function (x) {
            var lx = x.toLowerCase();
            return lx === "true" || lx === "false" || lx == "yes" || lx == "no";
        },
        convert: function (x) {
            var lx = x.toLowerCase();
            if (lx == "true" || lx == "yes") {
                return true;
            }
            else if (lx == "false" || lx == "no") {
                return false;
            }
            else {
                return null;
            }
        },
    },
    number: {
        test: function (x, localeNumberFormat) {
            if (x === "null") {
                return true;
            }
            var value = localeNumber(x, localeNumberFormat);
            return !isNaN(value);
        },
        convert: function (x, localeNumberFormat) {
            var value = localeNumber(x, localeNumberFormat);
            return isNaN(value) ? null : value;
        },
    },
    date: {
        test: function (x) { return datetime_1.parseDate(x) != null; },
        convert: function (x, timeZone) { return datetime_1.parseDate(x, timeZone); },
    },
    string: {
        // eslint-disable-next-line
        test: function (x) { return true; },
        convert: function (x) { return x.toString(); },
    },
    image: {
        test: function (x) { return isBase64Image(x); },
        convert: function (x) { return x.toString(); },
    },
};
/** Infer column type from a set of strings (not null) */
function inferColumnType(values, localeNumberFormat) {
    var candidates = [
        dataset_1.DataType.Image,
        dataset_1.DataType.Boolean,
        dataset_1.DataType.Number,
        dataset_1.DataType.Date,
    ];
    for (var i = 0; i < values.length; i++) {
        var v = values[i];
        v = v.trim();
        if (v == "") {
            continue;
        }
        // test for remaining candidates
        for (var j = 0; j < candidates.length; j++) {
            if (!exports.dataTypes[candidates[j]].test(v, localeNumberFormat)) {
                // console.log(candidates[j], "fail at", v);
                candidates.splice(j, 1);
                j -= 1;
            }
        }
        // if no types left, return "string"
        if (candidates.length == 0) {
            return dataset_1.DataType.String;
        }
    }
    return candidates[0];
}
exports.inferColumnType = inferColumnType;
/** Convert strings to value type, null & non-convertibles are set as null */
function convertColumn(type, values, localeNumberFormat, timeZone) {
    if (localeNumberFormat === void 0) { localeNumberFormat = {
        remove: ",",
        decimal: ".",
    }; }
    if (timeZone === void 0) { timeZone = 0; }
    var converter = exports.dataTypes[type].convert;
    return values.map(function (v) {
        if (type === dataset_1.DataType.Date) {
            return v != null ? converter(v, timeZone) : null;
        }
        else {
            return v != null ? converter(v, localeNumberFormat) : null;
        }
    });
}
exports.convertColumn = convertColumn;
/** Get distinct values from a non-null array of basic types */
function getDistinctValues(values) {
    var e_1, _a;
    var seen = new Set();
    try {
        for (var values_1 = __values(values), values_1_1 = values_1.next(); !values_1_1.done; values_1_1 = values_1.next()) {
            var v = values_1_1.value;
            seen.add(v);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (values_1_1 && !values_1_1.done && (_a = values_1.return)) _a.call(values_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return Array.from(seen);
}
exports.getDistinctValues = getDistinctValues;
/** Infer column metadata and update type if necessary */
// eslint-disable-next-line
function inferAndConvertColumn(values, localeFileFormat, hints) {
    var inferredType = inferColumnType(values.filter(function (x) { return x != null; }), localeFileFormat.numberFormat);
    var convertedValues = convertColumn(inferredType, values, localeFileFormat.numberFormat, localeFileFormat.utcTimeZone ? 0 : new Date().getTimezoneOffset() // time zone offset in minutes
    );
    if (hints == null) {
        hints = {};
    }
    switch (inferredType) {
        case dataset_1.DataType.Image: {
            var metadata = {
                kind: dataset_1.DataKind.Categorical,
                unit: hints.unit,
            };
            metadata.orderMode = types_1.OrderMode.order;
            metadata.kind = dataset_1.DataKind.Categorical;
            return {
                type: dataset_1.DataType.Image,
                values: convertedValues,
                metadata: metadata,
            };
            break;
        }
        case dataset_1.DataType.Number: {
            var validValues = convertedValues.filter(function (x) { return x != null; });
            var minValue = Math.min.apply(Math, __spread(validValues));
            var maxValue = Math.max.apply(Math, __spread(validValues));
            if (validValues.every(function (x) { return Math.round(x) == x; })) {
                // All integers
                if (minValue >= 1900 && maxValue <= 2100) {
                    // Special case: Year
                    return {
                        type: dataset_1.DataType.String,
                        values: convertedValues.map(function (x) { return x.toString(); }),
                        metadata: {
                            unit: "__year",
                            kind: dataset_1.DataKind.Ordinal,
                            orderMode: types_1.OrderMode.alphabetically,
                        },
                    };
                }
            }
            // let valuesFixed = values
            //   .map(d => +d)
            //   .filter(d => !isNaN(d))
            //   .map(d => d.toFixed(10));
            // valuesFixed = valuesFixed.map(d => {
            //   const m = d.match(/\.([0-9]{10})$/);
            //   if (m) {
            //     return m[1];
            //   } else {
            //     return "0000000000";
            //   }
            // });
            // let k: number;
            // for (k = 10 - 1; k >= 0; k--) {
            //   if (valuesFixed.every(v => v[k] == "0")) {
            //     continue;
            //   } else {
            //     break;
            //   }
            // }
            // const format = `.${k + 1}f`;
            return {
                type: dataset_1.DataType.Number,
                values: convertedValues,
                metadata: {
                    kind: dataset_1.DataKind.Numerical,
                    unit: hints.unit,
                },
            };
        }
        case dataset_1.DataType.Boolean: {
            return {
                type: dataset_1.DataType.Boolean,
                values: convertedValues,
                rawValues: values.map(function (v) { return v && v.toLowerCase(); }),
                metadata: {
                    kind: dataset_1.DataKind.Categorical,
                },
            };
        }
        case dataset_1.DataType.Date: {
            return {
                type: dataset_1.DataType.Date,
                values: convertedValues,
                rawValues: values,
                metadata: {
                    kind: dataset_1.DataKind.Temporal,
                    unit: hints.unit,
                    format: datetime_1.getDateFormat(values[0]),
                },
            };
        }
        case dataset_1.DataType.String: {
            var metadata = {
                kind: dataset_1.DataKind.Categorical,
                unit: hints.unit,
            };
            var validValues = convertedValues.filter(function (x) { return x != null; });
            if (validValues.every(function (x) { return datetime_1.testAndNormalizeMonthName(x) != null; })) {
                // Special case: month names
                // Return as ordinal column with month ordering, use normalized month names
                return {
                    type: dataset_1.DataType.String,
                    values: convertedValues.map(function (x) {
                        return x != null ? datetime_1.testAndNormalizeMonthName(x) : null;
                    }),
                    metadata: {
                        kind: dataset_1.DataKind.Ordinal,
                        order: datetime_1.monthNames,
                        unit: "__month",
                    },
                };
            }
            if (hints.order) {
                metadata.order = hints.order.split(",");
                metadata.kind = dataset_1.DataKind.Ordinal;
            }
            else {
                metadata.orderMode = types_1.OrderMode.alphabetically;
                metadata.kind = dataset_1.DataKind.Categorical;
            }
            return {
                type: dataset_1.DataType.String,
                values: convertedValues,
                metadata: metadata,
            };
        }
    }
    // We shouldn't get here.
    console.warn("inferAndConvertColumn: inferredType is unexpected");
    return {
        type: inferredType,
        values: convertedValues,
        metadata: { kind: dataset_1.DataKind.Categorical },
    };
}
exports.inferAndConvertColumn = inferAndConvertColumn;
function convertColumnType(values, type) {
    switch (type) {
        case dataset_1.DataType.Boolean: {
            return values.map(function (v) {
                if (v == null) {
                    return null;
                }
                if (typeof v == "boolean") {
                    return v;
                }
                if (typeof v == "number") {
                    return v > 0;
                }
                var l = v.toString().toLowerCase();
                return l == "yes" || l == "true";
            });
        }
        case dataset_1.DataType.Number: {
            return values.map(function (v) {
                // Check for null as well, since +null == 0
                if (v == null) {
                    return null;
                }
                var n = +v;
                return isNaN(n) ? null : n;
            });
        }
        case dataset_1.DataType.String: {
            return values.map(function (v) { return (v == null ? "" : v.toString()); });
        }
        case dataset_1.DataType.Date: {
            return values.map(function (v) {
                if (v == null) {
                    return null;
                }
                if (typeof v == "number") {
                    return v;
                }
                return datetime_1.parseDate(v.toString());
            });
        }
    }
}
exports.convertColumnType = convertColumnType;
function isBase64Image(string) {
    return (typeof string === "string" &&
        string.match(/data:image\/(ico|jpg|jpeg|png|webp|svg|gif|svg\+xml);base64,/) != null);
}
exports.isBase64Image = isBase64Image;
//# sourceMappingURL=data_types.js.map