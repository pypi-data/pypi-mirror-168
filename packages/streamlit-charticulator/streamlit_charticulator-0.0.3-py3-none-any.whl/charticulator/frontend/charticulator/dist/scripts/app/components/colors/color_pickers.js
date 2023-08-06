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
exports.ColorPickerButton = exports.PickerType = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var styles_1 = require("./styles");
var PickerType;
(function (PickerType) {
    PickerType["HCL"] = "hcl";
    PickerType["HSV"] = "hsv";
})(PickerType = exports.PickerType || (exports.PickerType = {}));
var ColorPickerButton = /** @class */ (function (_super) {
    __extends(ColorPickerButton, _super);
    function ColorPickerButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorPickerButton.prototype.render = function () {
        var text = this.props.type === PickerType.HCL ? "HCL Picker" : "HSV Picker";
        return (React.createElement(react_1.DefaultButton, { text: text, onClick: this.props.onClick, checked: this.props.state.currentPicker == this.props.type, styles: styles_1.defaultPaletteButtonsStyles }));
    };
    return ColorPickerButton;
}(React.Component));
exports.ColorPickerButton = ColorPickerButton;
//# sourceMappingURL=color_pickers.js.map