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
exports.ClickableSVGElement = exports.DraggableElement = void 0;
var React = require("react");
var globals = require("../globals");
var utils_1 = require("../utils");
var Hammer = require("hammerjs");
var DraggableElement = /** @class */ (function (_super) {
    __extends(DraggableElement, _super);
    function DraggableElement(props) {
        var _this = _super.call(this, props) || this;
        _this.state = { dragging: false };
        return _this;
    }
    DraggableElement.prototype.componentDidMount = function () {
        globals.dragController.registerDraggable(this, this.refs.draggableContainer, this.props.onTap);
    };
    DraggableElement.prototype.componentWillUnmount = function () {
        globals.dragController.unregisterDraggable(this);
    };
    DraggableElement.prototype.onDragStart = function () {
        this.setState({ dragging: true });
        if (this.props.onDragStart) {
            this.props.onDragStart();
        }
        return this.props.dragData();
    };
    DraggableElement.prototype.onDragEnd = function () {
        this.setState({ dragging: false });
        if (this.props.onDragEnd) {
            this.props.onDragEnd();
        }
    };
    DraggableElement.prototype.renderDragElement = function () {
        if (this.props.renderDragElement) {
            return this.props.renderDragElement();
        }
        else {
            return [React.createElement("span", null, this.props.children), { x: 0, y: 0 }];
        }
    };
    DraggableElement.prototype.render = function () {
        return (React.createElement("span", { ref: "draggableContainer", className: utils_1.classNames(this.props.className, "draggable", [
                "dragging",
                this.state.dragging,
            ]), style: { display: "inline-block", cursor: "pointer" } }, this.props.children));
    };
    return DraggableElement;
}(React.Component));
exports.DraggableElement = DraggableElement;
var ClickableSVGElement = /** @class */ (function (_super) {
    __extends(ClickableSVGElement, _super);
    function ClickableSVGElement() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ClickableSVGElement.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.container);
        this.hammer.add(new Hammer.Tap());
        this.hammer.on("tap", function () {
            if (_this.props.onClick) {
                _this.props.onClick();
            }
        });
    };
    ClickableSVGElement.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        this.hammer = null;
    };
    ClickableSVGElement.prototype.render = function () {
        return (React.createElement("g", { ref: "container", style: { cursor: "pointer" } }, this.props.children));
    };
    return ClickableSVGElement;
}(React.Component));
exports.ClickableSVGElement = ClickableSVGElement;
//# sourceMappingURL=draggable.js.map