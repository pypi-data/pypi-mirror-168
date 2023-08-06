"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DatasetLoader = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var dataset_1 = require("./dataset");
var dsv_parser_1 = require("./dsv_parser");
var DatasetLoader = /** @class */ (function () {
    function DatasetLoader() {
    }
    DatasetLoader.prototype.loadTextData = function (url) {
        return fetch(url).then(function (resp) { return resp.text(); });
    };
    DatasetLoader.prototype.loadDSVFromURL = function (url, localeFileFormat) {
        return this.loadTextData(url).then(function (data) {
            return dsv_parser_1.parseDataset(url, data, localeFileFormat);
        });
    };
    DatasetLoader.prototype.loadDSVFromContents = function (filename, contents, localeFileFormat) {
        return dsv_parser_1.parseDataset(filename, contents, localeFileFormat);
    };
    DatasetLoader.prototype.loadTableFromSourceSpecification = function (spec) {
        return __awaiter(this, void 0, void 0, function () {
            var tableContent, table, table;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!spec.url) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.loadTextData(spec.url)];
                    case 1:
                        tableContent = _a.sent();
                        if (spec.url.toLowerCase().endsWith(".tsv")) {
                            spec.localeFileFormat.delimiter = "\t";
                        }
                        table = dsv_parser_1.parseDataset(spec.url.split("/").pop(), tableContent, spec.localeFileFormat);
                        if (spec.name) {
                            table.name = spec.name;
                        }
                        return [2 /*return*/, table];
                    case 2:
                        if (spec.content) {
                            table = dsv_parser_1.parseDataset(spec.name, spec.content, spec.localeFileFormat);
                            table.name = spec.name;
                            return [2 /*return*/, table];
                        }
                        else {
                            throw new Error("invalid table specification, url or content must be specified");
                        }
                        _a.label = 3;
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    DatasetLoader.prototype.loadDatasetFromSourceSpecification = function (spec) {
        return __awaiter(this, void 0, void 0, function () {
            var tables, dataset;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, Promise.all(spec.tables.map(function (table) { return _this.loadTableFromSourceSpecification(table); }))];
                    case 1:
                        tables = _a.sent();
                        tables[0].type = dataset_1.TableType.Main;
                        if (tables[1]) {
                            tables[1].type = dataset_1.TableType.Links;
                        }
                        dataset = { name: spec.name, tables: tables };
                        if (!spec.name && tables.length > 0) {
                            dataset.name = tables[0].name;
                        }
                        return [2 /*return*/, dataset];
                }
            });
        });
    };
    return DatasetLoader;
}());
exports.DatasetLoader = DatasetLoader;
//# sourceMappingURL=loader.js.map