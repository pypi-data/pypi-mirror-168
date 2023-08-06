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
exports.InputText = void 0;
var React = require("react");
var InputText = /** @class */ (function (_super) {
    __extends(InputText, _super);
    function InputText() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputText.prototype.componentWillUpdate = function (newProps) {
        this.inputElement.value =
            newProps.defaultValue != null ? newProps.defaultValue : "";
    };
    InputText.prototype.doEnter = function () {
        if ((this.props.defaultValue != null ? this.props.defaultValue : "") ==
            this.inputElement.value) {
            return;
        }
        if (this.props.onEnter) {
            var ret = this.props.onEnter(this.inputElement.value);
            if (!ret) {
                this.inputElement.value =
                    this.props.defaultValue != null ? this.props.defaultValue : "";
            }
        }
        else {
            this.inputElement.value =
                this.props.defaultValue != null ? this.props.defaultValue : "";
        }
    };
    InputText.prototype.doCancel = function () {
        this.inputElement.value =
            this.props.defaultValue != null ? this.props.defaultValue : "";
        if (this.props.onCancel) {
            this.props.onCancel();
        }
    };
    Object.defineProperty(InputText.prototype, "value", {
        get: function () {
            return this.inputElement.value;
        },
        set: function (v) {
            this.inputElement.value = v;
        },
        enumerable: false,
        configurable: true
    });
    InputText.prototype.render = function () {
        var _this = this;
        return (React.createElement("input", { className: "charticulator__widget-control-input-field", type: "text", ref: function (e) { return (_this.inputElement = e); }, defaultValue: this.props.defaultValue != null ? this.props.defaultValue : "", placeholder: this.props.placeholder, onKeyDown: function (e) {
                if (e.key == "Enter") {
                    _this.doEnter();
                }
                if (e.key == "Escape") {
                    _this.doCancel();
                }
            }, onFocus: function () {
                // Select the text, with backward selection
                _this.inputElement.setSelectionRange(0, _this.inputElement.value.length, "backward");
            }, onBlur: function () {
                _this.doEnter();
            } }));
    };
    return InputText;
}(React.Component));
exports.InputText = InputText;
//# sourceMappingURL=input_text.js.map