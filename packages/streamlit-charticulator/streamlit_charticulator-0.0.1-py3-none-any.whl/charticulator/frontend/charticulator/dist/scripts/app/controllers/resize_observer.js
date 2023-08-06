"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResizeListeners = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var ElementInfo = /** @class */ (function () {
    function ElementInfo(element) {
        var rect = element.getBoundingClientRect();
        this.previousWidth = rect.width;
        this.previousHeight = rect.height;
        this.currentID = 0;
        this.callbacks = new Map();
        this.element = element;
    }
    ElementInfo.prototype.addCallback = function (cb) {
        this.currentID += 1;
        this.callbacks.set(this.currentID, cb);
        return this.currentID;
    };
    ElementInfo.prototype.removeCallback = function (handle) {
        this.callbacks.delete(handle);
    };
    ElementInfo.prototype.timerCallback = function () {
        var rect = this.element.getBoundingClientRect();
        if (rect.width != this.previousWidth ||
            rect.height != this.previousHeight) {
            this.previousWidth = rect.width;
            this.previousHeight = rect.height;
            this.callbacks.forEach(function (cb) {
                cb();
            });
        }
    };
    return ElementInfo;
}());
var ResizeListeners = /** @class */ (function () {
    function ResizeListeners() {
        this.entries = new Map();
        this.timer = setInterval(this.timerCallback.bind(this), 200);
    }
    ResizeListeners.prototype.addListener = function (element, callback) {
        if (this.entries.has(element)) {
            return this.entries.get(element).addCallback(callback);
        }
        else {
            var info = new ElementInfo(element);
            this.entries.set(element, info);
            return info.addCallback(callback);
        }
    };
    ResizeListeners.prototype.removeListener = function (element, handle) {
        if (this.entries.has(element)) {
            var info = this.entries.get(element);
            info.removeCallback(handle);
            if (info.callbacks.size == 0) {
                this.entries.delete(element);
            }
        }
    };
    ResizeListeners.prototype.timerCallback = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.entries), _c = _b.next(); !_c.done; _c = _b.next()) {
                var _d = __read(_c.value, 2), info = _d[1];
                info.timerCallback();
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
    return ResizeListeners;
}());
exports.ResizeListeners = ResizeListeners;
//# sourceMappingURL=resize_observer.js.map