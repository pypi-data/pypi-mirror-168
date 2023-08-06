"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReorderStringsValue = void 0;
var React = require("react");
var object_list_editor_1 = require("../../object_list_editor");
var button_1 = require("./button");
var components_1 = require("../../../../components");
var strings_1 = require("../../../../../strings");
var ReorderStringsValue = /** @class */ (function (_super) {
    __extends(ReorderStringsValue, _super);
    function ReorderStringsValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            items: _this.props.items.slice(),
            customOrder: false,
            sortOrder: false,
        };
        return _this;
    }
    ReorderStringsValue.prototype.render = function () {
        var _this = this;
        var items = this.state.items.slice();
        return (React.createElement("div", { className: "charticulator__widget-popup-reorder-widget" },
            React.createElement("div", { className: "el-row el-list-view" },
                React.createElement(object_list_editor_1.ReorderListView, { enabled: true, onReorder: function (a, b) {
                        object_list_editor_1.ReorderListView.ReorderArray(items, a, b);
                        _this.setState({ items: items, customOrder: true });
                    } }, items.map(function (x) { return (React.createElement("div", { key: x, className: "el-item" }, x)); }))),
            React.createElement("div", { className: "el-row" },
                React.createElement(button_1.Button, { icon: "Sort", text: strings_1.strings.reOrder.reverse, onClick: function () {
                        _this.setState({
                            items: _this.state.items.reverse(),
                            customOrder: true,
                        });
                    } }),
                " ",
                React.createElement(button_1.Button, { icon: "general/sort", text: strings_1.strings.reOrder.sort, onClick: function () {
                        _this.setState({
                            items: _this.state.items.sort(),
                            sortOrder: true,
                            customOrder: false,
                        });
                    } }),
                this.props.allowReset && (React.createElement(React.Fragment, null,
                    " ",
                    React.createElement(button_1.Button, { icon: "general/clear", text: strings_1.strings.reOrder.reset, onClick: function () {
                            if (_this.props.onReset) {
                                var items_1 = _this.props.onReset();
                                _this.setState({
                                    items: items_1,
                                    customOrder: false,
                                    sortOrder: false,
                                });
                            }
                        } })))),
            React.createElement("div", { className: "el-row" },
                React.createElement(components_1.ButtonRaised, { text: "OK", onClick: function () {
                        _this.props.onConfirm(_this.state.items, _this.state.customOrder, _this.state.sortOrder);
                    } }))));
    };
    return ReorderStringsValue;
}(React.Component));
exports.ReorderStringsValue = ReorderStringsValue;
//# sourceMappingURL=reorder_string_value.js.map