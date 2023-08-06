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
exports.InputField = exports.ColorSpacePicker = void 0;
var Hammer = require("hammerjs");
var React = require("react");
var core_1 = require("../../core");
var color_space_select_1 = require("./colors/color_space_select");
var color_hex_input_1 = require("./colors/color_hex_input");
var color_dimension_input_1 = require("./colors/color_dimension_input");
var color_rgb_input_1 = require("./colors/color_rgb_input");
// A general three component color picker
var ColorSpacePicker = /** @class */ (function (_super) {
    __extends(ColorSpacePicker, _super);
    function ColorSpacePicker(props) {
        var _this = _super.call(this, props) || this;
        _this.pickerSize = 200;
        var defaultValue = props.defaultValue || { r: 0, g: 0, b: 0 };
        var _a = __read(props.colorSpaces[0].fromRGB(defaultValue.r, defaultValue.g, defaultValue.b), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
        _this.state = {
            desc: props.colorSpaces[0],
            x1: x1,
            x2: x2,
            x3: x3,
        };
        return _this;
    }
    ColorSpacePicker.prototype.reset = function () {
        var _this = this;
        var props = this.props;
        var defaultValue = props.defaultValue || { r: 0, g: 0, b: 0 };
        var _a = __read(this.state.desc.fromRGB(defaultValue.r, defaultValue.g, defaultValue.b), 3), x1 = _a[0], x2 = _a[1], x3 = _a[2];
        this.setState({ x1: x1, x2: x2, x3: x3 }, function () { return _this.raiseChange(); });
    };
    ColorSpacePicker.prototype.raiseChange = function () {
        var currentColor = this.state.desc.toRGB(this.state.x1, this.state.x2, this.state.x3);
        var rgb = { r: currentColor[0], g: currentColor[1], b: currentColor[2] };
        if (this.props.onChange) {
            this.props.onChange(rgb);
        }
    };
    ColorSpacePicker.prototype.renderZ = function () {
        var _this = this;
        var width = 30;
        var height = this.pickerSize;
        var cWidth = 5;
        var cHeight = this.pickerSize * 2;
        var _a = __read(this.state.desc.dimension1.range, 2), x1Min = _a[0], x1Max = _a[1];
        return (React.createElement(ZCanvas, { width: width, height: height, canvasWidth: cWidth, canvasHeight: cHeight, x1Offset: x1Min, x1StrideZ: x1Max - x1Min, x2Offset: this.state.x2, x2StrideZ: 0, x3Offset: this.state.x3, x3StrideZ: 0, pz: (this.state.x1 - x1Min) / (x1Max - x1Min), toRGB: this.state.desc.toRGB, onMove: function (value, isEnd) {
                _this.setState({ x1: value * (x1Max - x1Min) + x1Min }, function () {
                    if (isEnd) {
                        _this.raiseChange();
                    }
                });
            } }));
    };
    ColorSpacePicker.prototype.renderXY = function () {
        var _this = this;
        var width = this.pickerSize;
        var height = this.pickerSize;
        var cWidth = this.pickerSize;
        var cHeight = this.pickerSize;
        var _a = __read(this.state.desc.dimension2.range, 2), x2Min = _a[0], x2Max = _a[1];
        var _b = __read(this.state.desc.dimension3.range, 2), x3Min = _b[0], x3Max = _b[1];
        return (React.createElement(XYCanvas, { width: width, height: height, canvasWidth: cWidth, canvasHeight: cHeight, x1Offset: this.state.x1, x1StrideX: 0, x1StrideY: 0, x2Offset: x2Min, x2StrideX: x2Max - x2Min, x2StrideY: 0, x3Offset: x3Min, x3StrideX: 0, x3StrideY: x3Max - x3Min, px: (this.state.x2 - x2Min) / (x2Max - x2Min), py: (this.state.x3 - x3Min) / (x3Max - x3Min), toRGB: this.state.desc.toRGB, onMove: function (v2, v3, isEnd) {
                _this.setState({
                    x2: v2 * (x2Max - x2Min) + x2Min,
                    x3: v3 * (x3Max - x3Min) + x3Min,
                }, function () {
                    if (isEnd) {
                        _this.raiseChange();
                    }
                });
            } }));
    };
    ColorSpacePicker.prototype.render = function () {
        var _this = this;
        var currentColor = this.state.desc.toRGB(this.state.x1, this.state.x2, this.state.x3);
        var rgb = { r: currentColor[0], g: currentColor[1], b: currentColor[2] };
        return (React.createElement("div", { className: "hcl-color-picker" },
            React.createElement("div", { className: "part-picker" },
                React.createElement("section", { className: "palette-xy" }, this.renderXY()),
                React.createElement("section", { className: "palette-z" }, this.renderZ()),
                React.createElement("section", { className: "values" },
                    React.createElement("div", { className: "row" },
                        React.createElement(color_space_select_1.ColorSpaceSelect, { colorSpaces: this.props.colorSpaces, state: this.state, updateState: function (value) {
                                return _this.setState(value);
                            } })),
                    React.createElement("div", { className: "row" },
                        React.createElement("div", { className: "columns" },
                            React.createElement("div", { className: "column" },
                                React.createElement("span", { className: "current-color" },
                                    React.createElement("span", { style: { backgroundColor: core_1.colorToHTMLColor(rgb) } }))),
                            React.createElement("div", { className: "column" },
                                React.createElement(color_hex_input_1.ColorHexInput, { state: this.state, updateState: function (value) {
                                        _this.setState(value, function () { return _this.raiseChange(); });
                                    } })))),
                    React.createElement("div", { className: "columns" },
                        React.createElement("div", { className: "column" },
                            React.createElement("div", { className: "row" },
                                React.createElement(color_dimension_input_1.ColorDimensionInput, { defaultValue: this.state.x1, range: this.state.desc.dimension1.range, updateState: function (num) {
                                        _this.setState({ x1: num }, function () { return _this.raiseChange(); });
                                    }, title: this.state.desc.dimension1.name })),
                            React.createElement("div", { className: "row" },
                                React.createElement(color_dimension_input_1.ColorDimensionInput, { defaultValue: this.state.x2, range: this.state.desc.dimension2.range, updateState: function (num) {
                                        _this.setState({ x2: num }, function () { return _this.raiseChange(); });
                                    }, title: this.state.desc.dimension2.name })),
                            React.createElement("div", { className: "row" },
                                React.createElement(color_dimension_input_1.ColorDimensionInput, { defaultValue: this.state.x3, range: this.state.desc.dimension3.range, updateState: function (num) {
                                        _this.setState({ x3: num }, function () { return _this.raiseChange(); });
                                    }, title: this.state.desc.dimension3.name }))),
                        React.createElement(color_rgb_input_1.ColorRgbInput, { state: this.state, updateState: function (value) {
                                _this.setState(value, function () { return _this.raiseChange(); });
                            } }))))));
    };
    return ColorSpacePicker;
}(React.Component));
exports.ColorSpacePicker = ColorSpacePicker;
var InputField = /** @class */ (function (_super) {
    __extends(InputField, _super);
    function InputField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputField.prototype.componentWillUpdate = function (newProps) {
        this.inputElement.value = newProps.defaultValue;
    };
    InputField.prototype.doEnter = function () {
        if (this.props.defaultValue == this.inputElement.value) {
            return;
        }
        if (this.props.onEnter) {
            var ret = this.props.onEnter(this.inputElement.value);
            if (!ret) {
                this.inputElement.value = this.props.defaultValue;
            }
        }
        else {
            this.inputElement.value = this.props.defaultValue;
        }
    };
    InputField.prototype.doCancel = function () {
        this.inputElement.value = this.props.defaultValue;
    };
    Object.defineProperty(InputField.prototype, "value", {
        get: function () {
            return this.inputElement.value;
        },
        set: function (v) {
            this.inputElement.value = v;
        },
        enumerable: false,
        configurable: true
    });
    InputField.prototype.render = function () {
        var _this = this;
        return (React.createElement("input", { type: "text", ref: function (e) { return (_this.inputElement = e); }, defaultValue: this.props.defaultValue, autoFocus: true, onKeyDown: function (e) {
                if (e.key == "Enter") {
                    _this.doEnter();
                }
                if (e.key == "Escape") {
                    _this.doCancel();
                }
            }, onFocus: function (e) {
                e.currentTarget.select();
            }, onBlur: function () {
                _this.doEnter();
            } }));
    };
    return InputField;
}(React.Component));
exports.InputField = InputField;
var XYCanvas = /** @class */ (function (_super) {
    __extends(XYCanvas, _super);
    function XYCanvas() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    XYCanvas.prototype.componentDidMount = function () {
        var _this = this;
        this.renderCanvas();
        this.hammer = new Hammer(this.refs.canvasElement);
        this.hammer.add(new Hammer.Pan({ threshold: 0 }));
        this.hammer.add(new Hammer.Tap());
        this.hammer.on("panstart tap pan panend", function (e) {
            var bounds = _this.refs.canvasElement.getBoundingClientRect();
            var x = e.center.x - bounds.left;
            var y = e.center.y - bounds.top;
            x /= _this.props.width;
            y /= _this.props.height;
            var isEnd = e.type == "tap" || e.type == "panend";
            x = Math.max(0, Math.min(1, x));
            y = Math.max(0, Math.min(1, y));
            _this.props.onMove(x, y, isEnd);
        });
    };
    XYCanvas.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        this.hammer = null;
    };
    XYCanvas.prototype.componentDidUpdate = function () {
        this.renderCanvas();
    };
    XYCanvas.prototype.renderCanvas = function () {
        var _this = this;
        var canvas = this.refs.canvasElement;
        var width = canvas.width;
        var height = canvas.height;
        var ctx = canvas.getContext("2d");
        setTimeout(function () {
            var data = ctx.getImageData(0, 0, width, height);
            var _a = _this.props, x1Offset = _a.x1Offset, x2Offset = _a.x2Offset, x3Offset = _a.x3Offset;
            var _b = _this.props, x1StrideX = _b.x1StrideX, x1StrideY = _b.x1StrideY;
            var _c = _this.props, x2StrideX = _c.x2StrideX, x2StrideY = _c.x2StrideY;
            var _d = _this.props, x3StrideX = _d.x3StrideX, x3StrideY = _d.x3StrideY;
            x1StrideX /= data.width - 1;
            x2StrideX /= data.width - 1;
            x3StrideX /= data.width - 1;
            x1StrideY /= data.height - 1;
            x2StrideY /= data.height - 1;
            x3StrideY /= data.height - 1;
            var ptr = 0;
            for (var j = 0; j < data.height; j++) {
                var th = x1Offset + j * x1StrideY;
                var tc = x2Offset + j * x2StrideY;
                var tl = x3Offset + j * x3StrideY;
                for (var i = 0; i < data.width; i++) {
                    var color = _this.props.toRGB(th + i * x1StrideX, tc + i * x2StrideX, tl + i * x3StrideX);
                    data.data[ptr++] = color[0];
                    data.data[ptr++] = color[1];
                    data.data[ptr++] = color[2];
                    data.data[ptr++] = color[3] ? 128 : 255;
                }
            }
            ctx.putImageData(data, 0, 0);
        }, 0);
    };
    XYCanvas.prototype.render = function () {
        var _a = this.props, width = _a.width, height = _a.height, canvasWidth = _a.canvasWidth, canvasHeight = _a.canvasHeight, px = _a.px, py = _a.py;
        var x = px * (width - 1) + 0.5;
        var y = py * (height - 1) + 0.5;
        return (React.createElement("div", { className: "canvas-xy" },
            React.createElement("div", { className: "canvas-container", style: { padding: "2px 2px" } },
                React.createElement("canvas", { ref: "canvasElement", width: canvasWidth, height: canvasHeight, style: { width: width + "px", height: height + "px" } })),
            React.createElement("svg", { width: width + 4, height: height + 4 },
                React.createElement("g", { transform: "translate(2, 2)" },
                    React.createElement("circle", { className: "bg", cx: x, cy: y, r: 5 }),
                    React.createElement("circle", { className: "fg", cx: x, cy: y, r: 5 })))));
    };
    return XYCanvas;
}(React.PureComponent));
var ZCanvas = /** @class */ (function (_super) {
    __extends(ZCanvas, _super);
    function ZCanvas(props) {
        return _super.call(this, props) || this;
    }
    ZCanvas.prototype.componentDidMount = function () {
        var _this = this;
        this.renderCanvas();
        this.hammer = new Hammer(this.refs.canvasElement);
        this.hammer.add(new Hammer.Pan({ threshold: 0 }));
        this.hammer.add(new Hammer.Tap());
        this.hammer.on("panstart tap pan panend", function (e) {
            var bounds = _this.refs.canvasElement.getBoundingClientRect();
            var y = e.center.y - bounds.top;
            y /= _this.props.height;
            var isEnd = e.type == "tap" || e.type == "panend";
            y = Math.max(0, Math.min(1, y));
            _this.props.onMove(y, isEnd);
        });
    };
    ZCanvas.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        this.hammer = null;
    };
    ZCanvas.prototype.componentDidUpdate = function () {
        this.renderCanvas();
    };
    ZCanvas.prototype.renderCanvas = function () {
        var _this = this;
        var canvas = this.refs.canvasElement;
        var width = canvas.width;
        var height = canvas.height;
        var ctx = canvas.getContext("2d");
        setTimeout(function () {
            var data = ctx.getImageData(0, 0, width, height);
            var _a = _this.props, x1Offset = _a.x1Offset, x2Offset = _a.x2Offset, x3Offset = _a.x3Offset;
            var _b = _this.props, x1StrideZ = _b.x1StrideZ, x2StrideZ = _b.x2StrideZ, x3StrideZ = _b.x3StrideZ;
            x1StrideZ /= data.height - 1;
            x2StrideZ /= data.height - 1;
            x3StrideZ /= data.height - 1;
            var ptr = 0;
            for (var j = 0; j < data.height; j++) {
                var th = x1Offset + j * x1StrideZ;
                var tc = x2Offset + j * x2StrideZ;
                var tl = x3Offset + j * x3StrideZ;
                var color = _this.props.toRGB(th, tc, tl);
                for (var i = 0; i < data.width; i++) {
                    data.data[ptr++] = color[0];
                    data.data[ptr++] = color[1];
                    data.data[ptr++] = color[2];
                    data.data[ptr++] = color[3] ? 128 : 255;
                }
            }
            ctx.putImageData(data, 0, 0);
        }, 0);
    };
    ZCanvas.prototype.render = function () {
        var _a = this.props, width = _a.width, height = _a.height, canvasWidth = _a.canvasWidth, canvasHeight = _a.canvasHeight, pz = _a.pz;
        var z = pz * (height - 1) + 0.5;
        return (React.createElement("div", { className: "canvas-z" },
            React.createElement("div", { className: "canvas-container", style: { padding: "2px 2px" } },
                React.createElement("canvas", { ref: "canvasElement", width: canvasWidth, height: canvasHeight, style: { width: width + "px", height: height + "px" } })),
            React.createElement("svg", { width: width + 4, height: height + 4 },
                React.createElement("g", { transform: "translate(2, 2)" },
                    React.createElement("rect", { className: "bg", x: 0, y: z - 2, width: 30, height: 4 }),
                    React.createElement("rect", { className: "fg", x: 0, y: z - 2, width: 30, height: 4 })))));
    };
    return ZCanvas;
}(React.PureComponent));
//# sourceMappingURL=color_space_picker.js.map