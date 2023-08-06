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
exports.ZoomableCanvas = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../core");
var ZoomableCanvas = /** @class */ (function (_super) {
    __extends(ZoomableCanvas, _super);
    function ZoomableCanvas(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            zoom: {
                centerX: props.width / 2,
                centerY: props.height / 2,
                scale: 1,
            },
        };
        return _this;
    }
    ZoomableCanvas.prototype.setZooming = function (zoom) {
        this.setState({
            zoom: zoom,
        });
    };
    ZoomableCanvas.prototype.canvasToPixel = function (pt) {
        return core_1.Geometry.applyZoom(this.state.zoom, pt);
    };
    ZoomableCanvas.prototype.pixelToCanvas = function (pt) {
        return core_1.Geometry.unapplyZoom(this.state.zoom, pt);
    };
    ZoomableCanvas.prototype.getRelativePoint = function (point) {
        var r = this.refs.container.getBoundingClientRect();
        return {
            x: point.x - r.left,
            y: point.y - r.top,
        };
    };
    ZoomableCanvas.prototype.componentDidMount = function () {
        this.hammer = new Hammer(this.refs.handler);
        // this.hammer.add(new Hammer.Pan());
        // this.hammer.add(new Hammer.Pinch());
        // let centerX: number = null;
        // let centerY: number = null;
        // this.hammer.on("panstart", (e) => {
        //     centerX = this.state.centerX;
        //     centerY = this.state.centerY;
        // });
        // this.hammer.on("pan", (e) => {
        //     this.setState({
        //         centerX: centerX + e.deltaX,
        //         centerY: centerY + e.deltaY,
        //     });
        // });
        // this.hammer.on("pinch", (e) => {
        //     console.log("Pinch", e);
        // });
    };
    ZoomableCanvas.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    ZoomableCanvas.prototype.render = function () {
        var transform = "translate(" + this.state.zoom.centerX + "," + this.state.zoom.centerY + ") scale(" + this.state.zoom.scale + ")";
        return (React.createElement("g", { ref: "container" },
            React.createElement("rect", { ref: "handler", x: 0, y: 0, width: this.props.width, height: this.props.height, style: {
                    fill: "transparent",
                    stroke: "none",
                    pointerEvents: "fill",
                } }),
            React.createElement("g", { transform: transform }, this.props.children)));
    };
    return ZoomableCanvas;
}(React.Component));
exports.ZoomableCanvas = ZoomableCanvas;
//# sourceMappingURL=zoomable.js.map