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
exports.PolarCoordinatorPlugin = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __1 = require("../..");
var polar_coordinator_1 = require("../../prototypes/guides/polar_coordinator");
var update_attribute_1 = require("../../prototypes/update_attribute");
var abstract_1 = require("../abstract");
// Converts Polar coordinates to cartesian coordinates
var PolarCoordinatorPlugin = /** @class */ (function (_super) {
    __extends(PolarCoordinatorPlugin, _super);
    function PolarCoordinatorPlugin(solver, cx, cy, radialVarable, angleVarable, attrs, chartConstraints, coordinatoObjectID, chartMananger) {
        var _this = _super.call(this) || this;
        _this.solver = solver;
        _this.cx = cx;
        _this.cy = cy;
        _this.radialVarable = radialVarable;
        _this.angleVarable = angleVarable;
        _this.attrs = attrs;
        _this.chartConstraints = chartConstraints;
        _this.coordinatoObjectID = coordinatoObjectID;
        _this.chartMananger = chartMananger;
        return _this;
    }
    PolarCoordinatorPlugin.prototype.apply = function () {
        var cx = this.solver.getValue(this.cx);
        var cy = this.solver.getValue(this.cy);
        var attrs = this.attrs;
        for (var i = 0; i < this.angleVarable.length; i++) {
            var angleAttr = this.solver.attr(attrs, this.angleVarable[i].name, {
                edit: false,
            });
            for (var j = 0; j < this.radialVarable.length; j++) {
                var attrXname = polar_coordinator_1.getPointValueName(i, j, "X");
                var attrYname = polar_coordinator_1.getPointValueName(i, j, "Y");
                var radialAttr = this.solver.attr(attrs, this.radialVarable[j].name, {
                    edit: false,
                });
                var pointX = this.solver.attr(attrs, attrXname, {
                    edit: false,
                });
                var pointY = this.solver.attr(attrs, attrYname, {
                    edit: false,
                });
                var angle = this.solver.getValue(angleAttr);
                var radians = __1.Geometry.degreesToRadians(angle);
                var radius = Math.abs(this.solver.getValue(radialAttr));
                var tx = Math.sin(radians) * radius;
                var ty = Math.cos(radians) * radius;
                this.solver.setValue(pointX, cx + tx);
                this.solver.setValue(pointY, cy + ty);
                // take snapped attributes and apply new value
                update_attribute_1.snapToAttribute(this.chartMananger, this.chartConstraints, this.coordinatoObjectID, attrXname, cx + tx);
                update_attribute_1.snapToAttribute(this.chartMananger, this.chartConstraints, this.coordinatoObjectID, attrYname, cy + ty);
            }
        }
        return true;
    };
    return PolarCoordinatorPlugin;
}(abstract_1.ConstraintPlugin));
exports.PolarCoordinatorPlugin = PolarCoordinatorPlugin;
//# sourceMappingURL=polar_coordinator.js.map