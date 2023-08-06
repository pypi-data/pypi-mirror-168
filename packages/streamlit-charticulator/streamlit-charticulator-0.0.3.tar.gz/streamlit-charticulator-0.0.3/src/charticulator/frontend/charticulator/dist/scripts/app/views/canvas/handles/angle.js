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
exports.AngleHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var utils_1 = require("../../../utils");
var common_1 = require("./common");
var AngleHandleView = /** @class */ (function (_super) {
    __extends(AngleHandleView, _super);
    function AngleHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
            newValue: _this.props.handle.value,
        };
        return _this;
    }
    AngleHandleView.prototype.clipAngle = function (v) {
        v = Math.round(v / 15) * 15;
        var min = this.props.handle.clipAngles[0];
        var max = this.props.handle.clipAngles[1];
        if (min != null) {
            while (v >= min) {
                v -= 360;
            }
            while (v <= min) {
                v += 360;
            }
        }
        if (max != null) {
            while (v <= max) {
                v += 360;
            }
            while (v >= max) {
                v -= 360;
            }
        }
        return v;
    };
    AngleHandleView.prototype.componentDidMount = function () {
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
                var newValue = _this.clipAngle((Math.atan2(-px, py) / Math.PI) * 180 + 180);
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
                var newValue = _this.clipAngle((Math.atan2(-px, py) / Math.PI) * 180 + 180);
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
    AngleHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    // eslint-disable-next-line
    AngleHandleView.prototype.render = function () {
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
        var radius = handle.radius * this.props.zoom.scale + 10;
        var shapeF = AngleHandleView.shapeCircle;
        if (handle.icon == "<") {
            shapeF = AngleHandleView.shapeLeft;
        }
        if (handle.icon == ">") {
            shapeF = AngleHandleView.shapeRight;
        }
        return (React.createElement("g", { ref: "margin", className: utils_1.classNames("handle", "handle-angle", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]) },
            React.createElement("g", { transform: "translate(" + cx + "," + cy + ") rotate(" + (180 + handle.value) + ")" },
                React.createElement("circle", { ref: "centerCircle", cx: 0, cy: 0, r: 0 }),
                React.createElement("line", { x1: 0, y1: 0, x2: 0, y2: radius, className: "element-line handle-ghost" }),
                React.createElement("path", { d: shapeF(9), transform: "translate(0," + radius + ")", className: "element-shape handle-ghost" }),
                React.createElement("line", { x1: 0, y1: 0, x2: 0, y2: radius, className: "element-line handle-highlight" }),
                React.createElement("path", { d: shapeF(5), transform: "translate(0," + radius + ")", className: "element-shape handle-highlight" })),
            this.state.dragging ? (React.createElement("g", { transform: "translate(" + cx + "," + cy + ") rotate(" + (180 + this.state.newValue) + ")" },
                React.createElement("line", { x1: 0, y1: 0, x2: 0, y2: radius, className: "element-line handle-hint" }),
                React.createElement("path", { d: shapeF(5), transform: "translate(0," + radius + ")", className: "element-shape handle-hint" }))) : null));
        // let x: number, y: number;
        // let nx: number, ny: number;
        // let shape: string;
        // let scale = this.props.handle.total || 1;
        // switch (handle.axis) {
        //     case "x": {
        //         x = fX(handle.x + handle.value * handle.sign * scale);
        //         y = fY(handle.y);
        //         nx = fX(handle.x + this.state.newValue * handle.sign * scale);
        //         ny = fY(handle.y);
        //         shape = "M0,0l5,12.72l-10,0Z";
        //     } break;
        //     case "y": {
        //         x = fX(handle.x);
        //         y = fY(handle.y + handle.value * handle.sign * scale);
        //         nx = fX(handle.x);
        //         ny = fY(handle.y + this.state.newValue * handle.sign * scale);
        //         shape = "M0,0l-12.72,5l0,-10Z";
        //     } break;
        // }
        // return (
        //     <g ref="margin" className={classNames("handle", "handle-gap-" + handle.axis, ["active", this.state.dragging], ["visible", handle.visible || this.props.visible])}>
        //         <path className="element-shape handle-ghost"
        //             transform={`translate(${x.toFixed(6)},${y.toFixed(6)})`}
        //             d={shape}
        //         />
        //         <path className="element-shape handle-highlight"
        //             transform={`translate(${x.toFixed(6)},${y.toFixed(6)})`}
        //             d={shape}
        //         />
        //         {this.state.dragging ? (
        //             <path className="element-shape handle-hint"
        //                 transform={`translate(${nx.toFixed(6)},${ny.toFixed(6)})`}
        //                 d={shape}
        //             />
        //         ) : null}
        //     </g>
        // );
    };
    AngleHandleView.shapeCircle = function (r) {
        return "M -" + r + " 0 A " + r + " " + r + " 0 1 0 " + r + " 0 A " + r + " " + r + " 0 1 0 " + -r + " 0 Z";
    };
    AngleHandleView.shapeRight = function (r) {
        return "M 0 " + -r + " L " + -1.5 * r + " 0 L 0 " + r + " Z";
    };
    AngleHandleView.shapeLeft = function (r) {
        return "M 0 " + -r + " L " + 1.5 * r + " 0 L 0 " + r + " Z";
    };
    return AngleHandleView;
}(React.Component));
exports.AngleHandleView = AngleHandleView;
//# sourceMappingURL=angle.js.map