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
exports.PointHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../../core");
var utils_1 = require("../../../utils");
var common_1 = require("./common");
var POINT_SIZE = 3;
var POINT_GHOST_SIZE = 6;
var PointHandleView = /** @class */ (function (_super) {
    __extends(PointHandleView, _super);
    function PointHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newXValue: _this.props.handle.x,
            newYValue: _this.props.handle.y,
        };
        return _this;
    }
    PointHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.circle);
        this.hammer.add(new Hammer.Pan());
        var context = null;
        var oldXValue;
        var oldYValue;
        var dXIntegrate = 0;
        var dXLast = 0;
        var dYIntegrate = 0;
        var dYLast = 0;
        this.hammer.on("panstart", function () {
            context = new common_1.HandlesDragContext();
            oldXValue = _this.props.handle.x;
            oldYValue = _this.props.handle.y;
            dXLast = 0;
            dYLast = 0;
            dXIntegrate = 0;
            dYIntegrate = 0;
            _this.setState({
                dragging: true,
                newXValue: oldXValue,
                newYValue: oldYValue,
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
                var newXValue = dXIntegrate + oldXValue;
                var newYValue = dYIntegrate + oldYValue;
                _this.setState({
                    newXValue: newXValue,
                    newYValue: newYValue,
                });
                context.emit("drag", { x: newXValue, y: newYValue });
            }
        });
        this.hammer.on("panend", function (e) {
            if (context) {
                dXIntegrate += (e.deltaX - dXLast) / _this.props.zoom.scale;
                dYIntegrate += -(e.deltaY - dYLast) / _this.props.zoom.scale;
                dXLast = e.deltaX;
                dYLast = e.deltaY;
                var newXValue = dXIntegrate + oldXValue;
                var newYValue = dYIntegrate + oldYValue;
                context.emit("end", { x: newXValue, y: newYValue });
                _this.setState({
                    dragging: false,
                });
                context = null;
            }
        });
    };
    PointHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    PointHandleView.prototype.render = function () {
        var handle = this.props.handle;
        var _a = core_1.Geometry.applyZoom(this.props.zoom, {
            x: handle.x,
            y: -handle.y,
        }), x = _a.x, y = _a.y;
        var _b = core_1.Geometry.applyZoom(this.props.zoom, {
            x: this.state.newXValue,
            y: -this.state.newYValue,
        }), hx = _b.x, hy = _b.y;
        return (React.createElement("g", { ref: "circle", className: utils_1.classNames("handle", "handle-point", ["active", this.state.dragging], ["snapped", this.props.snapped], ["visible", handle.visible || this.props.visible]) },
            React.createElement("circle", { className: "element-shape handle-ghost", cx: x, cy: y, r: POINT_GHOST_SIZE }),
            React.createElement("circle", { className: "element-shape handle-highlight", cx: x, cy: y, r: POINT_SIZE }),
            this.state.dragging ? (React.createElement("g", null,
                React.createElement("line", { className: "element-line handle-hint", x1: hx, y1: hy, x2: x, y2: y }),
                React.createElement("circle", { className: "element-shape handle-hint", cx: hx, cy: hy, r: POINT_SIZE }))) : null));
    };
    return PointHandleView;
}(React.Component));
exports.PointHandleView = PointHandleView;
//# sourceMappingURL=point.js.map