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
Object.defineProperty(exports, "__esModule", { value: true });
exports.PanelRadioControl = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var components_1 = require("../../../app/components");
var R = require("../../../app/resources");
var fluentui_customized_components_1 = require("../../../app/views/panels/widgets/controls/fluentui_customized_components");
var PanelRadioControl = /** @class */ (function (_super) {
    __extends(PanelRadioControl, _super);
    function PanelRadioControl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PanelRadioControl.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", null, this.props.options.map(function (option, index) {
            return (React.createElement(react_1.DefaultButton, { checked: _this.props.value == option, title: _this.props.labels[index], key: option, onClick: function () {
                    if (_this.props) {
                        _this.props.onChange(option);
                    }
                }, iconProps: _this.props.icons
                    ? {
                        iconName: _this.props.icons[index],
                    }
                    : null, text: _this.props.labels && _this.props.showText
                    ? _this.props.labels[index]
                    : null, styles: {
                    root: __assign({ marginRight: 5, marginLeft: 5 }, fluentui_customized_components_1.defultComponentsHeight),
                }, onRenderIcon: function () {
                    return _this.props.icons ? (React.createElement("span", { style: { marginRight: "0.3rem" } },
                        React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(_this.props.icons[index]) }))) : null;
                } }));
        })));
    };
    return PanelRadioControl;
}(React.Component));
exports.PanelRadioControl = PanelRadioControl;
//# sourceMappingURL=radio_control.js.map