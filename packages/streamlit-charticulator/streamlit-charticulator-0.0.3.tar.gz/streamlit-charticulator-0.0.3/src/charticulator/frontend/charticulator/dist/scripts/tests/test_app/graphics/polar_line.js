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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PolarLineTestView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../core");
var renderer_1 = require("../../../app/renderer");
var PolarLineTestView = /** @class */ (function (_super) {
    __extends(PolarLineTestView, _super);
    function PolarLineTestView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            slider1: 0,
            slider2: 0,
        };
        return _this;
    }
    PolarLineTestView.prototype.render = function () {
        var _this = this;
        var paths = [];
        var gridIndex = 0;
        var dAngle = this.state.slider2;
        var testAngles = function (angle1, angle2) {
            angle1 += dAngle;
            angle2 += dAngle;
            var r = 40;
            var cx = 50 + (gridIndex % 6) * 100 - 300;
            var cy = 50 + Math.floor(gridIndex / 6) * 100 - 300;
            gridIndex += 1;
            var path2 = core_1.Graphics.makePath({
                strokeColor: { r: 0, g: 0, b: 0 },
                fillColor: { r: 0, g: 255, b: 0 },
                fillOpacity: 0.1,
            });
            path2.polarLineTo(cx, cy, angle1, r, angle2, r, true);
            path2.polarLineTo(cx, cy, angle2, r, angle2, r - 10, false);
            path2.polarLineTo(cx, cy, angle2, r - 10, angle1, r - 10, false);
            path2.polarLineTo(cx, cy, angle1, r - 10, angle1, r, false);
            path2.closePath();
            paths.push(path2.path);
        };
        testAngles(0, this.state.slider1 - 500);
        testAngles(0, 180);
        testAngles(0, 270);
        testAngles(0, 360);
        testAngles(0, 200);
        testAngles(0, 400);
        testAngles(0, -90);
        testAngles(0, -180);
        testAngles(0, -270);
        testAngles(0, -360);
        testAngles(0, -200);
        testAngles(0, -400);
        return (React.createElement("div", null,
            React.createElement("div", null,
                React.createElement("input", { type: "range", min: 0, max: 1000, value: this.state.slider1, onChange: function (e) {
                        _this.setState({ slider1: +e.target.value });
                    } }),
                React.createElement("input", { type: "range", min: 0, max: 1000, value: this.state.slider2, onChange: function (e) {
                        _this.setState({ slider2: +e.target.value });
                    } })),
            React.createElement("svg", { width: 600, height: 300 },
                React.createElement("g", { transform: "translate(300, 0)" }, renderer_1.renderGraphicalElementSVG(core_1.Graphics.makeGroup(__spread(paths)))))));
    };
    return PolarLineTestView;
}(React.Component));
exports.PolarLineTestView = PolarLineTestView;
//# sourceMappingURL=polar_line.js.map