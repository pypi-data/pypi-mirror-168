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
Object.defineProperty(exports, "__esModule", { value: true });
exports.Radio = exports.Select = exports.DropdownListView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var components_1 = require("../../../../components");
var popup_controller_1 = require("../../../../controllers/popup_controller");
var globals = require("../../../../globals");
var R = require("../../../../resources");
var utils_1 = require("../../../../utils");
function DropdownListView(props) {
    return (React.createElement("ul", { className: "dropdown-list" }, props.list.map(function (item) { return (React.createElement("li", { tabIndex: 0, key: item.name, className: props.selected == item.name ? "is-active" : null, onClick: function () {
            var _a;
            if (props.onClick) {
                props.onClick(item.name);
            }
            props.context.close();
            (_a = props.onClose) === null || _a === void 0 ? void 0 : _a.call(props);
        }, onKeyPress: function (e) {
            var _a;
            if (e.key === "Enter") {
                if (props.onClick) {
                    props.onClick(item.name);
                }
                props.context.close();
                (_a = props.onClose) === null || _a === void 0 ? void 0 : _a.call(props);
            }
        } },
        item.url != null ? React.createElement(components_1.SVGImageIcon, { url: item.url }) : null,
        item.text != null ? (React.createElement("span", { className: "text", style: { fontFamily: item.font } }, item.text)) : null)); })));
}
exports.DropdownListView = DropdownListView;
var Select = /** @class */ (function (_super) {
    __extends(Select, _super);
    function Select(props) {
        var _this = _super.call(this, props) || this;
        _this._startDropdown = function (e) {
            e.stopPropagation();
            _this.startDropdown();
        };
        _this.state = {
            active: false,
        };
        return _this;
    }
    Select.prototype.startDropdown = function () {
        var _this = this;
        globals.popupController.popupAt(function (context) {
            context.addListener("close", function () {
                _this.setState({
                    active: false,
                });
            });
            var list = _this.props.options.map(function (x, i) {
                return {
                    url: _this.props.icons ? R.getSVGIcon(_this.props.icons[i]) : null,
                    name: x,
                    text: _this.props.labels ? _this.props.labels[i] : null,
                };
            });
            return (React.createElement(popup_controller_1.PopupView, { context: context },
                React.createElement(DropdownListView, { selected: _this.props.value, list: list, context: context, onClick: function (value) {
                        _this.props.onChange(value);
                    } })));
        }, { anchor: this.anchor });
        this.setState({
            active: true,
        });
    };
    Select.prototype.render = function () {
        var _this = this;
        var currentIndex = this.props.options.indexOf(this.props.value);
        var props = this.props;
        if (props.labelPosition === 1 /* Bottom */) {
            return (React.createElement("div", { className: "charticulator__widget-control-select-container", title: props.tooltip },
                React.createElement("span", { className: utils_1.classNames("charticulator__widget-control-select", ["is-active", this.state.active], ["has-text", this.props.labels != null && props.showText], ["has-icon", this.props.icons != null]), ref: function (e) { return (_this.anchor = e); }, onClick: this._startDropdown },
                    props.icons != null ? (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(props.icons[currentIndex]) })) : null,
                    React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("ChevronDown") })),
                React.createElement("span", { className: "el-text" }, props.labels[currentIndex])));
        }
        else {
            return (React.createElement("span", { className: utils_1.classNames("charticulator__widget-control-select", ["is-active", this.state.active], ["has-text", this.props.labels != null && props.showText], ["has-icon", this.props.icons != null]), ref: function (e) { return (_this.anchor = e); }, onClick: this._startDropdown },
                props.icons != null ? (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(props.icons[currentIndex]) })) : null,
                props.labels != null && props.showText ? (React.createElement("span", { className: "el-text" }, props.labels[currentIndex])) : null,
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("ChevronDown") })));
        }
    };
    return Select;
}(React.Component));
exports.Select = Select;
var Radio = /** @class */ (function (_super) {
    __extends(Radio, _super);
    function Radio() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Radio.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { className: "charticulator__widget-control-radio" }, this.props.options.map(function (value, index) {
            return (React.createElement("span", { key: value, className: utils_1.classNames("charticulator__widget-control-radio-item", ["is-active", value == _this.props.value]), title: _this.props.labels ? _this.props.labels[index] : null, onClick: function () {
                    _this.props.onChange(value);
                } },
                _this.props.icons ? (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(_this.props.icons[index]) })) : null,
                _this.props.showText ? (React.createElement("span", { className: "el-text" }, _this.props.labels[index])) : null));
        })));
    };
    return Radio;
}(React.Component));
exports.Radio = Radio;
//# sourceMappingURL=select.js.map