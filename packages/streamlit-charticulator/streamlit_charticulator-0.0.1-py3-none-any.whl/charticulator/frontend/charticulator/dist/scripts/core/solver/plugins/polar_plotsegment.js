"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.PolarPlotSegmentPlugin = void 0;
var abstract_1 = require("../abstract");
var common_1 = require("../../common");
var update_attribute_1 = require("../../prototypes/update_attribute");
var PolarPlotSegmentPlugin = /** @class */ (function (_super) {
    __extends(PolarPlotSegmentPlugin, _super);
    function PolarPlotSegmentPlugin(attrs, chartConstraints, objectID, manager, properties) {
        var _this = _super.call(this) || this;
        _this.attrs = attrs;
        _this.chartConstraints = chartConstraints;
        _this.objectID = objectID;
        _this.manager = manager;
        _this.properties = properties;
        return _this;
    }
    PolarPlotSegmentPlugin.prototype.apply = function () {
        var _this = this;
        var attrs = this.attrs;
        var angle1 = attrs.angle1, angle2 = attrs.angle2, radial1 = attrs.radial1, radial2 = attrs.radial2, x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        attrs.cx = (x2 + x1) / 2;
        attrs.cy = (y2 + y1) / 2;
        var cx = attrs.cx, cy = attrs.cy;
        var toPoint = function (radius, angle) {
            var radians = common_1.Geometry.degreesToRadians(angle);
            return {
                x: cx + Math.sin(radians) * radius,
                y: cy + Math.cos(radians) * radius,
            };
        };
        var a1r1 = toPoint(radial1, angle1);
        attrs.a1r1x = a1r1.x;
        attrs.a1r1y = a1r1.y;
        var a1r2 = toPoint(radial2, angle1);
        attrs.a1r2x = a1r2.x;
        attrs.a1r2y = a1r2.y;
        var a2r1 = toPoint(radial1, angle2);
        attrs.a2r1x = a2r1.x;
        attrs.a2r1y = a2r1.y;
        var a2r2 = toPoint(radial2, angle2);
        attrs.a2r2x = a2r2.x;
        attrs.a2r2y = a2r2.y;
        // take snapped attributes and apply new value
        [
            "a1r1x",
            "a1r1y",
            "a1r2x",
            "a1r2y",
            "a2r1x",
            "a2r1y",
            "a2r2x",
            "a2r2y",
        ].forEach(function (attrName) {
            update_attribute_1.snapToAttribute(_this.manager, _this.chartConstraints, _this.objectID, attrName, attrs[attrName]);
        });
        return true;
    };
    return PolarPlotSegmentPlugin;
}(abstract_1.ConstraintPlugin));
exports.PolarPlotSegmentPlugin = PolarPlotSegmentPlugin;
//# sourceMappingURL=polar_plotsegment.js.map