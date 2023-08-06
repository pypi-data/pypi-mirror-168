"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable @typescript-eslint/ban-types */
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
exports.ReorderStringsValue = exports.DropZoneView = void 0;
var React = require("react");
var globals = require("../../../globals");
var components_1 = require("../../../components");
var index_1 = require("../../../utils/index");
var object_list_editor_1 = require("../object_list_editor");
var controls_1 = require("./controls");
var container_1 = require("../../../../container");
var DropZoneView = /** @class */ (function (_super) {
    __extends(DropZoneView, _super);
    function DropZoneView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isInSession: false,
            isDraggingOver: false,
            data: null,
        };
        return _this;
    }
    DropZoneView.prototype.componentDidMount = function () {
        var _this = this;
        globals.dragController.registerDroppable(this, this.dropContainer);
        this.tokens = [
            globals.dragController.addListener("sessionstart", function () {
                var session = globals.dragController.getSession();
                if (_this.props.filter(session.data)) {
                    _this.setState({
                        isInSession: true,
                    });
                }
            }),
            globals.dragController.addListener("sessionend", function () {
                _this.setState({
                    isInSession: false,
                });
            }),
        ];
    };
    DropZoneView.prototype.componentWillUnmount = function () {
        globals.dragController.unregisterDroppable(this);
        this.tokens.forEach(function (x) { return x.remove(); });
    };
    DropZoneView.prototype.onDragEnter = function (ctx) {
        var _this = this;
        var data = ctx.data;
        var judge = this.props.filter(data);
        if (judge) {
            this.setState({
                isDraggingOver: true,
                data: data,
            });
            ctx.onLeave(function () {
                _this.setState({
                    isDraggingOver: false,
                    data: null,
                });
            });
            ctx.onDrop(function (point, modifiers) {
                _this.props.onDrop(data, point, modifiers);
            });
            return true;
        }
    };
    DropZoneView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: index_1.classNames(this.props.className, ["is-in-session", this.state.isInSession], ["is-dragging-over", this.state.isDraggingOver]), onClick: this.props.onClick, ref: function (e) { return (_this.dropContainer = e); } }, this.props.draggingHint == null
            ? this.props.children
            : this.state.isInSession
                ? this.props.draggingHint()
                : this.props.children));
    };
    return DropZoneView;
}(React.Component));
exports.DropZoneView = DropZoneView;
var ReorderStringsValue = /** @class */ (function (_super) {
    __extends(ReorderStringsValue, _super);
    function ReorderStringsValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            items: _this.props.items.slice(),
            customOrder: false,
        };
        return _this;
    }
    ReorderStringsValue.prototype.render = function () {
        var _this = this;
        var items = this.state.items.slice();
        return (React.createElement("div", { className: "charticulator__widget-popup-reorder-widget" },
            React.createElement("div", { className: "el-row el-list-view" },
                React.createElement(object_list_editor_1.ReorderListView, { enabled: true, onReorder: function (a, b) {
                        object_list_editor_1.ReorderListView.ReorderArray(items, a, b);
                        _this.setState({ items: items, customOrder: true });
                    } }, items.map(function (x) { return (React.createElement("div", { key: x, className: "el-item" }, x)); }))),
            React.createElement("div", { className: "el-row" },
                React.createElement(controls_1.Button, { icon: "Sort", text: "Reverse", onClick: function () {
                        _this.setState({ items: _this.state.items.reverse() });
                    } }),
                " ",
                React.createElement(controls_1.Button, { icon: "general/sort", text: "Sort", onClick: function () {
                        _this.setState({
                            items: _this.state.items.sort(container_1.getSortFunctionByData(_this.state.items)),
                            customOrder: false,
                        });
                    } }),
                this.props.allowReset && (React.createElement(React.Fragment, null,
                    " ",
                    React.createElement(controls_1.Button, { icon: "general/clear", text: "Reset", onClick: function () {
                            if (_this.props.onReset) {
                                var items_1 = _this.props.onReset();
                                _this.setState({ items: items_1 });
                            }
                        } })))),
            React.createElement("div", { className: "el-row" },
                React.createElement(components_1.ButtonRaised, { text: "OK", onClick: function () {
                        _this.props.onConfirm(_this.state.items, _this.state.customOrder);
                    } }))));
    };
    return ReorderStringsValue;
}(React.Component));
exports.ReorderStringsValue = ReorderStringsValue;
//# sourceMappingURL=types.js.map