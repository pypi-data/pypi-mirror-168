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
exports.ColorDimensionInput = void 0;
var React = require("react");
var core_1 = require("../../../core");
var color_space_picker_1 = require("../color_space_picker");
function clipToRange(num, range) {
    if (range[0] < range[1]) {
        return Math.max(range[0], Math.min(range[1], num));
    }
    else {
        return Math.max(range[1], Math.min(range[0], num));
    }
}
var ColorDimensionInput = /** @class */ (function (_super) {
    __extends(ColorDimensionInput, _super);
    function ColorDimensionInput() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorDimensionInput.prototype.render = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null,
            React.createElement("label", null, this.props.title),
            React.createElement(color_space_picker_1.InputField, { defaultValue: core_1.prettyNumber(this.props.defaultValue, 1), onEnter: function (v) {
                    var num = parseFloat(v);
                    if (num == num && num != null) {
                        num = clipToRange(num, _this.props.range);
                        _this.props.updateState(num);
                        // , () => this.raiseChange());
                        return true;
                    }
                } })));
    };
    return ColorDimensionInput;
}(React.Component));
exports.ColorDimensionInput = ColorDimensionInput;
//# sourceMappingURL=color_dimension_input.js.map