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
Object.defineProperty(exports, "__esModule", { value: true });
exports.makeDefaultDataset = void 0;
var core_1 = require("../core");
var dataset_1 = require("../core/dataset");
var strings_1 = require("../strings");
function makeDefaultDataset() {
    var e_1, _a, e_2, _b;
    var rows = [];
    var months = strings_1.strings.dataset.months;
    var monthIndex = 0;
    try {
        for (var months_1 = __values(months), months_1_1 = months_1.next(); !months_1_1.done; months_1_1 = months_1.next()) {
            var month = months_1_1.value;
            var cityIndex = 0;
            try {
                for (var _c = (e_2 = void 0, __values(["City1", "City2", "City3"])), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var city = _d.value;
                    var value = 50 +
                        30 *
                            Math.sin(((monthIndex + 0.5) * Math.PI) / 12 + (cityIndex * Math.PI) / 2);
                    rows.push({
                        _id: "ID" + rows.length,
                        Month: month,
                        City: city,
                        Value: +value.toFixed(1),
                    });
                    cityIndex += 1;
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                }
                finally { if (e_2) throw e_2.error; }
            }
            monthIndex += 1;
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (months_1_1 && !months_1_1.done && (_a = months_1.return)) _a.call(months_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return {
        tables: [
            {
                name: "Temperature",
                displayName: strings_1.strings.defaultDataset.temperature,
                columns: [
                    {
                        name: "Month",
                        displayName: strings_1.strings.defaultDataset.month,
                        type: core_1.Dataset.DataType.String,
                        metadata: {
                            kind: core_1.Dataset.DataKind.Categorical,
                            order: months,
                        },
                    },
                    {
                        name: "City",
                        displayName: strings_1.strings.defaultDataset.city,
                        type: core_1.Dataset.DataType.String,
                        metadata: { kind: core_1.Dataset.DataKind.Categorical },
                    },
                    {
                        name: "Value",
                        displayName: strings_1.strings.defaultDataset.value,
                        type: core_1.Dataset.DataType.Number,
                        metadata: { kind: core_1.Dataset.DataKind.Numerical, format: ".1f" },
                    },
                ],
                rows: rows,
                type: dataset_1.TableType.Main,
            },
        ],
        name: "demo",
    };
}
exports.makeDefaultDataset = makeDefaultDataset;
//# sourceMappingURL=default_dataset.js.map