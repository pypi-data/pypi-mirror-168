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
exports.CheckBox = exports.UpdownButton = exports.Button = void 0;
var React = require("react");
var R = require("../../../../resources");
var components_1 = require("../../../../components");
var utils_1 = require("../../../../utils");
var Button = /** @class */ (function (_super) {
    __extends(Button, _super);
    function Button() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Button.prototype.render = function () {
        var _this = this;
        return (React.createElement("button", { className: utils_1.classNames("charticulator__widget-control-button", ["is-active", this.props.active], ["has-text", this.props.text != null], ["has-icon", this.props.icon != null], ["is-disabled", this.props.disabled]), title: this.props.title, onClick: function (e) {
                if (_this.props.disabled === true) {
                    return;
                }
                e.stopPropagation();
                if (_this.props.onClick) {
                    _this.props.onClick();
                }
            } },
            this.props.icon ? (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(this.props.icon) })) : null,
            this.props.text ? (React.createElement("span", { className: "el-text" }, this.props.text)) : null));
    };
    return Button;
}(React.Component));
exports.Button = Button;
function UpdownButton(props) {
    return (React.createElement("span", { className: "charticulator__widget-control-updown-button" },
        React.createElement("span", { className: "el-part", onClick: function () { return props.onClick("up"); } },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("general/triangle-up") })),
        React.createElement("span", { className: "el-part", onClick: function () { return props.onClick("down"); } },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("general/triangle-down") }))));
}
exports.UpdownButton = UpdownButton;
var CheckBox = /** @class */ (function (_super) {
    __extends(CheckBox, _super);
    function CheckBox() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CheckBox.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { className: utils_1.classNames("charticulator__widget-control-checkbox", ["is-active", this.props.value], ["is-fill-width", this.props.fillWidth], ["has-text", this.props.text != null]), title: this.props.title, onClick: function (e) {
                e.stopPropagation();
                if (_this.props.onChange) {
                    _this.props.onChange(!_this.props.value);
                }
            } },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(this.props.value ? "checkbox/checked" : "checkbox/empty") }),
            this.props.text ? (React.createElement("span", { className: "el-text" }, this.props.text)) : null));
    };
    return CheckBox;
}(React.Component));
exports.CheckBox = CheckBox;
//# sourceMappingURL=button.js.map