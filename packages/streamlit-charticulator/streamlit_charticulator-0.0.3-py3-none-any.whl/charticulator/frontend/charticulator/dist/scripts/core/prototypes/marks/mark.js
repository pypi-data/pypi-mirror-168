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
Object.defineProperty(exports, "__esModule", { value: true });
exports.MarkClass = void 0;
var common_1 = require("../common");
var MarkClass = /** @class */ (function (_super) {
    __extends(MarkClass, _super);
    function MarkClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /** Fill the default state */
    // eslint-disable-next-line
    MarkClass.prototype.initializeState = function () { };
    /** Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    MarkClass.prototype.buildConstraints = function (solver, context, manager) { };
    /** Get the graphical element from the element */
    MarkClass.prototype.getGraphics = function (coordinateSystem, offset, glyphIndex, manager, emphasized) {
        return null;
    };
    /** Get DropZones given current state */
    MarkClass.prototype.getDropZones = function () {
        return [];
    };
    /** Get link anchors for this mark */
    MarkClass.prototype.getLinkAnchors = function (mode) {
        return [];
    };
    /** Get handles given current state */
    MarkClass.prototype.getHandles = function () {
        return [];
    };
    /** Get bounding box */
    MarkClass.prototype.getBoundingBox = function () {
        return null;
    };
    /** Get alignment guides */
    MarkClass.prototype.getSnappingGuides = function () {
        return [];
    };
    MarkClass.prototype.getGlyphClass = function () {
        return this.parent;
    };
    MarkClass.prototype.getPlotSegmentClass = function () {
        return this.parent.parent;
    };
    MarkClass.prototype.getChartClass = function () {
        return this.parent.parent.parent;
    };
    return MarkClass;
}(common_1.ObjectClass));
exports.MarkClass = MarkClass;
//# sourceMappingURL=mark.js.map