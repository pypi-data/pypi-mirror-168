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
exports.SelectionView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var SelectionView = /** @class */ (function (_super) {
    __extends(SelectionView, _super);
    function SelectionView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = _this.getDefaultState();
        return _this;
    }
    SelectionView.prototype.getDefaultState = function () {
        return {
            marquee: null,
        };
    };
    SelectionView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.handler);
        this.hammer.add(new Hammer.Pan());
        this.hammer.add(new Hammer.Tap());
        this.hammer.on("tap", function () {
            _this.setState({
                marquee: null,
            });
            if (_this.props.onTap) {
                _this.props.onTap();
            }
        });
        var currentMarquee = null;
        this.hammer.on("panstart", function (e) {
            var rect = _this.refs.handler.getBoundingClientRect();
            var _a = __read([e.center.x - rect.left, e.center.y - rect.top], 2), x = _a[0], y = _a[1];
            currentMarquee = {
                x1: x,
                y1: y,
                x2: x,
                y2: y,
            };
        });
        this.hammer.on("pan", function (e) {
            var rect = _this.refs.handler.getBoundingClientRect();
            var _a = __read([e.center.x - rect.left, e.center.y - rect.top], 2), x = _a[0], y = _a[1];
            currentMarquee.x2 = x;
            currentMarquee.y2 = y;
            _this.setState({
                marquee: currentMarquee,
            });
        });
        this.hammer.on("panend", function (e) {
            var rect = _this.refs.handler.getBoundingClientRect();
            var _a = __read([e.center.x - rect.left, e.center.y - rect.top], 2), x = _a[0], y = _a[1];
            currentMarquee.x2 = x;
            currentMarquee.y2 = y;
            if (_this.props.onMarqueeSelect) {
                _this.props.onMarqueeSelect(currentMarquee);
            }
            _this.setState({
                marquee: null,
            });
        });
    };
    SelectionView.prototype.render = function () {
        return (React.createElement("g", null,
            React.createElement("rect", { ref: "handler", className: "interaction-handler", style: { cursor: "crosshair" }, x: this.props.x, y: this.props.y, width: this.props.width, height: this.props.height }),
            this.state.marquee ? (React.createElement("rect", { className: "marquee-selection", x: Math.min(this.state.marquee.x1, this.state.marquee.x2), y: Math.min(this.state.marquee.y1, this.state.marquee.y2), width: Math.abs(this.state.marquee.x2 - this.state.marquee.x1), height: Math.abs(this.state.marquee.y2 - this.state.marquee.y1) })) : null));
    };
    return SelectionView;
}(React.Component));
exports.SelectionView = SelectionView;
//# sourceMappingURL=selecting.js.map