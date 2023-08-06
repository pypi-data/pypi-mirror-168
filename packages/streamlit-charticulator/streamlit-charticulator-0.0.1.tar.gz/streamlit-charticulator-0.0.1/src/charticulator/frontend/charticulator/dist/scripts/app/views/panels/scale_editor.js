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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ScaleEditor = void 0;
var React = require("react");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var stores_1 = require("../../stores");
var fluentui_manager_1 = require("./widgets/fluentui_manager");
var categorical_legend_1 = require("../../../core/prototypes/legends/categorical_legend");
var strings_1 = require("../../../strings");
var react_1 = require("@fluentui/react");
var observer_1 = require("./widgets/observer");
var panel_styles_1 = require("./panel_styles");
var ScaleEditor = /** @class */ (function (_super) {
    __extends(ScaleEditor, _super);
    function ScaleEditor() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ScaleEditor.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () {
            _this.forceUpdate();
        });
    };
    ScaleEditor.prototype.componentWillUnmount = function () {
        this.token.remove();
    };
    // eslint-disable-next-line
    ScaleEditor.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, scale = _b.scale, store = _b.store, scaleMapping = _b.scaleMapping;
        var scaleClass = store.chartManager.getClassById(scale._id);
        var manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, scaleClass, true);
        manager.onEditMappingHandler = function (attribute, mapping) {
            new actions_1.Actions.SetScaleAttribute(scale, attribute, mapping).dispatch(store.dispatcher);
        };
        var canAddLegend = true;
        if (scale.classID.startsWith("scale.format") ||
            scale.classID === "scale.categorical<string,image>" ||
            scale.classID === "scale.categorical<string,boolean>" ||
            scale.classID === "scale.linear<number,boolean>") {
            canAddLegend = false;
        }
        var canExtendLegend = false;
        if (scale.classID === "scale.categorical<string,color>" ||
            scale.classID === "scale.categorical<date,color>") {
            canExtendLegend = true;
        }
        var currentSelection = this.props.store.currentMappingAttributeFocus;
        return (React.createElement(panel_styles_1.ScaleEditorWrapper, { className: "scale-editor-view" },
            React.createElement("div", { className: "attribute-editor" },
                React.createElement("section", { className: "attribute-editor-element" },
                    React.createElement("div", { className: "header" },
                        React.createElement(components_1.EditableTextView, { text: scale.properties.name, onEdit: function (newText) {
                                new actions_1.Actions.SetObjectProperty(scale, "name", null, newText, true).dispatch(store.dispatcher);
                            } })),
                    manager.vertical.apply(manager, __spread(scaleClass.getAttributePanelWidgets(manager))),
                    React.createElement("div", { className: "action-buttons" },
                        canExtendLegend ? (React.createElement(React.Fragment, null,
                            React.createElement(react_1.DefaultButton, { iconProps: {
                                    iconName: "Add",
                                }, text: strings_1.strings.scaleEditor.add, onClick: function () {
                                    manager.eventManager.notify(observer_1.EventType.UPDATE_FIELD, {
                                        property: "autoDomainMin",
                                    }, false);
                                    manager.eventManager.notify(observer_1.EventType.UPDATE_FIELD, {
                                        property: "autoDomainMax",
                                    }, false);
                                    var mappingsKey = Object.keys(scale.properties.mapping);
                                    var theLastMapping = mappingsKey[mappingsKey.length - 1];
                                    var value = scale.properties.mapping[theLastMapping];
                                    new actions_1.Actions.SetObjectProperty(scale, "mapping", categorical_legend_1.ReservedMappingKeyNamePrefix + core_1.uniqueID(), value, true, true).dispatch(_this.props.store.dispatcher);
                                } }),
                            React.createElement(react_1.DefaultButton, { iconProps: {
                                    iconName: "Remove",
                                }, disabled: ((_a = currentSelection === null || currentSelection === void 0 ? void 0 : currentSelection.length) !== null && _a !== void 0 ? _a : 0) === 0, text: strings_1.strings.scaleEditor.removeSelected, onClick: function () {
                                    if ((currentSelection === null || currentSelection === void 0 ? void 0 : currentSelection.length) > 0) {
                                        new actions_1.Actions.DeleteObjectProperty(scale, "mapping", currentSelection, false, true).dispatch(_this.props.store.dispatcher);
                                        new actions_1.Actions.SetCurrentMappingAttribute(null).dispatch(_this.props.store.dispatcher);
                                    }
                                } }))) : null,
                        canAddLegend ? (React.createElement(react_1.DefaultButton, { iconProps: {
                                iconName: "CharticulatorLegend",
                            }, text: store.isLegendExistForScale(scale._id)
                                ? strings_1.strings.scaleEditor.removeLegend
                                : strings_1.strings.scaleEditor.addLegend, onClick: function () {
                                new actions_1.Actions.ToggleLegendForScale(scale._id, scaleMapping, _this.props.plotSegment).dispatch(store.dispatcher);
                            } })) : null)))));
    };
    return ScaleEditor;
}(React.Component));
exports.ScaleEditor = ScaleEditor;
//# sourceMappingURL=scale_editor.js.map