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
exports.TextAlignmentHandleView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../../core");
var globals = require("../../../globals");
var utils_1 = require("../../../utils");
var controllers_1 = require("../../../controllers");
var components_1 = require("../../../components");
var common_1 = require("./common");
var types_1 = require("../../../../core/specification/types");
var TextAlignmentHandleView = /** @class */ (function (_super) {
    __extends(TextAlignmentHandleView, _super);
    function TextAlignmentHandleView(props) {
        var _this = _super.call(this, props) || this;
        _this.handleClick = _this.handleClick.bind(_this);
        _this.state = {
            dragging: false,
            newAlignment: props.handle.alignment,
            newRotation: props.handle.rotation,
        };
        return _this;
    }
    TextAlignmentHandleView.prototype.getRelativePoint = function (px, py) {
        var anchorBounds = this.anchorCircle.getBoundingClientRect();
        var x = px - (anchorBounds.left + anchorBounds.width / 2);
        var y = py - (anchorBounds.top + anchorBounds.height / 2);
        return { x: x / this.props.zoom.scale, y: -y / this.props.zoom.scale };
    };
    // eslint-disable-next-line
    TextAlignmentHandleView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.container);
        this.hammer.add(new Hammer.Pan({ threshold: 1 }));
        this.hammer.add(new Hammer.Tap());
        var mode = null;
        var startX = 0;
        var startY = 0;
        var sumDeltaX = 0, dXLast = 0;
        var sumDeltaY = 0, dYLast = 0;
        var p0;
        var previousAlignment;
        var previousRotation;
        var context = null;
        var newStateFromMoveAndRotate = function (dx, dy, newRotation, snapping) {
            var rect = _this.getRectFromAlignment(previousAlignment, previousRotation);
            var acx = rect.cx - _this.props.handle.anchorX;
            var acy = rect.cy - _this.props.handle.anchorY;
            var newAlignment = {
                x: previousAlignment.x,
                y: previousAlignment.y,
                xMargin: previousAlignment.xMargin,
                yMargin: previousAlignment.yMargin,
            };
            var cos = Math.cos(core_1.Geometry.degreesToRadians(newRotation));
            var sin = Math.sin(core_1.Geometry.degreesToRadians(newRotation));
            var pdx = dx * cos + dy * sin;
            var pdy = -dx * sin + dy * cos;
            var pcx = acx * cos + acy * sin;
            var pcy = -acx * sin + acy * cos;
            var npcx = pcx + pdx;
            var npcy = pcy + pdy;
            if (snapping && Math.abs(npcy) < 5 / _this.props.zoom.scale) {
                newAlignment.y = types_1.TextAlignmentVertical.Middle;
            }
            else if (npcy < 0) {
                newAlignment.y = types_1.TextAlignmentVertical.Top;
                newAlignment.yMargin = -npcy - _this.props.handle.textHeight / 2;
                if (Math.abs(newAlignment.yMargin) < 5 / _this.props.zoom.scale) {
                    newAlignment.yMargin = 0;
                }
            }
            else {
                newAlignment.y = types_1.TextAlignmentVertical.Bottom;
                newAlignment.yMargin = npcy - _this.props.handle.textHeight / 2;
                if (Math.abs(newAlignment.yMargin) < 5 / _this.props.zoom.scale) {
                    newAlignment.yMargin = 0;
                }
            }
            if (snapping && Math.abs(npcx) < 5 / _this.props.zoom.scale) {
                newAlignment.x = types_1.TextAlignmentHorizontal.Middle;
            }
            else if (npcx < 0) {
                newAlignment.x = types_1.TextAlignmentHorizontal.Right;
                newAlignment.xMargin = -npcx - _this.props.handle.textWidth / 2;
                if (Math.abs(newAlignment.xMargin) < 5 / _this.props.zoom.scale) {
                    newAlignment.xMargin = 0;
                }
            }
            else {
                newAlignment.x = types_1.TextAlignmentHorizontal.Left;
                newAlignment.xMargin = npcx - _this.props.handle.textWidth / 2;
                if (Math.abs(newAlignment.xMargin) < 5 / _this.props.zoom.scale) {
                    newAlignment.xMargin = 0;
                }
            }
            return [newAlignment, newRotation];
        };
        var handleRotation = function (p1, commit) {
            if (commit === void 0) { commit = false; }
            var rect = _this.getRectFromAlignment(previousAlignment, previousRotation);
            var ox = rect.cx - _this.props.handle.anchorX;
            var oy = rect.cy - _this.props.handle.anchorY;
            var newRotation = (Math.atan2(p1.y - oy, p1.x - ox) / Math.PI) * 180 + 180;
            newRotation = Math.round(newRotation / 15) * 15;
            var newAlignment = newStateFromMoveAndRotate(0, 0, newRotation, false)[0];
            if (commit) {
                _this.setState({
                    dragging: false,
                });
                context.emit("end", { alignment: newAlignment, rotation: newRotation });
            }
            else {
                _this.setState({
                    newAlignment: newAlignment,
                    newRotation: newRotation,
                });
                context.emit("drag", {
                    alignment: newAlignment,
                    rotation: newRotation,
                });
            }
        };
        var handleAlignment = function (p1, commit) {
            if (commit === void 0) { commit = false; }
            var _a = __read(newStateFromMoveAndRotate(p1.x - p0.x, p1.y - p0.y, previousRotation, true), 1), newAlignment = _a[0];
            if (commit) {
                _this.setState({
                    dragging: false,
                });
                context.emit("end", {
                    alignment: newAlignment,
                    rotation: previousRotation,
                });
            }
            else {
                _this.setState({
                    newAlignment: newAlignment,
                });
                context.emit("drag", {
                    alignment: newAlignment,
                    rotation: previousRotation,
                });
            }
        };
        this.hammer.on("panstart", function (e) {
            var cx = e.center.x - e.deltaX;
            var cy = e.center.y - e.deltaY;
            startX = cx;
            startY = cy;
            dXLast = e.deltaX;
            dYLast = e.deltaY;
            sumDeltaX = e.deltaX;
            sumDeltaY = e.deltaY;
            var el = document.elementFromPoint(cx, cy);
            context = new common_1.HandlesDragContext();
            _this.props.onDragStart(_this.props.handle, context);
            p0 = _this.getRelativePoint(cx, cy);
            var p1 = _this.getRelativePoint(cx + e.deltaX, cy + e.deltaY);
            previousAlignment = _this.props.handle.alignment;
            previousRotation = _this.props.handle.rotation;
            if (el == _this.rotationCircle) {
                mode = "rotation";
                handleRotation(p1);
            }
            else {
                mode = "alignment";
                handleAlignment(p1);
            }
            _this.setState({
                dragging: true,
                newAlignment: previousAlignment,
                newRotation: previousRotation,
            });
        });
        this.hammer.on("pan", function (e) {
            sumDeltaX += e.deltaX - dXLast;
            sumDeltaY += e.deltaY - dYLast;
            dXLast = e.deltaX;
            dYLast = e.deltaY;
            var cx = startX + sumDeltaX;
            var cy = startY + sumDeltaY;
            // cx = e.center.x;
            // cy = e.center.y;
            var p1 = _this.getRelativePoint(cx, cy);
            if (mode == "rotation") {
                handleRotation(p1);
            }
            else {
                handleAlignment(p1);
            }
        });
        this.hammer.on("panend", function (e) {
            sumDeltaX += e.deltaX - dXLast;
            sumDeltaY += e.deltaY - dYLast;
            dXLast = e.deltaX;
            dYLast = e.deltaY;
            var cx = startX + sumDeltaX;
            var cy = startY + sumDeltaY;
            // cx = e.center.x;
            // cy = e.center.y;
            var p1 = _this.getRelativePoint(cx, cy);
            if (mode == "rotation") {
                handleRotation(p1, true);
            }
            else {
                handleAlignment(p1, true);
            }
            context = null;
        });
    };
    TextAlignmentHandleView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    TextAlignmentHandleView.prototype.handleClick = function () {
        var _this = this;
        if (this.props.handle.text == null) {
            return;
        }
        globals.popupController.popupAt(function (context) {
            return (React.createElement(controllers_1.PopupView, { context: context },
                React.createElement("div", { className: "handle-text-view-popup" },
                    React.createElement(components_1.EditableTextView, { text: _this.props.handle.text, autofocus: true, onEdit: function (newText) {
                            var dragContext = new common_1.HandlesDragContext();
                            _this.props.onDragStart(_this.props.handle, dragContext);
                            dragContext.emit("end", { text: newText });
                            context.close();
                        } }))));
        }, {
            anchor: this.container,
        });
    };
    TextAlignmentHandleView.prototype.getRectFromAlignment = function (alignment, rotation) {
        var cos = Math.cos(core_1.Geometry.degreesToRadians(rotation));
        var sin = Math.sin(core_1.Geometry.degreesToRadians(rotation));
        var dx = 0, dy = 0;
        if (alignment.x == "left") {
            dx = this.props.handle.textWidth / 2 + alignment.xMargin;
        }
        if (alignment.x == "right") {
            dx = -this.props.handle.textWidth / 2 - alignment.xMargin;
        }
        var fx = dx - this.props.handle.textWidth / 2 - 10 / this.props.zoom.scale;
        if (alignment.y == "top") {
            dy = -this.props.handle.textHeight / 2 - alignment.yMargin;
        }
        if (alignment.y == "bottom") {
            dy = +this.props.handle.textHeight / 2 + alignment.yMargin;
        }
        return {
            cx: this.props.handle.anchorX + dx * cos - dy * sin,
            cy: this.props.handle.anchorY + dx * sin + dy * cos,
            fx: this.props.handle.anchorX + fx * cos - dy * sin,
            fy: this.props.handle.anchorY + fx * sin + dy * cos,
            width: this.props.handle.textWidth,
            height: this.props.handle.textHeight,
            rotation: rotation,
        };
    };
    TextAlignmentHandleView.prototype.renderDragging = function () {
        if (this.state.dragging) {
            var zoom = this.props.zoom;
            var rect = this.getRectFromAlignment(this.state.newAlignment, this.state.newRotation);
            var p = core_1.Geometry.applyZoom(zoom, { x: rect.cx, y: -rect.cy });
            var margin = 0;
            return (React.createElement("g", null,
                React.createElement("rect", { className: "element-shape handle-hint", transform: "translate(" + p.x.toFixed(6) + "," + p.y.toFixed(6) + ")rotate(" + -rect.rotation + ")", x: (-rect.width / 2) * zoom.scale - margin, y: (-rect.height / 2) * zoom.scale - margin, width: rect.width * zoom.scale + margin * 2, height: rect.height * zoom.scale + margin * 2 })));
        }
        else {
            return null;
        }
    };
    TextAlignmentHandleView.prototype.render = function () {
        var _this = this;
        var handle = this.props.handle;
        var zoom = this.props.zoom;
        var margin = 0;
        var rect = this.getRectFromAlignment(handle.alignment, handle.rotation);
        var p = core_1.Geometry.applyZoom(zoom, { x: rect.cx, y: -rect.cy });
        var anchor = core_1.Geometry.applyZoom(zoom, {
            x: handle.anchorX,
            y: -handle.anchorY,
        });
        var fp = core_1.Geometry.applyZoom(zoom, { x: rect.fx, y: -rect.fy });
        return (React.createElement("g", { className: utils_1.classNames("handle", "handle-text-input", ["active", this.state.dragging], ["visible", handle.visible || this.props.visible]), onClick: this.handleClick, ref: function (e) { return (_this.container = e); } },
            React.createElement("circle", { className: "element-shape handle-ghost", cx: anchor.x, cy: anchor.y, r: 0, ref: function (e) { return (_this.anchorCircle = e); } }),
            React.createElement("g", { transform: "translate(" + (fp.x - 16) + "," + (fp.y - 16) + ")" },
                React.createElement("path", { className: "element-solid handle-highlight", d: "M22.05664,15a.99974.99974,0,0,0-1,1,5.05689,5.05689,0,1,1-6.07794-4.95319v2.38654l6.04468-3.49042L14.9787,6.45245V9.02539A7.05306,7.05306,0,1,0,23.05664,16,.99973.99973,0,0,0,22.05664,15Z" })),
            React.createElement("line", { className: "element-line handle-dashed-highlight", x1: anchor.x, y1: anchor.y, x2: p.x, y2: p.y }),
            React.createElement("rect", { className: "element-shape handle-ghost element-text-rect", transform: "translate(" + p.x.toFixed(6) + "," + p.y.toFixed(6) + ")rotate(" + -rect.rotation + ")", x: (-rect.width / 2) * zoom.scale - margin, y: (-rect.height / 2) * zoom.scale - margin, width: rect.width * zoom.scale + margin * 2, height: rect.height * zoom.scale + margin * 2 }),
            React.createElement("circle", { className: "element-shape handle-ghost element-rotation", ref: function (e) { return (_this.rotationCircle = e); }, cx: fp.x, cy: fp.y, r: 8 }),
            this.renderDragging()));
    };
    return TextAlignmentHandleView;
}(React.Component));
exports.TextAlignmentHandleView = TextAlignmentHandleView;
//# sourceMappingURL=text_alignment.js.map