"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable @typescript-eslint/ban-types */
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
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
exports.Dispatcher = exports.EventEmitter = exports.EventSubscription = void 0;
var EventSubscription = /** @class */ (function () {
    function EventSubscription(emitter, event, listener) {
        this.emitter = emitter;
        this.event = event;
        this.listener = listener;
    }
    EventSubscription.prototype.remove = function () {
        this.emitter.removeSubscription(this);
    };
    return EventSubscription;
}());
exports.EventSubscription = EventSubscription;
var EventEmitter = /** @class */ (function () {
    function EventEmitter() {
        this.eventSubscriptions = new Map();
    }
    EventEmitter.prototype.addListener = function (event, listener) {
        var sub = new EventSubscription(this, event, listener);
        sub.prev = null;
        sub.next = null;
        if (this.eventSubscriptions.has(event)) {
            var head = this.eventSubscriptions.get(event);
            if (head.first == null) {
                head.first = sub;
                head.last = sub;
            }
            else {
                head.last.next = sub;
                sub.prev = head.last;
                head.last = sub;
            }
        }
        else {
            this.eventSubscriptions.set(event, {
                first: sub,
                last: sub,
            });
        }
        return sub;
    };
    EventEmitter.prototype.emit = function (event) {
        var parameters = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            parameters[_i - 1] = arguments[_i];
        }
        if (this.eventSubscriptions.has(event)) {
            var p = this.eventSubscriptions.get(event).first;
            while (p) {
                p.listener.apply(p, __spread(parameters));
                p = p.next;
            }
        }
    };
    EventEmitter.prototype.removeSubscription = function (subscription) {
        var head = this.eventSubscriptions.get(subscription.event);
        if (subscription.prev != null) {
            subscription.prev.next = subscription.next;
        }
        else {
            head.first = subscription.next;
        }
        if (subscription.next != null) {
            subscription.next.prev = subscription.prev;
        }
        else {
            head.last = subscription.prev;
        }
    };
    return EventEmitter;
}());
exports.EventEmitter = EventEmitter;
function compareOrder(a, b) {
    if (a[0] == b[0]) {
        return a[1] - b[1];
    }
    else {
        return a[0] - b[0];
    }
}
var Dispatcher = /** @class */ (function () {
    function Dispatcher() {
        this.registeredItems = new Map();
        this.currentID = 0;
        this.isDispatching = false;
        this.dispatchingIndex = 0;
    }
    Dispatcher.prototype.dispatch = function (action) {
        var e_1, _a;
        if (this.isDispatching) {
            throw new Error("Dispatcher: cannot dispatch in the middle of a dispatch");
        }
        this.isDispatching = true;
        this.dispatchingIndex = 0;
        this.currentAction = action;
        this.registeredItems.forEach(function (x) { return (x.stage = 0); });
        try {
            // Order the items by order of registration
            var items = Array.from(this.registeredItems.values());
            items = items.sort(function (a, b) { return compareOrder(a.order, b.order); });
            try {
                // Dispatch in the order
                for (var items_1 = __values(items), items_1_1 = items_1.next(); !items_1_1.done; items_1_1 = items_1.next()) {
                    var item = items_1_1.value;
                    if (item.stage != 0) {
                        continue;
                    }
                    this.invoke(item);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (items_1_1 && !items_1_1.done && (_a = items_1.return)) _a.call(items_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        finally {
            delete this.currentAction;
            this.isDispatching = false;
        }
    };
    Dispatcher.prototype.invoke = function (item) {
        item.stage = 1;
        item.callback(this.currentAction);
        this.dispatchingIndex += 1;
        item.stage = 2;
    };
    Dispatcher.prototype.register = function (callback, priority) {
        if (priority === void 0) { priority = Dispatcher.PRIORITY_DEFAULT; }
        var id = "ID" + (this.currentID++).toString();
        this.registeredItems.set(id, {
            order: [priority, this.currentID],
            stage: 0,
            callback: callback,
        });
        return id;
    };
    Dispatcher.prototype.unregister = function (id) {
        this.registeredItems.delete(id);
    };
    Dispatcher.prototype.waitFor = function (ids) {
        var e_2, _a;
        var _this = this;
        ids = ids
            .filter(function (a) { return _this.registeredItems.has(a); })
            .sort(function (a, b) {
            return compareOrder(_this.registeredItems.get(a).order, _this.registeredItems.get(b).order);
        });
        try {
            for (var ids_1 = __values(ids), ids_1_1 = ids_1.next(); !ids_1_1.done; ids_1_1 = ids_1.next()) {
                var id = ids_1_1.value;
                var item = this.registeredItems.get(id);
                if (item.stage == 1) {
                    console.warn("Dispatcher: circular dependency detected in waitFor " + id);
                    continue;
                }
                else if (item.stage == 2) {
                    continue;
                }
                this.invoke(item);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (ids_1_1 && !ids_1_1.done && (_a = ids_1.return)) _a.call(ids_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
    };
    Dispatcher.PRIORITY_LOW = 70;
    Dispatcher.PRIORITY_DEFAULT = 50;
    Dispatcher.PRIORITY_HIGH = 30;
    return Dispatcher;
}());
exports.Dispatcher = Dispatcher;
//# sourceMappingURL=events.js.map