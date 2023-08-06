"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.UIManagerListener = exports.EventManager = exports.EventType = void 0;
var EventType;
(function (EventType) {
    EventType[EventType["UPDATE_FIELD"] = 0] = "UPDATE_FIELD";
})(EventType = exports.EventType || (exports.EventType = {}));
var EventManager = /** @class */ (function () {
    function EventManager() {
        this.listeners = [];
    }
    EventManager.prototype.subscribe = function (type, listener) {
        this.listeners.push({
            listener: listener,
            type: type,
        });
    };
    EventManager.prototype.notify = function (type, property, value) {
        for (var i = 0; i < this.listeners.length; i++) {
            if (this.listeners[i].type === type) {
                this.listeners[i].listener.update(property, value);
            }
        }
    };
    return EventManager;
}());
exports.EventManager = EventManager;
var UIManagerListener = /** @class */ (function () {
    function UIManagerListener(manager) {
        this.manager = manager;
    }
    UIManagerListener.prototype.update = function (property, value) {
        this.manager.emitSetProperty(property, value);
    };
    return UIManagerListener;
}());
exports.UIManagerListener = UIManagerListener;
//# sourceMappingURL=observer.js.map