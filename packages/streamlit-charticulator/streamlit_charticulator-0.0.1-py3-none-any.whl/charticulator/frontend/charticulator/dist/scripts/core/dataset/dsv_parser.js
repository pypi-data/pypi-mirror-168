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
exports.parseDataset = exports.parseHints = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var d3_dsv_1 = require("d3-dsv");
var data_types_1 = require("./data_types");
var dataset_1 = require("./dataset");
var common_1 = require("../common");
function parseHints(hints) {
    var e_1, _a;
    var items = hints.match(/ *\*(.*)/);
    if (items) {
        var entries = items[1]
            .trim()
            .split(";")
            .map(function (x) { return x.trim(); })
            .filter(function (x) { return x != ""; });
        var result = {};
        try {
            for (var entries_1 = __values(entries), entries_1_1 = entries_1.next(); !entries_1_1.done; entries_1_1 = entries_1.next()) {
                var entry = entries_1_1.value;
                var items_1 = entry.split(":").map(function (x) { return x.trim(); });
                if (items_1.length == 2) {
                    result[items_1[0]] = items_1[1];
                }
                else if (items_1.length == 1) {
                    result[items_1[0]] = "true";
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (entries_1_1 && !entries_1_1.done && (_a = entries_1.return)) _a.call(entries_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return result;
    }
    else {
        return {};
    }
}
exports.parseHints = parseHints;
/**
 * Parses data from file. Returns converted rows and list of colum names with types.
 * Calls {@link inferAndConvertColumn} method from {@link "core/dataset/data_types"} for convert types.
 * @param fileName input file name for parsing
 * @param content data of file
 * @param type type of file. *.csv - text with coma delimeter. *.tsv - tab separated text files
 */
function parseDataset(fileName, content, localeFileFormat) {
    var rows;
    var tableName = fileName.replace(/\W/g, "_");
    rows = d3_dsv_1.dsvFormat(localeFileFormat.delimiter).parseRows(content);
    // Remove empty rows if any
    rows = rows.filter(function (row) { return row.length > 0; });
    if (rows.length > 0) {
        var header_1 = rows[0];
        // eslint-disable-next-line
        // TODO fix it
        var columnHints = void 0;
        var data_1 = rows.slice(1);
        if (data_1.length > 0 && data_1[0].every(function (x) { return /^ *\*/.test(x); })) {
            columnHints = data_1[0].map(parseHints);
            data_1 = data_1.slice(1);
        }
        else {
            // eslint-disable-next-line
            columnHints = header_1.map(function () { return ({}); });
        }
        var columnValues_1 = header_1.map(function (name, index) {
            var values = data_1.map(function (row) { return row[index]; });
            return data_types_1.inferAndConvertColumn(values, localeFileFormat);
        });
        var additionalColumns_1 = [];
        columnValues_1.forEach(function (column, index) {
            if (column.rawValues) {
                var rawColumn = common_1.deepClone(column);
                rawColumn.metadata.isRaw = true;
                rawColumn.values = rawColumn.rawValues;
                delete rawColumn.rawValues;
                var rawColumnName = header_1[index] + dataset_1.rawColumnPostFix;
                column.metadata.rawColumnName = rawColumnName;
                delete column.rawValues;
                header_1.push(rawColumnName);
                additionalColumns_1.push(rawColumn);
            }
        });
        columnValues_1 = columnValues_1.concat(additionalColumns_1);
        var outRows = data_1.map(function (row, rindex) {
            var out = { _id: rindex.toString() };
            columnValues_1.forEach(function (column, cindex) {
                out[header_1[cindex]] = columnValues_1[cindex].values[rindex];
                if (columnValues_1[cindex].rawValues) {
                    out[header_1[cindex] + dataset_1.rawColumnPostFix] =
                        columnValues_1[cindex].rawValues[rindex];
                    if (!header_1.find(function (h) { return h === header_1[cindex] + dataset_1.rawColumnPostFix; })) {
                        header_1.push(header_1[cindex] + dataset_1.rawColumnPostFix);
                    }
                }
            });
            return out;
        });
        var columns = columnValues_1.map(function (x, i) { return ({
            name: header_1[i],
            displayName: header_1[i],
            type: x.type,
            metadata: x.metadata,
        }); });
        return {
            name: tableName,
            displayName: tableName,
            columns: columns,
            rows: outRows,
            type: null,
            localeNumberFormat: localeFileFormat.numberFormat,
        };
    }
    else {
        return null;
    }
}
exports.parseDataset = parseDataset;
//# sourceMappingURL=dsv_parser.js.map