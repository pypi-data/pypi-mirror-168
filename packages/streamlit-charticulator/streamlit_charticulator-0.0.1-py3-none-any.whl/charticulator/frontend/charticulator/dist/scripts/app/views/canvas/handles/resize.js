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
exports.ResizeHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var utils_1 = require("../../../utils");
var ResizeHandleView = /** @class */ (function (_super) {
    __extends(ResizeHandleView, _super);
    function ResizeHandleView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dragging: false,
            newX1: _this.props.cx - _this.props.width / 2,
            newY1: _this.props.cy - _this.props.height / 2,
            newX2: _this.props.cx + _this.props.width / 2,
            newY2: _this.props.cy + _this.props.height / 2,
        };
        return _this;
    }
    ResizeHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.container);
        this.hammer.add(new Hammer.Pan());
        var oldWidth, oldHeight;
        var dXIntegrate, dYIntegrate;
        var dXLast, dYLast;
        var opX, opY;
        var compute = function () {
            var newWidth = oldWidth + dXIntegrate * opX * 2;
            var newHeight = oldHeight + dYIntegrate * opY * 2;
            if (newWidth < 50) {
                newWidth = 50;
            }
            if (newHeight < 50) {
                newHeight = 50;
            }
            return [newWidth, newHeight];
        };
        this.hammer.on("panstart", function (e) {
            var element = document.elementFromPoint(e.center.x - e.deltaX, e.center.y - e.deltaY);
            oldWidth = _this.props.width;
            oldHeight = _this.props.height;
            dXIntegrate = e.deltaX / _this.props.zoom.scale;
            dXLast = e.deltaX;
            dYIntegrate = -e.deltaY / _this.props.zoom.scale;
            dYLast = e.deltaY;
            opX = 0;
            opY = 0;
            while (element) {
                if (element == _this.refs.lineX1) {
                    opX = -1;
                }
                if (element == _this.refs.lineX2) {
                    opX = 1;
                }
                if (element == _this.refs.lineY1) {
                    opY = -1;
                }
                if (element == _this.refs.lineY2) {
                    opY = 1;
                }
                if (element == _this.refs.cornerX1Y1) {
                    opX = -1;
                    opY = -1;
                }
                if (element == _this.refs.cornerX1Y2) {
                    opX = -1;
                    opY = 1;
                }
                if (element == _this.refs.cornerX2Y1) {
                    opX = 1;
                    opY = -1;
                }
                if (element == _this.refs.cornerX2Y2) {
                    opX = 1;
                    opY = 1;
                }
                element = element.parentElement;
            }
            var _a = __read(compute(), 2), nW = _a[0], nH = _a[1];
            _this.setState({
                dragging: true,
                newX1: _this.props.cx - nW / 2,
                newY1: _this.props.cy - nH / 2,
                newX2: _this.props.cx + nW / 2,
                newY2: _this.props.cy + nH / 2,
            });
        });
        this.hammer.on("pan", function (e) {
            dXIntegrate += (e.deltaX - dXLast) / _this.props.zoom.scale;
            dXLast = e.deltaX;
            dYIntegrate += -(e.deltaY - dYLast) / _this.props.zoom.scale;
            dYLast = e.deltaY;
            var _a = __read(compute(), 2), nW = _a[0], nH = _a[1];
            _this.setState({
                newX1: _this.props.cx - nW / 2,
                newY1: _this.props.cy - nH / 2,
                newX2: _this.props.cx + nW / 2,
                newY2: _this.props.cy + nH / 2,
            });
        });
        this.hammer.on("panend", function (e) {
            dXIntegrate += (e.deltaX - dXLast) / _this.props.zoom.scale;
            dXLast = e.deltaX;
            dYIntegrate += -(e.deltaY - dYLast) / _this.props.zoom.scale;
            dYLast = e.deltaY;
            var _a = __read(compute(), 2), nW = _a[0], nH = _a[1];
            _this.setState({
                dragging: false,
            });
            _this.props.onResize(nW, nH);
        });
    };
    ResizeHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    // eslint-disable-next-line
    ResizeHandleView.prototype.render = function () {
        var _this = this;
        var fX = function (x) {
            return x * _this.props.zoom.scale + _this.props.zoom.centerX;
        };
        var fY = function (y) {
            return -y * _this.props.zoom.scale + _this.props.zoom.centerY;
        };
        var x1 = this.props.cx - this.props.width / 2;
        var y1 = this.props.cy - this.props.height / 2;
        var x2 = this.props.cx + this.props.width / 2;
        var y2 = this.props.cy + this.props.height / 2;
        return (React.createElement("g", { className: utils_1.classNames("handle", "handle-resize", [
                "active",
                this.state.dragging,
            ]), ref: "container" },
            React.createElement("g", { ref: "lineY1", style: { cursor: "ns-resize" } },
                React.createElement("line", { className: "element-line handle-ghost", x1: fX(x1), y1: fY(y1), x2: fX(x2), y2: fY(y1) }),
                React.createElement("line", { className: "element-line handle-highlight", x1: fX(x1), y1: fY(y1), x2: fX(x2), y2: fY(y1) })),
            React.createElement("g", { ref: "lineY2", style: { cursor: "ns-resize" } },
                React.createElement("line", { className: "element-line handle-ghost", x1: fX(x1), y1: fY(y2), x2: fX(x2), y2: fY(y2) }),
                React.createElement("line", { className: "element-line handle-highlight", x1: fX(x1), y1: fY(y2), x2: fX(x2), y2: fY(y2) })),
            React.createElement("g", { ref: "lineX1", style: { cursor: "ew-resize" } },
                React.createElement("line", { className: "element-line handle-ghost", x1: fX(x1), y1: fY(y1), x2: fX(x1), y2: fY(y2) }),
                React.createElement("line", { className: "element-line handle-highlight", x1: fX(x1), y1: fY(y1), x2: fX(x1), y2: fY(y2) })),
            React.createElement("g", { ref: "lineX2", style: { cursor: "ew-resize" } },
                React.createElement("line", { className: "element-line handle-ghost", x1: fX(x2), y1: fY(y1), x2: fX(x2), y2: fY(y2) }),
                React.createElement("line", { className: "element-line handle-highlight", x1: fX(x2), y1: fY(y1), x2: fX(x2), y2: fY(y2) })),
            React.createElement("circle", { className: "element-shape handle-ghost", style: { cursor: "nesw-resize" }, ref: "cornerX1Y1", cx: fX(x1), cy: fY(y1), r: 5 }),
            React.createElement("circle", { className: "element-shape handle-ghost", style: { cursor: "nwse-resize" }, ref: "cornerX2Y1", cx: fX(x2), cy: fY(y1), r: 5 }),
            React.createElement("circle", { className: "element-shape handle-ghost", style: { cursor: "nwse-resize" }, ref: "cornerX1Y2", cx: fX(x1), cy: fY(y2), r: 5 }),
            React.createElement("circle", { className: "element-shape handle-ghost", style: { cursor: "nesw-resize" }, ref: "cornerX2Y2", cx: fX(x2), cy: fY(y2), r: 5 }),
            this.state.dragging ? (React.createElement("g", null,
                React.createElement("line", { className: "element-line handle-hint", x1: fX(this.state.newX1), y1: fY(this.state.newY1), x2: fX(this.state.newX2), y2: fY(this.state.newY1) }),
                React.createElement("line", { className: "element-line handle-hint", x1: fX(this.state.newX1), y1: fY(this.state.newY2), x2: fX(this.state.newX2), y2: fY(this.state.newY2) }),
                React.createElement("line", { className: "element-line handle-hint", x1: fX(this.state.newX1), y1: fY(this.state.newY1), x2: fX(this.state.newX1), y2: fY(this.state.newY2) }),
                React.createElement("line", { className: "element-line handle-hint", x1: fX(this.state.newX2), y1: fY(this.state.newY1), x2: fX(this.state.newX2), y2: fY(this.state.newY2) }))) : null));
    };
    return ResizeHandleView;
}(React.Component));
exports.ResizeHandleView = ResizeHandleView;
//# sourceMappingURL=resize.js.map