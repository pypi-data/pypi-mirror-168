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
exports.CanvasBar = void 0;
var React = require("react");
var CanvasBar = /** @class */ (function (_super) {
    __extends(CanvasBar, _super);
    function CanvasBar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CanvasBar.prototype.render = function () {
        var width = this.props.canvasWidth;
        var height = 20;
        return (React.createElement("g", { className: "charticulator__canvas-canvas-bar", transform: "translate(0," + (this.props.canvasHeight - height).toFixed(6) + ")" },
            React.createElement("rect", { className: "el-background", x: 0, y: 0, width: width, height: height })));
    };
    return CanvasBar;
}(React.Component));
exports.CanvasBar = CanvasBar;
//# sourceMappingURL=canvas_bar.js.map