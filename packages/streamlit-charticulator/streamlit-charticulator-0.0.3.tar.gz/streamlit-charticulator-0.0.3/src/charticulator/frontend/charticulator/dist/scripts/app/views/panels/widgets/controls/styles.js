"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ToolTipHostStyles = exports.ImageMappingTextFieldStyles = exports.ImageMappingDragStateWrapper = void 0;
var styled_components_1 = require("styled-components");
exports.ImageMappingDragStateWrapper = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: 1px solid #fa9e13;\n  padding-left: 4px;\n  width: 96%;\n  background: #fa9e136b;\n"], ["\n  border: 1px solid #fa9e13;\n  padding-left: 4px;\n  width: 96%;\n  background: #fa9e136b;\n"])));
exports.ImageMappingTextFieldStyles = {
    root: {
        height: 25,
    },
    wrapper: {
        height: 25,
    },
    field: {
        height: 25,
    },
};
exports.ToolTipHostStyles = {
    root: {
        width: "100%",
        display: "unset",
        paddingLeft: "4px",
        paddingRight: "4px",
    },
};
var templateObject_1;
//# sourceMappingURL=styles.js.map