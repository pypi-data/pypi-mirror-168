"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CustomGradientButtonsWrapper = exports.ColorGradientWrapper = exports.ColorCell = exports.ColorRowWrapper = exports.TabWrapper = exports.PalettesWrapper = exports.colorTextInputStyles = exports.dropdownStyles = exports.deleteColorStyles = exports.colorPalettesLabelStyles = exports.defaultActionButtonsStyles = void 0;
var styled_components_1 = require("styled-components");
exports.defaultActionButtonsStyles = {
    root: {
        height: 24,
        marginRight: 5,
    },
};
exports.colorPalettesLabelStyles = {
    root: {
        marginLeft: 5,
        display: "inline-block",
        fontWeight: 400,
        cursor: "pointer",
    },
};
exports.deleteColorStyles = {
    root: {
        height: 20,
        width: 20,
        minWidth: "unset",
        padding: "unset",
        border: "unset",
    },
};
exports.dropdownStyles = {
    root: {
        display: "inline-block",
        height: 24,
        width: "100%",
    },
    dropdown: {
        height: 24,
    },
    title: {
        lineHeight: 24,
        height: 24,
        fontWeight: 600,
    },
    caretDown: {
        lineHeight: 24,
        height: 24,
    },
};
exports.colorTextInputStyles = {
    root: {
        display: "inline-block",
        height: "unset",
        marginLeft: 5,
        marginRight: 5,
    },
    fieldGroup: {
        height: "unset",
    },
};
exports.PalettesWrapper = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n\n  &:hover {\n    background-color: #f3f2f1;\n  }\n"], ["\n  cursor: pointer;\n\n  &:hover {\n    background-color: #f3f2f1;\n  }\n"])));
exports.TabWrapper = styled_components_1.default.div(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-height: 300px;\n  overflow-y: auto;\n"], ["\n  max-height: 300px;\n  overflow-y: auto;\n"])));
exports.ColorRowWrapper = styled_components_1.default.div(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: 5px;\n  display: flex;\n"], ["\n  margin-top: 5px;\n  display: flex;\n"])));
exports.ColorCell = styled_components_1.default.span(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  width: 20px;\n  height: 20px;\n  display: inline-block;\n  cursor: pointer;\n  border: 1px solid #8a8886;\n  margin-right: 5px;\n"], ["\n  background: ", ";\n  width: 20px;\n  height: 20px;\n  display: inline-block;\n  cursor: pointer;\n  border: 1px solid #8a8886;\n  margin-right: 5px;\n"])), function (props) { return props.$color; });
exports.ColorGradientWrapper = styled_components_1.default.span(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 50%;\n  cursor: pointer;\n"], ["\n  width: 50%;\n  cursor: pointer;\n"])));
exports.CustomGradientButtonsWrapper = styled_components_1.default.div(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  margin-top: 10px;\n"], ["\n  display: flex;\n  margin-top: 10px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=styles.js.map