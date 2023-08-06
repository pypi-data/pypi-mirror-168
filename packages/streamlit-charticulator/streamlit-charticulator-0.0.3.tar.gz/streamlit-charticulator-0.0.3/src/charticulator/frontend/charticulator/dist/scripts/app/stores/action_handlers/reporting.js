"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
var actions_1 = require("../../actions");
var app_store_1 = require("../app_store");
function default_1(REG) {
    REG.add(actions_1.Actions.AddMessage, function (action) {
        this.messageState.set(action.type, action.options.text);
        this.emit(app_store_1.AppStore.EVENT_GRAPHICS);
    });
    REG.add(actions_1.Actions.ClearMessages, function () {
        this.messageState.clear();
        this.emit(app_store_1.AppStore.EVENT_GRAPHICS);
    });
    REG.add(actions_1.Actions.RemoveMessage, function (action) {
        this.messageState.delete(action.type);
        this.emit(app_store_1.AppStore.EVENT_GRAPHICS);
    });
}
exports.default = default_1;
//# sourceMappingURL=reporting.js.map