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
exports.ButtonRaised = exports.ButtonFlatPanel = exports.ButtonFlat = exports.MenuButton = exports.AppButton = exports.BaseButton = exports.FluentToolButton = exports.ToolButton = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var utils_1 = require("../utils");
var draggable_1 = require("./draggable");
var icons_1 = require("./icons");
var R = require("../resources");
var strings_1 = require("../../strings");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("../views/panels/widgets/controls/fluentui_customized_components");
var ToolButton = /** @class */ (function (_super) {
    __extends(ToolButton, _super);
    function ToolButton(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
        };
        return _this;
    }
    ToolButton.prototype.render = function () {
        var _this = this;
        var onClick = function () {
            if (_this.props.onClick) {
                _this.props.onClick();
            }
        };
        if (this.props.dragData) {
            return (React.createElement(draggable_1.DraggableElement, { dragData: this.props.dragData, onDragStart: function () { return _this.setState({ dragging: true }); }, onDragEnd: function () { return _this.setState({ dragging: false }); }, renderDragElement: function () {
                    return [
                        React.createElement(icons_1.SVGImageIcon, { url: _this.props.icon, width: 32, height: 32 }),
                        { x: -16, y: -16 },
                    ];
                } },
                React.createElement("span", { className: utils_1.classNames("charticulator__button-tool", ["is-active", this.props.active || this.state.dragging], ["is-disabled", this.props.disabled]), title: this.props.title, onClick: onClick },
                    this.props.icon ? React.createElement(icons_1.SVGImageIcon, { url: this.props.icon }) : null,
                    this.props.text ? (React.createElement("span", { className: "el-text" }, this.props.text)) : null),
                React.createElement("span", { style: {
                        position: "relative",
                        bottom: "-7px",
                        left: "-20px",
                    }, onClick: onClick }, this.props.compact ? (React.createElement(icons_1.SVGImageIcon, { url: R.getSVGIcon("general/triangle-right-bottom") })) : null)));
        }
        else {
            return (React.createElement("span", { className: utils_1.classNames("charticulator__button-tool", ["is-active", this.props.active], ["is-disabled", this.props.disabled]), title: this.props.title, onClick: onClick },
                this.props.icon ? React.createElement(icons_1.SVGImageIcon, { url: this.props.icon }) : null,
                this.props.text ? (React.createElement("span", { className: "el-text" }, this.props.text)) : null));
        }
    };
    return ToolButton;
}(React.Component));
exports.ToolButton = ToolButton;
var FluentToolButton = /** @class */ (function (_super) {
    __extends(FluentToolButton, _super);
    function FluentToolButton(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dragging: false,
        };
        return _this;
    }
    FluentToolButton.prototype.render = function () {
        var _this = this;
        var onClick = function () {
            if (_this.props.onClick) {
                _this.props.onClick();
            }
        };
        if (this.props.dragData) {
            return (React.createElement(draggable_1.DraggableElement, { dragData: this.props.dragData, onDragStart: function () { return _this.setState({ dragging: true }); }, onDragEnd: function () { return _this.setState({ dragging: false }); }, renderDragElement: function () {
                    return [
                        React.createElement(icons_1.SVGImageIcon, { url: _this.props.icon, width: 32, height: 32 }),
                        { x: -16, y: -16 },
                    ];
                } },
                React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px" },
                    React.createElement(react_1.CommandBarButton, { onClick: onClick, checked: this.props.active || this.state.dragging, disabled: this.props.disabled, text: this.props.text, title: this.props.title, iconProps: {
                            iconName: this.props.icon,
                        }, styles: {
                            root: {
                                minWidth: "unset",
                            },
                        } }))));
        }
        else {
            return (React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px" },
                React.createElement(react_1.CommandBarButton, { onClick: onClick, checked: this.props.active, disabled: this.props.disabled, text: this.props.text, title: this.props.title, iconProps: {
                        iconName: this.props.icon,
                    }, styles: {
                        root: {
                            minWidth: "unset",
                        },
                    } })));
        }
    };
    return FluentToolButton;
}(React.Component));
exports.FluentToolButton = FluentToolButton;
var BaseButton = /** @class */ (function (_super) {
    __extends(BaseButton, _super);
    function BaseButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._doClick = _this.doClick.bind(_this);
        return _this;
    }
    BaseButton.prototype.doClick = function (e) {
        if (this.props.onClick) {
            this.props.onClick();
        }
        if (this.props.stopPropagation) {
            e.stopPropagation();
        }
    };
    return BaseButton;
}(React.PureComponent));
exports.BaseButton = BaseButton;
var AppButton = /** @class */ (function (_super) {
    __extends(AppButton, _super);
    function AppButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AppButton.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { tabIndex: 0, className: "charticulator__button-menu-app charticulator-title__button", title: this.props.title, onClick: this._doClick, onKeyPress: function (e) {
                if (e.key === "Enter") {
                    _this._doClick();
                }
            } },
            React.createElement(icons_1.SVGImageIcon, { url: R.getSVGIcon("app-icon") }),
            React.createElement("span", { className: "el-text" }, this.props.name || strings_1.strings.app.name)));
    };
    return AppButton;
}(BaseButton));
exports.AppButton = AppButton;
var MenuButton = /** @class */ (function (_super) {
    __extends(MenuButton, _super);
    function MenuButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MenuButton.prototype.render = function () {
        var _this = this;
        var props = this.props;
        if (props.text) {
            return (React.createElement("span", { tabIndex: 0, className: utils_1.classNames("charticulator__button-menu-text", [
                    "is-disabled",
                    this.props.disabled,
                ]), title: props.title, onClick: this._doClick, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        _this._doClick();
                    }
                } },
                React.createElement(icons_1.SVGImageIcon, { url: props.url }),
                React.createElement("span", { className: "el-text" }, props.text)));
        }
        else {
            return (React.createElement("span", { tabIndex: 0, className: "charticulator__button-menu", title: props.title, onClick: this._doClick, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        _this._doClick();
                    }
                } },
                React.createElement(icons_1.SVGImageIcon, { url: props.url })));
        }
    };
    return MenuButton;
}(BaseButton));
exports.MenuButton = MenuButton;
var ButtonFlat = /** @class */ (function (_super) {
    __extends(ButtonFlat, _super);
    function ButtonFlat() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ButtonFlat.prototype.render = function () {
        var props = this.props;
        if (props.url) {
            if (props.text) {
                return (React.createElement("button", { className: "charticulator__button-flat", title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url }),
                    React.createElement("span", { className: "el-text" }, props.text)));
            }
            else {
                return (React.createElement("button", { className: "charticulator__button-flat", title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url })));
            }
        }
        else {
            return (React.createElement("button", { className: "charticulator__button-flat", title: props.title, onClick: this._doClick },
                React.createElement("span", { className: "el-text" }, props.text)));
        }
    };
    return ButtonFlat;
}(BaseButton));
exports.ButtonFlat = ButtonFlat;
var ButtonFlatPanel = /** @class */ (function (_super) {
    __extends(ButtonFlatPanel, _super);
    function ButtonFlatPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ButtonFlatPanel.prototype.render = function () {
        var props = this.props;
        if (props.url) {
            if (props.text) {
                return (React.createElement("span", { className: utils_1.classNames("charticulator__button-flat-panel", [
                        "is-disabled",
                        this.props.disabled,
                    ]), title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url }),
                    React.createElement("span", { className: "el-text" }, props.text)));
            }
            else {
                return (React.createElement("span", { className: utils_1.classNames("charticulator__button-flat-panel", [
                        "is-disabled",
                        this.props.disabled,
                    ]), title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url })));
            }
        }
        else {
            return (React.createElement("span", { className: utils_1.classNames("charticulator__button-flat-panel", [
                    "is-disabled",
                    this.props.disabled,
                ]), title: props.title, onClick: this._doClick },
                React.createElement("span", { className: "el-text" }, props.text)));
        }
    };
    return ButtonFlatPanel;
}(BaseButton));
exports.ButtonFlatPanel = ButtonFlatPanel;
var ButtonRaised = /** @class */ (function (_super) {
    __extends(ButtonRaised, _super);
    function ButtonRaised() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ButtonRaised.prototype.render = function () {
        var props = this.props;
        if (props.url) {
            if (props.text) {
                return (React.createElement("span", { className: utils_1.classNames("charticulator__button-raised", [
                        "is-disabled",
                        this.props.disabled,
                    ]), title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url }),
                    React.createElement("span", { className: "el-text" }, props.text)));
            }
            else {
                return (React.createElement("span", { className: utils_1.classNames("charticulator__button-raised", [
                        "is-disabled",
                        this.props.disabled,
                    ]), title: props.title, onClick: this._doClick },
                    React.createElement(icons_1.SVGImageIcon, { url: props.url })));
            }
        }
        else {
            return (React.createElement("span", { className: utils_1.classNames("charticulator__button-raised", [
                    "is-disabled",
                    this.props.disabled,
                ]), title: props.title, onClick: this._doClick },
                React.createElement("span", { className: "el-text" }, props.text)));
        }
    };
    return ButtonRaised;
}(BaseButton));
exports.ButtonRaised = ButtonRaised;
//# sourceMappingURL=buttons.js.map