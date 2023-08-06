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
exports.MarginHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var utils_1 = require("../../../utils");
var common_1 = require("./common");
var MarginHandleView = /** @class */ (function (_super) {
    __extends(MarginHandleView, _super);
    function MarginHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newValue: _this.props.handle.value,
        };
        return _this;
    }
    MarginHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.margin);
        this.hammer.add(new Hammer.Pan({ threshold: 1 }));
        var context = null;
        var oldValue;
        var sign;
        var total;
        var dXIntegrate = 0;
        var dXLast = 0;
        var dYIntegrate = 0;
        var dYLast = 0;
        this.hammer.on("panstart", function () {
            context = new common_1.HandlesDragContext();
            oldValue = _this.props.handle.value;
            sign = _this.props.handle.sign;
            if (_this.props.handle.total != null) {
                total = _this.props.handle.total;
            }
            else {
                total = 1;
            }
            dXLast = 0;
            dYLast = 0;
            dXIntegrate = 0;
            dYIntegrate = 0;
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
                var newValue = ((_this.props.handle.axis == "x" ? dXIntegrate : dYIntegrate) * sign) /
                    total +
                    oldValue;
                if (_this.props.handle.range) {
                    newValue = Math.min(_this.props.handle.range[1], Math.max(newValue, _this.props.handle.range[0]));
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
                var newValue = ((_this.props.handle.axis == "x" ? dXIntegrate : dYIntegrate) * sign) /
                    total +
                    oldValue;
                if (_this.props.handle.range) {
                    newValue = Math.min(_this.props.handle.range[1], Math.max(newValue, _this.props.handle.range[0]));
                }
                context.emit("end", { value: newValue });
                _this.setState({
                    dragging: false,
                });
                context = null;
            }
        });
    };
    MarginHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    MarginHandleView.prototype.render = function () {
        var _this = this;
        var handle = this.props.handle;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        var x, y;
        var nx, ny;
        var shape;
        var scale = this.props.handle.total || 1;
        switch (handle.axis) {
            case "x":
                {
                    x = fX(handle.x + handle.value * handle.sign * scale);
                    y = fY(handle.y);
                    nx = fX(handle.x + this.state.newValue * handle.sign * scale);
                    ny = fY(handle.y);
                    shape = "M0,0l5,12.72l-10,0Z";
                }
                break;
            case "y":
                {
                    x = fX(handle.x);
                    y = fY(handle.y + handle.value * handle.sign * scale);
                    nx = fX(handle.x);
                    ny = fY(handle.y + this.state.newValue * handle.sign * scale);
                    shape = "M0,0l-12.72,5l0,-10Z";
                }
                break;
        }
        return (React.createElement("g", { ref: "margin", className: utils_1.classNames("handle", "handle-gap-" + handle.axis, ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
            React.createElement("path", { className: "element-shape handle-ghost", transform: "translate(" + x.toFixed(6) + "," + y.toFixed(6) + ")", d: shape }),
            React.createElement("path", { className: "element-shape handle-highlight", transform: "translate(" + x.toFixed(6) + "," + y.toFixed(6) + ")", d: shape }),
            this.state.dragging ? (React.createElement("path", { className: "element-shape handle-hint", transform: "translate(" + nx.toFixed(6) + "," + ny.toFixed(6) + ")", d: shape })) : null));
    };
    return MarginHandleView;
}(React.Component));
exports.MarginHandleView = MarginHandleView;
//# sourceMappingURL=margin.js.map