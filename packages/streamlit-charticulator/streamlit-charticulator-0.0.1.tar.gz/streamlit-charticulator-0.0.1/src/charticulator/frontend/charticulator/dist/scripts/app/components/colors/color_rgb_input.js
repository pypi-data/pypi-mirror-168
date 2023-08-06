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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ColorRgbInput = void 0;
var React = require("react");
var core_1 = require("../../../core");
var color_space_picker_1 = require("../color_space_picker");
var ColorRgbInput = /** @class */ (function (_super) {
    __extends(ColorRgbInput, _super);
    function ColorRgbInput() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorRgbInput.prototype.transformColorValue = function (value) {
        var newColorValue = core_1.prettyNumber(value, 0);
        return newColorValue.length > 0 ? newColorValue : "0";
    };
    ColorRgbInput.prototype.render = function () {
        var _this = this;
        var currentColor = this.props.state.desc.toRGB(this.props.state.x1, this.props.state.x2, this.props.state.x3);
        var rgb = { r: currentColor[0], g: currentColor[1], b: currentColor[2] };
        return (React.createElement(React.Fragment, null,
            React.createElement("div", { className: "column" },
                React.createElement("div", { className: "row" },
                    React.createElement("label", null, "R"),
                    React.createElement(color_space_picker_1.InputField, { defaultValue: this.transformColorValue(rgb.r), onEnter: function (v) {
                            var num = parseFloat(v);
                            if (num == num && num != null) {
                                num = Math.max(0, Math.min(255, num));
                                var _a = __read(_this.props.state.desc.fromRGB(num, rgb.g, rgb.b), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
                                _this.props.updateState({
                                    x1: x1,
                                    x2: x2,
                                    x3: x3,
                                    desc: _this.props.state.desc,
                                });
                                return true;
                            }
                        } })),
                React.createElement("div", { className: "row" },
                    React.createElement("label", null, "G"),
                    React.createElement(color_space_picker_1.InputField, { defaultValue: this.transformColorValue(rgb.g), onEnter: function (v) {
                            var num = parseFloat(v);
                            if (num == num && num != null) {
                                num = Math.max(0, Math.min(255, num));
                                var _a = __read(_this.props.state.desc.fromRGB(rgb.r, num, rgb.b), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
                                _this.props.updateState({
                                    x1: x1,
                                    x2: x2,
                                    x3: x3,
                                    desc: _this.props.state.desc,
                                });
                                return true;
                            }
                        } })),
                React.createElement("div", { className: "row" },
                    React.createElement("label", null, "B"),
                    React.createElement(color_space_picker_1.InputField, { defaultValue: this.transformColorValue(rgb.b), onEnter: function (v) {
                            var num = parseFloat(v);
                            if (num == num && num != null) {
                                num = Math.max(0, Math.min(255, num));
                                var _a = __read(_this.props.state.desc.fromRGB(rgb.r, rgb.g, num), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
                                _this.props.updateState({
                                    x1: x1,
                                    x2: x2,
                                    x3: x3,
                                    desc: _this.props.state.desc,
                                });
                                return true;
                            }
                        } })))));
    };
    return ColorRgbInput;
}(React.Component));
exports.ColorRgbInput = ColorRgbInput;
//# sourceMappingURL=color_rgb_input.js.map