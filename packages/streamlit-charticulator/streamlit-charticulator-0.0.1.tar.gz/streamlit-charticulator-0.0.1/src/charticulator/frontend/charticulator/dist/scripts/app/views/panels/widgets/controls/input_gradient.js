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
exports.InputColorGradient = void 0;
var React = require("react");
var globals = require("../../../../globals");
var controllers_1 = require("../../../../controllers");
var components_1 = require("../../../../components");
var InputColorGradient = /** @class */ (function (_super) {
    __extends(InputColorGradient, _super);
    function InputColorGradient() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputColorGradient.prototype.render = function () {
        var _this = this;
        var colorButton;
        return (React.createElement("span", { className: "charticulator__widget-control-input-color-gradient" },
            React.createElement("span", { className: "el-color-gradient-display", ref: function (e) { return (colorButton = e); }, onClick: function () {
                    globals.popupController.popupAt(function (context) {
                        return (React.createElement(controllers_1.PopupView, { context: context },
                            React.createElement(components_1.GradientPicker, { defaultValue: _this.props.defaultValue, onPick: function (gradient) {
                                    _this.props.onEnter(gradient);
                                } })));
                    }, { anchor: colorButton });
                } },
                React.createElement(components_1.GradientView, { gradient: this.props.defaultValue }))));
    };
    return InputColorGradient;
}(React.Component));
exports.InputColorGradient = InputColorGradient;
//# sourceMappingURL=input_gradient.js.map