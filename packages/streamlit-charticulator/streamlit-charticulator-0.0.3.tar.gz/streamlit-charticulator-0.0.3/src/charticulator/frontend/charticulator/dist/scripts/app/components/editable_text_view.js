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
exports.EditableTextView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var fluentui_customized_components_1 = require("../views/panels/widgets/controls/fluentui_customized_components");
var react_1 = require("@fluentui/react");
var EditableTextView = /** @class */ (function (_super) {
    __extends(EditableTextView, _super);
    function EditableTextView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            editing: _this.props.autofocus || false,
            currentText: _this.props.text,
        };
        _this.confirmEdit = _this.confirmEdit.bind(_this);
        _this.cancelEdit = _this.cancelEdit.bind(_this);
        _this.startEdit = _this.startEdit.bind(_this);
        return _this;
    }
    EditableTextView.prototype.confirmEdit = function () {
        var text = this.state.currentText;
        this.setState({
            editing: false,
        });
        if (this.props.onEdit) {
            this.props.onEdit(text);
        }
    };
    EditableTextView.prototype.cancelEdit = function () {
        this.setState({
            editing: false,
        });
    };
    EditableTextView.prototype.startEdit = function () {
        this.setState({
            editing: true,
            currentText: this.props.text,
        });
    };
    EditableTextView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", null,
            React.createElement(fluentui_customized_components_1.FluentTextField, null,
                React.createElement(react_1.TextField, { value: this.state.currentText, onRenderLabel: fluentui_customized_components_1.labelRender, type: "text", onChange: function (event, newValue) {
                        _this.setState({ currentText: newValue });
                    }, onBlur: function () {
                        if (_this.state.currentText == _this.props.text) {
                            _this.cancelEdit();
                        }
                        else {
                            _this.setState({
                                currentText: _this.props.text,
                            });
                        }
                    }, onKeyDown: function (e) {
                        if (e.key == "Enter") {
                            _this.confirmEdit();
                        }
                        if (e.key == "Escape") {
                            _this.cancelEdit();
                        }
                    }, autoFocus: false, styles: {
                        fieldGroup: {
                            border: !this.state.editing && "none",
                        },
                    } }))));
    };
    return EditableTextView;
}(React.Component));
exports.EditableTextView = EditableTextView;
//# sourceMappingURL=editable_text_view.js.map