"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.DropZoneView = void 0;
var React = require("react");
var core_1 = require("../../../core");
var globals = require("../../globals");
var utils_1 = require("../../utils");
var DropZoneView = /** @class */ (function (_super) {
    __extends(DropZoneView, _super);
    function DropZoneView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = { active: false };
        return _this;
    }
    DropZoneView.prototype.componentDidMount = function () {
        globals.dragController.registerDroppable(this, this.refs.container);
    };
    DropZoneView.prototype.componentWillUnmount = function () {
        globals.dragController.unregisterDroppable(this);
    };
    DropZoneView.prototype.onDragEnter = function (ctx) {
        var _this = this;
        var data = ctx.data;
        var handler = this.props.onDragEnter(data);
        if (handler) {
            this.setState({
                active: true,
            });
            ctx.onLeave(function () {
                _this.setState({
                    active: false,
                });
            });
            ctx.onDrop(function (point, modifiers) {
                return handler(point, modifiers);
            });
            return true;
        }
        else {
            return false;
        }
    };
    DropZoneView.prototype.makeClosePath = function () {
        var points = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            points[_i] = arguments[_i];
        }
        return "M" + points.map(function (d) { return d.x + "," + d.y; }).join("L") + "Z";
    };
    DropZoneView.prototype.makeDashedLine = function (p1, p2) {
        return (React.createElement("line", { className: "dropzone-element-dashline", x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y }));
    };
    DropZoneView.prototype.makeLine = function (p1, p2, arrow1, arrow2) {
        if (arrow1 === void 0) { arrow1 = 0; }
        if (arrow2 === void 0) { arrow2 = 0; }
        var d1 = core_1.Geometry.vectorScale(core_1.Geometry.vectorNormalize(core_1.Geometry.vectorSub(p2, p1)), arrow1);
        var n1 = core_1.Geometry.vectorScale(core_1.Geometry.vectorRotate90(d1), 0.25);
        var p1n = core_1.Geometry.vectorAdd(p1, d1);
        var p1a1 = core_1.Geometry.vectorAdd(p1n, n1);
        var p1a2 = core_1.Geometry.vectorSub(p1n, n1);
        var d2 = core_1.Geometry.vectorScale(core_1.Geometry.vectorNormalize(core_1.Geometry.vectorSub(p2, p1)), arrow2);
        var n2 = core_1.Geometry.vectorScale(core_1.Geometry.vectorRotate90(d2), 0.25);
        var p2n = core_1.Geometry.vectorSub(p2, d2);
        var p2a1 = core_1.Geometry.vectorAdd(p2n, n2);
        var p2a2 = core_1.Geometry.vectorSub(p2n, n2);
        return (React.createElement("g", { className: "dropzone-element-line" },
            React.createElement("line", { x1: p1n.x, y1: p1n.y, x2: p2n.x, y2: p2n.y, style: { strokeLinecap: "butt" } }),
            arrow1 > 0 ? React.createElement("path", { d: this.makeClosePath(p1a1, p1a2, p1) }) : null,
            ",",
            arrow2 > 0 ? React.createElement("path", { d: this.makeClosePath(p2a1, p2a2, p2) }) : null));
    };
    DropZoneView.prototype.makeTextAtCenter = function (p1, p2, text, dx, dy) {
        if (dx === void 0) { dx = 0; }
        if (dy === void 0) { dy = 0; }
        var cx = (p1.x + p2.x) / 2;
        var cy = (p1.y + p2.y) / 2;
        var angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
        var height = 9;
        var extra = "";
        if (Math.abs(angle) < Math.PI / 2) {
            extra = "translate(0, " + -height / 2 + ") rotate(180) translate(0, " + height / 2 + ")";
        }
        return (React.createElement("g", { transform: "translate(" + cx + "," + cy + ") rotate(" + ((angle + Math.PI) / Math.PI) * 180 + ") translate(" + dx + "," + dy + ") " + extra },
            React.createElement("text", { className: "dropzone-element-text", x: 0, y: 0, style: { textAnchor: "middle" } }, text)));
    };
    // eslint-disable-next-line
    DropZoneView.prototype.renderElement = function (z) {
        switch (z.type) {
            case "line": {
                var zone = z;
                var zp2 = zone.p1, zp1 = zone.p2;
                zp1 = core_1.Geometry.applyZoom(this.props.zoom, { x: zp1.x, y: -zp1.y });
                zp2 = core_1.Geometry.applyZoom(this.props.zoom, { x: zp2.x, y: -zp2.y });
                var vD = core_1.Geometry.vectorNormalize(core_1.Geometry.vectorSub(zp2, zp1));
                var vN = core_1.Geometry.vectorRotate90(vD);
                return (React.createElement("g", null,
                    React.createElement("path", { className: "dropzone-highlighter", d: this.makeClosePath(
                        // zp1, zp2,
                        core_1.Geometry.vectorAdd(zp1, core_1.Geometry.vectorScale(vN, -10)), core_1.Geometry.vectorAdd(zp2, core_1.Geometry.vectorScale(vN, -10)), core_1.Geometry.vectorAdd(zp2, core_1.Geometry.vectorScale(vN, 25)), core_1.Geometry.vectorAdd(zp1, core_1.Geometry.vectorScale(vN, 25))) }),
                    React.createElement("path", { className: "dropzone-element-solid", d: this.makeClosePath(zp1, zp2, core_1.Geometry.vectorAdd(zp2, core_1.Geometry.vectorScale(vN, 5)), core_1.Geometry.vectorAdd(zp1, core_1.Geometry.vectorScale(vN, 5))) }),
                    this.makeTextAtCenter(zp1, zp2, zone.title, 0, -6)));
            }
            case "arc": {
                var makeArc = function (x, y, radius, startAngle, endAngle) {
                    var angleOffset = -90;
                    var start = [
                        x +
                            radius *
                                Math.cos(core_1.Geometry.degreesToRadians(angleOffset + startAngle)),
                        y +
                            radius *
                                Math.sin(core_1.Geometry.degreesToRadians(angleOffset + startAngle)),
                    ];
                    var end = [
                        x +
                            radius *
                                Math.cos(core_1.Geometry.degreesToRadians(angleOffset + endAngle)),
                        y +
                            radius *
                                Math.sin(core_1.Geometry.degreesToRadians(angleOffset + endAngle)),
                    ];
                    var largeArcFlag = endAngle - startAngle < 180 ? 0 : 1;
                    return [
                        "M",
                        start[0].toFixed(6),
                        start[1].toFixed(6),
                        "A",
                        radius.toFixed(6),
                        radius.toFixed(6),
                        0,
                        largeArcFlag,
                        1,
                        end[0].toFixed(6),
                        end[1].toFixed(6),
                    ].join(" ");
                };
                var zone = z;
                var zcenter = core_1.Geometry.applyZoom(this.props.zoom, {
                    x: zone.center.x,
                    y: -zone.center.y,
                });
                var zradius = zone.radius * this.props.zoom.scale;
                var width = 5;
                var angle1 = zone.angleStart;
                var angle2 = zone.angleEnd;
                var angleCenter = (angle1 + angle2) / 2;
                if ((angle2 - angle1) % 360 == 0) {
                    angle2 -= 1e-4;
                }
                var arc = makeArc(zcenter.x, zcenter.y, zradius + width / 2, angle1, angle2);
                var p1 = core_1.Geometry.vectorAdd(zcenter, core_1.Geometry.vectorRotate({ x: zradius + 5, y: 0 }, core_1.Geometry.degreesToRadians(-angleCenter + 1 + 90)));
                var p2 = core_1.Geometry.vectorAdd(zcenter, core_1.Geometry.vectorRotate({ x: zradius + 5, y: 0 }, core_1.Geometry.degreesToRadians(-angleCenter - 1 + 90)));
                return (React.createElement("g", null,
                    React.createElement("path", { className: "dropzone-highlighter-stroke", d: arc, style: { strokeWidth: 25 } }),
                    React.createElement("path", { className: "dropzone-element-arc", d: arc, style: { strokeWidth: 5 } }),
                    this.makeTextAtCenter(p1, p2, zone.title, 0, 8)));
            }
            // case "coordinate": {
            //     let zone = z as Prototypes.DropZones.Coordinate;
            //     let p1 = Geometry.applyZoom(this.props.zoom, { x: zone.p.x, y: zone.p.y });
            //     let p2 = Geometry.applyZoom(this.props.zoom, { x: zone.p.x, y: zone.p.y });
            //     let distance = 20;
            //     let length = 25;
            //     if (zone.mode == "x") {
            //         p1.y -= distance * zone.direction;
            //         p2.y -= distance * zone.direction;
            //         p1.x += length / 2 * zone.direction;
            //         p2.x -= length / 2 * zone.direction;
            //     }
            //     if (zone.mode == "y") {
            //         p1.x -= distance * zone.direction;
            //         p2.x -= distance * zone.direction;
            //         p1.y -= length / 2 * zone.direction;
            //         p2.y += length / 2 * zone.direction;
            //     }
            //     return (
            //         <g>
            //             {zone.mode == "x" ? (
            //                 <rect className="dropzone-highlighter"
            //                     x={Math.min(p1.x, p2.x)}
            //                     width={Math.abs(p2.x - p1.x)}
            //                     y={p1.y - 10}
            //                     height={20}
            //                 />
            //             ) : (
            //                     <rect className="dropzone-highlighter"
            //                         y={Math.min(p1.y, p2.y)}
            //                         height={Math.abs(p2.y - p1.y)}
            //                         x={p1.x - 10}
            //                         width={20}
            //                     />
            //                 )}
            //             {this.makeDashedLine({ x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 }, Geometry.applyZoom(this.props.zoom, zone.p))}
            //             {this.makeLine(p1, p2, 10, 10)}
            //             {this.makeTextAtCenter(p1, p2, zone.title, 0, -5)}
            //         </g>
            //     )
            // }
            case "region": {
                var zone = z;
                var p1 = core_1.Geometry.applyZoom(this.props.zoom, {
                    x: zone.p1.x,
                    y: -zone.p1.y,
                });
                var p2 = core_1.Geometry.applyZoom(this.props.zoom, {
                    x: zone.p2.x,
                    y: -zone.p2.y,
                });
                return (React.createElement("g", null,
                    React.createElement("rect", { className: "dropzone-highlighter", opacity: 0.5, x: Math.min(p1.x, p2.x), y: Math.min(p1.y, p2.y), width: Math.abs(p2.x - p1.x), height: Math.abs(p2.y - p1.y) }),
                    React.createElement("rect", { className: "dropzone-element-solid", opacity: 0.5, x: Math.min(p1.x, p2.x), y: Math.min(p1.y, p2.y), width: Math.abs(p2.x - p1.x), height: Math.abs(p2.y - p1.y) }),
                    this.makeTextAtCenter({ x: p1.x, y: (p1.y + p2.y) / 2 }, { x: p2.x, y: (p1.y + p2.y) / 2 }, zone.title, 0, 0)));
            }
            case "rectangle": {
                var zone = z;
                var c = core_1.Geometry.applyZoom(this.props.zoom, {
                    x: zone.cx,
                    y: -zone.cy,
                });
                var width = this.props.zoom.scale * zone.width;
                var height = this.props.zoom.scale * zone.height;
                return (React.createElement("g", { transform: "translate(" + c.x + "," + c.y + ") rotate(" + -zone.rotation + ")" },
                    React.createElement("rect", { className: "dropzone-highlighter", opacity: 0.5, x: -width / 2, y: -height / 2, width: width, height: height }),
                    React.createElement("rect", { className: "dropzone-element-solid", opacity: 0.5, x: -width / 2, y: -height / 2, width: width, height: height }),
                    this.makeTextAtCenter({ x: -width / 2, y: height / 2 }, { x: width / 2, y: height / 2 }, zone.title, 0, 0)));
            }
        }
    };
    DropZoneView.prototype.render = function () {
        var z = this.props.zone;
        return (React.createElement("g", { ref: "container", className: utils_1.classNames("dropzone", "dropzone-" + z.type, [
                "active",
                this.state.active,
            ]) }, this.renderElement(z)));
    };
    return DropZoneView;
}(React.Component));
exports.DropZoneView = DropZoneView;
//# sourceMappingURL=dropzone.js.map