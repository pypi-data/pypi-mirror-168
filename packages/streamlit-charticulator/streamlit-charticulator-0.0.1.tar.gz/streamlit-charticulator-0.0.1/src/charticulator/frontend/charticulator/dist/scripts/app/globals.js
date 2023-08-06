"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LocalStorageKeys = exports.resizeListeners = exports.popupController = exports.dragController = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var controllers_1 = require("./controllers");
exports.dragController = new controllers_1.DragController();
exports.popupController = new controllers_1.PopupController();
exports.resizeListeners = new controllers_1.ResizeListeners();
var LocalStorageKeys;
(function (LocalStorageKeys) {
    LocalStorageKeys["NumberFormatRemove"] = "numberFormatRemove";
    LocalStorageKeys["DelimiterSymbol"] = "delimiterSymbol";
    LocalStorageKeys["CurrencySymbol"] = "currencySymbol";
    LocalStorageKeys["GroupSymbol"] = "groupSymbol";
    LocalStorageKeys["UtcTimeZone"] = "utcTimeZone";
})(LocalStorageKeys = exports.LocalStorageKeys || (exports.LocalStorageKeys = {}));
//# sourceMappingURL=globals.js.map