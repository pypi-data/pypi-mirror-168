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
exports.CustomGradientMenu = void 0;
var React = require("react");
var object_list_editor_1 = require("../../views/panels/object_list_editor");
var core_1 = require("../../../core");
var fluentui_color_picker_1 = require("../fluentui_color_picker");
var react_1 = require("@fluentui/react");
var styles_1 = require("./styles");
var gradient_palettes_1 = require("./gradient_palettes");
var custom_gradient_buttons_1 = require("./custom_gradient_buttons");
var CustomGradientMenu = /** @class */ (function (_super) {
    __extends(CustomGradientMenu, _super);
    function CustomGradientMenu(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isPickerOpen: false,
            currentItemId: "",
            currentColor: null,
            currentItemIdx: null,
        };
        return _this;
    }
    CustomGradientMenu.prototype.render = function () {
        var _this = this;
        var currentGradient = this.props.currentGradient;
        return (React.createElement("div", null,
            React.createElement("div", null,
                React.createElement(gradient_palettes_1.GradientView, { gradient: currentGradient })),
            React.createElement("div", null,
                React.createElement(object_list_editor_1.ReorderListView, { enabled: true, onReorder: function (dragIndex, dropIndex) {
                        var newGradient = core_1.deepClone(currentGradient);
                        object_list_editor_1.ReorderListView.ReorderArray(newGradient.colors, dragIndex, dropIndex);
                        _this.props.selectGradient(newGradient, true);
                    } },
                    currentGradient.colors.map(function (color, i) {
                        return (React.createElement(styles_1.ColorRowWrapper, { key: "m" + i },
                            React.createElement("div", null,
                                React.createElement(styles_1.ColorCell, { id: "color_" + i, onClick: function () {
                                        _this.changeColorPickerState("color_" + i, color, i);
                                    }, "$color": fluentui_color_picker_1.colorToCSS(color) })),
                            React.createElement(react_1.TextField, { defaultValue: core_1.colorToHTMLColorHEX(color), onChange: function (event, value) {
                                    if (value) {
                                        var newColor = core_1.colorFromHTMLColor(value);
                                        var newGradient = core_1.deepClone(currentGradient);
                                        newGradient.colors[i] = newColor;
                                        _this.props.selectGradient(newGradient, true);
                                    }
                                }, underlined: true, styles: styles_1.colorTextInputStyles }),
                            React.createElement(react_1.DefaultButton, { iconProps: {
                                    iconName: "ChromeClose",
                                }, styles: styles_1.deleteColorStyles, onClick: function () {
                                    if (currentGradient.colors.length > 1) {
                                        var newGradient = core_1.deepClone(_this.props.currentGradient);
                                        newGradient.colors.splice(i, 1);
                                        _this.props.selectGradient(newGradient, true);
                                    }
                                } })));
                    }),
                    this.renderColorPicker())),
            React.createElement(custom_gradient_buttons_1.CustomGradientButtons, { selectGradient: this.props.selectGradient, currentGradient: currentGradient })));
    };
    CustomGradientMenu.prototype.changeColorPickerState = function (id, color, idx) {
        this.setState({
            isPickerOpen: !this.state.isPickerOpen,
            currentItemId: id,
            currentColor: color,
            currentItemIdx: idx,
        });
    };
    CustomGradientMenu.prototype.renderColorPicker = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null, this.state.isPickerOpen && (React.createElement(react_1.Callout, { target: "#" + this.state.currentItemId, onDismiss: function () {
                return _this.changeColorPickerState(_this.state.currentItemId, null, null);
            }, alignTargetEdge: true },
            React.createElement(fluentui_color_picker_1.ColorPicker, { defaultValue: this.state.currentColor, onPick: function (color) {
                    var newGradient = core_1.deepClone(_this.props.currentGradient);
                    newGradient.colors[_this.state.currentItemIdx] = color;
                    _this.props.selectGradient(newGradient, true);
                }, parent: this })))));
    };
    return CustomGradientMenu;
}(React.Component));
exports.CustomGradientMenu = CustomGradientMenu;
//# sourceMappingURL=custom_gradient_menu.js.map