"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.ensureColumnsHaveExamples = void 0;
var dataset_1 = require("./dataset");
var exampleCount = 3;
var delim = ",";
function ensureColumnsHaveExamples(table) {
    table.columns.forEach(function (c) {
        if (!c.metadata.examples) {
            var examples = [];
            if (c.type === dataset_1.DataType.Boolean) {
                examples = ["true", "false"];
            }
            else {
                var distinct = getDistinctValues(table, c);
                if (c.metadata.kind === dataset_1.DataKind.Ordinal) {
                    distinct.sort();
                }
                examples = distinct.slice(0, exampleCount);
            }
            examples = examples.map(function (e) {
                if (e.indexOf(delim) >= 0) {
                    return JSON.stringify(e);
                }
                else {
                    return e;
                }
            });
            c.metadata.examples = examples.join(delim + " ");
        }
    });
}
exports.ensureColumnsHaveExamples = ensureColumnsHaveExamples;
function getDistinctValues(t, c) {
    var o = {};
    t.rows.forEach(function (r) {
        var valueKey = r[c.name].toString();
        o[valueKey] = null;
    });
    return Object.keys(o);
}
//# sourceMappingURL=examples.js.map