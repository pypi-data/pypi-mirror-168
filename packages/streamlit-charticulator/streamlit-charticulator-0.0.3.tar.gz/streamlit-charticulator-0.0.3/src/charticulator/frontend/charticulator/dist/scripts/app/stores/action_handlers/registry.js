"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionHandlerRegistry = void 0;
/** A registry of action handlers */
var ActionHandlerRegistry = /** @class */ (function () {
    function ActionHandlerRegistry() {
        this.handlers = [];
    }
    /**
     * Register an action handler function
     * @param constructor the action constructor
     * @param handler the action handler
     */
    ActionHandlerRegistry.prototype.add = function (constructor, handler) {
        this.handlers.push({ constructor: constructor, handler: handler });
    };
    /**
     * Find and call the handler(s) for the action
     * @param thisArg the this argument for the handler
     * @param action the action to pass to
     */
    ActionHandlerRegistry.prototype.handleAction = function (thisArg, action) {
        var e_1, _a;
        try {
            for (var _b = __values(this.handlers), _c = _b.next(); !_c.done; _c = _b.next()) {
                var handler = _c.value;
                if (action instanceof handler.constructor) {
                    handler.handler.call(thisArg, action);
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    return ActionHandlerRegistry;
}());
exports.ActionHandlerRegistry = ActionHandlerRegistry;
//# sourceMappingURL=registry.js.map