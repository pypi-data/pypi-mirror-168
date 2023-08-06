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
exports.ScaleValueSelector = void 0;
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var R = require("../../resources");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var stores_1 = require("../../stores");
var fluentui_manager_1 = require("./widgets/fluentui_manager");
var ScaleValueSelector = /** @class */ (function (_super) {
    __extends(ScaleValueSelector, _super);
    function ScaleValueSelector(props) {
        var _this = _super.call(this, props) || this;
        var parsedExpression = core_1.Expression.parse(_this.props.scaleMapping.expression);
        var selectedIndex;
        try {
            selectedIndex = parsedExpression.args[0]
                .args[0].args[1].value;
        }
        catch (ex) {
            selectedIndex = 0;
        }
        _this.state = {
            selectedIndex: selectedIndex,
        };
        return _this;
    }
    ScaleValueSelector.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () {
            _this.forceUpdate();
        });
    };
    ScaleValueSelector.prototype.componentWillUnmount = function () {
        this.token.remove();
    };
    ScaleValueSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, scale = _a.scale, store = _a.store, scaleMapping = _a.scaleMapping;
        var scaleClass = store.chartManager.getClassById(scale._id);
        var manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, scaleClass, true);
        manager.onEditMappingHandler = function (attribute, mapping) {
            new actions_1.Actions.SetScaleAttribute(scale, attribute, mapping).dispatch(store.dispatcher);
        };
        var canSelectValue = false;
        if (typeof this.props.onSelect === "function") {
            canSelectValue = true;
        }
        return (React.createElement("div", { className: "scale-editor-view", style: { width: "400px", padding: "10px" } },
            React.createElement("div", { className: "attribute-editor" },
                React.createElement("section", { className: "attribute-editor-element" },
                    React.createElement("div", { className: "header" },
                        React.createElement(components_1.EditableTextView, { text: scale.properties.name, onEdit: function (newText) {
                                new actions_1.Actions.SetObjectProperty(scale, "name", null, newText, true).dispatch(store.dispatcher);
                            } })),
                    manager.sectionHeader("Color Mapping"),
                    manager.vertical(manager.scrollList(Object.keys(scale.properties.mapping).map(function (key, selectedIndex) {
                        return (React.createElement("div", { className: _this.props.onSelect &&
                                _this.state.selectedIndex === selectedIndex
                                ? "is-active"
                                : "", onClick: function () {
                                _this.setState({ selectedIndex: selectedIndex });
                                if (selectedIndex != null && _this.props.onSelect) {
                                    _this.props.onSelect(selectedIndex);
                                }
                            } }, manager.horizontal([2, 3], manager.label(key), manager.inputColor({
                            property: "mapping",
                            field: key,
                            noComputeLayout: true,
                        }, {
                            labelKey: key,
                            noDefaultMargin: true,
                            stopPropagation: true,
                            styles: {
                                marginTop: "0px",
                            },
                        }))));
                    }))),
                    canSelectValue ? (React.createElement("div", { className: "action-buttons" },
                        React.createElement(components_1.ButtonRaised, { url: R.getSVGIcon("CharticulatorLegend"), text: store.isLegendExistForScale(scale._id)
                                ? "Remove Legend"
                                : "Add Legend", onClick: function () {
                                new actions_1.Actions.ToggleLegendForScale(scale._id, scaleMapping, null).dispatch(store.dispatcher);
                            } }))) : null))));
    };
    return ScaleValueSelector;
}(React.Component));
exports.ScaleValueSelector = ScaleValueSelector;
//# sourceMappingURL=scale_value_selector.js.map