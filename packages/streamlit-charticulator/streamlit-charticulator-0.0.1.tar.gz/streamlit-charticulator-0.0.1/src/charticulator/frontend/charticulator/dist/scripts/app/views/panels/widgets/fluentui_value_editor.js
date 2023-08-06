"use strict";
/* eslint-disable max-lines-per-function */
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
exports.FluentValueEditor = void 0;
var react_1 = require("@fluentui/react");
var React = require("react");
var core_1 = require("../../../../core");
var fluentui_color_picker_1 = require("../../../components/fluentui_color_picker");
var context_component_1 = require("../../../context_component");
var controls_1 = require("./controls");
var fluentui_input_expression_1 = require("./controls/fluentui_input_expression");
var strings_1 = require("../../../../strings");
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var fluentui_image_1 = require("./controls/fluentui_image");
var fluentui_input_number_1 = require("./controls/fluentui_input_number");
var FluentValueEditor = /** @class */ (function (_super) {
    __extends(FluentValueEditor, _super);
    function FluentValueEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            open: false,
            value: _this.props.type === core_1.Specification.AttributeType.Color
                ? core_1.colorToHTMLColorHEX(_this.props.value)
                : "",
        };
        return _this;
    }
    FluentValueEditor.prototype.emitClearValue = function () {
        this.props.onClear();
    };
    FluentValueEditor.prototype.emitSetValue = function (value) {
        this.props.onEmitValue(value);
    };
    FluentValueEditor.prototype.emitMapping = function (mapping) {
        this.props.onEmitMapping(mapping);
    };
    FluentValueEditor.prototype.componentWillReceiveProps = function (nextProps) {
        var hex = "";
        if (this.props.type === core_1.Specification.AttributeType.Color &&
            nextProps.value) {
            hex = core_1.colorToHTMLColorHEX(nextProps.value);
        }
        if (hex !== this.state.value) {
            this.setState({
                value: hex,
            });
        }
    };
    FluentValueEditor.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var value = this.props.value;
        var placeholderText = this.props.placeholder || strings_1.strings.core.none;
        if (this.props.defaultValue != null) {
            placeholderText = this.props.defaultValue.toString();
        }
        switch (this.props.type) {
            case core_1.Specification.AttributeType.Number: {
                var numberOptions = this.props.numberOptions;
                if (!numberOptions) {
                    numberOptions = {
                        digits: 2,
                    };
                }
                return (React.createElement(fluentui_input_number_1.FluentInputNumber, __assign({ label: this.props.label, stopPropagation: this.props.stopPropagation, placeholder: this.props.placeholder, defaultValue: this.props.value, onEnter: function (newValue) {
                        if (newValue == null) {
                            _this.emitClearValue();
                            return true;
                        }
                        if (newValue == newValue) {
                            _this.emitSetValue(newValue);
                            return true;
                        }
                        else {
                            return false;
                        }
                    } }, numberOptions)));
            }
            case core_1.Specification.AttributeType.Color: {
                var color = value;
                var hex = core_1.colorToHTMLColorHEX(color);
                return (React.createElement("span", { className: "el-color-value" },
                    React.createElement(fluentui_customized_components_1.FluentTextField, null,
                        React.createElement(react_1.TextField, { styles: fluentui_customized_components_1.defaultStyle, label: this.props.label, placeholder: this.props.placeholder, onRenderLabel: fluentui_customized_components_1.labelRender, value: this.state.value, type: "text", onChange: function (event, newValue) {
                                newValue = newValue.trim();
                                if (newValue == "") {
                                    _this.emitClearValue();
                                }
                                else {
                                    _this.setState({
                                        value: newValue,
                                    });
                                    try {
                                        var color_1 = core_1.parseColorOrThrowException(newValue);
                                        if (color_1) {
                                            _this.emitSetValue(color_1);
                                        }
                                        else {
                                            return false;
                                        }
                                    }
                                    catch (ex) {
                                        //ignore
                                    }
                                }
                            }, onKeyDown: function (e) {
                                if (_this.props.stopPropagation) {
                                    e.stopPropagation();
                                }
                            } })),
                    React.createElement("span", { className: "el-color-item", style: { backgroundColor: hex }, id: "color_picker", onClick: function () {
                            _this.setState({ open: !_this.state.open });
                        } }),
                    this.state.open && (React.createElement(react_1.Callout, { target: "#color_picker", onDismiss: function () { return _this.setState({ open: !_this.state.open }); } },
                        React.createElement(fluentui_color_picker_1.ColorPicker, { store: this.store, allowNull: true, defaultValue: core_1.colorFromHTMLColor(hex), onPick: function (color) {
                                if (color == null) {
                                    _this.emitClearValue();
                                }
                                else {
                                    _this.emitSetValue(color);
                                }
                            }, parent: this, closePicker: function () {
                                _this.setState({ open: !_this.state.open });
                            } })))));
            }
            case core_1.Specification.AttributeType.FontFamily:
                return (React.createElement(controls_1.FluentComboBoxFontFamily, { label: this.props.label, defaultValue: value, onEnter: function (value) {
                        _this.emitSetValue(value);
                        return true;
                    } }));
            case core_1.Specification.AttributeType.Text: {
                var str = value;
                if (this.props.onEmitMapping) {
                    return (React.createElement(fluentui_input_expression_1.FluentInputExpression, { label: this.props.label, textExpression: true, validate: function (value) {
                            return _this.context.store.verifyUserExpressionWithTable(value, _this.props.getTable(), { textExpression: true, expectedTypes: ["string"] });
                        }, defaultValue: new core_1.Expression.TextExpression([
                            { string: str },
                        ]).toString(), value: new core_1.Expression.TextExpression([
                            { string: str },
                        ]).toString(), placeholder: placeholderText, allowNull: true, onEnter: function (newValue) {
                            if (newValue == null || newValue.trim() == "") {
                                _this.emitClearValue();
                            }
                            else {
                                if (core_1.Expression.parseTextExpression(newValue).isTrivialString()) {
                                    _this.emitMapping({
                                        type: "value",
                                        value: newValue,
                                    });
                                }
                                else {
                                    _this.emitMapping({
                                        type: "text",
                                        table: _this.props.getTable(),
                                        textExpression: newValue,
                                    });
                                }
                            }
                            return true;
                        }, stopPropagation: this.props.stopPropagation }));
                }
                else {
                    return (React.createElement(React.Fragment, null,
                        React.createElement(react_1.TextField, { label: this.props.label, defaultValue: str, onRenderLabel: fluentui_customized_components_1.labelRender, placeholder: placeholderText, onChange: function (event, newValue) {
                                if (newValue == null) {
                                    _this.emitClearValue();
                                }
                                else {
                                    _this.emitSetValue(newValue);
                                }
                                return true;
                            }, styles: fluentui_customized_components_1.defaultStyle, onKeyDown: function (e) {
                                if (_this.props.stopPropagation) {
                                    e.stopPropagation();
                                }
                            } })));
                }
            }
            case core_1.Specification.AttributeType.Enum: {
                var str = value;
                var strings_2 = this.props.hints.rangeEnum;
                return (React.createElement(react_1.Dropdown, { styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { title: __assign(__assign({}, fluentui_customized_components_1.defaultStyle.title), { lineHeight: fluentui_customized_components_1.defultBindButtonSize.height }) }), label: this.props.label, onRenderLabel: fluentui_customized_components_1.labelRender, selectedKey: str, options: strings_2.map(function (str) {
                        return {
                            key: str,
                            text: str,
                        };
                    }), onChange: function (event, value) {
                        if (value == null) {
                            _this.emitClearValue();
                        }
                        else {
                            _this.emitSetValue(value.key);
                        }
                        return true;
                    } }));
            }
            case core_1.Specification.AttributeType.Boolean: {
                var boolean_1 = value;
                if (this.props.onEmitMapping) {
                    return (React.createElement(React.Fragment, null,
                        React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, strings_1.strings.objects.visibleOn.visibility),
                        React.createElement(react_1.DefaultButton, { styles: {
                                root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                                menuIcon: { display: "none !important" },
                            }, text: strings_1.strings.attributesPanel.conditionedBy, menuProps: {
                                items: (_a = this.props.mainMenuItems) !== null && _a !== void 0 ? _a : [],
                                onRenderMenuList: (_b = this.props.menuRender) !== null && _b !== void 0 ? _b : null,
                            } })));
                }
                else {
                    return (React.createElement(React.Fragment, null,
                        React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, strings_1.strings.objects.visibleOn.visibility),
                        React.createElement(react_1.DefaultButton, { checked: false, iconProps: {
                                iconName: boolean_1 ? "CheckboxComposite" : "Checkbox",
                            }, onClick: function () {
                                _this.emitSetValue(!boolean_1);
                            } })));
                }
            }
            case core_1.Specification.AttributeType.Image: {
                var str = value;
                return (React.createElement(fluentui_image_1.InputImage, { label: this.props.label, value: str, onChange: function (newValue) {
                        if (newValue == null) {
                            _this.emitClearValue();
                        }
                        else {
                            _this.emitSetValue(newValue);
                        }
                        return true;
                    } }));
            }
        }
        return React.createElement("span", null, "(not implemented)");
    };
    return FluentValueEditor;
}(context_component_1.ContextedComponent));
exports.FluentValueEditor = FluentValueEditor;
//# sourceMappingURL=fluentui_value_editor.js.map