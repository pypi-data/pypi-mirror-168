"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
exports.DataFieldSelector = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../core");
var components_1 = require("../../components");
var R = require("../../resources");
var utils_1 = require("../../utils");
var common_1 = require("./common");
var controls_1 = require("../panels/widgets/controls");
var DataFieldSelector = /** @class */ (function (_super) {
    __extends(DataFieldSelector, _super);
    function DataFieldSelector(props) {
        var _this = _super.call(this, props) || this;
        _this.state = _this.getDefaultState(props);
        return _this;
    }
    DataFieldSelector.prototype.getDefaultState = function (props) {
        var e_1, _a;
        var expression = this.props.defaultValue
            ? this.props.defaultValue.expression
            : null;
        var expressionAggregation = null;
        if (props.useAggregation) {
            if (expression != null) {
                var parsed = core_1.Expression.parse(expression);
                if (parsed instanceof core_1.Expression.FunctionCall) {
                    expression = parsed.args[0].toString();
                    expressionAggregation = parsed.name;
                }
            }
        }
        if (props.defaultValue) {
            try {
                for (var _b = __values(this.getAllFields()), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var f = _c.value;
                    if (props.defaultValue.table != null &&
                        f.table != props.defaultValue.table) {
                        continue;
                    }
                    if (expression != null) {
                        if (f.expression == expression) {
                            return {
                                currentSelection: f,
                                currentSelectionAggregation: expressionAggregation,
                                currentSelections: [f],
                                currentSelectionsAggregations: [expressionAggregation],
                            };
                        }
                    }
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
        return {
            currentSelection: null,
            currentSelectionAggregation: null,
            currentSelections: [],
            currentSelectionsAggregations: [],
        };
    };
    Object.defineProperty(DataFieldSelector.prototype, "value", {
        get: function () {
            if (this.props.multiSelect) {
                return this.state.currentSelections;
            }
            else {
                return this.state.currentSelection;
            }
        },
        enumerable: false,
        configurable: true
    });
    DataFieldSelector.prototype.getAllFields = function () {
        var e_2, _a, e_3, _b;
        var fields = this.getFields();
        var r = [];
        try {
            for (var fields_1 = __values(fields), fields_1_1 = fields_1.next(); !fields_1_1.done; fields_1_1 = fields_1.next()) {
                var item = fields_1_1.value;
                r.push(item);
                if (item.derived) {
                    try {
                        for (var _c = (e_3 = void 0, __values(item.derived)), _d = _c.next(); !_d.done; _d = _c.next()) {
                            var ditem = _d.value;
                            r.push(ditem);
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (fields_1_1 && !fields_1_1.done && (_a = fields_1.return)) _a.call(fields_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return r;
    };
    DataFieldSelector.prototype.getFields = function () {
        var _this = this;
        var store = this.props.datasetStore;
        var table = store
            .getTables()
            .filter(function (table) { return table.name == _this.props.table || _this.props.table == null; })[0];
        var columns = table.columns;
        var columnFilters = [];
        columnFilters.push(function (x) { return !x.metadata.isRaw; });
        if (this.props.table) {
            columnFilters.push(function (x) { return x.table == _this.props.table; });
        }
        if (this.props.kinds) {
            columnFilters.push(function (x) {
                return x.metadata != null &&
                    common_1.isKindAcceptable(x.metadata.kind, _this.props.kinds);
            });
        }
        if (this.props.types) {
            columnFilters.push(function (x) { return x.metadata != null && _this.props.types.indexOf(x.type) >= 0; });
        }
        var columnFilter = function (x) {
            var e_4, _a;
            try {
                for (var columnFilters_1 = __values(columnFilters), columnFilters_1_1 = columnFilters_1.next(); !columnFilters_1_1.done; columnFilters_1_1 = columnFilters_1.next()) {
                    var f = columnFilters_1_1.value;
                    if (!f(x)) {
                        return false;
                    }
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (columnFilters_1_1 && !columnFilters_1_1.done && (_a = columnFilters_1.return)) _a.call(columnFilters_1);
                }
                finally { if (e_4) throw e_4.error; }
            }
            return true;
        };
        var candidates = columns.map(function (c) {
            var e_5, _a;
            var r = {
                selectable: true,
                table: table.name,
                columnName: c.name,
                expression: core_1.Expression.variable(c.name).toString(),
                rawExpression: core_1.Expression.variable(c.metadata.rawColumnName || c.name).toString(),
                type: c.type,
                displayName: c.name,
                metadata: c.metadata,
                derived: [],
            };
            // Compute derived columns.
            var derivedColumns = common_1.type2DerivedColumns[r.type];
            if (derivedColumns) {
                try {
                    for (var derivedColumns_1 = __values(derivedColumns), derivedColumns_1_1 = derivedColumns_1.next(); !derivedColumns_1_1.done; derivedColumns_1_1 = derivedColumns_1.next()) {
                        var item = derivedColumns_1_1.value;
                        var ditem = {
                            table: table.name,
                            columnName: null,
                            expression: core_1.Expression.functionCall(item.function, core_1.Expression.parse(r.expression)).toString(),
                            rawExpression: core_1.Expression.functionCall(item.function, core_1.Expression.parse(r.rawExpression)).toString(),
                            type: item.type,
                            metadata: item.metadata,
                            displayName: item.name,
                            selectable: true,
                        };
                        if (columnFilter(ditem)) {
                            r.derived.push(ditem);
                        }
                    }
                }
                catch (e_5_1) { e_5 = { error: e_5_1 }; }
                finally {
                    try {
                        if (derivedColumns_1_1 && !derivedColumns_1_1.done && (_a = derivedColumns_1.return)) _a.call(derivedColumns_1);
                    }
                    finally { if (e_5) throw e_5.error; }
                }
            }
            r.selectable = columnFilter(r);
            return r;
        });
        // Make sure we only show good ones
        candidates = candidates.filter(function (x) { return (x.derived.length > 0 || x.selectable) && !x.metadata.isRaw; });
        return candidates;
    };
    DataFieldSelector.prototype.isValueEqual = function (v1, v2) {
        if (v1 == v2) {
            return true;
        }
        if (v1 == null || v2 == null) {
            return false;
        }
        return v1.expression == v2.expression && v1.table == v2.table;
    };
    DataFieldSelector.prototype.isValueExists = function (v1, v2) {
        if (v2.find(function (v) { return v == v1 || (v1.expression == v.expression && v1.table == v.table); })) {
            return true;
        }
        if (v1 == null || v2.length == 0) {
            return false;
        }
        return false;
    };
    DataFieldSelector.prototype.selectItem = function (item, aggregation) {
        var _this = this;
        var _a;
        if (aggregation === void 0) { aggregation = null; }
        if (item == null) {
            if (this.props.onChange) {
                this.props.onChange(null);
            }
        }
        else {
            if (this.props.useAggregation) {
                if (aggregation == null) {
                    aggregation = core_1.Expression.getDefaultAggregationFunction(item.type, (_a = item.metadata) === null || _a === void 0 ? void 0 : _a.kind);
                }
            }
            if (this.props.multiSelect) {
                this.setState(function (current) {
                    var found = current.currentSelections.find(function (i) { return i.expression === item.expression; });
                    if (found) {
                        return __assign(__assign({}, current), { currentSelections: current.currentSelections.filter(function (i) { return i.expression !== item.expression; }), currentSelectionsAggregations: current.currentSelectionsAggregations.filter(function (a) { return a !== aggregation; }) });
                    }
                    else {
                        return __assign(__assign({}, current), { currentSelections: __spread(current.currentSelections, [item]), currentSelectionsAggregations: __spread(current.currentSelectionsAggregations, [
                                aggregation,
                            ]) });
                    }
                });
            }
            else {
                this.setState({
                    currentSelection: item,
                    currentSelectionAggregation: aggregation,
                });
            }
            if (this.props.onChange) {
                if (this.props.multiSelect) {
                    var rlist = __spread(this.state.currentSelections, [item]).map(function (item) {
                        var r = {
                            table: item.table,
                            expression: item.expression,
                            rawExpression: item.rawExpression,
                            columnName: item.columnName,
                            type: item.type,
                            metadata: item.metadata,
                        };
                        if (_this.props.useAggregation) {
                            r.expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.expression)).toString();
                            r.rawExpression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.rawExpression)).toString();
                        }
                        return r;
                    });
                    this.props.onChangeSelectionList(rlist);
                }
                else {
                    var r = {
                        table: item.table,
                        expression: item.expression,
                        rawExpression: item.rawExpression,
                        columnName: item.columnName,
                        type: item.type,
                        metadata: item.metadata,
                    };
                    if (this.props.useAggregation) {
                        r.expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.expression)).toString();
                        r.rawExpression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.rawExpression)).toString();
                    }
                    this.props.onChange(r);
                }
            }
        }
    };
    DataFieldSelector.prototype.renderCandidate = function (item) {
        var _this = this;
        var elDerived;
        var onClick = function (item) {
            if (item.selectable) {
                _this.selectItem(item, _this.isValueEqual(_this.state.currentSelection, item)
                    ? _this.state.currentSelectionAggregation
                    : null);
            }
        };
        return (React.createElement("div", { className: "el-column-item", key: item.table + item.expression },
            React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-field-item", [
                    "is-active",
                    this.props.multiSelect
                        ? this.isValueExists(item, this.state.currentSelections)
                        : this.isValueEqual(this.state.currentSelection, item),
                ], ["is-selectable", item.selectable]), onClick: function () { return onClick(item); }, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        onClick(item);
                    }
                } },
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(common_1.kind2Icon[item.metadata.kind]) }),
                React.createElement("span", { className: "el-text" }, item.displayName),
                this.props.useAggregation &&
                    this.isValueEqual(this.state.currentSelection, item) ? (React.createElement(controls_1.Select, { value: this.state.currentSelectionAggregation, options: core_1.Expression.getCompatibleAggregationFunctionsByDataType(item.type).map(function (x) { return x.name; }), labels: core_1.Expression.getCompatibleAggregationFunctionsByDataType(item.type).map(function (x) { return x.displayName; }), showText: true, onChange: function (newValue) {
                        _this.selectItem(item, newValue);
                    } })) : null,
                item.derived && item.derived.length > 0 ? (React.createElement(controls_1.Button, { icon: "general/more-vertical", onClick: function () {
                        if (elDerived) {
                            if (elDerived.style.display == "none") {
                                elDerived.style.display = "block";
                            }
                            else {
                                elDerived.style.display = "none";
                            }
                        }
                    } })) : null),
            item.derived && item.derived.length > 0 ? (React.createElement("div", { className: "el-derived-fields", style: { display: "none" }, ref: function (e) { return (elDerived = e); } }, item.derived.map(function (df) { return _this.renderCandidate(df); }))) : null));
    };
    //Update desing
    DataFieldSelector.prototype.render = function () {
        var _this = this;
        var fields = this.getFields();
        return (React.createElement("div", { className: "charticulator__data-field-selector" },
            this.props.nullDescription ? (React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-field-item", "is-null", "is-selectable", [
                    "is-active",
                    !this.props.nullNotHighlightable &&
                        this.state.currentSelection == null,
                ]), onClick: function () { return _this.selectItem(null); }, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        _this.selectItem(null);
                    }
                } }, this.props.nullDescription)) : null,
            fields.length == 0 && !this.props.nullDescription ? (React.createElement("div", { className: "el-field-item is-null" }, "(no suitable column)")) : null,
            fields.map(function (f) { return _this.renderCandidate(f); })));
    };
    return DataFieldSelector;
}(React.Component));
exports.DataFieldSelector = DataFieldSelector;
//# sourceMappingURL=fluent_ui_data_field_selector.js.map