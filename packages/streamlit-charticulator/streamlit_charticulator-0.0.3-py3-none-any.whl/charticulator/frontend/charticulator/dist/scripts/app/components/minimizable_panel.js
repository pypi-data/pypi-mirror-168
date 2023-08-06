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
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FloatingPanel = exports.MinimizablePane = exports.MinimizablePanelView = void 0;
var React = require("react");
var resources_1 = require("../resources");
var buttons_1 = require("./buttons");
var Hammer = require("hammerjs");
var utils_1 = require("../utils");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("../views/panels/widgets/controls/fluentui_customized_components");
var MinimizablePanelView = /** @class */ (function (_super) {
    __extends(MinimizablePanelView, _super);
    function MinimizablePanelView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MinimizablePanelView.prototype.render = function () {
        return React.createElement("div", { className: "minimizable-panel-view" }, this.props.children);
    };
    return MinimizablePanelView;
}(React.Component));
exports.MinimizablePanelView = MinimizablePanelView;
var MinimizablePane = /** @class */ (function (_super) {
    __extends(MinimizablePane, _super);
    function MinimizablePane(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            minimized: props.defaultMinimized || false,
        };
        return _this;
    }
    MinimizablePane.prototype.renderHeader = function () {
        var _this = this;
        if (this.props.hideHeader) {
            return null;
        }
        return (React.createElement("div", { className: "header", onClick: function () { return _this.setState({ minimized: !_this.state.minimized }); } },
            React.createElement(react_1.DefaultButton, { onClick: function () { return _this.setState({ minimized: !_this.state.minimized }); }, iconProps: {
                    iconName: this.state.minimized ? "ChevronRight" : "ChevronDown",
                    styles: {
                        root: {
                            fontSize: "unset",
                            height: 12,
                        },
                    },
                }, styles: fluentui_customized_components_1.PanelHeaderStyles }),
            React.createElement("span", { className: "title" }, this.props.title),
            this.props.onMaximize ? (React.createElement("span", { className: "buttons", onClick: function (e) { return e.stopPropagation(); } },
                React.createElement(buttons_1.ButtonFlat, { title: "Show as separate window", url: resources_1.getSVGIcon("general/popout"), onClick: function () { return _this.props.onMaximize(); } }))) : null));
    };
    MinimizablePane.prototype.render = function () {
        if (this.state.minimized) {
            return React.createElement("div", { className: "minimizable-pane" }, this.renderHeader());
        }
        else {
            if (this.props.scroll) {
                if (this.props.height != null) {
                    return (React.createElement("div", { className: "minimizable-pane minimizable-pane-scrollable" },
                        this.renderHeader(),
                        React.createElement("div", { className: "content", style: { height: this.props.height + "px" } }, this.props.children)));
                }
                else if (this.props.maxHeight != null) {
                    return (React.createElement("div", { className: "minimizable-pane minimizable-pane-scrollable" },
                        this.renderHeader(),
                        React.createElement("div", { className: "content", style: { maxHeight: this.props.maxHeight + "px" } }, this.props.children)));
                }
                else {
                    return (React.createElement("div", { className: "minimizable-pane minimizable-pane-scrollable minimizable-pane-autosize" },
                        this.renderHeader(),
                        React.createElement("div", { className: "content", style: { flex: "1 1" } }, this.props.children)));
                }
            }
            else {
                return (React.createElement("div", { className: "minimizable-pane" },
                    this.renderHeader(),
                    React.createElement("div", { className: "content" }, this.props.children)));
            }
        }
    };
    return MinimizablePane;
}(React.Component));
exports.MinimizablePane = MinimizablePane;
var FloatingPanel = /** @class */ (function (_super) {
    __extends(FloatingPanel, _super);
    function FloatingPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        return _this;
    }
    FloatingPanel.prototype.getInitialState = function () {
        var e_1, _a;
        // Figure out a position that doesn't overlap with existing windows
        var initialX = 100;
        var initialY = 100;
        var width = this.props.width || 324;
        var height = this.props.height || 324;
        if (this.props.floatInCenter) {
            initialX = window.innerWidth / 2 - width / 2;
            initialY = window.innerHeight / 2 - height / 2;
        }
        else {
            // eslint-disable-next-line
            while (true) {
                var found = false;
                if (FloatingPanel.peerGroups.has(this.props.peerGroup)) {
                    try {
                        for (var _b = (e_1 = void 0, __values(FloatingPanel.peerGroups.get(this.props.peerGroup))), _c = _b.next(); !_c.done; _c = _b.next()) {
                            var peer = _c.value;
                            if (peer.state.x == initialX && peer.state.y == initialY) {
                                found = true;
                                break;
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                }
                if (found && initialX < 400 && initialY < 400) {
                    initialX += 50;
                    initialY += 50;
                }
                else {
                    break;
                }
            }
        }
        return {
            x: initialX,
            y: initialY,
            width: width,
            height: height,
            focus: false,
            minimized: false,
        };
    };
    FloatingPanel.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer.Manager(this.refContainer);
        this.hammer.add(new Hammer.Pan({ threshold: 0 }));
        this.hammer.on("panstart", function (e) {
            if (e.target == _this.refHeader) {
                var x0_1 = _this.state.x - e.deltaX;
                var y0_1 = _this.state.y - e.deltaY;
                var panListener_1 = function (e) {
                    _this.setState({
                        x: x0_1 + e.deltaX,
                        y: Math.max(0, y0_1 + e.deltaY),
                    });
                };
                var panEndListener_1 = function () {
                    _this.hammer.off("pan", panListener_1);
                    _this.hammer.off("panend", panEndListener_1);
                };
                _this.hammer.on("pan", panListener_1);
                _this.hammer.on("panend", panEndListener_1);
            }
            if (e.target == _this.refResizer) {
                var x0_2 = _this.state.width - e.deltaX;
                var y0_2 = _this.state.height - e.deltaY;
                var panListener_2 = function (e) {
                    _this.setState({
                        width: Math.max(324, x0_2 + e.deltaX),
                        height: Math.max(100, y0_2 + e.deltaY),
                    });
                };
                var panEndListener_2 = function () {
                    _this.hammer.off("pan", panListener_2);
                    _this.hammer.off("panend", panEndListener_2);
                };
                _this.hammer.on("pan", panListener_2);
                _this.hammer.on("panend", panEndListener_2);
            }
        });
        if (FloatingPanel.peerGroups.has(this.props.peerGroup)) {
            FloatingPanel.peerGroups.get(this.props.peerGroup).add(this);
        }
        else {
            FloatingPanel.peerGroups.set(this.props.peerGroup, new Set([this]));
        }
        this.focus();
    };
    FloatingPanel.prototype.focus = function () {
        var e_2, _a;
        if (FloatingPanel.peerGroups.has(this.props.peerGroup)) {
            try {
                for (var _b = __values(FloatingPanel.peerGroups.get(this.props.peerGroup)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var peer = _c.value;
                    if (peer != this) {
                        peer.setState({ focus: false });
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
        this.setState({ focus: true });
    };
    FloatingPanel.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        if (FloatingPanel.peerGroups.has(this.props.peerGroup)) {
            FloatingPanel.peerGroups.get(this.props.peerGroup).delete(this);
        }
    };
    FloatingPanel.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: utils_1.classNames("charticulator__floating-panel", ["is-focus", this.state.focus], ["is-scroll", this.props.scroll]), ref: function (e) { return (_this.refContainer = e); }, style: {
                left: this.state.x + "px",
                top: this.state.y + "px",
                width: this.state.width + "px",
                height: this.state.minimized ? undefined : this.state.height + "px",
            }, onMouseDown: function () {
                _this.focus();
            }, onTouchStart: function () {
                _this.focus();
            } },
            React.createElement("div", { className: "charticulator__floating-panel-header", ref: function (e) { return (_this.refHeader = e); } },
                React.createElement("span", { className: "title" }, this.props.title),
                React.createElement("span", { className: "buttons", onClick: function (e) { return e.stopPropagation(); } },
                    React.createElement(buttons_1.ButtonFlat, { url: resources_1.getSVGIcon("general/minus"), title: "Minimize", onClick: function () {
                            return _this.setState({ minimized: !_this.state.minimized });
                        } }),
                    this.props.onClose ? (React.createElement(buttons_1.ButtonFlat, { url: resources_1.getSVGIcon(this.props.closeButtonIcon || "general/popout"), title: "Restore to panel", onClick: function () { return _this.props.onClose(); } })) : null)),
            !this.state.minimized ? (React.createElement("div", { className: "charticulator__floating-panel-content" }, this.props.children)) : null,
            !this.state.minimized ? (React.createElement("div", { className: "charticulator__floating-panel-resizer", ref: function (e) { return (_this.refResizer = e); } })) : null));
    };
    FloatingPanel.peerGroups = new Map();
    return FloatingPanel;
}(React.Component));
exports.FloatingPanel = FloatingPanel;
//# sourceMappingURL=minimizable_panel.js.map