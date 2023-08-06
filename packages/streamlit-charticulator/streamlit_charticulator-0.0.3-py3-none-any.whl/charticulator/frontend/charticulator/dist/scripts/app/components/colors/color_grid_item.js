"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
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
exports.ColorGridItem = void 0;
var fluentui_color_picker_1 = require("../fluentui_color_picker");
var React = require("react");
var styled_components_1 = require("styled-components");
var ColorItem = styled_components_1.default.span(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n  box-sizing: border-box;\n  border: 1px solid #8a8886;\n  width: 20px;\n  height: 20px;\n  margin: 4px;\n  background-color: ", ";\n  cursor: pointer;\n"], ["\n  display: block;\n  box-sizing: border-box;\n  border: 1px solid #8a8886;\n  width: 20px;\n  height: 20px;\n  margin: 4px;\n  background-color: ", ";\n  cursor: pointer;\n"])), function (props) { return props.color; });
var ColorGridItem = /** @class */ (function (_super) {
    __extends(ColorGridItem, _super);
    function ColorGridItem() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorGridItem.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { onClick: function () {
                if (_this.props.onClick) {
                    _this.props.onClick(_this.props.color);
                }
            } },
            React.createElement(ColorItem, { color: fluentui_color_picker_1.colorToCSS(this.props.color) })));
    };
    return ColorGridItem;
}(React.Component));
exports.ColorGridItem = ColorGridItem;
var templateObject_1;
//# sourceMappingURL=color_grid_item.js.map