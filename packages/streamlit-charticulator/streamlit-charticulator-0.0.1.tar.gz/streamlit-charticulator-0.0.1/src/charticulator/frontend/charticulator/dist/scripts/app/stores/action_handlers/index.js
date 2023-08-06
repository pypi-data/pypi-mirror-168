"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionHandlerRegistry = exports.registerActionHandlers = void 0;
var registry_1 = require("./registry");
Object.defineProperty(exports, "ActionHandlerRegistry", { enumerable: true, get: function () { return registry_1.ActionHandlerRegistry; } });
var chart_1 = require("./chart");
var document_1 = require("./document");
var glyph_1 = require("./glyph");
var mark_1 = require("./mark");
var selection_1 = require("./selection");
var reporting_1 = require("./reporting");
function registerActionHandlers(REG) {
    document_1.default(REG);
    chart_1.default(REG);
    glyph_1.default(REG);
    mark_1.default(REG);
    selection_1.default(REG);
    reporting_1.default(REG);
}
exports.registerActionHandlers = registerActionHandlers;
//# sourceMappingURL=index.js.map