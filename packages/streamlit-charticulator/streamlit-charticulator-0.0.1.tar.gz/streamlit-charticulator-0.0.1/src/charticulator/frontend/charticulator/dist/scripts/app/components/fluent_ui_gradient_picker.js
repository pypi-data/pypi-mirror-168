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
exports.FluentUIGradientPicker = exports.Colorspace = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var custom_gradient_menu_1 = require("./gradient/custom_gradient_menu");
var gradient_palettes_1 = require("./gradient/gradient_palettes");
var Colorspace;
(function (Colorspace) {
    Colorspace["LAB"] = "lab";
    Colorspace["HCL"] = "hcl";
})(Colorspace = exports.Colorspace || (exports.Colorspace = {}));
var FluentUIGradientPicker = /** @class */ (function (_super) {
    __extends(FluentUIGradientPicker, _super);
    function FluentUIGradientPicker(props) {
        var _this = _super.call(this, props) || this;
        _this.selectGradient = _this.selectGradient.bind(_this);
        _this.state = {
            currentTab: "palettes",
            currentGradient: _this.props.defaultValue || {
                colorspace: Colorspace.LAB,
                colors: [
                    { r: 0, g: 0, b: 0 },
                    { r: 255, g: 255, b: 255 },
                ],
            },
        };
        return _this;
    }
    FluentUIGradientPicker.prototype.selectGradient = function (gradient, emit) {
        var _this = this;
        if (emit === void 0) { emit = false; }
        this.setState({
            currentGradient: gradient,
        }, function () {
            if (emit) {
                if (_this.props.onPick) {
                    _this.props.onPick(gradient);
                }
            }
        });
    };
    FluentUIGradientPicker.prototype.render = function () {
        return (React.createElement("div", { className: "gradient-picker" },
            React.createElement(react_1.Pivot, { "aria-label": "Basic Pivot Example" },
                React.createElement(react_1.PivotItem, { headerText: "Palettes" },
                    React.createElement(gradient_palettes_1.GradientPalettes, { selectGradient: this.selectGradient })),
                React.createElement(react_1.PivotItem, { headerText: "Custom" },
                    React.createElement(custom_gradient_menu_1.CustomGradientMenu, { currentGradient: this.state.currentGradient, selectGradient: this.selectGradient })))));
    };
    return FluentUIGradientPicker;
}(React.Component));
exports.FluentUIGradientPicker = FluentUIGradientPicker;
//# sourceMappingURL=fluent_ui_gradient_picker.js.map