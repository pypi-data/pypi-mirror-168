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
exports.ModalView = exports.PopupView = exports.PopupContainer = exports.PopupController = exports.PopupContext = exports.getAlignment = exports.PopupAlignment = void 0;
var React = require("react");
var core_1 = require("../../core");
var utils_1 = require("../utils");
var components_1 = require("../components");
var PopupAlignment;
(function (PopupAlignment) {
    PopupAlignment["Inner"] = "inner";
    PopupAlignment["Outer"] = "outer";
    PopupAlignment["StartInner"] = "start-inner";
    PopupAlignment["StartOuter"] = "start-outer";
    PopupAlignment["EndInner"] = "end-inner";
    PopupAlignment["EndOuter"] = "end-outer";
})(PopupAlignment = exports.PopupAlignment || (exports.PopupAlignment = {}));
function getAlignment(anchor) {
    var alignX;
    var avgPopupWindowWidth = 500;
    var anchorCloseToWindowBorder = window.innerWidth - anchor.getBoundingClientRect().right <
        avgPopupWindowWidth;
    var alignLeft = false;
    if (anchorCloseToWindowBorder) {
        alignX = PopupAlignment.StartOuter;
        alignLeft = true;
    }
    return { alignLeft: alignLeft, alignX: alignX };
}
exports.getAlignment = getAlignment;
var popupViewMapping = new WeakMap();
var newlyCreatedContexts = new WeakSet();
function findParentPopup(anchor) {
    while (anchor) {
        if (anchor instanceof HTMLDivElement && popupViewMapping.has(anchor)) {
            return popupViewMapping.get(anchor);
        }
        anchor = anchor.parentElement;
    }
}
var PopupContext = /** @class */ (function (_super) {
    __extends(PopupContext, _super);
    function PopupContext(id, renderElement, options) {
        var _this = _super.call(this) || this;
        _this.isClosed = false;
        _this.children = [];
        _this.id = id;
        _this.options = options;
        if (options.parent) {
            _this.parent = options.parent;
            options.parent.children.push(_this);
        }
        else {
            _this.parent = null;
        }
        _this.element = renderElement(_this);
        newlyCreatedContexts.add(_this);
        return _this;
    }
    PopupContext.prototype.close = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.children), _c = _b.next(); !_c.done; _c = _b.next()) {
                var child = _c.value;
                child.close();
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.isClosed = true;
        if (this.parent) {
            var idx = this.parent.children.indexOf(this);
            if (idx >= 0) {
                this.parent.children.splice(idx, 1);
            }
        }
        this.emit("close");
    };
    PopupContext.prototype.traverse = function (visitor) {
        var e_2, _a;
        visitor(this);
        try {
            for (var _b = __values(this.children), _c = _b.next(); !_c.done; _c = _b.next()) {
                var child = _c.value;
                child.traverse(visitor);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
    };
    return PopupContext;
}(core_1.EventEmitter));
exports.PopupContext = PopupContext;
var PopupController = /** @class */ (function (_super) {
    __extends(PopupController, _super);
    function PopupController() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.currentID = 0;
        _this.rootPopup = null;
        _this.currentModal = null;
        return _this;
    }
    PopupController.prototype.traverse = function (visitor) {
        if (this.rootPopup) {
            this.rootPopup.traverse(visitor);
        }
    };
    PopupController.prototype.popupAt = function (renderElement, options) {
        var _this = this;
        if (options.alignX == undefined) {
            options.alignX = PopupAlignment.StartInner;
        }
        if (options.alignY == undefined) {
            options.alignY = PopupAlignment.Outer;
        }
        if (!options.parent && options.anchor) {
            options.parent = findParentPopup(options.anchor);
        }
        var context = new PopupContext("#" + (this.currentID++).toString(), renderElement, options);
        if (!options.parent) {
            this.rootPopup = context;
        }
        context.addListener("close", function () {
            if (_this.rootPopup == context) {
                _this.rootPopup = null;
            }
            _this.emit("changed");
        });
        this.emit("changed");
    };
    PopupController.prototype.showModal = function (renderElement, options) {
        var _this = this;
        var context = new PopupContext("#" + (this.currentID++).toString(), renderElement, options);
        this.reset();
        this.currentModal = context;
        context.addListener("close", function () {
            _this.currentModal = null;
            _this.emit("changed");
        });
        this.emit("changed");
    };
    PopupController.prototype.reset = function () {
        if (this.rootPopup) {
            this.rootPopup.close();
            this.rootPopup = null;
        }
        if (this.currentModal) {
            this.currentModal.close();
            this.currentModal = null;
        }
    };
    PopupController.prototype.resetPopups = function () {
        if (this.rootPopup) {
            this.rootPopup.close();
            this.rootPopup = null;
        }
    };
    return PopupController;
}(core_1.EventEmitter));
exports.PopupController = PopupController;
var PopupContainer = /** @class */ (function (_super) {
    __extends(PopupContainer, _super);
    function PopupContainer(props) {
        var _this = _super.call(this, props) || this;
        _this.onKeyDown = _this.onKeyDown.bind(_this);
        return _this;
    }
    PopupContainer.prototype.onKeyDown = function (e) {
        if (e.target == document.body) {
            var prefix = "";
            if (e.shiftKey) {
                prefix = "shift-" + prefix;
            }
            if (e.ctrlKey) {
                prefix = "ctrl-" + prefix;
            }
            var name_1 = ("" + prefix + e.key).toLowerCase();
            if (name_1 == "escape") {
                if (this.props.controller.rootPopup) {
                    this.props.controller.resetPopups();
                }
                else {
                    this.props.controller.reset();
                }
            }
        }
    };
    PopupContainer.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.props.controller.addListener("changed", function () {
            _this.forceUpdate();
        });
        window.addEventListener("keydown", this.onKeyDown);
        setTimeout(function () {
            if (_this.popupContainer) {
                _this.popupContainer.focus();
            }
        }, 100);
    };
    PopupContainer.prototype.componentWillUnmount = function () {
        this.token.remove();
        window.removeEventListener("keydown", this.onKeyDown);
    };
    PopupContainer.prototype.render = function () {
        var _this = this;
        if (this.props.controller.currentModal) {
            var modal = this.props.controller.currentModal;
            return (React.createElement("div", { tabIndex: 0, className: "popup-container popup-container-modal", style: {
                    position: "fixed",
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0,
                    pointerEvents: "all",
                }, onMouseDown: function () {
                    _this.props.controller.reset();
                }, ref: function (r) { return (_this.popupContainer = r); } },
                modal.element,
                this.renderPopups()));
        }
        else {
            return this.renderPopups();
        }
    };
    PopupContainer.prototype.renderPopups = function () {
        var _this = this;
        var popups = [];
        this.props.controller.traverse(function (p) {
            if (!p.isClosed) {
                popups.push(p);
            }
        });
        if (popups.length == 0) {
            return React.createElement("div", null);
        }
        else {
            return (React.createElement("div", { tabIndex: 0, className: "popup-container", style: {
                    position: "fixed",
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0,
                    pointerEvents: "all",
                }, ref: function (r) { return (_this.popupContainer = r); }, onMouseDown: function () {
                    _this.props.controller.resetPopups();
                } }, popups.map(function (popup) {
                return (React.createElement("div", { key: popup.id, ref: function (ref) {
                        if (ref) {
                            popupViewMapping.set(ref, popup);
                        }
                    } }, popup.element));
            })));
        }
    };
    return PopupContainer;
}(React.Component));
exports.PopupContainer = PopupContainer;
var PopupView = /** @class */ (function (_super) {
    __extends(PopupView, _super);
    function PopupView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PopupView.prototype.componentDidMount = function () {
        var _this = this;
        setTimeout(function () {
            if (_this.popupContainer) {
                _this.popupContainer.focus();
            }
        }, 100);
    };
    // eslint-disable-next-line
    PopupView.prototype.render = function () {
        var _this = this;
        var popup = this.props.context;
        var position = popup.options.anchor.getBoundingClientRect();
        var style = { position: "absolute" };
        var marginX = 0;
        var marginY = 0;
        var alignX = popup.options.alignX;
        var alignY = popup.options.alignY;
        switch (popup.options.alignX) {
            case "inner":
                {
                    if ((position.left + position.right) / 2 < window.innerWidth / 2) {
                        style.left = position.left + "px";
                        alignX = PopupAlignment.StartInner;
                    }
                    else {
                        style.right =
                            window.innerWidth - (position.left + position.width) + "px";
                        alignX = PopupAlignment.EndInner;
                    }
                }
                break;
            case "outer":
                {
                    if ((position.left + position.right) / 2 > window.innerWidth / 2) {
                        style.right = window.innerWidth - position.left + marginX + "px";
                        alignX = PopupAlignment.StartOuter;
                    }
                    else {
                        style.left = position.left + position.width + marginX + "px";
                        alignX = PopupAlignment.EndOuter;
                    }
                }
                break;
            case "start-inner":
                {
                    style.left = position.left + "px";
                }
                break;
            case "end-inner":
                {
                    style.right =
                        window.innerWidth - (position.left + position.width) + "px";
                }
                break;
            case "start-outer":
                {
                    style.right = window.innerWidth - position.left + marginX + "px";
                }
                break;
            case "end-outer":
                {
                    style.left = position.left + position.width + marginX + "px";
                }
                break;
        }
        switch (popup.options.alignY) {
            case "inner":
                {
                    if ((position.top + position.bottom) / 2 < window.innerHeight / 2) {
                        style.top = position.top + "px";
                        alignY = PopupAlignment.StartInner;
                    }
                    else {
                        style.bottom =
                            window.innerHeight - (position.top + position.height) + "px";
                        alignY = PopupAlignment.EndInner;
                    }
                }
                break;
            case "outer":
                {
                    if ((position.top + position.bottom) / 2 > window.innerHeight / 2) {
                        style.bottom = window.innerHeight - position.top + marginY + "px";
                        alignY = PopupAlignment.StartOuter;
                    }
                    else {
                        style.top = position.top + position.height + marginY + "px";
                        alignY = PopupAlignment.EndOuter;
                    }
                }
                break;
            case "start-inner":
                {
                    style.top = position.top + "px";
                }
                break;
            case "end-inner":
                {
                    style.bottom =
                        window.innerHeight - (position.top + position.height) + "px";
                }
                break;
            case "start-outer":
                {
                    style.bottom = window.innerHeight - position.top + marginY + "px";
                }
                break;
            case "end-outer":
                {
                    style.top = position.top + position.height + marginY + "px";
                }
                break;
        }
        if (this.props.width != null) {
            style.width = this.props.width + "px";
        }
        return (React.createElement("div", { tabIndex: 0, ref: function (r) { return (_this.popupContainer = r); }, className: this.props.className
                ? this.props.className + " popup-view-container"
                : "popup-view-container", style: style, onMouseDownCapture: function () {
                newlyCreatedContexts = new WeakSet();
            }, onMouseDown: function (e) {
                var e_3, _a;
                e.stopPropagation();
                try {
                    for (var _b = __values(_this.props.context.children), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var child = _c.value;
                        if (!newlyCreatedContexts.has(child)) {
                            child.close();
                        }
                    }
                }
                catch (e_3_1) { e_3 = { error: e_3_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_3) throw e_3.error; }
                }
            } },
            React.createElement("div", { className: utils_1.classNames("popup-view", [
                    "popup-x-top-left",
                    alignX == "start-inner" && alignY == "end-outer",
                ], [
                    "popup-x-bottom-left",
                    alignX == "start-inner" && alignY == "start-outer",
                ], [
                    "popup-x-top-right",
                    alignX == "end-inner" && alignY == "end-outer",
                ], [
                    "popup-x-bottom-right",
                    alignX == "end-inner" && alignY == "start-outer",
                ], [
                    "popup-y-top-left",
                    alignX == "start-outer" && alignY == "start-inner",
                ], [
                    "popup-y-top-right",
                    alignX == "end-outer" && alignY == "start-inner",
                ], [
                    "popup-y-bottom-left",
                    alignX == "start-outer" && alignY == "end-inner",
                ], [
                    "popup-y-bottom-right",
                    alignX == "end-outer" && alignY == "end-inner",
                ]) },
                React.createElement(components_1.TelemetryContext.Consumer, null, function (telemetryRecorder) {
                    return (React.createElement(components_1.ErrorBoundary, { telemetryRecorder: telemetryRecorder }, _this.props.children));
                }))));
    };
    return PopupView;
}(React.Component));
exports.PopupView = PopupView;
var ModalView = /** @class */ (function (_super) {
    __extends(ModalView, _super);
    function ModalView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ModalView.prototype.render = function () {
        var type = this.props.type || "default";
        return (React.createElement("div", { className: "charticulator__modal-" + type, onMouseDown: function (e) {
                e.stopPropagation();
            } },
            React.createElement("div", { className: "charticulator__modal-" + type + "-container" }, this.props.children)));
    };
    return ModalView;
}(React.Component));
exports.ModalView = ModalView;
//# sourceMappingURL=popup_controller.js.map