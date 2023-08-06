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
exports.FileViewNew = void 0;
var React = require("react");
var strings_1 = require("../../../strings");
var actions_1 = require("../../actions");
var import_data_view_1 = require("./import_data_view");
var FileViewNew = /** @class */ (function (_super) {
    __extends(FileViewNew, _super);
    function FileViewNew() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FileViewNew.prototype.render = function () {
        var _this = this;
        return (React.createElement("section", { className: "charticulator__file-view-content" },
            React.createElement("h1", null, strings_1.strings.mainTabs.new),
            React.createElement(import_data_view_1.ImportDataView, { store: this.props.store, onConfirmImport: function (dataset) {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.ImportDataset(dataset));
                    _this.props.onClose();
                } })));
    };
    return FileViewNew;
}(React.Component));
exports.FileViewNew = FileViewNew;
//# sourceMappingURL=new_view.js.map