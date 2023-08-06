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
exports.SVGImageIcon = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var SVGImageIcon = /** @class */ (function (_super) {
    __extends(SVGImageIcon, _super);
    function SVGImageIcon() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SVGImageIcon.prototype.render = function () {
        var style = {};
        if (this.props.width != null) {
            style.width = this.props.width + "px";
        }
        if (this.props.height != null) {
            style.height = this.props.height + "px";
        }
        if (this.props.url) {
            style.backgroundImage = "url(" + this.props.url + ")";
            return (React.createElement("span", { className: "el-svg-icon svg-image-icon", style: style, onDragStart: function () { return false; } }));
        }
        else {
            return React.createElement("span", { className: "el-svg-icon svg-image-icon" });
        }
    };
    return SVGImageIcon;
}(React.PureComponent));
exports.SVGImageIcon = SVGImageIcon;
//# sourceMappingURL=icons.js.map