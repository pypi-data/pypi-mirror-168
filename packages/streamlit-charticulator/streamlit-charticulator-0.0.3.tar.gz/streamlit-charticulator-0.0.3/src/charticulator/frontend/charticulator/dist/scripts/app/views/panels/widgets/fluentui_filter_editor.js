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
exports.FluentUIFilterEditor = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var react_1 = require("@fluentui/react");
var React = require("react");
var core_1 = require("../../../../core");
var strings_1 = require("../../../../strings");
var actions_1 = require("../../../actions");
var data_field_selector_1 = require("../../dataset/data_field_selector");
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var fluentui_input_expression_1 = require("./controls/fluentui_input_expression");
var FluentUIFilterEditor = /** @class */ (function (_super) {
    __extends(FluentUIFilterEditor, _super);
    function FluentUIFilterEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState(_this.props.value);
        return _this;
    }
    FluentUIFilterEditor.prototype.getDefaultState = function (value) {
        var filterType = "none";
        if (value) {
            if (value.expression) {
                filterType = "expression";
            }
            if (value.categories) {
                filterType = "categories";
            }
        }
        return {
            type: filterType,
            currentValue: value,
        };
    };
    FluentUIFilterEditor.prototype.emitUpdateFilter = function (newValue) {
        if (this.props.options.target.property) {
            this.props.manager.emitSetProperty(this.props.options.target.property, newValue);
        }
        if (this.props.options.target.plotSegment) {
            this.props.manager.store.dispatcher.dispatch(new actions_1.Actions.SetPlotSegmentFilter(this.props.options.target.plotSegment, newValue));
        }
        this.setState(this.getDefaultState(newValue));
    };
    // eslint-disable-next-line
    FluentUIFilterEditor.prototype.render = function () {
        var _this = this;
        var _a = this.props, manager = _a.manager, options = _a.options;
        var value = this.state.currentValue;
        var typedControls = [];
        switch (this.state.type) {
            case "expression":
                {
                    typedControls = [
                        React.createElement(fluentui_input_expression_1.FluentInputExpression, { validate: function (newValue) {
                                if (newValue) {
                                    return manager.store.verifyUserExpressionWithTable(newValue, options.table, { expectedTypes: ["boolean"] });
                                }
                                else {
                                    return {
                                        pass: true,
                                    };
                                }
                            }, allowNull: true, value: this.state.currentValue.expression, onEnter: function (newValue) {
                                _this.emitUpdateFilter({
                                    expression: newValue,
                                });
                                return true;
                            }, label: strings_1.strings.filter.expression }),
                    ];
                }
                break;
            case "categories":
                {
                    var keysSorted = [];
                    if (value && value.categories) {
                        for (var k in value.categories.values) {
                            if (Object.prototype.hasOwnProperty.call(value.categories.values, k)) {
                                keysSorted.push(k);
                            }
                        }
                        keysSorted.sort(function (a, b) { return (a < b ? -1 : 1); });
                    }
                    typedControls = [
                        manager.vertical(manager.label(strings_1.strings.filter.column), React.createElement("div", { className: "charticulator__filter-editor-column-selector" },
                            React.createElement(data_field_selector_1.DataFieldSelector, { defaultValue: {
                                    table: options.table,
                                    expression: this.state.currentValue.categories.expression,
                                }, table: options.table, datasetStore: this.props.manager.store, kinds: [core_1.Specification.DataKind.Categorical], onChange: function (field) {
                                    // Enumerate all values of this field
                                    if (field.expression) {
                                        var parsed = core_1.Expression.parse(field.expression);
                                        var table = _this.props.manager.store.chartManager.dataflow.getTable(field.table);
                                        var exprValues = {};
                                        for (var i = 0; i < table.rows.length; i++) {
                                            var rowContext = table.getRowContext(i);
                                            exprValues[parsed.getStringValue(rowContext)] = true;
                                        }
                                        _this.emitUpdateFilter({
                                            categories: {
                                                expression: field.expression,
                                                values: exprValues,
                                            },
                                        });
                                    }
                                } }))),
                        keysSorted.length > 0
                            ? manager.vertical(manager.label(strings_1.strings.filter.values), React.createElement("div", { className: "charticulator__filter-editor-values-selector" },
                                React.createElement("div", { className: "el-buttons" },
                                    React.createElement(react_1.DefaultButton, { text: strings_1.strings.filter.selectAll, onClick: function () {
                                            for (var key in value.categories.values) {
                                                if (Object.prototype.hasOwnProperty.call(value.categories.values, key)) {
                                                    value.categories.values[key] = true;
                                                }
                                            }
                                            _this.emitUpdateFilter({
                                                categories: {
                                                    expression: value.categories.expression,
                                                    values: value.categories.values,
                                                },
                                            });
                                        } }),
                                    " ",
                                    React.createElement(react_1.DefaultButton, { text: strings_1.strings.filter.clear, onClick: function () {
                                            for (var key in value.categories.values) {
                                                if (Object.prototype.hasOwnProperty.call(value.categories.values, key)) {
                                                    value.categories.values[key] = false;
                                                }
                                            }
                                            _this.emitUpdateFilter({
                                                categories: {
                                                    expression: value.categories.expression,
                                                    values: value.categories.values,
                                                },
                                            });
                                        } })),
                                React.createElement("div", null, keysSorted.map(function (key) { return (React.createElement("div", { key: key },
                                    React.createElement(fluentui_customized_components_1.FluentCheckbox, null,
                                        React.createElement(react_1.Checkbox, { checked: value.categories.values[key], label: key, onChange: function (ev, newValue) {
                                                value.categories.values[key] = newValue;
                                                _this.emitUpdateFilter({
                                                    categories: {
                                                        expression: value.categories.expression,
                                                        values: value.categories.values,
                                                    },
                                                });
                                            } })))); }))))
                            : null,
                    ];
                }
                break;
        }
        return (React.createElement("div", { className: "charticulator__filter-editor" },
            React.createElement("div", { className: "attribute-editor" },
                React.createElement("div", { className: "header" }, strings_1.strings.filter.editFilter),
                manager.vertical.apply(manager, __spread([React.createElement(react_1.Dropdown, { label: strings_1.strings.filter.filterType, styles: {
                            root: {
                                minWidth: 105,
                            },
                        }, onRenderLabel: fluentui_customized_components_1.labelRender, options: [
                            strings_1.strings.filter.none,
                            strings_1.strings.filter.categories,
                            strings_1.strings.filter.expression,
                        ].map(function (type) {
                            return {
                                key: type.toLowerCase(),
                                text: type,
                            };
                        }), selectedKey: this.state.type, onChange: function (event, newValue) {
                            if (_this.state.type != newValue.key) {
                                if (newValue.key == "none") {
                                    _this.emitUpdateFilter(null);
                                }
                                else {
                                    _this.setState({
                                        type: newValue.key,
                                        currentValue: {
                                            expression: "",
                                            categories: {
                                                expression: "",
                                                values: {},
                                            },
                                        },
                                    });
                                }
                            }
                        } })], typedControls)))));
    };
    return FluentUIFilterEditor;
}(React.Component));
exports.FluentUIFilterEditor = FluentUIFilterEditor;
//# sourceMappingURL=fluentui_filter_editor.js.map