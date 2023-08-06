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
exports.Slider = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Hammer = require("hammerjs");
var React = require("react");
var utils_1 = require("../../../../utils");
var Slider = /** @class */ (function (_super) {
    __extends(Slider, _super);
    function Slider(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            currentValue: props.defaultValue,
            dragging: false,
        };
        return _this;
    }
    Slider.prototype.componentWillReceiveProps = function (props) {
        this.setState({
            currentValue: props.defaultValue,
        });
    };
    Slider.prototype.niceValue = function (v) {
        var digits = Math.ceil(Math.log(this.props.max - this.props.min) / Math.log(10) + 2);
        v = parseFloat(v.toPrecision(digits));
        v = Math.min(this.props.max, Math.max(this.props.min, v));
        return v;
    };
    Slider.prototype.valueToRatio = function (v) {
        if (this.props.mapping == "sqrt") {
            return ((Math.sqrt(v) - Math.sqrt(this.props.min)) /
                (Math.sqrt(this.props.max) - Math.sqrt(this.props.min)));
        }
        else {
            return (v - this.props.min) / (this.props.max - this.props.min);
        }
    };
    Slider.prototype.ratioToValue = function (r) {
        if (this.props.mapping == "sqrt") {
            var f = r * (Math.sqrt(this.props.max) - Math.sqrt(this.props.min)) +
                Math.sqrt(this.props.min);
            return f * f;
        }
        else {
            return r * (this.props.max - this.props.min) + this.props.min;
        }
    };
    Slider.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.svg);
        this.hammer.add(new Hammer.Pan({ threshold: 0 }));
        this.hammer.add(new Hammer.Tap());
        var margin = 13;
        this.hammer.on("panstart pan panend tap", function (e) {
            var left = _this.refs.svg.getBoundingClientRect().left;
            var x = e.center.x - left;
            var pos = (x - margin) / (_this.props.width - margin - margin);
            pos = Math.max(0, Math.min(1, pos));
            var value = _this.niceValue(_this.ratioToValue(pos));
            _this.setState({
                currentValue: value,
            });
            if (_this.props.onChange) {
                if (e.type == "panend" || e.type == "tap") {
                    _this.props.onChange(value, true);
                }
                else {
                    _this.props.onChange(value, false);
                }
            }
            if (e.type == "panstart") {
                _this.setState({
                    dragging: true,
                });
            }
            if (e.type == "panend") {
                _this.setState({
                    dragging: false,
                });
            }
        });
    };
    Slider.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    Slider.prototype.render = function () {
        var _this = this;
        var height = 24;
        var _a = this.props, min = _a.min, max = _a.max, width = _a.width;
        var margin = height / 2 + 1;
        var scale = function (v) {
            return _this.valueToRatio(v) * (width - margin - margin) + margin;
        };
        var y = height / 2;
        var px = scale(this.state.currentValue != null
            ? this.state.currentValue
            : (min + max) / 2);
        return (React.createElement("span", { className: "charticulator__widget-control-slider" },
            React.createElement("svg", { width: width, height: height, ref: "svg", className: utils_1.classNames(["invalid", this.state.currentValue == null], ["active", this.state.dragging]) },
                React.createElement("line", { className: "track", x1: margin, x2: width - margin, y1: y, y2: y }),
                React.createElement("line", { className: "track-highlight", x1: margin, x2: px, y1: y, y2: y }),
                React.createElement("circle", { className: "indicator", cx: px, cy: y, r: (height / 2) * 0.5 }))));
    };
    return Slider;
}(React.Component));
exports.Slider = Slider;
//# sourceMappingURL=slider.js.map