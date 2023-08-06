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
exports.InputNumber = void 0;
var React = require("react");
var core_1 = require("../../../../../core");
var button_1 = require("./button");
var input_text_1 = require("./input_text");
var slider_1 = require("./slider");
var InputNumber = /** @class */ (function (_super) {
    __extends(InputNumber, _super);
    function InputNumber() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputNumber.prototype.formatNumber = function (value) {
        if (value == null) {
            return "";
        }
        if (value != value) {
            return "N/A";
        }
        if (this.props.percentage) {
            return (core_1.prettyNumber(value * 100, this.props.digits != null ? this.props.digits : 2) + "%");
        }
        else {
            return core_1.prettyNumber(value, this.props.digits != null ? this.props.digits : 2);
        }
    };
    InputNumber.prototype.parseNumber = function (str) {
        str = str.trim();
        if (str == "") {
            return null;
        }
        if (this.props.percentage) {
            str = str.replace(/%$/, "");
            return +str / 100;
        }
        else {
            return +str;
        }
    };
    InputNumber.prototype.reportValue = function (value) {
        if (value == null) {
            return this.props.onEnter(value);
        }
        else {
            if (this.props.minimum != null) {
                value = Math.max(this.props.minimum, value);
            }
            if (this.props.maximum != null) {
                value = Math.min(this.props.maximum, value);
            }
            return this.props.onEnter(value);
        }
    };
    InputNumber.prototype.renderSlider = function () {
        var _this = this;
        var sliderMin = 0;
        var sliderMax = 1;
        if (this.props.minimum != null) {
            sliderMin = this.props.minimum;
        }
        if (this.props.maximum != null) {
            sliderMax = this.props.maximum;
        }
        if (this.props.sliderRange != null) {
            sliderMin = this.props.sliderRange[0];
            sliderMax = this.props.sliderRange[1];
        }
        return (React.createElement(slider_1.Slider, { width: 70, min: sliderMin, max: sliderMax, defaultValue: this.props.defaultValue, mapping: this.props.sliderFunction, onChange: function (newValue, isFinished) {
                _this.textInput.value = _this.formatNumber(newValue);
                if (isFinished) {
                    _this.reportValue(newValue);
                }
            } }));
    };
    InputNumber.prototype.renderUpdown = function () {
        var _this = this;
        var tick = this.props.updownTick || 0.1;
        if (this.props.updownStyle == "font") {
            return [
                React.createElement(button_1.Button, { key: "up", icon: "general/text-size-up", onClick: function () {
                        _this.reportValue(_this.props.defaultValue + tick);
                    } }),
                React.createElement(button_1.Button, { key: "down", icon: "general/text-size-down", onClick: function () {
                        _this.reportValue(_this.props.defaultValue - tick);
                    } }),
            ];
        }
        else {
            return (React.createElement(button_1.UpdownButton, { onClick: function (part) {
                    if (part == "up") {
                        _this.reportValue(_this.props.defaultValue + tick);
                    }
                    else {
                        _this.reportValue(_this.props.defaultValue - tick);
                    }
                } }));
        }
    };
    InputNumber.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { className: "charticulator__widget-control-input-number" },
            React.createElement("div", { className: "charticulator__widget-control-input-number-input" },
                React.createElement(input_text_1.InputText, { ref: function (e) { return (_this.textInput = e); }, placeholder: this.props.placeholder, defaultValue: this.formatNumber(this.props.defaultValue), onEnter: function (str) {
                        var num = _this.parseNumber(str);
                        return _this.reportValue(num);
                    } })),
            this.props.showSlider ? this.renderSlider() : null,
            this.props.showUpdown ? this.renderUpdown() : null));
    };
    return InputNumber;
}(React.Component));
exports.InputNumber = InputNumber;
//# sourceMappingURL=input_number.js.map