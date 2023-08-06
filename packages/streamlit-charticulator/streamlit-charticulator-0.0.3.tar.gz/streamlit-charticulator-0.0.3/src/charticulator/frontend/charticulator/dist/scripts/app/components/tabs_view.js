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
exports.TabsView = void 0;
var React = require("react");
var icons_1 = require("./icons");
var utils_1 = require("../utils");
var TabsView = /** @class */ (function (_super) {
    __extends(TabsView, _super);
    function TabsView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TabsView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__tabs-view" },
            React.createElement("div", { className: "charticulator__tabs-view-tabs" }, this.props.tabs.map(function (tab) { return (React.createElement("span", { key: tab.name, className: utils_1.classNames("charticulator__tabs-view-tab", [
                    "is-active",
                    _this.props.currentTab == tab.name,
                ]), onClick: function () { return _this.props.onSelect(tab.name); } },
                tab.icon ? React.createElement(icons_1.SVGImageIcon, { url: tab.icon }) : null,
                React.createElement("span", { className: "el-label" }, tab.label))); }))));
    };
    return TabsView;
}(React.Component));
exports.TabsView = TabsView;
//# sourceMappingURL=tabs_view.js.map