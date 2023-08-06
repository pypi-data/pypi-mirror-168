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
exports.RowContext = exports.TableContext = exports.DatasetContext = void 0;
var DatasetContext = /** @class */ (function () {
    function DatasetContext(dataset) {
        var e_1, _a;
        this.dataset = dataset;
        this.fields = {};
        try {
            for (var _b = __values(dataset.tables), _c = _b.next(); !_c.done; _c = _b.next()) {
                var table = _c.value;
                this.fields[table.name] = table.rows;
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
    DatasetContext.prototype.getTableContext = function (table) {
        return new TableContext(this, table);
    };
    DatasetContext.prototype.getVariable = function (name) {
        return this.fields[name];
    };
    return DatasetContext;
}());
exports.DatasetContext = DatasetContext;
var TableContext = /** @class */ (function () {
    function TableContext(parent, table) {
        this.parent = parent;
        this.table = table;
        this.fields = {};
        this.fields.table = table.rows;
    }
    TableContext.prototype.getRowContext = function (row) {
        return new RowContext(this, row);
    };
    TableContext.prototype.getVariable = function (name) {
        var r = this.fields[name];
        if (r === undefined) {
            return this.parent.getVariable(name);
        }
    };
    return TableContext;
}());
exports.TableContext = TableContext;
var RowContext = /** @class */ (function () {
    function RowContext(parent, row) {
        this.parent = parent;
        this.row = row;
    }
    RowContext.prototype.getVariable = function (name) {
        var r = this.row[name];
        if (r === undefined) {
            return this.parent.getVariable(name);
        }
        else {
            return r;
        }
    };
    return RowContext;
}());
exports.RowContext = RowContext;
//# sourceMappingURL=context.js.map