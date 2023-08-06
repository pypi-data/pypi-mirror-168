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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.InputColorGradient = exports.FluentInputColor = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var globals = require("../../../../globals");
var core_1 = require("../../../../../core");
var components_1 = require("../../../../components");
var popup_controller_1 = require("../../../../controllers/popup_controller");
var fluentui_color_picker_1 = require("../../../../components/fluentui_color_picker");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
var strings_1 = require("../../../../../strings");
var fluent_ui_gradient_picker_1 = require("../../../../components/fluent_ui_gradient_picker");
var fluentui_empty_mapping_1 = require("./fluentui_empty_mapping");
var ID_PREFIX = "id_";
var FluentInputColor = /** @class */ (function (_super) {
    __extends(FluentInputColor, _super);
    function FluentInputColor(props) {
        var _this = _super.call(this, props) || this;
        var hex = "";
        if (_this.props.defaultValue) {
            hex = core_1.colorToHTMLColorHEX(_this.props.defaultValue);
        }
        _this.state = { open: false, color: hex, value: hex };
        return _this;
    }
    FluentInputColor.prototype.componentWillReceiveProps = function (nextProps) {
        var hex = "";
        if (nextProps.defaultValue) {
            hex = core_1.colorToHTMLColorHEX(nextProps.defaultValue);
        }
        if (hex !== this.state.value) {
            this.setState({
                value: hex,
            });
        }
    };
    FluentInputColor.prototype.renderPicker = function () {
        var _this = this;
        var hex = "";
        if (this.props.defaultValue) {
            hex = core_1.colorToHTMLColorHEX(this.props.defaultValue);
        }
        var pickerId = this.props.labelKey.replace(/\W/g, "_");
        return (React.createElement("span", { className: "el-color-display", style: {
                backgroundColor: hex == "" ? "transparent" : hex,
                marginTop: this.props.noDefaultMargin ? 0 : null,
                marginRight: 5,
            }, id: ID_PREFIX + pickerId, onClick: function () {
                _this.setState({ open: !_this.state.open });
            } }));
    };
    FluentInputColor.prototype.renderEmptyColorPicker = function () {
        var _this = this;
        var pickerId = this.props.labelKey.replace(/\W/g, "_");
        return (React.createElement("span", { id: ID_PREFIX + pickerId },
            React.createElement(fluentui_empty_mapping_1.EmptyColorButton, { onClick: function () {
                    _this.setState({ open: !_this.state.open });
                }, styles: this.props.styles })));
    };
    FluentInputColor.prototype.render = function () {
        var _this = this;
        var _a;
        var hex = "";
        if (this.props.defaultValue) {
            hex = core_1.colorToHTMLColorHEX(this.props.defaultValue);
        }
        var pickerId = this.props.labelKey.replace(/\W/g, "_");
        var picker = this.renderPicker();
        var emptyPicker = this.renderEmptyColorPicker();
        return (React.createElement("span", { className: "charticulator__widget-control-input-color" },
            this.props.pickerBeforeTextField && (hex == "" ? emptyPicker : picker),
            React.createElement(fluentui_customized_components_1.FluentTextField, null,
                React.createElement(react_1.TextField, { label: this.props.label, onRenderLabel: fluentui_customized_components_1.labelRender, onChange: function (event, newValue) {
                        newValue = newValue.trim();
                        if (newValue == "") {
                            if (_this.props.allowNull) {
                                return _this.props.onEnter(null);
                            }
                            else {
                                return false;
                            }
                        }
                        _this.setState({
                            value: newValue,
                        });
                        try {
                            var color = core_1.parseColorOrThrowException(newValue);
                            if (color) {
                                return _this.props.onEnter(color);
                            }
                            else {
                                return false;
                            }
                        }
                        catch (ex) {
                            //ignore
                        }
                    }, placeholder: this.props.allowNull ? strings_1.strings.core.none : "", value: this.state.value, onKeyDown: function (e) {
                        if (_this.props.stopPropagation) {
                            e.stopPropagation();
                        }
                    }, styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { fieldGroup: __assign(__assign({}, fluentui_customized_components_1.defultComponentsHeight), { width: this.props.width }), root: __assign({}, fluentui_customized_components_1.defultComponentsHeight), subComponentStyles: {
                            label: __assign({}, fluentui_customized_components_1.defaultLabelStyle),
                        } }), underlined: (_a = this.props.underline) !== null && _a !== void 0 ? _a : false })),
            !this.props.pickerBeforeTextField &&
                (hex == "" ? emptyPicker : picker),
            this.state.open && (React.createElement(react_1.Callout, { target: "#" + ID_PREFIX + pickerId, onDismiss: function () { return _this.setState({ open: !_this.state.open }); } },
                React.createElement(fluentui_color_picker_1.ColorPicker, { store: this.props.store, allowNull: true, onPick: function (color) {
                        if (color == null) {
                            _this.props.onEnter(null);
                        }
                        else {
                            _this.props.onEnter(color);
                        }
                    }, defaultValue: core_1.colorFromHTMLColor(hex), parent: this, closePicker: function () {
                        _this.setState({ open: !_this.state.open });
                    } })))));
    };
    return FluentInputColor;
}(React.Component));
exports.FluentInputColor = FluentInputColor;
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
                        return (React.createElement(popup_controller_1.PopupView, { context: context },
                            React.createElement(fluent_ui_gradient_picker_1.FluentUIGradientPicker, { defaultValue: _this.props.defaultValue, onPick: function (gradient) {
                                    _this.props.onEnter(gradient);
                                } })));
                    }, { anchor: colorButton });
                } },
                React.createElement(components_1.GradientView, { gradient: this.props.defaultValue }))));
    };
    return InputColorGradient;
}(React.Component));
exports.InputColorGradient = InputColorGradient;
//# sourceMappingURL=fluentui_input_color.js.map