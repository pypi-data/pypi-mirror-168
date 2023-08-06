"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
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
exports.PanelHeaderStyles = exports.defaultStyle = exports.FluentDatePickerWrapper = exports.FluentDropdownWrapper = exports.FluentDropdown = exports.PlaceholderStyle = exports.groupStyles = exports.groupHeaderStyles = exports.defultComponentsHeight = exports.FluentGroupedList = exports.NestedChartButtonsWrapper = exports.labelRender = exports.defaultLabelStyle = exports.defaultFontWeight = exports.FluentLayoutItem = exports.FluentColumnLayout = exports.FluentDataBindingMenuLabel = exports.FluentDataBindingMenuItem = exports.FluentRowLayout = exports.FluentCheckbox = exports.FluentTextField = exports.FluentActionButton = exports.FluentLabelHeader = exports.FluentButton = exports.defultBindButtonSize = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var styled_components_1 = require("styled-components");
exports.defultBindButtonSize = {
    height: "24px",
    width: "24px",
};
exports.FluentButton = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n  margin-left: ", ";\n  display: inline-block;\n  padding: 0px ", " 0px 0px;\n  height: ", ";\n  line-height: ", ";\n  button {\n    padding: 4px;\n  }\n"], ["\n  margin-top: ", ";\n  margin-left: ", ";\n  display: inline-block;\n  padding: 0px ", " 0px 0px;\n  height: ", ";\n  line-height: ", ";\n  button {\n    padding: 4px;\n  }\n"])), function (_a) {
    var marginTop = _a.marginTop;
    return marginTop || "24px";
}, function (_a) {
    var marginLeft = _a.marginLeft;
    return marginLeft || "unset";
}, function (_a) {
    var paddingRight = _a.paddingRight;
    return paddingRight || "4px";
}, exports.defultBindButtonSize.height, exports.defultBindButtonSize.height);
exports.FluentLabelHeader = styled_components_1.default.div(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: ", ";\n  margin-right: ", ";\n"], ["\n  margin-bottom: ", ";\n  margin-top: ", ";\n  margin-right: ", ";\n"])), function (_a) {
    var marginBottom = _a.marginBottom;
    return marginBottom || "24px";
}, function (_a) {
    var marginTop = _a.marginTop;
    return marginTop || "20px";
}, function (_a) {
    var marginLeft = _a.marginRight;
    return marginLeft || "2px";
});
exports.FluentActionButton = styled_components_1.default.div(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  button {\n    border: 1px solid;\n    width: 100%;\n    overflow: hidden;\n  }\n"], ["\n  button {\n    border: 1px solid;\n    width: 100%;\n    overflow: hidden;\n  }\n"])));
exports.FluentTextField = styled_components_1.default.div(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n  * {\n    flex: 1;\n  }\n"], ["\n  flex: 1;\n  * {\n    flex: 1;\n  }\n"])));
exports.FluentCheckbox = styled_components_1.default.div(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: 2px;\n"], ["\n  margin-bottom: 2px;\n"])));
exports.FluentRowLayout = styled_components_1.default.div(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
exports.FluentDataBindingMenuItem = styled_components_1.default.div(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: stretch;\n  justify-content: center;\n  height: 26px;\n  line-height: unset;\n  background-color: ", ";\n  &:hover {\n    background-color: ", ";\n  }\n  .ms-Dropdown-container {\n    margin-top: 2px;\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: stretch;\n  justify-content: center;\n  height: 26px;\n  line-height: unset;\n  background-color: ", ";\n  &:hover {\n    background-color: ",
    ";\n  }\n  .ms-Dropdown-container {\n    margin-top: 2px;\n  }\n"])), function (_a) {
    var backgroundColor = _a.backgroundColor;
    return backgroundColor || null;
}, function (_a) {
    var backgroundColorHover = _a.backgroundColorHover;
    return backgroundColorHover || null;
});
exports.FluentDataBindingMenuLabel = styled_components_1.default.div(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n  margin-left: 5px;\n"], ["\n  flex: 1;\n  margin-left: 5px;\n"])));
exports.FluentColumnLayout = styled_components_1.default.div(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
exports.FluentLayoutItem = styled_components_1.default.div(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  flex: ", ";\n"], ["\n  flex: ", ";\n"])), function (_a) {
    var flex = _a.flex;
    return flex || "1";
});
exports.defaultFontWeight = 400;
exports.defaultLabelStyle = {
    root: {
        fontWeight: exports.defaultFontWeight,
        lineHeight: "unset",
    },
};
exports.labelRender = function (_a) {
    var label = _a.label;
    return (label ? React.createElement(react_1.Label, { styles: exports.defaultLabelStyle }, label) : null);
};
exports.NestedChartButtonsWrapper = styled_components_1.default.div(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-top: 5px;\n"], ["\n  margin-top: 5px;\n"])));
exports.FluentGroupedList = styled_components_1.default.div(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  .charticulator__widget-collapsible-panel-item {\n    margin-left: ", ";\n    margin-right: 15px;\n    min-width: 270px;\n  }\n\n  .ms-List-surface .ms-List-cell .ms-List-cell:last-child {\n    margin-bottom: 5px;\n  }\n\n  .ms-List-surface .ms-List-page .ms-List-cell {\n    min-height: 24px;\n  }\n"], ["\n  .charticulator__widget-collapsible-panel-item {\n    margin-left: ",
    ";\n    margin-right: 15px;\n    min-width: 270px;\n  }\n\n  .ms-List-surface .ms-List-cell .ms-List-cell:last-child {\n    margin-bottom: 5px;\n  }\n\n  .ms-List-surface .ms-List-page .ms-List-cell {\n    min-height: 24px;\n  }\n"])), function (_a) {
    var marginLeft = _a.marginLeft;
    return marginLeft != null ? marginLeft : "25px";
});
exports.defultComponentsHeight = {
    height: "24px",
    lineHeight: "unset",
};
exports.groupHeaderStyles = {
    title: {
        fontWeight: 600,
    },
    headerCount: {
        display: "none",
    },
    groupHeaderContainer: __assign({}, exports.defultComponentsHeight),
    expand: __assign(__assign({}, exports.defultBindButtonSize), { fontSize: "unset" }),
    dropIcon: {
        display: "none",
    },
};
exports.groupStyles = {
    group: {
        borderTop: "1px #C8C6C4 solid",
    },
};
exports.PlaceholderStyle = styled_components_1.default.div(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  input {\n    ::-webkit-input-placeholder {\n      /* Chrome/Opera/Safari */\n      color: ", ";\n    }\n    ::-moz-placeholder {\n      /* Firefox 19+ */\n      color: ", ";\n    }\n    :-ms-input-placeholder {\n      /* IE 10+ */\n      color: ", ";\n    }\n    :-moz-placeholder {\n      /* Firefox 18- */\n      color: ", ";\n    }\n  }\n"], ["\n  input {\n    ::-webkit-input-placeholder {\n      /* Chrome/Opera/Safari */\n      color: ", ";\n    }\n    ::-moz-placeholder {\n      /* Firefox 19+ */\n      color: ", ";\n    }\n    :-ms-input-placeholder {\n      /* IE 10+ */\n      color: ", ";\n    }\n    :-moz-placeholder {\n      /* Firefox 18- */\n      color: ", ";\n    }\n  }\n"])), function (_a) {
    var color = _a.color;
    return color || "lightgray";
}, function (_a) {
    var color = _a.color;
    return color || "lightgray";
}, function (_a) {
    var color = _a.color;
    return color || "lightgray";
}, function (_a) {
    var color = _a.color;
    return color || "lightgray";
});
exports.FluentDropdown = styled_components_1.default.div(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  & svg {\n    stroke: rgb(128, 128, 128) !important;\n    fill: rgb(128, 128, 128) !important;\n  }\n  display: inline;\n"], ["\n  & svg {\n    stroke: rgb(128, 128, 128) !important;\n    fill: rgb(128, 128, 128) !important;\n  }\n  display: inline;\n"])));
exports.FluentDropdownWrapper = styled_components_1.default.div(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  height: 20px;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  height: 20px;\n"])));
exports.FluentDatePickerWrapper = styled_components_1.default.div(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  .ms-TextField-fieldGroup {\n    height: 24px;\n  }\n  i {\n    padding: 4px 5px 5px;\n    line-height: unset;\n  }\n"], ["\n  .ms-TextField-fieldGroup {\n    height: 24px;\n  }\n  i {\n    padding: 4px 5px 5px;\n    line-height: unset;\n  }\n"])));
exports.defaultStyle = {
    field: {
        defultComponentsHeight: exports.defultComponentsHeight,
        height: "20px",
    },
    fieldGroup: exports.defultComponentsHeight,
    dropdown: __assign({ boxSizing: "unset" }, exports.defultComponentsHeight),
    dropdownOptionText: __assign({ boxSizing: "unset" }, exports.defultComponentsHeight),
    dropdownItem: __assign({ boxSizing: "unset", minHeight: "25px" }, exports.defultComponentsHeight),
    dropdownItemHeader: __assign({ boxSizing: "unset" }, exports.defultComponentsHeight),
    dropdownItemSelected: __assign({ boxSizing: "unset", minHeight: "24px", lineHeight: "24px" }, exports.defultComponentsHeight),
    caretDown: __assign({ boxSizing: "unset" }, exports.defultComponentsHeight),
    caretDownWrapper: __assign({ boxSizing: "unset", marginTop: "5px" }, exports.defultComponentsHeight),
    title: __assign(__assign({ boxSizing: "unset" }, exports.defultComponentsHeight), { height: "22px", lineHeight: "unset" }),
    label: {
        lineHeight: "unset",
    },
};
exports.PanelHeaderStyles = {
    root: {
        border: "unset",
        height: 24,
        width: 24,
        display: "inline",
        padding: 0,
        minWidth: 24,
    },
    textContainer: {
        flexGrow: "unset",
    },
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=fluentui_customized_components.js.map