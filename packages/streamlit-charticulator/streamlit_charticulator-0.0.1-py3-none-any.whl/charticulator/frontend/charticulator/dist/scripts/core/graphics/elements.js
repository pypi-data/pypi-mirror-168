"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.transformDirection = exports.transform = exports.concatTransform = exports.rotation = exports.translation = exports.makePath = exports.PathMaker = exports.makeText = exports.makePolygon = exports.makeLine = exports.makeGroup = exports.makeEllipse = exports.makeCircle = exports.makeRect = exports.PathTextAlignment = void 0;
var common_1 = require("../common");
var PathTextAlignment;
(function (PathTextAlignment) {
    PathTextAlignment["Start"] = "start";
    PathTextAlignment["Middle"] = "middle";
    PathTextAlignment["End"] = "end";
})(PathTextAlignment = exports.PathTextAlignment || (exports.PathTextAlignment = {}));
function makeRect(x1, y1, x2, y2, style, rx, ry) {
    return { type: "rect", x1: x1, x2: x2, y1: y1, y2: y2, style: style, rx: rx, ry: ry };
}
exports.makeRect = makeRect;
function makeCircle(cx, cy, r, style) {
    return { type: "circle", cx: cx, cy: cy, r: r, style: style };
}
exports.makeCircle = makeCircle;
function makeEllipse(x1, y1, x2, y2, style) {
    return { type: "ellipse", x1: x1, x2: x2, y1: y1, y2: y2, style: style };
}
exports.makeEllipse = makeEllipse;
function makeGroup(elements) {
    return { type: "group", elements: elements, transform: { x: 0, y: 0, angle: 0 } };
}
exports.makeGroup = makeGroup;
function makeLine(x1, y1, x2, y2, style) {
    return { type: "line", x1: x1, x2: x2, y1: y1, y2: y2, style: style };
}
exports.makeLine = makeLine;
function makePolygon(points, style) {
    return { type: "polygon", points: points, style: style };
}
exports.makePolygon = makePolygon;
function makeText(cx, cy, text, fontFamily, fontSize, style, selectable) {
    return {
        type: "text",
        cx: cx,
        cy: cy,
        text: text,
        fontFamily: fontFamily,
        fontSize: fontSize,
        style: style,
        selectable: selectable,
    };
}
exports.makeText = makeText;
var PathMaker = /** @class */ (function () {
    function PathMaker() {
        this.path = { type: "path", cmds: [], transform: "" };
    }
    PathMaker.prototype.moveTo = function (x, y) {
        this.path.cmds.push({ cmd: "M", args: [x, y] });
    };
    PathMaker.prototype.lineTo = function (x, y) {
        this.path.cmds.push({ cmd: "L", args: [x, y] });
    };
    PathMaker.prototype.transformRotation = function (angle, x, y) {
        if (x === void 0) { x = 0; }
        if (y === void 0) { y = 0; }
        this.path.transform = "rotate(" + angle + " " + x + " " + y + ")";
    };
    PathMaker.prototype.setBeginArrowType = function (arrowType) {
        this.path.beginArrowType = arrowType;
    };
    PathMaker.prototype.setEndArrowType = function (arrowType) {
        this.path.endArrowType = arrowType;
    };
    PathMaker.prototype.cubicBezierCurveTo = function (c1x, c1y, c2x, c2y, x, y) {
        this.path.cmds.push({ cmd: "C", args: [c1x, c1y, c2x, c2y, x, y] });
    };
    PathMaker.prototype.quadraticBezierCurveTo = function (cx, cy, x, y) {
        this.path.cmds.push({ cmd: "Q", args: [cx, cy, x, y] });
    };
    PathMaker.prototype.arcTo = function (rx, ry, xAxisRotation, largeArcFlag, sweepFlag, x, y) {
        this.path.cmds.push({
            cmd: "A",
            args: [rx, ry, xAxisRotation, largeArcFlag, sweepFlag, x, y],
        });
    };
    /** Compose a Archimedean spiral with r = a + b theta, theta from thetaMin to thetaMax */
    PathMaker.prototype.archimedeanSpiral = function (cx, cy, a, b, thetaMin, thetaMax, moveTo) {
        if (moveTo === void 0) { moveTo = false; }
        var ticks = Math.ceil(Math.abs(thetaMax - thetaMin) / (Math.PI / 6)) + 1;
        for (var i = 0; i < ticks; i++) {
            var theta1 = (i / ticks) * (thetaMax - thetaMin) + thetaMin;
            var r1 = a + b * theta1;
            var x1 = r1 * Math.cos(theta1);
            var y1 = r1 * Math.sin(theta1);
            var theta2 = ((i + 1) / ticks) * (thetaMax - thetaMin) + thetaMin;
            var r2 = a + b * theta2;
            var x2 = r2 * Math.cos(theta2);
            var y2 = r2 * Math.sin(theta2);
            var scaler = (theta2 - theta1) / 3;
            if (moveTo && i == 0) {
                this.moveTo(cx + x1, cy + y1);
            }
            var dx1 = (b * Math.cos(theta1) - y1) * scaler;
            var dy1 = (b * Math.sin(theta1) + x1) * scaler;
            var dx2 = (b * Math.cos(theta2) - y2) * scaler;
            var dy2 = (b * Math.sin(theta2) + x2) * scaler;
            this.cubicBezierCurveTo(cx + x1 + dx1, cy + y1 + dy1, cx + x2 - dx2, cy + y2 - dy2, cx + x2, cy + y2);
        }
    };
    // public archimedeanSpiralReference(cx: number, cy: number, a: number, b: number, thetaMin: number, thetaMax: number) {
    //     let ticks = 3000;
    //     for (let i = 0; i < ticks; i++) {
    //         let theta2 = ((i + 1) / ticks) * (thetaMax - thetaMin) + thetaMin;
    //         let r2 = a + b * theta2;
    //         let x2 = r2 * Math.cos(theta2);
    //         let y2 = r2 * Math.sin(theta2);
    //         if (i == 0) {
    //             let theta1 = (i / ticks) * (thetaMax - thetaMin) + thetaMin;
    //             let r1 = a + b * theta1;
    //             let x1 = r1 * Math.cos(theta1);
    //             let y1 = r1 * Math.sin(theta1);
    //             this.moveTo(cx + x1, cy + y1);
    //         }
    //         this.lineTo(cx + x2, cy + y2);
    //     }
    // }
    PathMaker.prototype.polarLineTo = function (cx, cy, angle1, r1, angle2, r2, moveTo) {
        if (moveTo === void 0) { moveTo = false; }
        if (moveTo) {
            var p1x = cx + Math.cos(common_1.Geometry.degreesToRadians(angle1)) * r1;
            var p1y = cy + Math.sin(common_1.Geometry.degreesToRadians(angle1)) * r1;
            this.moveTo(p1x, p1y);
        }
        if (Math.abs(angle2 - angle1) < 1e-6) {
            var p2x = cx + Math.cos(common_1.Geometry.degreesToRadians(angle2)) * r2;
            var p2y = cy + Math.sin(common_1.Geometry.degreesToRadians(angle2)) * r2;
            this.lineTo(p2x, p2y);
        }
        else {
            if (Math.abs(r1 - r2) < 1e-6) {
                if (angle2 > angle1) {
                    var a1 = angle1;
                    while (angle2 > a1) {
                        var a2 = angle2;
                        if (a2 > a1 + 180) {
                            a2 = a1 + 180;
                        }
                        var p2x = cx + Math.cos(common_1.Geometry.degreesToRadians(a2)) * r1;
                        var p2y = cy + Math.sin(common_1.Geometry.degreesToRadians(a2)) * r1;
                        this.arcTo(r1, r1, 0, 0, 0, p2x, p2y);
                        a1 = a2;
                    }
                }
                else if (angle2 < angle1) {
                    var a1 = angle1;
                    while (angle2 < a1) {
                        var a2 = angle2;
                        if (a2 < a1 - 180) {
                            a2 = a1 - 180;
                        }
                        var p2x = cx + Math.cos(common_1.Geometry.degreesToRadians(a2)) * r1;
                        var p2y = cy + Math.sin(common_1.Geometry.degreesToRadians(a2)) * r1;
                        this.arcTo(r1, r1, 0, 0, 1, p2x, p2y);
                        a1 = a2;
                    }
                }
            }
            else {
                var b = (r2 - r1) / (angle2 - angle1);
                var a = r1 - b * angle1;
                var deg2rad = Math.PI / 180;
                this.archimedeanSpiral(cx, cy, a, b / deg2rad, angle1 * deg2rad, angle2 * deg2rad);
            }
        }
    };
    PathMaker.prototype.closePath = function () {
        this.path.cmds.push({ cmd: "Z", args: [] });
    };
    return PathMaker;
}());
exports.PathMaker = PathMaker;
function makePath(style) {
    var maker = new PathMaker();
    maker.path.style = style;
    return maker;
}
exports.makePath = makePath;
function translation(x, y) {
    if (x === void 0) { x = 0; }
    if (y === void 0) { y = 0; }
    return { x: x, y: y, angle: 0 };
}
exports.translation = translation;
function rotation(angle) {
    return { x: 0, y: 0, angle: angle };
}
exports.rotation = rotation;
/** Concat two transforms, f(p) := a(b(p))  */
function concatTransform(a, b) {
    var theta = common_1.Geometry.degreesToRadians(a.angle);
    var cos = Math.cos(theta);
    var sin = Math.sin(theta);
    return {
        x: a.x + b.x * cos - b.y * sin,
        y: a.y + b.x * sin + b.y * cos,
        angle: a.angle + b.angle,
    };
}
exports.concatTransform = concatTransform;
function transform(transform, a) {
    var theta = common_1.Geometry.degreesToRadians(transform.angle);
    var cos = Math.cos(theta);
    var sin = Math.sin(theta);
    return {
        x: a.x * cos - a.y * sin + transform.x,
        y: a.x * sin + a.y * cos + transform.y,
    };
}
exports.transform = transform;
function transformDirection(transform, a) {
    var theta = common_1.Geometry.degreesToRadians(transform.angle);
    var cos = Math.cos(theta);
    var sin = Math.sin(theta);
    return {
        x: a.x * cos - a.y * sin,
        y: a.x * sin + a.y * cos,
    };
}
exports.transformDirection = transformDirection;
//# sourceMappingURL=elements.js.map