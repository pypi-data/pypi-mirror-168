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
exports.GapRatioHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../../core");
var utils_1 = require("../../../utils");
var renderer_1 = require("../../../renderer");
var common_1 = require("./common");
var GapRatioHandleView = /** @class */ (function (_super) {
    __extends(GapRatioHandleView, _super);
    function GapRatioHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newValue: _this.props.handle.value,
        };
        return _this;
    }
    // eslint-disable-next-line
    GapRatioHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.line);
        this.hammer.add(new Hammer.Pan({ threshold: 1 }));
        var context = null;
        var oldValue;
        var xStart = 0;
        var yStart = 0;
        var dXIntegrate = 0;
        var dXLast = 0;
        var dYIntegrate = 0;
        var dYLast = 0;
        var scale = 1 / this.props.handle.scale;
        var getNewValue = function () {
            var cs = _this.props.handle.coordinateSystem;
            if (cs == null || cs instanceof core_1.Graphics.CartesianCoordinates) {
                if (_this.props.handle.axis == "x") {
                    return oldValue + scale * dXIntegrate;
                }
                if (_this.props.handle.axis == "y") {
                    return oldValue + scale * dYIntegrate;
                }
            }
            if (cs instanceof core_1.Graphics.PolarCoordinates) {
                if (_this.props.handle.axis == "x") {
                    var getAngle = function (x, y) {
                        return 90 - (Math.atan2(y, x) / Math.PI) * 180;
                    };
                    var angle0 = getAngle(xStart, yStart);
                    var angle1 = getAngle(xStart + dXIntegrate, yStart + dYIntegrate);
                    if (angle1 > angle0 + 180) {
                        angle1 -= 360;
                    }
                    if (angle1 < angle0 - 180) {
                        angle1 += 360;
                    }
                    return oldValue + scale * (angle1 - angle0);
                }
                if (_this.props.handle.axis == "y") {
                    var nX = xStart + dXIntegrate;
                    var nY = yStart + dYIntegrate;
                    var radius0 = Math.sqrt(xStart * xStart + yStart * yStart);
                    var radius1 = Math.sqrt(nX * nX + nY * nY);
                    return oldValue + scale * (radius1 - radius0);
                }
            }
            return oldValue;
        };
        this.hammer.on("panstart", function (e) {
            context = new common_1.HandlesDragContext();
            oldValue = _this.props.handle.value;
            if (_this.refs.cOrigin) {
                var bbox = _this.refs.cOrigin.getBoundingClientRect();
                xStart = (e.center.x - e.deltaX - bbox.left) / _this.props.zoom.scale;
                yStart = -(e.center.y - e.deltaY - bbox.top) / _this.props.zoom.scale;
            }
            else {
                xStart = (e.center.x - e.deltaX) / _this.props.zoom.scale;
                yStart = -(e.center.y - e.deltaY) / _this.props.zoom.scale;
            }
            dXLast = e.deltaX;
            dYLast = e.deltaY;
            dXIntegrate = e.deltaX / _this.props.zoom.scale;
            dYIntegrate = -e.deltaY / _this.props.zoom.scale;
            scale = 1 / _this.props.handle.scale;
            _this.setState({
                dragging: true,
                newValue: oldValue,
            });
            if (_this.props.onDragStart) {
                _this.props.onDragStart(_this.props.handle, context);
            }
        });
        this.hammer.on("pan", function (e) {
            if (context) {
                dXIntegrate += (e.deltaX - dXLast) / _this.props.zoom.scale;
                dYIntegrate += -(e.deltaY - dYLast) / _this.props.zoom.scale;
                dXLast = e.deltaX;
                dYLast = e.deltaY;
                var newValue = getNewValue();
                if (_this.props.handle.range) {
                    newValue = Math.min(_this.props.handle.range[1], Math.max(newValue, _this.props.handle.range[0]));
                }
                else {
                    newValue = Math.min(1, Math.max(newValue, 0));
                }
                _this.setState({
                    newValue: newValue,
                });
                context.emit("drag", { value: newValue });
            }
        });
        this.hammer.on("panend", function (e) {
            if (context) {
                dXIntegrate += (e.deltaX - dXLast) / _this.props.zoom.scale;
                dYIntegrate += -(e.deltaY - dYLast) / _this.props.zoom.scale;
                dXLast = e.deltaX;
                dYLast = e.deltaY;
                var newValue = getNewValue();
                if (_this.props.handle.range) {
                    newValue = Math.min(_this.props.handle.range[1], Math.max(newValue, _this.props.handle.range[0]));
                }
                else {
                    newValue = Math.min(1, Math.max(newValue, 0));
                }
                context.emit("end", { value: newValue });
                _this.setState({
                    dragging: false,
                });
                context = null;
            }
        });
    };
    GapRatioHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    GapRatioHandleView.prototype.render = function () {
        var handle = this.props.handle;
        if (handle.coordinateSystem == null ||
            handle.coordinateSystem instanceof core_1.Graphics.CartesianCoordinates) {
            return this.renderCartesian();
        }
        if (handle.coordinateSystem instanceof core_1.Graphics.PolarCoordinates) {
            return this.renderPolar();
        }
        return null;
    };
    // eslint-disable-next-line
    GapRatioHandleView.prototype.renderPolar = function () {
        var handle = this.props.handle;
        var polar = handle.coordinateSystem;
        var center = core_1.Geometry.applyZoom(this.props.zoom, {
            x: polar.origin.x,
            y: -polar.origin.y,
        });
        switch (handle.axis) {
            case "x": {
                // angular axis
                var pathValue = core_1.Graphics.makePath();
                var pathRegion = core_1.Graphics.makePath();
                var angle = handle.reference + handle.scale * handle.value;
                var angleRef = handle.reference;
                var r1 = handle.span[0] * this.props.zoom.scale, r2 = handle.span[1] * this.props.zoom.scale;
                pathValue.polarLineTo(center.x, -center.y, -angle + 90, r1, -angle + 90, r2, true);
                pathRegion.polarLineTo(center.x, -center.y, -angle + 90, r1, -angle + 90, r2, true);
                pathRegion.polarLineTo(center.x, -center.y, -angle + 90, r2, -angleRef + 90, r2, false);
                pathRegion.polarLineTo(center.x, -center.y, -angleRef + 90, r2, -angleRef + 90, r1, false);
                pathRegion.polarLineTo(center.x, -center.y, -angleRef + 90, r1, -angle + 90, r1, false);
                pathRegion.closePath();
                var pathNew = core_1.Graphics.makePath();
                if (this.state.dragging) {
                    var angleNew = handle.reference + handle.scale * this.state.newValue;
                    pathNew.polarLineTo(center.x, -center.y, -angleNew + 90, r1, -angleNew + 90, r2, true);
                }
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-angular", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("circle", { ref: "cOrigin", cx: center.x, cy: center.y, r: 0 }),
                    React.createElement("g", { ref: "line" },
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathRegion.path.cmds), className: "element-region handle-ghost" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathValue.path.cmds), className: "element-line handle-ghost" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathRegion.path.cmds), className: "element-region handle-highlight" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathValue.path.cmds), className: "element-line handle-highlight" })),
                    this.state.dragging ? (React.createElement("path", { d: renderer_1.renderSVGPath(pathNew.path.cmds), className: "element-line handle-hint" })) : null));
            }
            case "y": {
                var pathValue = core_1.Graphics.makePath();
                var pathRegion = core_1.Graphics.makePath();
                var radius = (handle.reference + handle.scale * handle.value) *
                    this.props.zoom.scale;
                var radiusRef = handle.reference * this.props.zoom.scale;
                var angle1 = handle.span[0], angle2 = handle.span[1];
                pathValue.polarLineTo(center.x, -center.y, -angle1 + 90, radius, -angle2 + 90, radius, true);
                pathRegion.polarLineTo(center.x, -center.y, -angle1 + 90, radius, -angle2 + 90, radius, true);
                pathRegion.polarLineTo(center.x, -center.y, -angle2 + 90, radius, -angle2 + 90, radiusRef, false);
                pathRegion.polarLineTo(center.x, -center.y, -angle2 + 90, radiusRef, -angle1 + 90, radiusRef, false);
                pathRegion.polarLineTo(center.x, -center.y, -angle1 + 90, radiusRef, -angle1 + 90, radius, false);
                pathRegion.closePath();
                var pathNew = core_1.Graphics.makePath();
                if (this.state.dragging) {
                    var radiusNew = (handle.reference + handle.scale * this.state.newValue) *
                        this.props.zoom.scale;
                    pathNew.polarLineTo(center.x, -center.y, -angle1 + 90, radiusNew, -angle2 + 90, radiusNew, true);
                }
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-radial", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("circle", { ref: "cOrigin", cx: center.x, cy: center.y, r: 0 }),
                    React.createElement("g", { ref: "line" },
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathRegion.path.cmds), className: "element-region handle-ghost" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathValue.path.cmds), className: "element-line handle-ghost" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathRegion.path.cmds), className: "element-region handle-highlight" }),
                        React.createElement("path", { d: renderer_1.renderSVGPath(pathValue.path.cmds), className: "element-line handle-highlight" })),
                    this.state.dragging ? (React.createElement("path", { d: renderer_1.renderSVGPath(pathNew.path.cmds), className: "element-line handle-hint" })) : null));
            }
        }
    };
    // eslint-disable-next-line
    GapRatioHandleView.prototype.renderCartesian = function () {
        var _this = this;
        var handle = this.props.handle;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        switch (handle.axis) {
            case "x": {
                var fxRef = fX(handle.reference);
                var fxVal = fX(handle.reference + handle.scale * handle.value);
                var fy1 = fY(handle.span[0]);
                var fy2 = fY(handle.span[1]);
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-x", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("g", { ref: "line" },
                        React.createElement("line", { className: "element-line handle-ghost", x1: fxVal, x2: fxVal, y1: fy1, y2: fy2 }),
                        React.createElement("rect", { className: "element-region handle-ghost", x: Math.min(fxRef, fxVal), width: Math.abs(fxRef - fxVal), y: Math.min(fy1, fy2), height: Math.abs(fy2 - fy1) }),
                        React.createElement("line", { className: "element-line handle-highlight", x1: fxVal, x2: fxVal, y1: fy1, y2: fy2 }),
                        React.createElement("rect", { className: "element-region handle-highlight", x: Math.min(fxRef, fxVal), width: Math.abs(fxRef - fxVal), y: Math.min(fy1, fy2), height: Math.abs(fy2 - fy1) })),
                    this.state.dragging ? (React.createElement("g", null,
                        React.createElement("line", { className: "element-line handle-hint", x1: fX(handle.reference + handle.scale * this.state.newValue), x2: fX(handle.reference + handle.scale * this.state.newValue), y1: fY(handle.span[0]), y2: fY(handle.span[1]) }))) : null));
            }
            case "y": {
                var fyRef = fY(handle.reference);
                var fyVal = fY(handle.reference + handle.scale * handle.value);
                var fx1 = fX(handle.span[0]);
                var fx2 = fX(handle.span[1]);
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-y", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("g", { ref: "line" },
                        React.createElement("line", { className: "element-line handle-ghost", y1: fyVal, y2: fyVal, x1: fx1, x2: fx2 }),
                        React.createElement("rect", { className: "element-region handle-ghost", y: Math.min(fyRef, fyVal), height: Math.abs(fyRef - fyVal), x: Math.min(fx1, fx2), width: Math.abs(fx2 - fx1) }),
                        React.createElement("line", { className: "element-line handle-highlight", y1: fyVal, y2: fyVal, x1: fx1, x2: fx2 }),
                        React.createElement("rect", { className: "element-region handle-highlight", y: Math.min(fyRef, fyVal), height: Math.abs(fyRef - fyVal), x: Math.min(fx1, fx2), width: Math.abs(fx2 - fx1) })),
                    this.state.dragging ? (React.createElement("g", null,
                        React.createElement("line", { className: "element-line handle-hint", y1: fY(handle.reference + handle.scale * this.state.newValue), y2: fY(handle.reference + handle.scale * this.state.newValue), x1: fx1, x2: fx2 }))) : null));
            }
        }
    };
    return GapRatioHandleView;
}(React.Component));
exports.GapRatioHandleView = GapRatioHandleView;
//# sourceMappingURL=gap_ratio.js.map