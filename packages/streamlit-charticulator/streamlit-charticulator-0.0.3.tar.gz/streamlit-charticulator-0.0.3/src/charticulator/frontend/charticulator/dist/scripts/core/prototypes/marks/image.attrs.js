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
exports.imageAttributes = void 0;
var attrs_1 = require("../attrs");
exports.imageAttributes = __assign(__assign(__assign(__assign(__assign({}, attrs_1.AttrBuilder.line()), attrs_1.AttrBuilder.center()), attrs_1.AttrBuilder.size()), attrs_1.AttrBuilder.style({ fill: true })), attrs_1.AttrBuilder.image());
//# sourceMappingURL=image.attrs.js.map