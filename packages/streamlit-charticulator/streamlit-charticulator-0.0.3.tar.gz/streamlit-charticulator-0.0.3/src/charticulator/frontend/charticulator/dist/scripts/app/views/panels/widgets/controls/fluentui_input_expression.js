"use strict";
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
exports.FluentInputExpression = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../../../core");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
exports.FluentInputExpression = function (props) {
    var _a = __read(React.useState(props.defaultValue), 2), value = _a[0], setValue = _a[1];
    React.useEffect(function () {
        if (props.value || props.value == "") {
            setValue(props.value);
        }
    }, [props.value]);
    var doEnter = React.useCallback(function () {
        var _a, _b;
        if (props.allowNull && (value === null || value === void 0 ? void 0 : value.trim()) == "") {
            setValue("");
            (_a = props.onEnter) === null || _a === void 0 ? void 0 : _a.call(props, null);
        }
        else {
            var result = props.validate(core_1.replaceTabBySymbol(core_1.replaceNewLineBySymbol(value)));
            if (result.pass) {
                setValue(result.formatted);
                (_b = props.onEnter) === null || _b === void 0 ? void 0 : _b.call(props, result.formatted);
            }
        }
    }, [setValue, props, value]);
    var doCancel = React.useCallback(function () {
        var _a;
        setValue(props.defaultValue || "");
        (_a = props.onCancel) === null || _a === void 0 ? void 0 : _a.call(props);
    }, [props, setValue]);
    return (React.createElement("span", { className: "charticulator__widget-control-input-expression" },
        React.createElement(react_1.TextField, { styles: fluentui_customized_components_1.defaultStyle, label: props.label, onRenderLabel: fluentui_customized_components_1.labelRender, placeholder: props.placeholder, type: "text", onGetErrorMessage: function () {
                var _a;
                var validateResults = (_a = props.validate) === null || _a === void 0 ? void 0 : _a.call(props, value);
                if (!validateResults.pass) {
                    return validateResults.error;
                }
            }, value: core_1.replaceSymbolByTab(core_1.replaceSymbolByNewLine(value || (props.allowNull && value == "")
                ? value
                : props.defaultValue)), onChange: function (event, newValue) {
                // Check for parse errors while input
                if (props.allowNull && (newValue === null || newValue === void 0 ? void 0 : newValue.trim()) == "") {
                    setValue(newValue);
                }
                else {
                    core_1.Expression.verifyUserExpression(core_1.replaceTabBySymbol(core_1.replaceNewLineBySymbol(newValue)), {
                        textExpression: props.textExpression,
                    });
                    setValue(newValue);
                }
            }, onBlur: function () {
                doEnter();
            }, onFocus: function (e) {
                e.target.select();
            }, onKeyDown: function (e) {
                if (e.key == "Enter") {
                    doEnter();
                }
                if (e.key == "Escape") {
                    doCancel();
                }
                if (props.stopPropagation) {
                    e.stopPropagation();
                }
            } })));
};
//# sourceMappingURL=fluentui_input_expression.js.map