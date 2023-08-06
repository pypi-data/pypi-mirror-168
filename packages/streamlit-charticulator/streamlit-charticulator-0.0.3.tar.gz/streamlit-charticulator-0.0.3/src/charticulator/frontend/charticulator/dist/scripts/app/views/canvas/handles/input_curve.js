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
exports.InputCurveHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../../core");
var globals = require("../../../globals");
var R = require("../../../resources");
var utils_1 = require("../../../utils");
var controllers_1 = require("../../../controllers");
var components_1 = require("../../../components");
var controls_1 = require("../../panels/widgets/controls");
var common_1 = require("./common");
var strings_1 = require("../../../../strings");
var InputCurveHandleView = /** @class */ (function (_super) {
    __extends(InputCurveHandleView, _super);
    function InputCurveHandleView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            enabled: false,
            drawing: false,
            points: [],
        };
        return _this;
    }
    InputCurveHandleView.prototype.getPoint = function (x, y) {
        var bbox = this.refs.interaction.getBoundingClientRect();
        x -= bbox.left;
        y -= bbox.top + bbox.height;
        x /= this.props.zoom.scale;
        y /= -this.props.zoom.scale;
        // Scale x, y
        var w = Math.abs(this.props.handle.x2 - this.props.handle.x1);
        var h = Math.abs(this.props.handle.y2 - this.props.handle.y1);
        return {
            x: (x - w / 2) / (w / 2),
            y: (y - h / 2) / (w / 2),
        };
    };
    InputCurveHandleView.prototype.getBezierCurvesFromMousePoints = function (points) {
        if (points.length < 2) {
            return [];
        }
        var segs = [];
        for (var i = 0; i < points.length - 1; i++) {
            segs.push(new core_1.Graphics.LineSegmentParametrization(points[i], points[i + 1]));
        }
        var lp = new core_1.Graphics.MultiCurveParametrization(segs);
        var lpLength = lp.getLength();
        var segments = Math.ceil(lpLength / 0.2);
        var sampleAtS = function (s) {
            var p = lp.getPointAtS(s);
            var tx = 0, ty = 0;
            for (var k = -5; k <= 5; k++) {
                var ks = s + ((k / 40) * lpLength) / segments;
                ks = Math.max(0, Math.min(lpLength, ks));
                var t_1 = lp.getTangentAtS(ks);
                tx += t_1.x;
                ty += t_1.y;
            }
            var t = core_1.Geometry.vectorNormalize({ x: tx, y: ty });
            return [p, t];
        };
        var _a = __read(sampleAtS(0), 2), p0 = _a[0], t0 = _a[1];
        var s0 = 0;
        var curves = [];
        for (var i = 1; i <= segments; i++) {
            var s = (i / segments) * lpLength;
            var _b = __read(sampleAtS(s), 2), pi = _b[0], ti = _b[1];
            var ds = (s - s0) / 3;
            curves.push([
                p0,
                core_1.Geometry.vectorAdd(p0, core_1.Geometry.vectorScale(t0, ds)),
                core_1.Geometry.vectorAdd(pi, core_1.Geometry.vectorScale(ti, -ds)),
                pi,
            ]);
            s0 = s;
            p0 = pi;
            t0 = ti;
        }
        return curves;
    };
    InputCurveHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.interaction);
        this.hammer.on("panstart", function (e) {
            var x = e.center.x - e.deltaX;
            var y = e.center.y - e.deltaY;
            _this.setState({
                drawing: true,
                points: [_this.getPoint(x, y)],
            });
        });
        this.hammer.on("pan", function (e) {
            _this.state.points.push(_this.getPoint(e.center.x, e.center.y));
            _this.setState({
                points: _this.state.points,
            });
        });
        this.hammer.on("panend", function () {
            var curve = _this.getBezierCurvesFromMousePoints(_this.state.points);
            var context = new common_1.HandlesDragContext();
            _this.props.onDragStart(_this.props.handle, context);
            context.emit("end", { value: curve });
            _this.setState({
                drawing: false,
                enabled: false,
            });
        });
    };
    InputCurveHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    InputCurveHandleView.prototype.renderDrawing = function () {
        var _this = this;
        var handle = this.props.handle;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        var transformPoint = function (p) {
            var scaler = Math.abs(handle.x2 - handle.x1) / 2;
            var x = p.x * scaler + (handle.x1 + handle.x2) / 2;
            var y = p.y * scaler + (handle.y1 + handle.y2) / 2;
            return {
                x: fX(x),
                y: fY(y),
            };
        };
        return (React.createElement("path", { d: "M" +
                this.state.points
                    .map(function (p) {
                    var pt = transformPoint(p);
                    return utils_1.toSVGNumber(pt.x) + "," + utils_1.toSVGNumber(pt.y);
                })
                    .join("L"), className: "handle-hint element-line" }));
    };
    InputCurveHandleView.prototype.renderButton = function (x, y) {
        var _this = this;
        var margin = 2;
        var cx = x - 16 - margin;
        var cy = y + 16 + margin;
        return (React.createElement("g", { className: "handle-button", onClick: function () {
                _this.setState({ enabled: true });
            } },
            React.createElement("rect", { x: cx - 16, y: cy - 16, width: 32, height: 32 }),
            React.createElement("image", { xlinkHref: R.getSVGIcon("Edit"), x: cx - 12, y: cy - 12, width: 24, height: 24 })));
    };
    // eslint-disable-next-line
    InputCurveHandleView.prototype.renderSpiralButton = function (x, y) {
        var _this = this;
        var margin = 2;
        var cx = x - 16 - margin;
        var cy = y + 16 + margin;
        var anchorElement;
        return (React.createElement("g", { className: "handle-button", 
            // eslint-disable-next-line
            onClick: function () {
                globals.popupController.popupAt(
                // eslint-disable-next-line
                function (context) {
                    var windings = 4;
                    var startAngle = 180;
                    return (React.createElement(controllers_1.PopupView, { context: context },
                        React.createElement("div", { style: { padding: "10px" } },
                            React.createElement("div", { className: "charticulator__widget-row" },
                                React.createElement("span", { className: "charticulator__widget-row-label" },
                                    strings_1.strings.handles.windings,
                                    ":"),
                                React.createElement(controls_1.InputNumber, { defaultValue: windings, onEnter: function (value) {
                                        windings = value;
                                        return true;
                                    } })),
                            React.createElement("div", { className: "charticulator__widget-row" },
                                React.createElement("span", { className: "charticulator__widget-row-label" },
                                    strings_1.strings.handles.startAngle,
                                    ":"),
                                React.createElement(controls_1.InputNumber, { defaultValue: startAngle, onEnter: function (value) {
                                        startAngle = value;
                                        return true;
                                    } })),
                            React.createElement("div", { style: { textAlign: "right", marginTop: "10px" } },
                                React.createElement(components_1.ButtonRaised, { text: strings_1.strings.handles.drawSpiral, onClick: function () {
                                        context.close();
                                        // Make sprial and emit.
                                        var dragContext = new common_1.HandlesDragContext();
                                        var curve = [];
                                        _this.props.onDragStart(_this.props.handle, dragContext);
                                        var thetaStart = core_1.Geometry.degreesToRadians(startAngle);
                                        var thetaEnd = thetaStart + windings * Math.PI * 2;
                                        var N = 64;
                                        var a = 1 / thetaEnd; // r = a theta
                                        var swapXY = function (p) {
                                            return { x: p.y, y: p.x };
                                        };
                                        for (var i = 0; i < N; i++) {
                                            var theta1 = thetaStart + (i / N) * (thetaEnd - thetaStart);
                                            var theta2 = thetaStart +
                                                ((i + 1) / N) * (thetaEnd - thetaStart);
                                            var scaler = 3 / (theta2 - theta1);
                                            var r1 = a * theta1;
                                            var r2 = a * theta2;
                                            var p1 = {
                                                x: r1 * Math.cos(theta1),
                                                y: r1 * Math.sin(theta1),
                                            };
                                            var p2 = {
                                                x: r2 * Math.cos(theta2),
                                                y: r2 * Math.sin(theta2),
                                            };
                                            var cp1 = {
                                                x: p1.x +
                                                    (a *
                                                        (Math.cos(theta1) -
                                                            theta1 * Math.sin(theta1))) /
                                                        scaler,
                                                y: p1.y +
                                                    (a *
                                                        (Math.sin(theta1) +
                                                            theta1 * Math.cos(theta1))) /
                                                        scaler,
                                            };
                                            var cp2 = {
                                                x: p2.x -
                                                    (a *
                                                        (Math.cos(theta2) -
                                                            theta2 * Math.sin(theta2))) /
                                                        scaler,
                                                y: p2.y -
                                                    (a *
                                                        (Math.sin(theta2) +
                                                            theta2 * Math.cos(theta2))) /
                                                        scaler,
                                            };
                                            curve.push([p1, cp1, cp2, p2].map(swapXY));
                                        }
                                        dragContext.emit("end", { value: curve });
                                    } })))));
                }, { anchor: anchorElement });
            } },
            React.createElement("rect", { x: cx - 16, y: cy - 16, width: 32, height: 32, ref: function (e) { return (anchorElement = e); } }),
            React.createElement("image", { xlinkHref: R.getSVGIcon("scaffold/spiral"), x: cx - 12, y: cy - 12, width: 24, height: 24 })));
    };
    InputCurveHandleView.prototype.render = function () {
        var _this = this;
        var handle = this.props.handle;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        return (React.createElement("g", { className: "handle" },
            React.createElement("rect", { ref: "interaction", style: {
                    pointerEvents: this.state.enabled ? "fill" : "none",
                    cursor: "crosshair",
                }, className: "handle-ghost element-region", x: Math.min(fX(handle.x1), fX(handle.x2)), y: Math.min(fY(handle.y1), fY(handle.y2)), width: Math.abs(fX(handle.x1) - fX(handle.x2)), height: Math.abs(fY(handle.y1) - fY(handle.y2)) }),
            this.state.drawing ? this.renderDrawing() : null,
            !this.state.enabled ? (React.createElement("g", null,
                this.renderSpiralButton(Math.max(fX(handle.x1), fX(handle.x2)) - 38, Math.min(fY(handle.y1), fY(handle.y2))),
                this.renderButton(Math.max(fX(handle.x1), fX(handle.x2)), Math.min(fY(handle.y1), fY(handle.y2))))) : null));
    };
    return InputCurveHandleView;
}(React.Component));
exports.InputCurveHandleView = InputCurveHandleView;
//# sourceMappingURL=input_curve.js.map