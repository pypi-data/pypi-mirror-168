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
exports.GroupByEditor = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../../../core");
var strings_1 = require("../../../../strings");
var actions_1 = require("../../../actions");
var data_field_selector_1 = require("../../dataset/data_field_selector");
var GroupByEditor = /** @class */ (function (_super) {
    __extends(GroupByEditor, _super);
    function GroupByEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState(_this.props.value);
        return _this;
    }
    GroupByEditor.prototype.getDefaultState = function (value) {
        var groupByType = "none";
        if (value) {
            if (value.expression) {
                groupByType = "expression";
            }
        }
        return {
            type: groupByType,
            currentValue: value,
        };
    };
    GroupByEditor.prototype.emitUpdateGroupBy = function (newValue) {
        if (this.props.options.target.property) {
            this.props.manager.emitSetProperty(this.props.options.target.property, newValue);
        }
        if (this.props.options.target.plotSegment) {
            this.props.manager.store.dispatcher.dispatch(new actions_1.Actions.SetPlotSegmentGroupBy(this.props.options.target.plotSegment, newValue));
        }
        this.setState(this.getDefaultState(newValue));
    };
    GroupByEditor.prototype.render = function () {
        var _this = this;
        var options = this.props.options;
        return (React.createElement("div", { className: "charticulator__groupby-editor" },
            React.createElement(data_field_selector_1.DataFieldSelector, { defaultValue: this.state.currentValue && this.state.currentValue.expression
                    ? {
                        table: options.table,
                        expression: this.state.currentValue.expression,
                    }
                    : null, table: options.table, nullDescription: strings_1.strings.core.none, datasetStore: this.props.manager.store, kinds: [core_1.Specification.DataKind.Categorical], onChange: function (field) {
                    if (field == null) {
                        _this.emitUpdateGroupBy(null);
                    }
                    else {
                        _this.emitUpdateGroupBy({
                            expression: field.expression,
                        });
                    }
                } })));
    };
    return GroupByEditor;
}(React.Component));
exports.GroupByEditor = GroupByEditor;
//# sourceMappingURL=groupby_editor.js.map