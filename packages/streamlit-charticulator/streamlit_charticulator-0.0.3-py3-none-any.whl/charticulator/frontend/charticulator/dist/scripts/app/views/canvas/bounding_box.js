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
exports.BoundingBoxView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../core");
var utils_1 = require("../../utils");
var renderer_1 = require("../../renderer");
var BoundingBoxView = /** @class */ (function (_super) {
    __extends(BoundingBoxView, _super);
    function BoundingBoxView(props) {
        var _this = _super.call(this, props) || this;
        _this.handleClick = _this.handleClick.bind(_this);
        _this.handleMouseEnter = _this.handleMouseEnter.bind(_this);
        _this.handleMouseLeave = _this.handleMouseLeave.bind(_this);
        return _this;
    }
    BoundingBoxView.prototype.handleClick = function () {
        if (this.props.onClick) {
            this.props.onClick();
        }
    };
    BoundingBoxView.prototype.handleMouseEnter = function () {
        if (this.props.onMouseEnter) {
            this.props.onMouseEnter();
        }
    };
    BoundingBoxView.prototype.handleMouseLeave = function () {
        if (this.props.onMouseLeave) {
            this.props.onMouseLeave();
        }
    };
    // eslint-disable-next-line
    BoundingBoxView.prototype.render = function () {
        var bbox = this.props.boundingBox;
        var zoom = this.props.zoom;
        var offset = this.props.offset || { x: 0, y: 0 };
        var coordinateSystem = this.props.coordinateSystem || new core_1.Graphics.CartesianCoordinates();
        var helper = new core_1.Graphics.CoordinateSystemHelper(coordinateSystem);
        var mainClassName = utils_1.classNames("bounding-box", ["active", this.props.active], ["visible", bbox.visible], ["interactable", this.props.onClick != null]);
        switch (bbox.type) {
            case "rectangle": {
                var rect = bbox;
                var cx = rect.cx + offset.x;
                var cy = rect.cy + offset.y;
                var element = helper.rect(cx - rect.width / 2, cy - rect.height / 2, cx + rect.width / 2, cy + rect.height / 2);
                return (React.createElement("g", { className: mainClassName, onClick: this.handleClick, onMouseEnter: this.handleMouseEnter, onMouseLeave: this.handleMouseLeave, transform: utils_1.toSVGZoom(zoom) + " translate(" + utils_1.toSVGNumber(coordinateSystem.getBaseTransform().x) + "," + utils_1.toSVGNumber(-coordinateSystem.getBaseTransform().y) + ")" },
                    renderer_1.renderGraphicalElementSVG(element, {
                        className: "element-shape ghost",
                        noStyle: true,
                    }),
                    renderer_1.renderGraphicalElementSVG(element, {
                        className: "element-shape indicator",
                        noStyle: true,
                    })));
            }
            case "anchored-rectangle": {
                var rect = bbox;
                var cx = rect.anchorX + offset.x;
                var cy = rect.anchorY + offset.y;
                var trCenter = {
                    x: rect.cx,
                    y: rect.cy,
                    angle: rect.rotation,
                };
                var tr = core_1.Graphics.concatTransform(core_1.Graphics.concatTransform(coordinateSystem.getBaseTransform(), coordinateSystem.getLocalTransform(cx, cy)), trCenter);
                var p = core_1.Geometry.applyZoom(zoom, { x: tr.x, y: -tr.y });
                var margin = 0;
                return (React.createElement("g", { className: mainClassName, transform: "translate(" + utils_1.toSVGNumber(p.x) + "," + utils_1.toSVGNumber(p.y) + ")rotate(" + -tr.angle + ")", onClick: this.handleClick, onMouseEnter: this.handleMouseEnter, onMouseLeave: this.handleMouseLeave },
                    React.createElement("rect", { className: "element-shape ghost", x: (-rect.width / 2) * zoom.scale - margin, y: (-rect.height / 2) * zoom.scale - margin, width: rect.width * zoom.scale + margin * 2, height: rect.height * zoom.scale + margin * 2 }),
                    React.createElement("rect", { className: "element-shape indicator", x: (-rect.width / 2) * zoom.scale, y: (-rect.height / 2) * zoom.scale, width: rect.width * zoom.scale, height: rect.height * zoom.scale })));
            }
            case "circle": {
                var circle = bbox;
                var cx = circle.cx + offset.x;
                var cy = circle.cy + offset.y;
                var center = coordinateSystem.transformPointWithBase(cx, cy);
                var margin = 2;
                var p = core_1.Geometry.applyZoom(zoom, { x: center.x, y: -center.y });
                var radius = circle.radius * zoom.scale;
                return (React.createElement("g", { className: mainClassName, onClick: this.handleClick, onMouseEnter: this.handleMouseEnter, onMouseLeave: this.handleMouseLeave },
                    React.createElement("circle", { className: "element-shape ghost", cx: p.x, cy: p.y, r: radius + margin }),
                    React.createElement("circle", { className: "element-shape indicator", cx: p.x, cy: p.y, r: radius })));
            }
            case "line": {
                var line = bbox;
                if (line.morphing) {
                    var element = helper.line(line.x1 + offset.x, line.y1 + offset.y, line.x2 + offset.x, line.y2 + offset.y);
                    return (React.createElement("g", { className: mainClassName, onClick: this.handleClick, onMouseEnter: this.handleMouseEnter, onMouseLeave: this.handleMouseLeave, transform: utils_1.toSVGZoom(zoom) + " translate(" + utils_1.toSVGNumber(coordinateSystem.getBaseTransform().x) + "," + utils_1.toSVGNumber(-coordinateSystem.getBaseTransform().y) + ")" },
                        renderer_1.renderGraphicalElementSVG(element, {
                            className: "element-line ghost",
                            noStyle: true,
                        }),
                        renderer_1.renderGraphicalElementSVG(element, {
                            className: "element-line indicator",
                            noStyle: true,
                        })));
                }
                else {
                    var p1 = coordinateSystem.transformPointWithBase(line.x1 + offset.x, line.y1 + offset.y);
                    var p2 = coordinateSystem.transformPointWithBase(line.x2 + offset.x, line.y2 + offset.y);
                    p1 = core_1.Geometry.applyZoom(zoom, { x: p1.x, y: -p1.y });
                    p2 = core_1.Geometry.applyZoom(zoom, { x: p2.x, y: -p2.y });
                    return (React.createElement("g", { className: mainClassName, onClick: this.handleClick, onMouseEnter: this.handleMouseEnter, onMouseLeave: this.handleMouseLeave },
                        React.createElement("line", { className: "element-line ghost", x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y }),
                        React.createElement("line", { className: "element-line indicator", x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y })));
                }
            }
        }
    };
    return BoundingBoxView;
}(React.Component));
exports.BoundingBoxView = BoundingBoxView;
//# sourceMappingURL=bounding_box.js.map