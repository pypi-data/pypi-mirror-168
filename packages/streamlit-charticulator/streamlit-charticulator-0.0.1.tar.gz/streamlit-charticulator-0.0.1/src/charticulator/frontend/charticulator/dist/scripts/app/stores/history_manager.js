"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.HistoryManager = void 0;
var HistoryManager = /** @class */ (function () {
    function HistoryManager() {
        this.statesBefore = [];
        this.statesAfter = [];
    }
    HistoryManager.prototype.addState = function (state) {
        this.statesAfter = [];
        this.statesBefore.push(state);
    };
    HistoryManager.prototype.undo = function (currentState) {
        if (this.statesBefore.length > 0) {
            var item = this.statesBefore.pop();
            this.statesAfter.push(currentState);
            return item;
        }
        else {
            return null;
        }
    };
    HistoryManager.prototype.redo = function (currentState) {
        if (this.statesAfter.length > 0) {
            var item = this.statesAfter.pop();
            this.statesBefore.push(currentState);
            return item;
        }
        else {
            return null;
        }
    };
    HistoryManager.prototype.clear = function () {
        this.statesAfter = [];
        this.statesBefore = [];
    };
    HistoryManager.prototype.getState = function () {
        return {
            statesAfter: this.statesAfter,
            statesBefore: this.statesBefore,
        };
    };
    HistoryManager.prototype.setState = function (statesAfter, statesBefore) {
        this.statesAfter = statesAfter;
        this.statesBefore = statesBefore;
    };
    return HistoryManager;
}());
exports.HistoryManager = HistoryManager;
//# sourceMappingURL=history_manager.js.map