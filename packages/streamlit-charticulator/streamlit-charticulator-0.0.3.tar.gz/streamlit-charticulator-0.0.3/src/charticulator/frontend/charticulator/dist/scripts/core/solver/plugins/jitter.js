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
exports.JitterPlugin = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __1 = require("../..");
var abstract_1 = require("../abstract");
var JitterPlugin = /** @class */ (function (_super) {
    __extends(JitterPlugin, _super);
    function JitterPlugin(solver, x1, y1, x2, y2, points, axisOnly, options) {
        var _this = _super.call(this) || this;
        _this.solver = solver;
        _this.x1 = x1;
        _this.y1 = y1;
        _this.x2 = x2;
        _this.y2 = y2;
        _this.points = points;
        _this.xEnable = axisOnly == null || axisOnly == "x";
        _this.yEnable = axisOnly == null || axisOnly == "y";
        _this.options = options;
        return _this;
    }
    JitterPlugin.prototype.apply = function () {
        var x1 = this.solver.getValue(this.x1);
        var x2 = this.solver.getValue(this.x2);
        var y1 = this.solver.getValue(this.y1);
        var y2 = this.solver.getValue(this.y2);
        var nodes = this.points.map(function () {
            var x = __1.getRandom(x1, x2);
            var y = __1.getRandom(y1, y2);
            // Use forceSimulation's default initialization
            return {
                x: x,
                y: y,
            };
        });
        for (var i = 0; i < nodes.length; i++) {
            if (this.options.horizontal) {
                this.solver.setValue(this.points[i][0], nodes[i].x);
            }
            if (this.options.vertical) {
                this.solver.setValue(this.points[i][1], nodes[i].y);
            }
        }
        return true;
    };
    return JitterPlugin;
}(abstract_1.ConstraintPlugin));
exports.JitterPlugin = JitterPlugin;
//# sourceMappingURL=jitter.js.map