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
exports.MessagePanel = void 0;
var React = require("react");
var R = require("../resources");
var core_1 = require("../../core");
var stores_1 = require("../stores");
var context_component_1 = require("../context_component");
var _1 = require(".");
var actions_1 = require("../actions/actions");
var MessagePanel = /** @class */ (function (_super) {
    __extends(MessagePanel, _super);
    function MessagePanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MessagePanel.prototype.componentDidMount = function () {
        var _this = this;
        this.tokens = [
            this.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); }),
        ];
    };
    MessagePanel.prototype.componentWillUnmount = function () {
        this.tokens.forEach(function (token) { return token.remove(); });
        this.tokens = [];
    };
    MessagePanel.prototype.renderUnexpectedState = function (message) {
        return (React.createElement("div", { className: "attribute-editor charticulator__widget-container" },
            React.createElement("div", { className: "attribute-editor-unexpected" }, message)));
    };
    MessagePanel.prototype.render = function () {
        var _this = this;
        var store = this.props.store;
        var messages = store.messageState;
        return (React.createElement("div", { className: "charticulator__object-list-editor" }, Array.from(messages, function (_a) {
            var _b = __read(_a, 1), key = _b[0];
            return key;
        }).map(function (key, index) {
            var message = messages.get(key);
            if (core_1.messageTypes.find(function (k) { return k === key; })) {
                return (React.createElement("div", { key: index },
                    React.createElement("div", { key: index, className: "el-object-item auto-height" },
                        React.createElement("span", { className: "el-text" }, message))));
            }
            else {
                return (React.createElement("div", { key: index },
                    React.createElement("div", { key: index, className: "el-object-item auto-height", onClick: function () {
                            _this.store.dispatcher.dispatch(new actions_1.RemoveMessage(key));
                        } },
                        React.createElement("span", { className: "el-text" }, message),
                        React.createElement(_1.SVGImageIcon, { url: R.getSVGIcon("ChromeClose") }))));
            }
        })));
    };
    return MessagePanel;
}(context_component_1.ContextedComponent));
exports.MessagePanel = MessagePanel;
//# sourceMappingURL=messsage_box.js.map