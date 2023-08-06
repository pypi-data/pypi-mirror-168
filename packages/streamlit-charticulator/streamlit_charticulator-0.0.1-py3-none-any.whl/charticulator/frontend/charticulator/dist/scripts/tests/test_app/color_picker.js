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
exports.register = exports.GradientPickerTestView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var components_1 = require("../../app/components");
var GradientPickerTestView = /** @class */ (function (_super) {
    __extends(GradientPickerTestView, _super);
    function GradientPickerTestView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GradientPickerTestView.prototype.render = function () {
        return (React.createElement("div", null,
            React.createElement("div", { style: {
                    background: "#eee",
                    border: "10px solid #aaa",
                    width: "300px",
                    display: "inline-block",
                } },
                React.createElement(components_1.GradientPicker, null))));
    };
    return GradientPickerTestView;
}(React.Component));
exports.GradientPickerTestView = GradientPickerTestView;
function register(f) {
    f("GradientPicker", GradientPickerTestView);
}
exports.register = register;
//# sourceMappingURL=color_picker.js.map