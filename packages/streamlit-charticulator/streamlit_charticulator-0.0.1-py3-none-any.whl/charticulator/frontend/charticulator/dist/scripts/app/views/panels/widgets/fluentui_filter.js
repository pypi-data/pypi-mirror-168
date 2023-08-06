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
Object.defineProperty(exports, "__esModule", { value: true });
exports.FilterPanel = void 0;
var react_1 = require("@fluentui/react");
var React = require("react");
var strings_1 = require("../../../../strings");
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var fluentui_filter_editor_1 = require("./fluentui_filter_editor");
exports.FilterPanel = function (_a) {
    var text = _a.text, options = _a.options, manager = _a.manager;
    var _b = __read(React.useState(false), 2), isOpen = _b[0], setOpen = _b[1];
    switch (options.mode) {
        case "button" /* Button */:
            if (options.value) {
                if (options.value.categories) {
                    text = strings_1.strings.filter.filterBy + options.value.categories.expression;
                }
                if (options.value.expression) {
                    text = strings_1.strings.filter.filterBy + options.value.expression;
                }
            }
            return (React.createElement(React.Fragment, null,
                React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px" },
                    React.createElement(react_1.DefaultButton, { id: "filterTarget", text: text, iconProps: {
                            iconName: "Filter",
                        }, onClick: function () {
                            setOpen(!isOpen);
                        }, styles: {
                            root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight),
                        } })),
                isOpen ? (React.createElement(react_1.Callout, { onDismiss: function () { return setOpen(false); }, target: "#filterTarget", directionalHint: react_1.DirectionalHint.topCenter },
                    React.createElement(fluentui_filter_editor_1.FluentUIFilterEditor, { manager: manager, value: options.value, options: options }))) : null));
        case "panel" /* Panel */:
            return (React.createElement(fluentui_filter_editor_1.FluentUIFilterEditor, { manager: manager, value: options.value, options: options }));
    }
};
//# sourceMappingURL=fluentui_filter.js.map