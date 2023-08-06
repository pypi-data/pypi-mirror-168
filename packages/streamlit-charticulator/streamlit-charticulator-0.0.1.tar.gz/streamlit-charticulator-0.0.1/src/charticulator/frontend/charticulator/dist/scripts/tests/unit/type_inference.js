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
Object.defineProperty(exports, "__esModule", { value: true });
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var chai_1 = require("chai");
var data_types_1 = require("../../core/dataset/data_types");
var dataset_1 = require("../../core/dataset");
var localeNumberFormat = { remove: ",", decimal: "." };
describe("Data Type Inference", function () {
    it("inferColumnType", function () {
        var e_1, _a;
        var cases = [
            [["1", "3", "4.5", "23"], dataset_1.DataType.Number],
            [["1990-01-13", "2012-12-30", "12:34:56", "11:05am"], dataset_1.DataType.Date],
            [["true", "true", "false", "yes", "no"], dataset_1.DataType.Boolean],
            [["Hello", "World", "Charticulator"], dataset_1.DataType.String],
            [["2010", "2011", "2013", "2012"], dataset_1.DataType.Number],
            [["Jan", "Feb", "Mar", "Nov"], dataset_1.DataType.String],
        ];
        try {
            for (var cases_1 = __values(cases), cases_1_1 = cases_1.next(); !cases_1_1.done; cases_1_1 = cases_1.next()) {
                var _b = __read(cases_1_1.value, 2), values = _b[0], type = _b[1];
                var inferredType = data_types_1.inferColumnType(values, localeNumberFormat);
                chai_1.expect(inferredType).to.equals(type, values.join(", "));
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (cases_1_1 && !cases_1_1.done && (_a = cases_1.return)) _a.call(cases_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
    });
    it("inferAndConvertColumn", function () {
        var e_2, _a, e_3, _b;
        var cases = [
            [
                ["1", "3", "4.5", "23", null],
                {
                    type: dataset_1.DataType.Number,
                    values: [1, 3, 4.5, 23, null],
                    metadata: { kind: "numerical" },
                },
            ],
            [
                ["1990-01-13", "2012-12-30", "12:34:56", "11:05am"],
                { type: dataset_1.DataType.Date, metadata: { kind: "temporal" } },
            ],
            [
                ["true", "true", "false", "yes", "no"],
                { type: dataset_1.DataType.Boolean, metadata: { kind: "categorical" } },
            ],
            [
                ["Hello", "World", "Charticulator"],
                { type: dataset_1.DataType.String, metadata: { kind: "categorical" } },
            ],
            [
                ["2010", "2011", "2013", "2012"],
                {
                    type: dataset_1.DataType.String,
                    metadata: {
                        unit: "__year",
                        orderMode: "alphabetically",
                        kind: "ordinal",
                    },
                },
            ],
            [
                ["Jan", "Feb", "MAR", "november", "sept."],
                {
                    type: dataset_1.DataType.String,
                    values: ["Jan", "Feb", "Mar", "Nov", "Sep"],
                    metadata: {
                        kind: "ordinal",
                        order: "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(","),
                        unit: "__month",
                    },
                },
            ],
        ];
        try {
            for (var cases_2 = __values(cases), cases_2_1 = cases_2.next(); !cases_2_1.done; cases_2_1 = cases_2.next()) {
                var _c = __read(cases_2_1.value, 2), values = _c[0], expectedResult = _c[1];
                var r = data_types_1.inferAndConvertColumn(values, {
                    delimiter: ", ",
                    numberFormat: localeNumberFormat,
                    currency: '["$",""]',
                    group: "[3]",
                    utcTimeZone: true,
                });
                if (expectedResult.type) {
                    chai_1.expect(r.type).to.equals(expectedResult.type);
                }
                if (expectedResult.metadata) {
                    try {
                        for (var _d = (e_3 = void 0, __values(Object.keys(expectedResult.metadata))), _e = _d.next(); !_e.done; _e = _d.next()) {
                            var k = _e.value;
                            chai_1.expect(r.metadata[k]).to.deep.equals(expectedResult.metadata[k]);
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (_e && !_e.done && (_b = _d.return)) _b.call(_d);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (cases_2_1 && !cases_2_1.done && (_a = cases_2.return)) _a.call(cases_2);
            }
            finally { if (e_2) throw e_2.error; }
        }
    });
});
//# sourceMappingURL=type_inference.js.map