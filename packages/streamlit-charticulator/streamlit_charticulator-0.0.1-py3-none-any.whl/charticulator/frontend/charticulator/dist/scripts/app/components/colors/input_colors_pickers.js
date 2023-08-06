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
Object.defineProperty(exports, "__esModule", { value: true });
exports.HSVColorPicker = exports.HCLColorPicker = void 0;
var React = require("react");
var core_1 = require("../../../core");
var color_space_picker_1 = require("../color_space_picker");
var sRGB_to_HCL = core_1.getColorConverter("sRGB", "hcl");
var HCL_to_sRGB = core_1.getColorConverter("hcl", "sRGB");
function HSVtoRGB(h, s, v) {
    h /= 360;
    s /= 100;
    v /= 100;
    var r, g, b;
    var i = Math.floor(h * 6);
    var f = h * 6 - i;
    var p = v * (1 - s);
    var q = v * (1 - f * s);
    var t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0:
            (r = v), (g = t), (b = p);
            break;
        case 1:
            (r = q), (g = v), (b = p);
            break;
        case 2:
            (r = p), (g = v), (b = t);
            break;
        case 3:
            (r = p), (g = q), (b = v);
            break;
        case 4:
            (r = t), (g = p), (b = v);
            break;
        case 5:
            (r = v), (g = p), (b = q);
            break;
    }
    return [
        Math.max(0, Math.min(255, r * 255)),
        Math.max(0, Math.min(255, g * 255)),
        Math.max(0, Math.min(255, b * 255)),
        false,
    ];
}
function RGBtoHSV(r, g, b) {
    var max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min, s = max === 0 ? 0 : d / max, v = max / 255;
    var h;
    switch (max) {
        case min:
            h = 0;
            break;
        case r:
            h = g - b + d * (g < b ? 6 : 0);
            h /= 6 * d;
            break;
        case g:
            h = b - r + d * 2;
            h /= 6 * d;
            break;
        case b:
            h = r - g + d * 4;
            h /= 6 * d;
            break;
    }
    return [h * 360, s * 100, v * 100];
}
var HCLColorPicker = /** @class */ (function (_super) {
    __extends(HCLColorPicker, _super);
    function HCLColorPicker() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HCLColorPicker.prototype.render = function () {
        return (React.createElement(color_space_picker_1.ColorSpacePicker, __assign({}, this.props, { colorSpaces: HCLColorPicker.colorSpaces })));
    };
    HCLColorPicker.colorSpaces = [
        {
            name: "Lightness",
            description: "Hue, Chroma | Lightness",
            dimension1: { name: "Lightness", range: [100, 0] },
            dimension2: { name: "Hue", range: [0, 360] },
            dimension3: { name: "Chroma", range: [100, 0] },
            toRGB: function (x1, x2, x3) {
                return HCL_to_sRGB(x2, x3, x1);
            },
            fromRGB: function (r, g, b) {
                var _a = __read(sRGB_to_HCL(r, g, b), 3), h = _a[0], c = _a[1], l = _a[2];
                return [l, h, c];
            },
        },
        {
            name: "Hue",
            description: "Chroma, Lightness | Hue",
            dimension1: { name: "Hue", range: [0, 360] },
            dimension2: { name: "Chroma", range: [0, 100] },
            dimension3: { name: "Lightness", range: [100, 0] },
            toRGB: function (x1, x2, x3) {
                return HCL_to_sRGB(x1, x2, x3);
            },
            fromRGB: function (r, g, b) {
                return sRGB_to_HCL(r, g, b);
            },
        },
        {
            name: "Chroma",
            description: "Hue, Lightness | Chroma",
            dimension1: { name: "Chroma", range: [100, 0] },
            dimension2: { name: "Hue", range: [0, 360] },
            dimension3: { name: "Lightness", range: [100, 0] },
            toRGB: function (x1, x2, x3) {
                return HCL_to_sRGB(x2, x1, x3);
            },
            fromRGB: function (r, g, b) {
                var _a = __read(sRGB_to_HCL(r, g, b), 3), h = _a[0], c = _a[1], l = _a[2];
                return [c, h, l];
            },
        },
    ];
    return HCLColorPicker;
}(React.Component));
exports.HCLColorPicker = HCLColorPicker;
var HSVColorPicker = /** @class */ (function (_super) {
    __extends(HSVColorPicker, _super);
    function HSVColorPicker() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HSVColorPicker.prototype.render = function () {
        return (React.createElement(color_space_picker_1.ColorSpacePicker, __assign({}, this.props, { colorSpaces: HSVColorPicker.colorSpaces })));
    };
    HSVColorPicker.colorSpaces = [
        {
            name: "Hue",
            description: "Saturation, Value | Hue",
            dimension1: { name: "Hue", range: [360, 0] },
            dimension2: { name: "Saturation", range: [0, 100] },
            dimension3: { name: "Value", range: [100, 0] },
            toRGB: HSVtoRGB,
            fromRGB: RGBtoHSV,
        },
        {
            name: "Saturation",
            description: "Hue, Value | Saturation",
            dimension1: { name: "Saturation", range: [100, 0] },
            dimension2: { name: "Hue", range: [360, 0] },
            dimension3: { name: "Value", range: [100, 0] },
            toRGB: function (x1, x2, x3) { return HSVtoRGB(x2, x1, x3); },
            fromRGB: function (r, g, b) {
                var _a = __read(RGBtoHSV(r, g, b), 3), h = _a[0], s = _a[1], v = _a[2];
                return [s, h, v];
            },
        },
        {
            name: "Value",
            description: "Hue, Saturation | Value",
            dimension1: { name: "Value", range: [100, 0] },
            dimension2: { name: "Hue", range: [360, 0] },
            dimension3: { name: "Saturation", range: [100, 0] },
            toRGB: function (x1, x2, x3) { return HSVtoRGB(x2, x3, x1); },
            fromRGB: function (r, g, b) {
                var _a = __read(RGBtoHSV(r, g, b), 3), h = _a[0], s = _a[1], v = _a[2];
                return [v, h, s];
            },
        },
    ];
    return HSVColorPicker;
}(React.Component));
exports.HSVColorPicker = HSVColorPicker;
//# sourceMappingURL=input_colors_pickers.js.map