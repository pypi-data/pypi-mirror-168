"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.register = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var polar_line_1 = require("./polar_line");
var colorFilter_1 = require("./colorFilter");
function register(f) {
    f("Graphics/PolarLine", polar_line_1.PolarLineTestView);
    f("Graphics/ColorFilter", colorFilter_1.ColorFilterTestView);
}
exports.register = register;
//# sourceMappingURL=index.js.map