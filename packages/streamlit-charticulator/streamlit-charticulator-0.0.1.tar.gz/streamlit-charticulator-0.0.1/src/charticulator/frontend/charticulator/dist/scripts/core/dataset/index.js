"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !exports.hasOwnProperty(p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Charticulator uses [d3-dsv](https://github.com/d3/d3-dsv) package to load and parse csv data.
 *
 * The module contains methods to parse and convert data on importing into Charticulator.
 *
 * {@link "core/dataset/data_types"} contains methods for converting strings into correspond data types.
 *
 * {@link "core/dataset/dsv_parser"} wrapper to call methods from {@link "core/dataset/data_types"} for whole dataset. The main method of module is {@link parseDataset}
 *
 * {@link "core/dataset/datetime"} contains methods to parse dates.
 *
 * {@link "core/dataset/context"} provides proxy classes for data and expressions. Expressions module ({@link "core/expression/index"}) classes use data through context.
 *
 * {@link "core/dataset/dataset"} interfaces for describe dataset stuctures of charticulator as Table, Column, Dataset e.t.c.
 *
 * @packageDocumentation
 * @preferred
 */
__exportStar(require("./dataset"), exports);
var loader_1 = require("./loader");
Object.defineProperty(exports, "DatasetLoader", { enumerable: true, get: function () { return loader_1.DatasetLoader; } });
var context_1 = require("./context");
Object.defineProperty(exports, "DatasetContext", { enumerable: true, get: function () { return context_1.DatasetContext; } });
Object.defineProperty(exports, "TableContext", { enumerable: true, get: function () { return context_1.TableContext; } });
Object.defineProperty(exports, "RowContext", { enumerable: true, get: function () { return context_1.RowContext; } });
var data_types_1 = require("./data_types");
Object.defineProperty(exports, "convertColumnType", { enumerable: true, get: function () { return data_types_1.convertColumnType; } });
Object.defineProperty(exports, "inferColumnType", { enumerable: true, get: function () { return data_types_1.inferColumnType; } });
Object.defineProperty(exports, "inferAndConvertColumn", { enumerable: true, get: function () { return data_types_1.inferAndConvertColumn; } });
Object.defineProperty(exports, "dataTypes", { enumerable: true, get: function () { return data_types_1.dataTypes; } });
//# sourceMappingURL=index.js.map