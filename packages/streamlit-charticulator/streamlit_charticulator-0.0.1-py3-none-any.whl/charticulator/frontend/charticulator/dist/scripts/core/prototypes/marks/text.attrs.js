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
exports.textAttributes = void 0;
var defaults_1 = require("../../../app/stores/defaults");
var specification_1 = require("../../specification");
var attrs_1 = require("../attrs");
exports.textAttributes = __assign(__assign(__assign(__assign({}, attrs_1.AttrBuilder.point()), { text: {
        name: "text",
        type: specification_1.AttributeType.Text,
        solverExclude: true,
        defaultValue: "",
    }, fontFamily: {
        name: "fontFamily",
        type: specification_1.AttributeType.FontFamily,
        solverExclude: true,
        defaultValue: defaults_1.defaultFont,
    }, fontSize: {
        name: "fontSize",
        type: specification_1.AttributeType.Number,
        solverExclude: true,
        defaultRange: [0, 24],
        defaultValue: defaults_1.defaultFontSize,
    }, color: {
        name: "color",
        type: specification_1.AttributeType.Color,
        solverExclude: true,
        defaultValue: null,
    }, backgroundColor: {
        name: "backgroundColor",
        type: specification_1.AttributeType.Color,
        solverExclude: true,
        defaultValue: null,
    }, backgroundColorFilterId: {
        name: "backgroundColorFilterId",
        type: specification_1.AttributeType.Text,
        solverExclude: true,
        defaultValue: null,
    }, outline: {
        name: "outline",
        type: specification_1.AttributeType.Color,
        solverExclude: true,
        defaultValue: null,
    } }), attrs_1.AttrBuilder.opacity()), attrs_1.AttrBuilder.visible());
//# sourceMappingURL=text.attrs.js.map