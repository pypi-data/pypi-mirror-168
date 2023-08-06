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
exports.CustomGradientButtons = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var strings_1 = require("../../../strings");
var core_1 = require("../../../core");
var styles_1 = require("./styles");
var fluent_ui_gradient_picker_1 = require("../fluent_ui_gradient_picker");
var CustomGradientButtons = /** @class */ (function (_super) {
    __extends(CustomGradientButtons, _super);
    function CustomGradientButtons() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CustomGradientButtons.prototype.render = function () {
        var _this = this;
        var currentGradient = this.props.currentGradient;
        var dropdownItems = [
            { key: fluent_ui_gradient_picker_1.Colorspace.HCL, text: "HCL" },
            { key: fluent_ui_gradient_picker_1.Colorspace.LAB, text: "Lab" },
        ];
        return (React.createElement(styles_1.CustomGradientButtonsWrapper, null,
            React.createElement("div", null,
                React.createElement(react_1.DefaultButton, { iconProps: {
                        iconName: "Add",
                    }, text: strings_1.strings.scaleEditor.add, onClick: function () {
                        var newGradient = core_1.deepClone(currentGradient);
                        newGradient.colors.push({ r: 150, g: 150, b: 150 });
                        _this.props.selectGradient(newGradient, true);
                    }, styles: styles_1.defaultActionButtonsStyles })),
            React.createElement("div", null,
                React.createElement(react_1.DefaultButton, { iconProps: {
                        iconName: "Sort",
                    }, text: strings_1.strings.scaleEditor.reverse, onClick: function () {
                        var newGradient = core_1.deepClone(currentGradient);
                        newGradient.colors.reverse();
                        _this.props.selectGradient(newGradient, true);
                    }, styles: styles_1.defaultActionButtonsStyles })),
            React.createElement(react_1.Dropdown, { options: dropdownItems, onChange: function (event, option) {
                    if (option) {
                        var newGradient = core_1.deepClone(currentGradient);
                        newGradient.colorspace = option.key;
                        _this.props.selectGradient(newGradient, true);
                    }
                }, defaultSelectedKey: currentGradient.colorspace, styles: styles_1.dropdownStyles })));
    };
    return CustomGradientButtons;
}(React.Component));
exports.CustomGradientButtons = CustomGradientButtons;
//# sourceMappingURL=custom_gradient_buttons.js.map