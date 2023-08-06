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
exports.ScrollView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var noop_1 = require("../utils/noop");
var ScrollView = /** @class */ (function (_super) {
    __extends(ScrollView, _super);
    function ScrollView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ScrollView.prototype.componentDidMount = function () {
        this.hammer = new Hammer(this.refs.container);
        this.hammer.on("panstart", noop_1.noop);
    };
    ScrollView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    ScrollView.prototype.render = function () {
        return (React.createElement("div", { className: "scroll-view", ref: "container" },
            React.createElement("div", { className: "scroll-view-content" }, this.props.children),
            React.createElement("div", { className: "scroll-bar" },
                React.createElement("div", { className: "scroll-bar-handle" }))));
    };
    return ScrollView;
}(React.Component));
exports.ScrollView = ScrollView;
//# sourceMappingURL=scroll_view.js.map