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
exports.LineHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var utils_1 = require("../../../utils");
var common_1 = require("./common");
var LineHandleView = /** @class */ (function (_super) {
    __extends(LineHandleView, _super);
    function LineHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newValue: _this.props.handle.value,
        };
        return _this;
    }
    LineHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.line);
        this.hammer.add(new Hammer.Pan({ threshold: 1 }));
        var context = null;
        var oldValue;
        var dXIntegrate = 0;
        var dXLast = 0;
        var dYIntegrate = 0;
        var dYLast = 0;
        this.hammer.on("panstart", function () {
            context = new common_1.HandlesDragContext();
            oldValue = _this.props.handle.value;
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
                var newValue = (_this.props.handle.axis == "x" ? dXIntegrate : dYIntegrate) +
                    oldValue;
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
                var newValue = (_this.props.handle.axis == "x" ? dXIntegrate : dYIntegrate) +
                    oldValue;
                context.emit("end", { value: newValue });
                _this.setState({
                    dragging: false,
                });
                context = null;
            }
        });
    };
    LineHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    LineHandleView.prototype.render = function () {
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
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-x", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("g", { ref: "line" },
                        React.createElement("line", { className: "element-line handle-ghost", x1: fX(handle.value), x2: fX(handle.value), y1: fY(handle.span[0]), y2: fY(handle.span[1]) }),
                        React.createElement("line", { className: "element-line handle-highlight", x1: fX(handle.value), x2: fX(handle.value), y1: fY(handle.span[0]), y2: fY(handle.span[1]) })),
                    this.state.dragging ? (React.createElement("g", null,
                        React.createElement("line", { className: "element-line handle-hint", x1: fX(this.state.newValue), x2: fX(this.state.newValue), y1: fY(handle.span[0]), y2: fY(handle.span[1]) }))) : null));
            }
            case "y": {
                return (React.createElement("g", { className: utils_1.classNames("handle", "handle-line-y", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
                    React.createElement("g", { ref: "line" },
                        React.createElement("line", { className: "element-line handle-ghost", y1: fY(handle.value), y2: fY(handle.value), x1: fX(handle.span[0]), x2: fX(handle.span[1]) }),
                        React.createElement("line", { className: "element-line handle-highlight", y1: fY(handle.value), y2: fY(handle.value), x1: fX(handle.span[0]), x2: fX(handle.span[1]) })),
                    this.state.dragging ? (React.createElement("g", null,
                        React.createElement("line", { className: "element-line handle-hint", y1: fY(this.state.newValue), y2: fY(this.state.newValue), x1: fX(handle.span[0]), x2: fX(handle.span[1]) }))) : null));
            }
        }
    };
    return LineHandleView;
}(React.Component));
exports.LineHandleView = LineHandleView;
//# sourceMappingURL=line.js.map