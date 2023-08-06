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
exports.CoordinateSystemHelper = exports.BezierCurveCoordinates = exports.PolarCoordinates = exports.CartesianCoordinates = exports.CoordinateSystem = void 0;
/**
 * @packageDocumentation
 * @preferred
 */
var _1 = require(".");
var common_1 = require("../common");
var elements_1 = require("./elements");
var CoordinateSystem = /** @class */ (function () {
    function CoordinateSystem() {
    }
    return CoordinateSystem;
}());
exports.CoordinateSystem = CoordinateSystem;
/** Normal cartesian coordinate system */
var CartesianCoordinates = /** @class */ (function (_super) {
    __extends(CartesianCoordinates, _super);
    function CartesianCoordinates(origin) {
        if (origin === void 0) { origin = { x: 0, y: 0 }; }
        var _this = _super.call(this) || this;
        _this.origin = origin;
        return _this;
    }
    CartesianCoordinates.prototype.getBaseTransform = function () {
        return {
            x: this.origin.x,
            y: this.origin.y,
            angle: 0,
        };
    };
    CartesianCoordinates.prototype.transformPoint = function (x, y) {
        return { x: x, y: y };
    };
    CartesianCoordinates.prototype.transformDirectionAtPoint = function (x, y, dx, dy) {
        return { x: dx, y: dy };
    };
    CartesianCoordinates.prototype.transformPointWithBase = function (x, y) {
        return { x: x + this.origin.x, y: y + this.origin.y };
    };
    CartesianCoordinates.prototype.transformDirectionAtPointWithBase = function (x, y, dx, dy) {
        return { x: dx, y: dy };
    };
    CartesianCoordinates.prototype.getLocalTransform = function (x, y) {
        return {
            x: x,
            y: y,
            angle: 0,
        };
    };
    return CartesianCoordinates;
}(CoordinateSystem));
exports.CartesianCoordinates = CartesianCoordinates;
var sqrt60 = Math.sqrt(60);
/** Polar coordinates. Angle is in degrees, clockwise, top is 0  */
var PolarCoordinates = /** @class */ (function (_super) {
    __extends(PolarCoordinates, _super);
    function PolarCoordinates(origin, radial1, radial2, distortY) {
        if (origin === void 0) { origin = { x: 0, y: 0 }; }
        if (radial1 === void 0) { radial1 = 0; }
        if (radial2 === void 0) { radial2 = 1; }
        if (distortY === void 0) { distortY = false; }
        var _this = _super.call(this) || this;
        _this.origin = origin;
        _this.radial1 = radial1;
        _this.radial2 = radial2;
        _this.distortY = distortY;
        return _this;
    }
    PolarCoordinates.prototype.getBaseTransform = function () {
        return {
            x: this.origin.x,
            y: this.origin.y,
            angle: 0,
        };
    };
    PolarCoordinates.prototype.transformRadial = function (radial) {
        if (this.distortY) {
            return Math.sqrt(Math.max(0, (this.radial1 + this.radial2) * radial - this.radial1 * this.radial2));
        }
        else {
            return radial;
        }
    };
    PolarCoordinates.prototype.inverseTransformRadial = function (distance) {
        var y = distance / sqrt60;
        return y * y;
    };
    PolarCoordinates.prototype.transformPoint = function (angle, radial) {
        return {
            x: this.transformRadial(radial) *
                Math.sin(common_1.Geometry.degreesToRadians(angle)),
            y: this.transformRadial(radial) *
                Math.cos(common_1.Geometry.degreesToRadians(angle)),
        };
    };
    PolarCoordinates.prototype.transformDirectionAtPoint = function (angle, radial, dx, dy) {
        var t = common_1.Geometry.degreesToRadians(-angle);
        return {
            x: dx * Math.cos(t) - dy * Math.sin(t),
            y: dx * Math.sin(t) + dy * Math.cos(t),
        };
    };
    PolarCoordinates.prototype.getLocalTransform = function (angle, radial) {
        var t = common_1.Geometry.degreesToRadians(angle);
        return {
            x: this.transformRadial(radial) * Math.sin(t),
            y: this.transformRadial(radial) * Math.cos(t),
            angle: -angle,
        };
    };
    PolarCoordinates.prototype.transformPointWithBase = function (angle, radial) {
        var t = common_1.Geometry.degreesToRadians(angle);
        return {
            x: this.transformRadial(radial) * Math.sin(t) + this.origin.x,
            y: this.transformRadial(radial) * Math.cos(t) + this.origin.y,
        };
    };
    PolarCoordinates.prototype.transformDirectionAtPointWithBase = function (angle, radial, dx, dy) {
        var t = common_1.Geometry.degreesToRadians(-angle);
        return {
            x: dx * Math.cos(t) - dy * Math.sin(t),
            y: dx * Math.sin(t) + dy * Math.cos(t),
        };
    };
    return PolarCoordinates;
}(CoordinateSystem));
exports.PolarCoordinates = PolarCoordinates;
/** Bezier curve coordinate system. */
var BezierCurveCoordinates = /** @class */ (function (_super) {
    __extends(BezierCurveCoordinates, _super);
    function BezierCurveCoordinates(origin, curve) {
        if (origin === void 0) { origin = { x: 0, y: 0 }; }
        var _this = _super.call(this) || this;
        _this.origin = origin;
        _this.curve = curve;
        return _this;
    }
    BezierCurveCoordinates.prototype.getBaseTransform = function () {
        return {
            x: this.origin.x,
            y: this.origin.y,
            angle: 0,
        };
    };
    BezierCurveCoordinates.prototype.transformPoint = function (x, y) {
        var frame = this.curve.getFrameAtS(x);
        return {
            x: frame.p.x + y * frame.n.x,
            y: frame.p.y + y * frame.n.y,
        };
    };
    BezierCurveCoordinates.prototype.transformDirectionAtPoint = function (x, y, dx, dy) {
        var frame = this.curve.getFrameAtS(x);
        return {
            x: dx * frame.t.x + dy * frame.n.x,
            y: dx * frame.t.y + dy * frame.n.y,
        };
    };
    BezierCurveCoordinates.prototype.getLocalTransform = function (x, y) {
        var frame = this.curve.getFrameAtS(x);
        var angle = (Math.atan2(frame.t.y, frame.t.x) / Math.PI) * 180;
        return {
            x: frame.p.x + y * frame.n.x,
            y: frame.p.y + y * frame.n.y,
            angle: angle,
        };
    };
    BezierCurveCoordinates.prototype.transformPointWithBase = function (x, y) {
        var p = this.transformPoint(x, y);
        return {
            x: p.x + this.origin.x,
            y: p.y + this.origin.y,
        };
    };
    BezierCurveCoordinates.prototype.transformDirectionAtPointWithBase = function (x, y, dx, dy) {
        return this.transformDirectionAtPoint(x, y, dx, dy);
    };
    BezierCurveCoordinates.prototype.getLength = function () {
        return this.curve.getLength();
    };
    BezierCurveCoordinates.prototype.getCurve = function () {
        return this.curve;
    };
    return BezierCurveCoordinates;
}(CoordinateSystem));
exports.BezierCurveCoordinates = BezierCurveCoordinates;
var CoordinateSystemHelper = /** @class */ (function () {
    function CoordinateSystemHelper(coordinateSystem) {
        this.coordinateSystem = coordinateSystem;
    }
    CoordinateSystemHelper.prototype.rect = function (x1, y1, x2, y2, style, rx, ry) {
        if (style === void 0) { style = {}; }
        if (rx === void 0) { rx = 0; }
        if (ry === void 0) { ry = 0; }
        var cs = this.coordinateSystem;
        if (cs instanceof CartesianCoordinates) {
            return _1.makeRect(x1, y1, x2, y2, style, rx, ry);
        }
        else {
            var path = _1.makePath(style);
            this.lineTo(path, x1, y1, x1, y2, true);
            this.lineTo(path, x1, y2, x2, y2, false);
            this.lineTo(path, x2, y2, x2, y1, false);
            this.lineTo(path, x2, y1, x1, y1, false);
            path.closePath();
            return path.path;
        }
    };
    CoordinateSystemHelper.prototype.ellipse = function (x1, y1, x2, y2, style) {
        if (style === void 0) { style = {}; }
        var cs = this.coordinateSystem;
        if (cs instanceof CartesianCoordinates) {
            return elements_1.makeEllipse(x1, y1, x2, y2, style);
        }
        else {
            var path = _1.makePath(style);
            var cx = (x1 + x2) / 2, cy = (y1 + y2) / 2;
            var rx = Math.abs(x2 - x1) / 2, ry = Math.abs(y2 - y1) / 2;
            var N = 32;
            for (var i = 0; i < N; i++) {
                var theta1 = (i / N) * (Math.PI * 2);
                var theta2 = ((i + 1) / N) * (Math.PI * 2);
                this.lineTo(path, cx + rx * Math.cos(theta1), cy + ry * Math.sin(theta1), cx + rx * Math.cos(theta2), cy + ry * Math.sin(theta2), i == 0);
            }
            path.closePath();
            return path.path;
        }
    };
    CoordinateSystemHelper.prototype.line = function (x1, y1, x2, y2, style) {
        if (style === void 0) { style = {}; }
        var cs = this.coordinateSystem;
        if (cs instanceof CartesianCoordinates) {
            return _1.makeLine(x1, y1, x2, y2, style);
        }
        else {
            var path = _1.makePath(style);
            this.lineTo(path, x1, y1, x2, y2, true);
            return path.path;
        }
    };
    CoordinateSystemHelper.prototype.lineTo = function (path, x1, y1, x2, y2, newPath) {
        var cs = this.coordinateSystem;
        if (newPath) {
            var p = cs.transformPoint(x1, y1);
            path.moveTo(p.x, p.y);
        }
        if (cs instanceof CartesianCoordinates) {
            path.lineTo(x2, y2);
        }
        if (cs instanceof PolarCoordinates) {
            path.polarLineTo(0, 0, 90 - x1, cs.transformRadial(y1), 90 - x2, cs.transformRadial(y2), false);
        }
        if (cs instanceof BezierCurveCoordinates) {
            if (Math.abs(x1 - x2) < 1e-6) {
                var p = cs.transformPoint(x2, y2);
                path.lineTo(p.x, p.y);
            }
            else {
                var framePrevious = cs.getLocalTransform(x1, y1);
                var direction = Math.atan2(y2 - y1, x2 - x1);
                var segments = Math.max(2, Math.ceil((3 * cs.getCurve().getSegments().length * Math.abs(x2 - x1)) /
                    cs.getCurve().getLength()));
                for (var i = 1; i <= segments; i++) {
                    var t = i / segments;
                    var frame = cs.getLocalTransform((x2 - x1) * t + x1, (y2 - y1) * t + y1);
                    var len = common_1.Geometry.pointDistance(frame, framePrevious) / 3;
                    var angle1 = common_1.Geometry.degreesToRadians(framePrevious.angle) + direction;
                    var angle2 = common_1.Geometry.degreesToRadians(frame.angle) + direction;
                    path.cubicBezierCurveTo(framePrevious.x + Math.cos(angle1) * len, framePrevious.y + Math.sin(angle1) * len, frame.x - Math.cos(angle2) * len, frame.y - Math.sin(angle2) * len, frame.x, frame.y);
                    // path.lineTo(frame.x, frame.y);
                    framePrevious = frame;
                }
            }
        }
    };
    CoordinateSystemHelper.prototype.arcTo = function (path, rx, ry, x1, y1, x2, y2, sweepFlag) {
        if (sweepFlag === void 0) { sweepFlag = 1; }
        var cs = this.coordinateSystem;
        if (cs instanceof CartesianCoordinates) {
            path.arcTo(rx, ry, 0, 0, sweepFlag, x2, y2);
            return path.path;
        }
        else {
            //IGNORE NOW. TODO: handle arc for CartesianCoordinates and BezierCurveCoordinates
            this.lineTo(path, x1, y1, x2, y2, true);
            return path.path;
        }
    };
    return CoordinateSystemHelper;
}());
exports.CoordinateSystemHelper = CoordinateSystemHelper;
//# sourceMappingURL=coordinate_system.js.map