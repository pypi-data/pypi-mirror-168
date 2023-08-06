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
exports.ColorGrid = void 0;
var React = require("react");
var color_grid_item_1 = require("./color_grid_item");
var styles_1 = require("./styles");
var ColorGrid = /** @class */ (function (_super) {
    __extends(ColorGrid, _super);
    function ColorGrid() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorGrid.prototype.render = function () {
        var _this = this;
        return (React.createElement(styles_1.ColorGridRowWrapper, null, this.props.colors.map(function (colors, index) { return (React.createElement(styles_1.ColorGridColumnWrapper, { key: "column-color-" + index }, colors.map(function (color, i) { return (React.createElement(color_grid_item_1.ColorGridItem, { key: "color-item-" + i, color: color, onClick: _this.props.onClick, defaultValue: _this.props.defaultValue })); }))); })));
    };
    return ColorGrid;
}(React.PureComponent));
exports.ColorGrid = ColorGrid;
//# sourceMappingURL=color_grid.js.map