"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeIcons = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var fabric_icons_1 = require("./fabric-icons");
var iconAliases_1 = require("./iconAliases");
var DEFAULT_BASE_URL = "https://spoprod-a.akamaihd.net/files/fabric/assets/icons/";
function initializeIcons(baseUrl, options) {
    if (baseUrl === void 0) { baseUrl = DEFAULT_BASE_URL; }
    [fabric_icons_1.initializeIcons].forEach(function (initialize) {
        return initialize(baseUrl, options);
    });
    iconAliases_1.registerIconAliases();
}
exports.initializeIcons = initializeIcons;
//# sourceMappingURL=index.js.map