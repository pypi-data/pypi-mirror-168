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
exports.DataflowManager = exports.DataflowTable = exports.DataflowTableGroupedContext = void 0;
/**
 * Expressions context providers.
 *
 * {@link DataflowTable} provides data context for charticulator's expressions, solver, plotsegments.
 *
 * {@link DataflowManager} is a proxy between dateset and other parts of charticualtor.
 *
 * @packageDocumentation
 * @preferred
 */
var Dataset = require("../../dataset");
var Expression = require("../../expression");
var DataflowTableGroupedContext = /** @class */ (function () {
    function DataflowTableGroupedContext(table, indices) {
        this.table = table;
        this.indices = indices;
    }
    DataflowTableGroupedContext.prototype.getTable = function () {
        return this.table;
    };
    DataflowTableGroupedContext.prototype.getVariable = function (name) {
        var _this = this;
        var _a;
        if (Object.prototype.hasOwnProperty.call((_a = this.table.rows[this.indices[0]]) !== null && _a !== void 0 ? _a : {}, name)) {
            return this.indices.map(function (i) { return _this.table.rows[i][name]; });
        }
        return this.table.getVariable(name);
    };
    return DataflowTableGroupedContext;
}());
exports.DataflowTableGroupedContext = DataflowTableGroupedContext;
var DataflowTable = /** @class */ (function () {
    function DataflowTable(parent, name, rows, columns, options) {
        this.parent = parent;
        this.name = name;
        this.rows = rows;
        this.columns = columns;
        this.options = options;
    }
    /** Implements Expression.Context */
    DataflowTable.prototype.getVariable = function (name) {
        if (name == "rows") {
            return this.rows;
        }
        if (name == "columns") {
            return this.columns;
        }
        return this.parent.getVariable(name);
    };
    /** Get a row with index */
    DataflowTable.prototype.getRow = function (index) {
        return this.rows[index];
    };
    /** Get a row context with index */
    DataflowTable.prototype.getRowContext = function (index) {
        return new Expression.ShadowContext(this, this.rows[index]);
    };
    DataflowTable.prototype.getGroupedContext = function (rowIndices) {
        return new DataflowTableGroupedContext(this, rowIndices);
    };
    return DataflowTable;
}());
exports.DataflowTable = DataflowTable;
var DataflowManager = /** @class */ (function () {
    function DataflowManager(dataset) {
        var e_1, _a;
        this.context = new Dataset.DatasetContext(dataset);
        this.cache = new Expression.ExpressionCache();
        this.tables = new Map();
        try {
            for (var _b = __values(dataset.tables), _c = _b.next(); !_c.done; _c = _b.next()) {
                var table = _c.value;
                var dfTable = new DataflowTable(this, table.name, table.rows, table.columns, {
                    displayName: table.displayName,
                });
                this.tables.set(table.name, dfTable);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    /** Get a table by name (either original table or derived table) */
    DataflowManager.prototype.getTable = function (name) {
        return this.tables.get(name);
    };
    /** Implements Expression.Context */
    DataflowManager.prototype.getVariable = function (name) {
        if (this.tables.has(name)) {
            return this.tables.get(name);
        }
    };
    return DataflowManager;
}());
exports.DataflowManager = DataflowManager;
//# sourceMappingURL=index.js.map