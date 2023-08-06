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
exports.FileViewSaveAs = void 0;
var React = require("react");
var R = require("../../resources");
var _1 = require(".");
var components_1 = require("../../components");
var actions_1 = require("../../actions");
var strings_1 = require("../../../strings");
var react_1 = require("@fluentui/react");
var container_1 = require("../../../container");
var FileViewSaveAs = /** @class */ (function (_super) {
    __extends(FileViewSaveAs, _super);
    function FileViewSaveAs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        return _this;
    }
    FileViewSaveAs.prototype.render = function () {
        var _this = this;
        var inputSaveChartName;
        return (React.createElement("section", { className: "charticulator__file-view-content is-fix-width" },
            React.createElement("h1", null, strings_1.strings.mainTabs.save),
            React.createElement("section", null,
                React.createElement(_1.CurrentChartView, { store: this.props.store }),
                React.createElement("div", { className: "form-group" },
                    React.createElement("input", { ref: function (e) { return (inputSaveChartName = e); }, type: "text", required: true, defaultValue: this.props.store.dataset.name }),
                    React.createElement("label", null, strings_1.strings.fileSave.chartName),
                    React.createElement("i", { className: "bar" })),
                React.createElement("div", { className: "buttons" },
                    React.createElement("span", { className: "el-progress" }, this.state.saving ? (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("loading") })) : null),
                    React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "Save",
                        }, styles: container_1.primaryButtonStyles, text: strings_1.strings.fileSave.saveButton, onClick: function () {
                            var name = inputSaveChartName.value.trim();
                            _this.setState({
                                saving: true,
                            }, function () {
                                _this.props.store.dispatcher.dispatch(new actions_1.Actions.SaveAs(name, function (error) {
                                    if (error) {
                                        _this.setState({
                                            saving: true,
                                            error: error.message,
                                        });
                                    }
                                    else {
                                        _this.props.onClose();
                                    }
                                }));
                            });
                        } })),
                this.state.error ? (React.createElement("div", { className: "error" }, this.state.error)) : null)));
    };
    return FileViewSaveAs;
}(React.Component));
exports.FileViewSaveAs = FileViewSaveAs;
//# sourceMappingURL=save_view.js.map