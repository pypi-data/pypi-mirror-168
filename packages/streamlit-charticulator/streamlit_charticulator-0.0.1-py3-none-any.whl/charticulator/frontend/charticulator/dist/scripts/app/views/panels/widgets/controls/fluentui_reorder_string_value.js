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
exports.FluentUIReorderStringsValue = void 0;
var React = require("react");
var object_list_editor_1 = require("../../object_list_editor");
var components_1 = require("../../../../components");
var strings_1 = require("../../../../../strings");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
var core_1 = require("../../../../../core");
var FluentUIReorderStringsValue = /** @class */ (function (_super) {
    __extends(FluentUIReorderStringsValue, _super);
    function FluentUIReorderStringsValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            items: _this.props.items.slice(),
            customOrder: false,
            sortOrder: false,
        };
        return _this;
    }
    // eslint-disable-next-line max-lines-per-function
    FluentUIReorderStringsValue.prototype.render = function () {
        var _this = this;
        var _a;
        var items = this.state.items;
        return (React.createElement("div", { className: "charticulator__widget-popup-reorder-widget" },
            React.createElement("div", { className: "el-row el-list-view" },
                React.createElement(object_list_editor_1.ReorderListView, { enabled: (_a = this.props.allowDragItems) !== null && _a !== void 0 ? _a : true, onReorder: function (a, b) {
                        object_list_editor_1.ReorderListView.ReorderArray(items, a, b);
                        _this.setState({ items: items, customOrder: true, sortOrder: false });
                        if (_this.props.onReorderHandler) {
                            _this.props.onReorderHandler();
                        }
                    } }, items.map(function (x) { return (React.createElement("div", { key: x + core_1.getRandomNumber(), className: "el-item" },
                    React.createElement(react_1.TooltipHost, { content: x }, x))); }))),
            React.createElement("div", { className: "el-row" },
                React.createElement(react_1.DefaultButton, { iconProps: {
                        iconName: "SortLines",
                    }, text: strings_1.strings.reOrder.sort, onClick: function () {
                        var _a;
                        _this.setState({
                            items: (_a = __spread(_this.props.sortedCategories)) !== null && _a !== void 0 ? _a : _this.state.items.sort(),
                            customOrder: false,
                            sortOrder: true,
                        });
                        if (_this.props.onButtonHandler) {
                            _this.props.onButtonHandler();
                        }
                    }, styles: {
                        root: __assign(__assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight), { padding: 0, marginRight: 5 }),
                    } }),
                React.createElement(react_1.DefaultButton, { iconProps: {
                        iconName: "Sort",
                    }, styles: {
                        root: __assign(__assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight), { padding: 0, marginRight: 5 }),
                    }, text: strings_1.strings.reOrder.reverse, onClick: function () {
                        _this.setState({
                            items: _this.state.items.reverse(),
                            customOrder: true,
                        });
                        if (_this.props.onButtonHandler) {
                            _this.props.onButtonHandler();
                        }
                    } }),
                this.props.allowReset && (React.createElement(React.Fragment, null,
                    React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "Clear",
                        }, styles: {
                            root: __assign(__assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight), { padding: 0 }),
                        }, text: strings_1.strings.reOrder.reset, onClick: function () {
                            if (_this.props.onReset) {
                                var items_1 = _this.props.onReset();
                                _this.setState({
                                    items: items_1,
                                    customOrder: false,
                                    sortOrder: false,
                                });
                                if (_this.props.onButtonHandler) {
                                    _this.props.onButtonHandler();
                                }
                            }
                        } })))),
            React.createElement("div", { className: "el-row" },
                React.createElement(components_1.ButtonRaised, { text: "OK", onClick: function () {
                        _this.props.onConfirm(_this.state.items, _this.state.customOrder, _this.state.sortOrder);
                    } }))));
    };
    return FluentUIReorderStringsValue;
}(React.Component));
exports.FluentUIReorderStringsValue = FluentUIReorderStringsValue;
//# sourceMappingURL=fluentui_reorder_string_value.js.map