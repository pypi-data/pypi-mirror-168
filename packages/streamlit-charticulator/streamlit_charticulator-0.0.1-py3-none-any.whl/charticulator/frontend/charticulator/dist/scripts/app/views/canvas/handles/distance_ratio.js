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
exports.DistanceRatioHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../../core");
var utils_1 = require("../../../utils");
var renderer_1 = require("../../../renderer");
var common_1 = require("./common");
var DistanceRatioHandleView = /** @class */ (function (_super) {
    __extends(DistanceRatioHandleView, _super);
    function DistanceRatioHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newValue: _this.props.handle.value,
        };
        return _this;
    }
    DistanceRatioHandleView.prototype.clip = function (v) {
        var min = this.props.handle.clipRange[0];
        var max = this.props.handle.clipRange[1];
        if (v < min) {
            v = min;
        }
        if (v > max) {
            v = max;
        }
        if (v < 0.05) {
            v = 0;
        }
        return v;
    };
    DistanceRatioHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.margin);
        this.hammer.add(new Hammer.Pan({ threshold: 1 }));
        var context = null;
        var oldValue = 0;
        this.hammer.on("panstart", function () {
            context = new common_1.HandlesDragContext();
            oldValue = _this.props.handle.value;
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
                var cc = _this.refs.centerCircle.getBoundingClientRect();
                var px = e.center.x - (cc.left + cc.width / 2);
                var py = e.center.y - (cc.top + cc.height / 2);
                var d = Math.sqrt(px * px + py * py) / _this.props.zoom.scale;
                d =
                    (d - _this.props.handle.startDistance) /
                        (_this.props.handle.endDistance - _this.props.handle.startDistance);
                d = _this.clip(d);
                var newValue = d;
                _this.setState({
                    newValue: newValue,
                });
                context.emit("drag", { value: newValue });
            }
        });
        this.hammer.on("panend", function (e) {
            if (context) {
                var cc = _this.refs.centerCircle.getBoundingClientRect();
                var px = e.center.x - (cc.left + cc.width / 2);
                var py = e.center.y - (cc.top + cc.height / 2);
                var d = Math.sqrt(px * px + py * py) / _this.props.zoom.scale;
                d =
                    (d - _this.props.handle.startDistance) /
                        (_this.props.handle.endDistance - _this.props.handle.startDistance);
                d = _this.clip(d);
                var newValue = d;
                // if (this.props.handle.range) {
                //     newValue = Math.min(this.props.handle.range[1], Math.max(newValue, this.props.handle.range[0]));
                // }
                context.emit("end", { value: newValue });
                _this.setState({
                    dragging: false,
                });
                context = null;
            }
        });
    };
    DistanceRatioHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    DistanceRatioHandleView.prototype.render = function () {
        var _this = this;
        var handle = this.props.handle;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        var cx = fX(handle.cx);
        var cy = fY(handle.cy);
        var d1 = handle.startDistance * this.props.zoom.scale;
        var d2 = handle.endDistance * this.props.zoom.scale;
        var fRadius = function (x) { return x * (d2 - d1) + d1; };
        var makePath = function (value) {
            var path = core_1.Graphics.makePath();
            path.polarLineTo(0, 0, 90 - handle.startAngle, fRadius(value), 90 - handle.endAngle, fRadius(value), true);
            return renderer_1.renderSVGPath(path.path.cmds);
        };
        var px = function (value) {
            var alpha = core_1.Geometry.degreesToRadians(90 - handle.startAngle);
            return Math.cos(alpha) * fRadius(value);
        };
        var py = function (value) {
            var alpha = core_1.Geometry.degreesToRadians(90 - handle.startAngle);
            return -Math.sin(alpha) * fRadius(value);
        };
        return (React.createElement("g", { ref: "margin", className: utils_1.classNames("handle", "handle-distance", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
            React.createElement("g", { transform: "translate(" + cx + "," + cy + ")" },
                React.createElement("circle", { ref: "centerCircle", cx: 0, cy: 0, r: 0 }),
                React.createElement("path", { d: makePath(handle.value), className: "element-line handle-ghost" }),
                React.createElement("path", { d: makePath(handle.value), className: "element-line handle-highlight" }),
                handle.value == 0 ? (React.createElement("circle", { cx: px(handle.value), cy: py(handle.value), r: 3, className: "element-shape handle-highlight" })) : null),
            this.state.dragging ? (React.createElement("g", { transform: "translate(" + cx + "," + cy + ")" },
                React.createElement("path", { d: makePath(this.state.newValue), className: "element-line handle-hint" }),
                this.state.newValue == 0 ? (React.createElement("circle", { cx: px(this.state.newValue), cy: py(this.state.newValue), r: 3, className: "element-shape handle-hint" })) : null)) : null));
    };
    return DistanceRatioHandleView;
}(React.Component));
exports.DistanceRatioHandleView = DistanceRatioHandleView;
//# sourceMappingURL=distance_ratio.js.map