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
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DragStateView = exports.DragController = exports.DragSession = exports.DragContext = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../core");
var DragContext = /** @class */ (function () {
    function DragContext() {
        this._onleave = null;
        this._onover = null;
        this._ondrop = null;
    }
    // Set drag event handlers
    DragContext.prototype.onLeave = function (f) {
        this._onleave = f;
    };
    DragContext.prototype.onOver = function (f) {
        this._onover = f;
    };
    DragContext.prototype.onDrop = function (f) {
        this._ondrop = f;
    };
    return DragContext;
}());
exports.DragContext = DragContext;
var DragSession = /** @class */ (function () {
    function DragSession(parent, draggable, startPoint) {
        this.candidates = [];
        this.states = new Map();
        this.parent = parent;
        this.obj = draggable;
        this.startPoint = startPoint;
        this.point = startPoint;
        this.data = draggable.onDragStart();
    }
    DragSession.prototype.handlePan = function (point, modifiers) {
        var _this = this;
        this.point = point;
        var element = document.elementFromPoint(point.x, point.y);
        var withins = new Set();
        while (element != null) {
            var droppable = this.parent.getDroppableFromElement(element);
            if (droppable) {
                withins.add(droppable);
            }
            element = element.parentElement;
        }
        // states:
        // 0: undefined
        // -1: ignored (onDragEnter returned false)
        // 1: drag entered
        withins.forEach(function (droppable) {
            var ctx = _this.states.get(droppable);
            if (!ctx) {
                ctx = new DragContext();
                ctx.draggable = _this.obj;
                ctx.data = _this.data;
                ctx._state = 0;
                _this.states.set(droppable, ctx);
            }
            if (ctx._state == 0) {
                var r = false;
                try {
                    r = droppable.onDragEnter ? droppable.onDragEnter(ctx) : false;
                }
                catch (e) {
                    console.trace(e);
                }
                if (r) {
                    ctx._state = 1;
                }
                else {
                    ctx._state = -1;
                }
            }
            else if (ctx._state == 1) {
                if (ctx._onover) {
                    ctx._onover(point, modifiers);
                }
            }
        });
        this.states.forEach(function (context, droppable) {
            if (!withins.has(droppable)) {
                if (context._state == 1) {
                    if (context._onleave) {
                        context._onleave();
                    }
                    context._state = 0;
                    context._onover = null;
                    context._onleave = null;
                    context._ondrop = null;
                }
            }
        });
        this.parent.emit("session");
    };
    DragSession.prototype.handleEnd = function (point, modifiers) {
        this.states.forEach(function (context) {
            if (context._state == 1) {
                if (context._ondrop) {
                    try {
                        context._ondrop(point, modifiers);
                    }
                    catch (e) {
                        console.trace(e);
                    }
                }
            }
        });
        this.states.forEach(function (context) {
            if (context._state == 1) {
                if (context._onleave) {
                    try {
                        context._onleave();
                    }
                    catch (e) {
                        console.trace(e);
                    }
                }
            }
        });
        this.states.clear();
        if (this.obj.onDragEnd) {
            try {
                this.obj.onDragEnd();
            }
            catch (e) {
                console.trace(e);
            }
        }
    };
    DragSession.prototype.pushCandidate = function (droppable, remove) {
        this.candidates.push([droppable, remove]);
    };
    DragSession.prototype.popCandidate = function (droppable) {
        this.candidates = this.candidates.filter(function (_a) {
            var _b = __read(_a, 2), obj = _b[0], remove = _b[1];
            if (obj === droppable) {
                remove();
                return false;
            }
            else {
                return true;
            }
        });
    };
    DragSession.prototype.removeCandidate = function (droppable) {
        this.states.delete(droppable);
    };
    return DragSession;
}());
exports.DragSession = DragSession;
var DragController = /** @class */ (function (_super) {
    __extends(DragController, _super);
    function DragController() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._draggables = new WeakMap();
        _this._droppables = new WeakMap();
        _this._element2Droppable = new WeakMap();
        _this._dragSession = null;
        return _this;
    }
    DragController.prototype.getDroppableFromElement = function (element) {
        return this._element2Droppable.get(element);
    };
    DragController.prototype.registerDroppable = function (obj, rootElement) {
        var _this = this;
        // Remove any existing stuff
        this.unregisterDroppable(obj);
        this._element2Droppable.set(rootElement, obj);
        this._droppables.set(obj, {
            remove: function () {
                _this._element2Droppable.delete(rootElement);
            },
        });
    };
    DragController.prototype.unregisterDroppable = function (obj) {
        if (this._droppables.has(obj)) {
            this._droppables.get(obj).remove();
            this._droppables.delete(obj);
        }
        if (this._dragSession) {
            this._dragSession.removeCandidate(obj);
        }
    };
    DragController.prototype.registerDraggable = function (obj, rootElement, onTap) {
        var _this = this;
        // Remove any existing stuff
        this.unregisterDraggable(obj);
        // Create hammer object and setup handlers
        var hammer = new Hammer.Manager(rootElement);
        hammer.add(new Hammer.Pan());
        hammer.on("panstart", function (e) {
            try {
                _this._dragSession = new DragSession(_this, obj, {
                    x: e.center.x,
                    y: e.center.y,
                });
            }
            catch (e) {
                console.trace(e);
                return;
            }
            _this.emit("sessionstart");
            _this.emit("session");
        });
        hammer.on("pan", function (e) {
            if (_this._dragSession != null) {
                var modifiers = {
                    shiftKey: e.srcEvent.shiftKey,
                    ctrlKey: e.srcEvent.ctrlKey,
                };
                _this._dragSession.handlePan({ x: e.center.x, y: e.center.y }, modifiers);
            }
        });
        hammer.on("panend", function (e) {
            if (_this._dragSession != null) {
                var modifiers = {
                    shiftKey: e.srcEvent.shiftKey,
                    ctrlKey: e.srcEvent.ctrlKey,
                };
                _this._dragSession.handleEnd({ x: e.center.x, y: e.center.y }, modifiers);
                _this._dragSession = null;
                _this.emit("session");
                _this.emit("sessionend");
            }
        });
        if (onTap) {
            hammer.add(new Hammer.Tap());
            hammer.on("tap", onTap);
        }
        this._draggables.set(obj, {
            hammer: hammer,
        });
    };
    DragController.prototype.unregisterDraggable = function (obj) {
        if (this._draggables.has(obj)) {
            var info = this._draggables.get(obj);
            info.hammer.destroy();
            this._draggables.delete(obj);
        }
    };
    DragController.prototype.getSession = function () {
        return this._dragSession;
    };
    return DragController;
}(core_1.EventEmitter));
exports.DragController = DragController;
var DragStateView = /** @class */ (function (_super) {
    __extends(DragStateView, _super);
    function DragStateView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DragStateView.prototype.onSession = function () {
        this.forceUpdate();
    };
    DragStateView.prototype.componentDidMount = function () {
        this.token = this.props.controller.addListener("session", this.onSession.bind(this));
    };
    DragStateView.prototype.componentWillUnmount = function () {
        this.token.remove();
    };
    DragStateView.prototype.render = function () {
        var session = this.props.controller.getSession();
        if (!session) {
            return React.createElement("div", null);
        }
        var _a = __read(session.obj.renderDragElement(), 2), element = _a[0], offset = _a[1];
        return (React.createElement("div", { className: "drag-state-view", style: {
                position: "fixed",
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                pointerEvents: "none",
            } },
            React.createElement("div", { style: {
                    position: "absolute",
                    left: session.point.x + offset.x + "px",
                    top: session.point.y + offset.y + "px",
                } }, element)));
    };
    return DragStateView;
}(React.Component));
exports.DragStateView = DragStateView;
//# sourceMappingURL=drag_controller.js.map