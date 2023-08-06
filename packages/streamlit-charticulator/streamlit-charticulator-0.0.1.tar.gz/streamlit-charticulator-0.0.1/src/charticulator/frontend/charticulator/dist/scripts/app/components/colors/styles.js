"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ColorsPickerLeftSectionWrapper = exports.ColorsPickerWrapper = exports.ColorsSectionWrapper = exports.PickersSection = exports.PickersSectionWrapper = exports.ColorGridColumnWrapper = exports.ColorGridRowWrapper = exports.NullButtonWrapper = exports.defaultPaletteButtonsStyles = exports.defaultNoneButtonStyles = void 0;
var styled_components_1 = require("styled-components");
exports.defaultNoneButtonStyles = {
    root: {
        border: "unset",
        width: "100%",
        padding: "unset",
        height: 24,
    },
    label: {
        textAlign: "start",
    },
};
exports.defaultPaletteButtonsStyles = {
    root: {
        border: "unset",
        height: 24,
        width: "100%",
    },
    label: {
        textAlign: "start",
        fontWeight: 400,
    },
};
exports.NullButtonWrapper = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid #e6e6e6;\n"], ["\n  border-top: 1px solid #e6e6e6;\n"])));
exports.ColorGridRowWrapper = styled_components_1.default.div(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
exports.ColorGridColumnWrapper = styled_components_1.default.div(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
exports.PickersSectionWrapper = styled_components_1.default.div(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 5px;\n  width: 150px;\n  display: flex;\n  flex-direction: column;\n"], ["\n  margin: 5px;\n  width: 150px;\n  display: flex;\n  flex-direction: column;\n"])));
exports.PickersSection = styled_components_1.default.div(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
exports.ColorsSectionWrapper = styled_components_1.default.div(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 5px;\n"], ["\n  margin: 5px;\n"])));
exports.ColorsPickerWrapper = styled_components_1.default.div(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
exports.ColorsPickerLeftSectionWrapper = styled_components_1.default.div(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  border-right: 1px solid #e6e6e6;\n  display: flex;\n"], ["\n  border-right: 1px solid #e6e6e6;\n  display: flex;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=styles.js.map