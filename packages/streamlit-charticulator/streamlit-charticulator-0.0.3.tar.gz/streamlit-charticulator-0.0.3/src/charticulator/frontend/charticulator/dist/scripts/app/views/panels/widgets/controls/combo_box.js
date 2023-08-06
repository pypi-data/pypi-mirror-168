"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FluentComboBoxFontFamily = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var core_1 = require("../../../../../core");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
exports.FluentComboBoxFontFamily = function (props) {
    var _a = __read(React.useState(props.defaultValue), 2), currentValue = _a[0], setCurrentValue = _a[1];
    var optionsWithCustomStyling = React.useMemo(function () {
        var currentFontList = __spread(new Set(__spread(core_1.fontList, [currentValue])));
        return currentFontList.map(function (fontName) { return ({
            key: fontName,
            text: fontName,
            styles: {
                optionText: {
                    fontFamily: fontName,
                },
                root: __assign(__assign({}, fluentui_customized_components_1.defultComponentsHeight), { minHeight: fluentui_customized_components_1.defultComponentsHeight.height }),
            },
        }); });
    }, [currentValue]);
    var onCancel = React.useCallback(function () { var _a; return (_a = props.onCancel) === null || _a === void 0 ? void 0 : _a.call(props); }, [props]);
    var onEnter = React.useCallback(function (event, value) {
        var _a, _b, _c;
        var currentInputValue = event.target.value;
        var currentFontValue = (_b = (_a = value === null || value === void 0 ? void 0 : value.key) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : (currentInputValue.length > 0 ? currentInputValue : props.defaultValue);
        setCurrentValue(currentFontValue);
        (_c = props.onEnter) === null || _c === void 0 ? void 0 : _c.call(props, currentFontValue);
    }, [props]);
    return (React.createElement(react_1.ComboBox, { styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { root: __assign({}, fluentui_customized_components_1.defultComponentsHeight) }), selectedKey: currentValue, label: props.label, onRenderLabel: function (_a) {
            var props = _a.props;
            return (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, props.label));
        }, autoComplete: "on", options: optionsWithCustomStyling, onChange: onEnter, onAbort: onCancel, allowFreeform: true }));
};
//# sourceMappingURL=combo_box.js.map