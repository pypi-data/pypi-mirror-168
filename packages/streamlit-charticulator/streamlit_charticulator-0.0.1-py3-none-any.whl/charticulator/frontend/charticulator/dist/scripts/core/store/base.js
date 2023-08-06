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
exports.BaseStore = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../common");
var BaseStore = /** @class */ (function (_super) {
    __extends(BaseStore, _super);
    function BaseStore(parent) {
        var _this = _super.call(this) || this;
        _this._id = common_1.uniqueID();
        _this.parent = parent;
        if (parent != null) {
            _this.dispatcher = parent.dispatcher;
        }
        else {
            _this.dispatcher = new common_1.Dispatcher();
        }
        _this.dispatcherID = _this.dispatcher.register(function (action) {
            return _this.handleAction(action);
        });
        return _this;
    }
    // Override this in the child store
    BaseStore.prototype.handleAction = function (action) {
        action.digest();
    };
    BaseStore.prototype.destroy = function () {
        if (this.dispatcherID != null) {
            this.dispatcher.unregister(this.dispatcherID);
        }
    };
    return BaseStore;
}(common_1.EventEmitter));
exports.BaseStore = BaseStore;
//# sourceMappingURL=base.js.map