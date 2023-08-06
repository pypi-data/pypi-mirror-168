"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.FluentInputNumber = void 0;
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var react_1 = require("@fluentui/react");
var React = require("react");
var core_1 = require("../../../../../core");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
exports.FluentInputNumber = function (props) {
    var _a = __read(React.useState(props.defaultValue), 2), value = _a[0], setValue = _a[1];
    React.useEffect(function () {
        setValue(props.defaultValue);
    }, [props.defaultValue]);
    var formatNumber = function (value) {
        if (value == null) {
            return "";
        }
        if (value != value) {
            return "N/A";
        }
        if (props.percentage) {
            return core_1.prettyNumber(value * 100, props.digits != null ? props.digits : 2);
        }
        else {
            return core_1.prettyNumber(value, props.digits != null ? props.digits : 2);
        }
    };
    var parseNumber = function (str) {
        str = str.trim();
        if (str == "" || isNaN(+str)) {
            return null;
        }
        if (props.percentage) {
            str = str.replace(/%$/, "");
            return +str / 100;
        }
        else {
            return +str;
        }
    };
    var reportValue = function (value) {
        if (value == null) {
            return props.onEnter(value);
        }
        else {
            if (props.minimum != null) {
                value = Math.max(props.minimum, value);
            }
            if (props.maximum != null) {
                value = Math.min(props.maximum, value);
            }
            return props.onEnter(value);
        }
    };
    var renderSlider = function () {
        var sliderMin = 0;
        var sliderMax = 1;
        if (props.minimum != null) {
            sliderMin = props.minimum;
        }
        if (props.maximum != null) {
            sliderMax = props.maximum;
        }
        if (props.percentage) {
            sliderMax = 1;
            sliderMin = 0;
        }
        if (props.sliderRange != null) {
            sliderMin = props.sliderRange[0];
            sliderMax = props.sliderRange[1];
        }
        return (React.createElement(react_1.Slider, { styles: {
                root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                slideBox: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
            }, min: sliderMin, max: sliderMax, value: +value, showValue: true, step: props.percentage ? 0.01 : props.step != undefined ? props.step : 1, onChange: function (newValue) {
                setValue(+newValue.toFixed(4));
                reportValue(newValue);
            } }));
    };
    var renderUpdown = function () {
        var tick = props.updownTick || 0.1;
        return (React.createElement(React.Fragment, null,
            React.createElement(react_1.SpinButton, { label: !props.showSlider ? props.label : null, labelPosition: react_1.Position.top, value: formatNumber(+value), iconProps: props.updownStyle == "font"
                    ? {
                        iconName: "Font",
                    }
                    : null, step: tick, onIncrement: function (value) {
                    if (reportValue(parseNumber(value) + tick)) {
                        setValue(parseNumber(value) + tick);
                    }
                }, onDecrement: function (value) {
                    if (reportValue(parseNumber(value) - tick)) {
                        setValue(parseNumber(value) - tick);
                    }
                }, onValidate: function (value) {
                    var num = parseNumber(value);
                    if (reportValue(num)) {
                        var val = num;
                        if (props.minimum != null) {
                            val = Math.max(props.minimum, num);
                        }
                        if (props.maximum != null) {
                            val = Math.min(props.maximum, num);
                        }
                        setValue(val);
                        return formatNumber(parseNumber(value));
                    }
                }, styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { label: {
                        lineHeight: "unset",
                        fontWeight: fluentui_customized_components_1.defaultFontWeight,
                        height: 25,
                    }, spinButtonWrapper: {
                        height: fluentui_customized_components_1.defaultStyle.fieldGroup.height,
                        lineHeight: fluentui_customized_components_1.defaultStyle.fieldGroup.lineHeight,
                    } }) })));
    };
    return (React.createElement(React.Fragment, null,
        props.showSlider ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, props.label)) : null,
        React.createElement(fluentui_customized_components_1.FluentRowLayout, { style: props.styles },
            React.createElement(fluentui_customized_components_1.FluentLayoutItem, { flex: 1 }, props.showUpdown ? (renderUpdown()) : (React.createElement(fluentui_customized_components_1.PlaceholderStyle, null,
                React.createElement(react_1.TextField, { styles: fluentui_customized_components_1.defaultStyle, onRenderLabel: fluentui_customized_components_1.labelRender, label: !props.showSlider ? props.label : null, placeholder: props.placeholder, value: typeof value === "string" &&
                        (value.indexOf(".") === value.length - 1 ||
                            (value.indexOf("-") === 0 &&
                                value.length === 1))
                        ? value
                        : value == null
                            ? null
                            : formatNumber(+value), onChange: function (event, str) {
                        if ((str != "" && str.indexOf(".") === str.length - 1) ||
                            (str.indexOf("-") === 0 && str.length === 1)) {
                            setValue(str);
                        }
                        else {
                            var num = parseNumber(str);
                            if (reportValue(num)) {
                                setValue(num);
                            }
                        }
                    }, onKeyDown: function (e) {
                        if (props.stopPropagation) {
                            e.stopPropagation();
                        }
                    }, suffix: props.percentage ? "%" : undefined })))),
            props.showSlider ? (React.createElement(fluentui_customized_components_1.FluentLayoutItem, { flex: 2 }, renderSlider())) : null)));
};
//# sourceMappingURL=fluentui_input_number.js.map