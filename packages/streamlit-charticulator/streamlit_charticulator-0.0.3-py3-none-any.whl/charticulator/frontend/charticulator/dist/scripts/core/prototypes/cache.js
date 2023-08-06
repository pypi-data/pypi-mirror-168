"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ObjectClassCache = void 0;
var object_1 = require("./object");
var ObjectClassCache = /** @class */ (function () {
    function ObjectClassCache() {
        this.cache = new WeakMap();
    }
    /** Clear the cache */
    ObjectClassCache.prototype.clear = function () {
        this.cache = new WeakMap();
    };
    ObjectClassCache.prototype.hasClass = function (state) {
        return this.cache.has(state);
    };
    ObjectClassCache.prototype.getMarkClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getGlyphClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getPlotSegmentClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getChartElementClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getScaleClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getChartClass = function (state) {
        return this.getClass(state);
    };
    ObjectClassCache.prototype.getClass = function (state) {
        if (this.cache.has(state)) {
            return this.cache.get(state);
        }
        else {
            throw new Error("class not found for state");
        }
    };
    ObjectClassCache.prototype.createMarkClass = function (parent, object, state) {
        return this.createClass(parent, object, state);
    };
    ObjectClassCache.prototype.createGlyphClass = function (parent, object, state) {
        return this.createClass(parent, object, state);
    };
    ObjectClassCache.prototype.createPlotSegmentClass = function (parent, object, state) {
        return (this.createClass(parent, object, state));
    };
    ObjectClassCache.prototype.createChartElementClass = function (parent, object, state) {
        return this.createClass(parent, object, state);
    };
    ObjectClassCache.prototype.createScaleClass = function (parent, object, state) {
        return this.createClass(parent, object, state);
    };
    ObjectClassCache.prototype.createChartClass = function (parent, object, state) {
        return this.createClass(parent, object, state);
    };
    ObjectClassCache.prototype.createClass = function (parent, object, state) {
        var newClass = object_1.ObjectClasses.Create(parent, object, state);
        this.cache.set(state, newClass);
        return newClass;
    };
    return ObjectClassCache;
}());
exports.ObjectClassCache = ObjectClassCache;
//# sourceMappingURL=cache.js.map