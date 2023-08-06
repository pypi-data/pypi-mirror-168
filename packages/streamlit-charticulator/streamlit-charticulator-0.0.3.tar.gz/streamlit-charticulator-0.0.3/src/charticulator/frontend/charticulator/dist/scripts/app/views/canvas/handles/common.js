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
exports.HandlesDragContext = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var core_1 = require("../../../../core");
var HandlesDragContext = /** @class */ (function (_super) {
    __extends(HandlesDragContext, _super);
    function HandlesDragContext() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HandlesDragContext.prototype.onDrag = function (listener) {
        return this.addListener("drag", listener);
    };
    HandlesDragContext.prototype.onEnd = function (listener) {
        return this.addListener("end", listener);
    };
    return HandlesDragContext;
}(core_1.EventEmitter));
exports.HandlesDragContext = HandlesDragContext;
//# sourceMappingURL=common.js.map