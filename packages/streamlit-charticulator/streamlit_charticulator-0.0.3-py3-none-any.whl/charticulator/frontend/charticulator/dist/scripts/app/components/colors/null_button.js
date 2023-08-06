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
exports.NullButton = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var styles_1 = require("./styles");
var NullButton = /** @class */ (function (_super) {
    __extends(NullButton, _super);
    function NullButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NullButton.prototype.render = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null, this.props.allowNull ? (React.createElement(styles_1.NullButtonWrapper, null,
            React.createElement(react_1.DefaultButton, { text: "none", iconProps: {
                    iconName: "ChromeClose",
                }, styles: styles_1.defaultNoneButtonStyles, onClick: function () {
                    _this.props.onPick(null);
                } }))) : null));
    };
    return NullButton;
}(React.Component));
exports.NullButton = NullButton;
//# sourceMappingURL=null_button.js.map