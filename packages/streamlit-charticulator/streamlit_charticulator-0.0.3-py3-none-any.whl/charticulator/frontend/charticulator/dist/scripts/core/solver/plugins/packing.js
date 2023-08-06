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
Object.defineProperty(exports, "__esModule", { value: true });
exports.PackingPlugin = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var d3_force_1 = require("d3-force");
var abstract_1 = require("../abstract");
var PackingPlugin = /** @class */ (function (_super) {
    __extends(PackingPlugin, _super);
    function PackingPlugin(solver, cx, cy, points, axisOnly, getXYScale, options) {
        var _this = _super.call(this) || this;
        _this.solver = solver;
        _this.cx = cx;
        _this.cy = cy;
        _this.points = points;
        _this.xEnable = axisOnly == null || axisOnly == "x";
        _this.yEnable = axisOnly == null || axisOnly == "y";
        _this.getXYScale = getXYScale;
        _this.gravityX = options.gravityX;
        _this.gravityY = options.gravityY;
        _this.boxed = options.boxed;
        return _this;
    }
    PackingPlugin.prototype.apply = function () {
        var _this = this;
        var xScale = 1;
        var yScale = 1;
        if (this.getXYScale != null) {
            var _a = this.getXYScale(), x = _a.x, y = _a.y;
            xScale = x;
            yScale = y;
        }
        var cx = this.solver.getValue(this.cx);
        var cy = this.solver.getValue(this.cy);
        var nodes = this.points.map(function (pt) {
            var x = (_this.solver.getValue(pt[0]) - cx) / xScale;
            var y = (_this.solver.getValue(pt[1]) - cy) / yScale;
            // Use forceSimulation's default initialization
            return {
                fx: !_this.xEnable ? x : undefined,
                fy: !_this.yEnable ? y : undefined,
                r: pt[2],
            };
        });
        var force = d3_force_1.forceSimulation(nodes);
        force.force("collision", d3_force_1.forceCollide(function (d) { return d.r; }));
        force.force("gravityX", d3_force_1.forceX().strength(this.gravityX || 0.1));
        force.force("gravityY", d3_force_1.forceY().strength(this.gravityY || 0.1));
        force.stop();
        var n = Math.ceil(Math.log(force.alphaMin()) / Math.log(1 - force.alphaDecay()));
        for (var i = 0; i < n * 2; i++) {
            force.tick();
        }
        for (var i = 0; i < nodes.length; i++) {
            if (this.xEnable) {
                if (this.boxed && this.boxed.x1 != null && this.boxed.x2 != null) {
                    if (nodes[i].x < (this.boxed.x1 - cx) / xScale) {
                        nodes[i].x = (this.boxed.x1 - cx) / xScale;
                    }
                    else if (nodes[i].x > (this.boxed.x2 - cx) / xScale) {
                        nodes[i].x = (this.boxed.x2 - cx) / xScale;
                    }
                }
                this.solver.setValue(this.points[i][0], nodes[i].x * xScale + cx);
            }
            if (this.yEnable) {
                if (this.boxed && this.boxed.y1 != null && this.boxed.y2 != null) {
                    if (nodes[i].y < (this.boxed.y1 - cy) / yScale) {
                        nodes[i].y = (this.boxed.y1 - cy) / yScale;
                    }
                    else if (nodes[i].y > (this.boxed.y2 - cy) / yScale) {
                        nodes[i].y = (this.boxed.y2 - cy) / yScale;
                    }
                }
                this.solver.setValue(this.points[i][1], nodes[i].y * yScale + cy);
            }
        }
        return true;
    };
    return PackingPlugin;
}(abstract_1.ConstraintPlugin));
exports.PackingPlugin = PackingPlugin;
//# sourceMappingURL=packing.js.map