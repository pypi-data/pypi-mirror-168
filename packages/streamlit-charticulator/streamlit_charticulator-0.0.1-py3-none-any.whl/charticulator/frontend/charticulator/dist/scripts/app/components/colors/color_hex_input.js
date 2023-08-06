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
exports.ColorHexInput = void 0;
var React = require("react");
var core_1 = require("../../../core");
var color_space_picker_1 = require("../color_space_picker");
var ColorHexInput = /** @class */ (function (_super) {
    __extends(ColorHexInput, _super);
    function ColorHexInput() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorHexInput.prototype.render = function () {
        var _this = this;
        var currentColor = this.props.state.desc.toRGB(this.props.state.x1, this.props.state.x2, this.props.state.x3);
        var rgb = { r: currentColor[0], g: currentColor[1], b: currentColor[2] };
        return (React.createElement(React.Fragment, null,
            React.createElement("label", null, "HEX"),
            React.createElement(color_space_picker_1.InputField, { defaultValue: core_1.colorToHTMLColorHEX(rgb), onEnter: function (v) {
                    var color = core_1.colorFromHTMLColor(v);
                    if (color) {
                        var _a = __read(_this.props.state.desc.fromRGB(color.r, color.g, color.b), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
                        _this.props.updateState({
                            x1: x1,
                            x2: x2,
                            x3: x3,
                            desc: _this.props.state.desc,
                        });
                        return true;
                    }
                } })));
    };
    return ColorHexInput;
}(React.Component));
exports.ColorHexInput = ColorHexInput;
//# sourceMappingURL=color_hex_input.js.map