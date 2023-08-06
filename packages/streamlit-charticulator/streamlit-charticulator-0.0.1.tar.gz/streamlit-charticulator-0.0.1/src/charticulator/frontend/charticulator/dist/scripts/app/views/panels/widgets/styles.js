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
exports.onRenderTitle = exports.onRenderOption = exports.iconStyles = exports.dropdownStyles = void 0;
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var Icon_1 = require("@fluentui/react/lib/Icon");
var React = require("react");
var components_1 = require("../../../../app/components");
var R = require("../../../../app/resources");
exports.dropdownStyles = function (options) {
    return {
        title: __assign(__assign({}, fluentui_customized_components_1.defultComponentsHeight), { borderWidth: options.hideBorder ? "0px" : null }),
        dropdownItemsWrapper: {
            minWidth: 90,
        },
        callout: {
            marginTop: options.shiftCallout ? options.shiftCallout : null,
        },
    };
};
exports.iconStyles = { marginRight: "8px" };
exports.onRenderOption = function (option) {
    return (React.createElement(React.Fragment, null,
        option.data && option.data.icon && (React.createElement(fluentui_customized_components_1.FluentDropdown, null, option.data.isLocalIcons ? (React.createElement("span", { style: exports.iconStyles },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(option.data.icon) }))) : (React.createElement(Icon_1.Icon, { style: exports.iconStyles, iconName: option.data.icon, "aria-hidden": "true", title: option.data.icon })))),
        React.createElement("span", null, option.text)));
};
exports.onRenderTitle = function (options) {
    var option = options[0];
    return (React.createElement(fluentui_customized_components_1.FluentDropdownWrapper, null,
        option.data && option.data.icon && (React.createElement(fluentui_customized_components_1.FluentDropdown, null, option.data.isLocalIcons ? (React.createElement("span", { style: exports.iconStyles },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(option.data.icon) }))) : (React.createElement(Icon_1.Icon, { style: exports.iconStyles, iconName: option.data.icon, "aria-hidden": "true", title: option.data.icon })))),
        React.createElement("span", null, option.text)));
};
//# sourceMappingURL=styles.js.map