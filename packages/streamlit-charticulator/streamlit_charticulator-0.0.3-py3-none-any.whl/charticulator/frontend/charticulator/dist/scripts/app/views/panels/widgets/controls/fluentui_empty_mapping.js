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
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmptyColorButton = exports.EmptyMapping = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
var strings_1 = require("../../../../../strings");
var core_1 = require("../../../../../core");
exports.EmptyMapping = function (_a) {
    var renderColorPicker = _a.renderColorPicker, onClick = _a.onClick, options = _a.options, type = _a.type;
    var render = function () {
        if (options.defaultAuto) {
            return (React.createElement(React.Fragment, null,
                renderColorPicker(),
                type === core_1.Specification.AttributeType.Color ? (React.createElement(EmptyColorInput, { onClick: onClick, label: options.label })) : (React.createElement(react_1.TextField, { id: "id_" + options.label, styles: fluentui_customized_components_1.defaultStyle, label: options.label, onRenderLabel: fluentui_customized_components_1.labelRender, placeholder: strings_1.strings.core.auto, onClick: onClick }))));
        }
        else {
            return (React.createElement(React.Fragment, null,
                renderColorPicker(),
                type === core_1.Specification.AttributeType.Color ? (React.createElement(EmptyColorInput, { onClick: onClick, label: options.label })) : (React.createElement(react_1.TextField, { id: "id_" + options.label, styles: fluentui_customized_components_1.defaultStyle, label: options.label, onRenderLabel: fluentui_customized_components_1.labelRender, placeholder: strings_1.strings.core.none, onClick: onClick }))));
        }
    };
    return React.createElement(React.Fragment, null, render());
};
var EmptyColorInput = function (_a) {
    var label = _a.label, onClick = _a.onClick;
    return (React.createElement("span", { className: "el-color-value" },
        React.createElement(fluentui_customized_components_1.FluentTextField, null,
            React.createElement(react_1.TextField, { id: "id_" + label, styles: fluentui_customized_components_1.defaultStyle, label: label, onRenderLabel: fluentui_customized_components_1.labelRender, placeholder: strings_1.strings.core.none, type: "text", onClick: onClick })),
        React.createElement(exports.EmptyColorButton, { onClick: onClick })));
};
exports.EmptyColorButton = function (_a) {
    var onClick = _a.onClick, styles = _a.styles;
    return (React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: styles === null || styles === void 0 ? void 0 : styles.marginTop },
        React.createElement(react_1.DefaultButton, { iconProps: {
                iconName: "UnSetColor",
            }, styles: {
                root: __assign(__assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize), { marginLeft: 5 }),
            }, onClick: onClick, title: strings_1.strings.mappingEditor.chooseColor })));
};
//# sourceMappingURL=fluentui_empty_mapping.js.map