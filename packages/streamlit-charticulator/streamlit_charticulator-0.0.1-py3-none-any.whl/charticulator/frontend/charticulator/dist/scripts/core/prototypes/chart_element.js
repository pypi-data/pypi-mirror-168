"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable */
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChartElementClass = void 0;
var object_1 = require("./object");
var ChartElementClass = /** @class */ (function (_super) {
    __extends(ChartElementClass, _super);
    function ChartElementClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /** Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    ChartElementClass.prototype.buildConstraints = function (solver, context, manager) { };
    /** Get the graphics that represent this layout */
    ChartElementClass.prototype.getGraphics = function (manager) {
        return null;
    };
    /** Get handles given current state */
    ChartElementClass.prototype.getHandles = function () {
        return [];
    };
    ChartElementClass.prototype.getBoundingBox = function () {
        return null;
    };
    ChartElementClass.prototype.getSnappingGuides = function () {
        return [];
    };
    ChartElementClass.prototype.getDropZones = function () {
        return [];
    };
    /** Get controls given current state */
    ChartElementClass.prototype.getPopupEditor = function (manager) {
        return null;
    };
    ChartElementClass.createDefault = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var element = _super.createDefault.apply(this, __spread(args));
        return element;
    };
    return ChartElementClass;
}(object_1.ObjectClass));
exports.ChartElementClass = ChartElementClass;
//# sourceMappingURL=chart_element.js.map