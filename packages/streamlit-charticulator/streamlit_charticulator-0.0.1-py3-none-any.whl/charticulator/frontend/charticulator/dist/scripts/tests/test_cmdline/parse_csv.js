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
var e_1, _a;
Object.defineProperty(exports, "__esModule", { value: true });
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var fs = require("fs");
var Dataset = require("../../core/dataset");
var args = process.argv.slice(2);
if (args.length == 0) {
    console.log("Charticulator Commandline Test: parse_csv");
    console.log("This utility parses a CSV file and print out the result");
    console.log("Usage: node path/to/parse_csv.js csv1.csv csv2.csv ...");
    process.exit(0);
}
try {
    for (var args_1 = __values(args), args_1_1 = args_1.next(); !args_1_1.done; args_1_1 = args_1.next()) {
        var path = args_1_1.value;
        console.log("================================================================================");
        console.log("FILE: " + path);
        var contents = fs.readFileSync(path, "utf-8");
        var loader = new Dataset.DatasetLoader();
        var result = loader.loadDSVFromContents(path, contents, {
            delimiter: ", ",
            numberFormat: {
                remove: ",",
                decimal: ".",
            },
            currency: '["$",""]',
            group: "[3]",
            utcTimeZone: true,
        });
        console.log(JSON.stringify(result.columns, null, 2));
        console.log(JSON.stringify(result.rows.slice(0, 2), null, 2));
    }
}
catch (e_1_1) { e_1 = { error: e_1_1 }; }
finally {
    try {
        if (args_1_1 && !args_1_1.done && (_a = args_1.return)) _a.call(args_1);
    }
    finally { if (e_1) throw e_1.error; }
}
//# sourceMappingURL=parse_csv.js.map