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
exports.MainReactContext = exports.ContextedComponent = exports.MainContextTypes = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var stores_1 = require("./stores");
var strings_1 = require("../strings");
exports.MainContextTypes = {
    store: function (props, propName, componentName) {
        if (props[propName] instanceof stores_1.AppStore) {
            return null;
        }
        else {
            return new Error(strings_1.strings.error.storeNotFound(componentName));
        }
    },
};
var ContextedComponent = /** @class */ (function (_super) {
    __extends(ContextedComponent, _super);
    function ContextedComponent(props, context) {
        return _super.call(this, props, context) || this;
    }
    ContextedComponent.prototype.dispatch = function (action) {
        this.context.store.dispatcher.dispatch(action);
    };
    Object.defineProperty(ContextedComponent.prototype, "store", {
        get: function () {
            return this.context.store;
        },
        enumerable: false,
        configurable: true
    });
    ContextedComponent.contextTypes = exports.MainContextTypes;
    return ContextedComponent;
}(React.Component));
exports.ContextedComponent = ContextedComponent;
exports.MainReactContext = React.createContext(null);
//# sourceMappingURL=context_component.js.map