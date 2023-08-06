"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
exports.MoveSnappingSession = void 0;
var session_1 = require("./session");
var MoveSnappingSession = /** @class */ (function (_super) {
    __extends(MoveSnappingSession, _super);
    function MoveSnappingSession(handle) {
        return _super.call(this, [], handle, 10, handle.options && handle.options.snapToClosestPoint) || this;
    }
    MoveSnappingSession.prototype.getUpdates = function (actions) {
        var e_1, _a;
        var updates = {};
        try {
            for (var actions_1 = __values(actions), actions_1_1 = actions_1.next(); !actions_1_1.done; actions_1_1 = actions_1.next()) {
                var action = actions_1_1.value;
                updates[action.attribute] = action.value;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (actions_1_1 && !actions_1_1.done && (_a = actions_1.return)) _a.call(actions_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return updates;
    };
    return MoveSnappingSession;
}(session_1.SnappingSession));
exports.MoveSnappingSession = MoveSnappingSession;
//# sourceMappingURL=move.js.map