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
exports.MultiCurveParametrization = exports.LineSegmentParametrization = exports.BezierCurveParameterization = exports.CurveParameterization = exports.linearInvert = exports.findSegment = exports.linearApproximation = exports.RK4 = void 0;
/**
 * Compute numerical integral y' = f(t, y), y(t0) = y0,
 *  start from t0, step size h, with specified number of steps,
 *  with Runge-Kutta Method order 4
 */
function RK4(f, y0, t0, h, steps, result) {
    if (result === void 0) { result = new Array(steps); }
    if (steps == 0) {
        return result;
    }
    result[0] = y0;
    var yp = y0;
    var tp = t0;
    for (var i = 1; i < steps; i++) {
        var k1 = f(tp, yp);
        var k2 = f(tp + h / 2, yp + (h * k1) / 2);
        var k3 = f(tp + h / 2, yp + (h * k2) / 2);
        var k4 = f(tp + h, yp + h * k3);
        var yi = yp + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
        var ti = tp + h;
        result[i] = yi;
        yp = yi;
        tp = ti;
    }
    return result;
}
exports.RK4 = RK4;
function linearApproximation(points, t) {
    var i1, i2;
    var w = t * (points.length - 1);
    i1 = Math.floor(w);
    i2 = i1 + 1;
    var k = w - i1;
    if (i1 < 0) {
        i1 = 0;
        i2 = 0;
    }
    if (i1 >= points.length - 1) {
        i1 = points.length - 1;
        i2 = points.length - 1;
    }
    return points[i1] * (1 - k) + points[i2] * k;
}
exports.linearApproximation = linearApproximation;
function findSegment(bounds, k) {
    // Linear search
    for (var i = 0; i < bounds.length - 1; i++) {
        var b1 = bounds[i];
        var b2 = bounds[i + 1];
        if (k >= b1 && k <= b2) {
            return [i, k - b1];
        }
    }
    if (k < bounds[0]) {
        return [0, 0];
    }
    else {
        return [
            bounds.length - 2,
            bounds[bounds.length - 1] - bounds[bounds.length - 2],
        ];
    }
}
exports.findSegment = findSegment;
function linearInvert(points, result) {
    if (result === void 0) { result = new Array(points.length); }
    var s0 = points[0];
    var s1 = points[points.length - 1];
    var ptr = 0;
    for (var i = 0; i < points.length; i++) {
        var si = s0 + ((s1 - s0) * i) / (points.length - 1);
        while (ptr + 2 < points.length && si >= points[ptr + 1]) {
            ptr += 1;
        }
        var sA = points[ptr];
        var tA = ptr / (points.length - 1);
        var sB = points[ptr + 1];
        var tB = (ptr + 1) / (points.length - 1);
        var ti = ((si - sA) / (sB - sA)) * (tB - tA) + tA;
        result[i] = ti;
    }
    return result;
}
exports.linearInvert = linearInvert;
var CurveParameterization = /** @class */ (function () {
    function CurveParameterization() {
    }
    CurveParameterization.prototype.getNormalAtT = function (t) {
        var tangent = this.getTangentAtT(t);
        return {
            x: -tangent.y,
            y: tangent.x,
        };
    };
    return CurveParameterization;
}());
exports.CurveParameterization = CurveParameterization;
/** Parametrize a given bezier curve */
var BezierCurveParameterization = /** @class */ (function (_super) {
    __extends(BezierCurveParameterization, _super);
    /** Construct the cubic bezier curve with four control points */
    function BezierCurveParameterization(p1, p2, p3, p4) {
        var _this = _super.call(this) || this;
        _this.k3x = 3 * (p2.x - p3.x) + p4.x - p1.x;
        _this.k2x = 3 * (p1.x + p3.x - 2 * p2.x);
        _this.k1x = 3 * (p2.x - p1.x);
        _this.k0x = p1.x;
        _this.k3y = 3 * (p2.y - p3.y) + p4.y - p1.y;
        _this.k2y = 3 * (p1.y + p3.y - 2 * p2.y);
        _this.k1y = 3 * (p2.y - p1.y);
        _this.k0y = p1.y;
        // Len = 8.080527392389182  10000
        //       8.080527036296594  100
        //       8.084824756247663  10
        var steps = 100;
        _this.tToS = RK4(function (t) { return _this.getDsDtAtT(t); }, 0, 0, 1 / (steps - 1), steps);
        _this.len = _this.tToS[steps - 1];
        _this.sToT = linearInvert(_this.tToS);
        return _this;
    }
    BezierCurveParameterization.prototype.getPointAtT = function (t) {
        return {
            x: this.k0x + t * (this.k1x + t * (this.k2x + t * this.k3x)),
            y: this.k0y + t * (this.k1y + t * (this.k2y + t * this.k3y)),
        };
    };
    /** Get the tangent direction at t */
    BezierCurveParameterization.prototype.getTangentAtT = function (t) {
        var t2 = t * t;
        var dxdt = 3 * t2 * this.k3x + 2 * t * this.k2x + this.k1x;
        var dydt = 3 * t2 * this.k3y + 2 * t * this.k2y + this.k1y;
        var length = Math.sqrt(dxdt * dxdt + dydt * dydt);
        return {
            x: dxdt / length,
            y: dydt / length,
        };
    };
    /** Get ds/dt at t */
    BezierCurveParameterization.prototype.getDsDtAtT = function (t) {
        var t2 = t * t;
        var dxdt = 3 * t2 * this.k3x + 2 * t * this.k2x + this.k1x;
        var dydt = 3 * t2 * this.k3y + 2 * t * this.k2y + this.k1y;
        return Math.sqrt(dxdt * dxdt + dydt * dydt);
    };
    BezierCurveParameterization.prototype.getSFromT = function (t) {
        return linearApproximation(this.tToS, t);
    };
    BezierCurveParameterization.prototype.getTFromS = function (s) {
        return linearApproximation(this.sToT, s / this.len);
    };
    BezierCurveParameterization.prototype.getLength = function () {
        return this.len;
    };
    return BezierCurveParameterization;
}(CurveParameterization));
exports.BezierCurveParameterization = BezierCurveParameterization;
var LineSegmentParametrization = /** @class */ (function (_super) {
    __extends(LineSegmentParametrization, _super);
    function LineSegmentParametrization(p1, p2) {
        var _this = _super.call(this) || this;
        _this.p1 = p1;
        _this.p2 = p2;
        _this.length = Math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
        _this.tangent = {
            x: (p2.x - p1.x) / _this.length,
            y: (p2.y - p1.y) / _this.length,
        };
        return _this;
    }
    // eslint-disable-next-line
    LineSegmentParametrization.prototype.getTangentAtT = function (t) {
        return this.tangent;
    };
    LineSegmentParametrization.prototype.getPointAtT = function (t) {
        return {
            x: this.p1.x + (this.p2.x - this.p1.x) * t,
            y: this.p1.y + (this.p2.y - this.p1.y) * t,
        };
    };
    LineSegmentParametrization.prototype.getSFromT = function (t) {
        return t * this.length;
    };
    LineSegmentParametrization.prototype.getTFromS = function (s) {
        return s / this.length;
    };
    LineSegmentParametrization.prototype.getLength = function () {
        return this.length;
    };
    return LineSegmentParametrization;
}(CurveParameterization));
exports.LineSegmentParametrization = LineSegmentParametrization;
var MultiCurveParametrization = /** @class */ (function () {
    function MultiCurveParametrization(segments) {
        this.segments = segments;
        this.len = 0;
        this.sBounds = new Array(this.segments.length + 1);
        this.sBounds[0] = 0;
        for (var i = 0; i < this.segments.length; i++) {
            this.len += this.segments[i].getLength();
            this.sBounds[i + 1] = this.len;
        }
    }
    MultiCurveParametrization.prototype.getSegmentAtS = function (s) {
        var _a = __read(findSegment(this.sBounds, s), 2), pi = _a[0], ps = _a[1];
        var p = this.segments[pi];
        var pt = p.getTFromS(ps);
        return [p, pt];
    };
    MultiCurveParametrization.prototype.getPointAtS = function (s) {
        var _a = __read(this.getSegmentAtS(s), 2), p = _a[0], t = _a[1];
        return p.getPointAtT(t);
    };
    MultiCurveParametrization.prototype.getTangentAtS = function (s) {
        var _a = __read(this.getSegmentAtS(s), 2), p = _a[0], t = _a[1];
        return p.getTangentAtT(t);
    };
    MultiCurveParametrization.prototype.getNormalAtS = function (s) {
        var _a = __read(this.getSegmentAtS(s), 2), p = _a[0], k = _a[1];
        return p.getNormalAtT(k);
    };
    MultiCurveParametrization.prototype.getFrameAtS = function (s) {
        var _a = __read(this.getSegmentAtS(s), 2), p = _a[0], t = _a[1];
        return {
            p: p.getPointAtT(t),
            t: p.getTangentAtT(t),
            n: p.getNormalAtT(t),
        };
    };
    MultiCurveParametrization.prototype.getLength = function () {
        return this.len;
    };
    MultiCurveParametrization.prototype.getSegments = function () {
        return this.segments;
    };
    return MultiCurveParametrization;
}());
exports.MultiCurveParametrization = MultiCurveParametrization;
//# sourceMappingURL=bezier_curve.js.map