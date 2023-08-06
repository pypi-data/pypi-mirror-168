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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ColorFilterTestView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../core");
var renderer_1 = require("../../../app/renderer");
var graphics_1 = require("../../../core/graphics");
var ColorFilterTestView = /** @class */ (function (_super) {
    __extends(ColorFilterTestView, _super);
    function ColorFilterTestView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            slider1: 200,
            slider2: 200,
        };
        return _this;
    }
    ColorFilterTestView.prototype.render = function () {
        var _this = this;
        var colors = [
            "#000000",
            "#0f0f0f",
            "#191919",
            "#222222",
            "#2b2b2b",
            "#343434",
            "#3e3e3e",
            "#484848",
            "#525252",
            "#5c5c5c",
            "#676767",
            "#717171",
            "#7c7c7c",
            "#888888",
            "#939393",
            "#9e9e9e",
            "#aaaaaa",
            "#b6b6b6",
            "#c2c2c2",
            "#cecece",
            "#dadada",
            "#e6e6e6",
            "#f2f2f2",
            "#ffffff",
            "#1f77b4",
            "#aec7e8",
            "#ff7f0e",
            "#ffbb78",
            "#2ca02c",
            "#98df8a",
            "#d62728",
            "#ff9896",
            "#9467bd",
            "#c5b0d5",
            "#8c564b",
            "#c49c94",
            "#e377c2",
            "#f7b6d2",
            "#7f7f7f",
            "#c7c7c7",
            "#bcbd22",
            "#dbdb8d",
            "#17becf",
            "#9edae5",
        ].map(function (x) { return core_1.colorFromHTMLColor(x); });
        var elements = colors.map(function (color, i) {
            var x = (i % 4) * 150;
            var y = Math.floor(i / 4) * 50;
            var style = {
                fillColor: color,
            };
            return graphics_1.makeGroup([
                graphics_1.makeRect(x, y, x + 60, y + 40, style),
                graphics_1.makeRect(x + 70, y, x + 130, y + 40, __assign(__assign({}, style), { colorFilter: {
                        saturation: { multiply: _this.state.slider1 / 1000 },
                        lightness: { add: 0.01, pow: _this.state.slider2 / 1000 },
                    } })),
            ]);
        });
        return (React.createElement("div", null,
            React.createElement("div", null, "Check saturation function with colors"),
            React.createElement("div", null,
                "Saturation = ",
                React.createElement("input", { type: "range", min: 1, max: 1000, value: this.state.slider1, onChange: function (e) {
                        _this.setState({ slider1: +e.target.value });
                    } }),
                " " + (this.state.slider1 / 1000).toFixed(3)),
            React.createElement("div", null,
                "Lightness.pow = ",
                React.createElement("input", { type: "range", min: 0, max: 1000, value: this.state.slider2, onChange: function (e) {
                        _this.setState({ slider2: +e.target.value });
                    } }),
                " " + (this.state.slider2 / 1000).toFixed(3)),
            React.createElement("svg", { width: 600, height: 600 },
                React.createElement("g", { transform: "translate(0, 599)" }, renderer_1.renderGraphicalElementSVG(core_1.Graphics.makeGroup(__spread(elements)))))));
    };
    return ColorFilterTestView;
}(React.Component));
exports.ColorFilterTestView = ColorFilterTestView;
//# sourceMappingURL=colorFilter.js.map