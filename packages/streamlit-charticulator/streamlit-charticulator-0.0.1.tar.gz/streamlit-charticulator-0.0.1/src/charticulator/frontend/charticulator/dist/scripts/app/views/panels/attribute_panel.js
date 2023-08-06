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
exports.AttributePanel = void 0;
var React = require("react");
var R = require("../../resources");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var stores_1 = require("../../stores");
var fluentui_manager_1 = require("./widgets/fluentui_manager");
var strings_1 = require("../../../strings");
function getObjectIcon(classID) {
    return R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(classID).iconPath || "object");
}
var AttributePanel = /** @class */ (function (_super) {
    __extends(AttributePanel, _super);
    function AttributePanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tokens = [];
        return _this;
    }
    AttributePanel.prototype.componentDidMount = function () {
        var _this = this;
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () {
            _this.forceUpdate();
        }));
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_SELECTION, function () {
            _this.forceUpdate();
        }));
    };
    AttributePanel.prototype.componentWillUnmount = function () {
        this.tokens.forEach(function (token) { return token.remove(); });
        this.tokens = [];
    };
    AttributePanel.prototype.renderUnexpectedState = function (message) {
        return (React.createElement("div", { className: "attribute-editor charticulator__widget-container" },
            React.createElement("div", { className: "attribute-editor-unexpected" }, message)));
    };
    // eslint-disable-next-line
    AttributePanel.prototype.render = function () {
        var _this = this;
        var selection = this.props.store.currentSelection;
        var object;
        var objectClass;
        var manager;
        if (selection) {
            if (selection instanceof stores_1.GlyphSelection) {
                if (!selection.plotSegment) {
                    return this.renderUnexpectedState(strings_1.strings.canvas.markContainer);
                }
                var glyph_1 = selection.glyph;
                object = glyph_1;
                objectClass = this.props.store.chartManager.getGlyphClass(this.props.store.chartManager.findGlyphState(selection.plotSegment, selection.glyph, this.props.store.getSelectedGlyphIndex(selection.plotSegment._id)));
                manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, objectClass);
                manager.onEditMappingHandler = function (attribute, mapping) {
                    new actions_1.Actions.SetGlyphAttribute(glyph_1, attribute, mapping).dispatch(_this.props.store.dispatcher);
                };
            }
            if (selection instanceof stores_1.MarkSelection) {
                if (!selection.plotSegment) {
                    return this.renderUnexpectedState(strings_1.strings.canvas.markContainer);
                }
                var glyph_2 = selection.glyph;
                var mark_1 = selection.mark;
                object = mark_1;
                objectClass = this.props.store.chartManager.getMarkClass(this.props.store.chartManager.findMarkState(selection.plotSegment, selection.glyph, selection.mark, this.props.store.getSelectedGlyphIndex(selection.plotSegment._id)));
                manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, objectClass);
                manager.onEditMappingHandler = function (attribute, mapping) {
                    new actions_1.Actions.SetMarkAttribute(glyph_2, mark_1, attribute, mapping).dispatch(_this.props.store.dispatcher);
                };
                manager.onMapDataHandler = function (attribute, data, hints) {
                    new actions_1.Actions.MapDataToMarkAttribute(glyph_2, mark_1, attribute, objectClass.attributes[attribute].type, data.expression, data.valueType, data.metadata, hints, data.table.name).dispatch(_this.props.store.dispatcher);
                };
            }
            if (selection instanceof stores_1.ChartElementSelection) {
                var markLayout_1 = selection.chartElement;
                var layoutClass = this.props.store.chartManager.getClassById(markLayout_1._id);
                object = markLayout_1;
                objectClass = layoutClass;
                manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, objectClass);
                manager.onEditMappingHandler = function (attribute, mapping) {
                    new actions_1.Actions.SetChartElementMapping(markLayout_1, attribute, mapping).dispatch(_this.props.store.dispatcher);
                };
                manager.onMapDataHandler = function (attribute, data, hints) {
                    new actions_1.Actions.MapDataToChartElementAttribute(markLayout_1, attribute, objectClass.attributes[attribute].type, data.table.name, data.expression, data.valueType, data.metadata, hints).dispatch(_this.props.store.dispatcher);
                };
            }
        }
        else {
            var chart = this.props.store.chart;
            var boundClass = this.props.store.chartManager.getChartClass(this.props.store.chartState);
            object = chart;
            objectClass = boundClass;
            manager = new fluentui_manager_1.FluentUIWidgetManager(this.props.store, objectClass);
            manager.onEditMappingHandler = function (attribute, mapping) {
                new actions_1.Actions.SetChartAttribute(attribute, mapping).dispatch(_this.props.store.dispatcher);
            };
        }
        if (manager) {
            return (React.createElement("div", { className: "attribute-editor charticulator__widget-container" },
                React.createElement("section", { className: "attribute-editor-element", key: object._id },
                    React.createElement("div", { className: "header", key: "header" },
                        React.createElement(components_1.SVGImageIcon, { url: getObjectIcon(object.classID), height: 32, width: 32 }),
                        React.createElement(components_1.EditableTextView, { text: object.properties.name, onEdit: function (newValue) {
                                new actions_1.Actions.SetObjectProperty(object, "name", null, newValue, true).dispatch(_this.props.store.dispatcher);
                            } })),
                    manager.searchInput({
                        placeholder: "Search",
                    }),
                    manager.vertical.apply(manager, __spread(objectClass.getAttributePanelWidgets(manager))))));
        }
    };
    return AttributePanel;
}(React.Component));
exports.AttributePanel = AttributePanel;
//# sourceMappingURL=attribute_panel.js.map