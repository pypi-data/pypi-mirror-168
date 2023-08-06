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
exports.ScalesPanel = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var R = require("../../resources");
var core_1 = require("../../../core");
var components_1 = require("../../components");
var stores_1 = require("../../stores");
var object_list_editor_1 = require("./object_list_editor");
var context_component_1 = require("../../context_component");
var specification_1 = require("../../../core/specification");
var __1 = require("../..");
var utils_1 = require("../../utils");
var expression_1 = require("../../../core/expression");
var ScalesPanel = /** @class */ (function (_super) {
    __extends(ScalesPanel, _super);
    function ScalesPanel(props) {
        var _this = _super.call(this, props, null) || this;
        _this.state = {
            isSelected: "",
        };
        return _this;
    }
    ScalesPanel.prototype.componentDidMount = function () {
        var _this = this;
        this.tokens = [
            this.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); }),
            this.store.addListener(stores_1.AppStore.EVENT_SELECTION, function () {
                return _this.forceUpdate();
            }),
            this.store.addListener(stores_1.AppStore.EVENT_SAVECHART, function () {
                return _this.forceUpdate();
            }),
        ];
    };
    ScalesPanel.prototype.componentWillUnmount = function () {
        this.tokens.forEach(function (token) { return token.remove(); });
        this.tokens = [];
    };
    ScalesPanel.prototype.renderUnexpectedState = function (message) {
        return (React.createElement("div", { className: "attribute-editor charticulator__widget-container" },
            React.createElement("div", { className: "attribute-editor-unexpected" }, message)));
    };
    ScalesPanel.prototype.getPropertyDisplayName = function (name) {
        return name[0].toUpperCase() + name.slice(1);
    };
    // eslint-disable-next-line
    ScalesPanel.prototype.render = function () {
        var _this = this;
        var store = this.props.store;
        var scales = store.chart.scales;
        var filterElementByScalePredicate = function (scaleID) { return function (element) {
            return (Object.keys(element.mappings).find(function (key) {
                var mapping = element.mappings[key];
                return ((mapping.type === specification_1.MappingType.scale ||
                    mapping.type === specification_1.MappingType.expressionScale) &&
                    mapping.scale === scaleID);
            }) != undefined);
        }; };
        var filterElementProperties = function (scaleID, element) {
            return Object.keys(element.mappings).filter(function (key) {
                var mapping = element.mappings[key];
                return ((mapping.type === specification_1.MappingType.scale ||
                    mapping.type === specification_1.MappingType.expressionScale) &&
                    mapping.scale === scaleID);
            });
        };
        // eslint-disable-next-line
        var mapToUI = function (scale) { return function (glyph, element
        // eslint-disable-next-line
        ) { return function (key) {
            if (!element) {
                return (React.createElement("div", { key: scale._id, className: "el-object-item" },
                    React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(scale.classID).iconPath) }),
                    React.createElement("span", { className: "el-text" }, scale.properties.name)));
            }
            else {
                var expr_1 = element.mappings[key].expression;
                var rawColumnExpr_1 = null; // TODO handle
                return (React.createElement("div", { className: "el-object-item el-object-scale-attribute", key: scale._id + "_" + element._id + "_" + key, onClick: function () {
                        if (glyph) {
                            _this.dispatch(new __1.Actions.SelectMark(null, glyph, element));
                        }
                        else {
                            _this.dispatch(new __1.Actions.SelectChartElement(element));
                        }
                        _this.dispatch(new __1.Actions.FocusToMarkAttribute(key));
                    } },
                    React.createElement(components_1.DraggableElement, { key: key, className: utils_1.classNames("charticulator__scale-panel-property", [
                            "is-active",
                            _this.state.isSelected === expr_1,
                        ]), onDragStart: function () { return _this.setState({ isSelected: expr_1 }); }, onDragEnd: function () { return _this.setState({ isSelected: null }); }, dragData: function () {
                            var type = element.mappings[key].valueType;
                            var scaleID = element.mappings[key].scale;
                            var allowSelectValue = element.mappings[key]
                                .allowSelectValue;
                            var aggregation = core_1.Expression.getDefaultAggregationFunction(type, null);
                            var applyAggregation = function (expr) {
                                return core_1.Expression.functionCall(aggregation, core_1.Expression.parse(expr)).toString();
                            };
                            var table = _this.store.dataset.tables.find(function (table) { return table.name === element.mappings[key].table; });
                            var parsedExpression = core_1.Expression.parse(expr_1);
                            var metadata = {};
                            if (parsedExpression instanceof expression_1.FunctionCall &&
                                parsedExpression.args[0] instanceof expression_1.Variable) {
                                var firstArgument_1 = parsedExpression.args[0];
                                var column = table.columns.find(function (col) { return col.name === firstArgument_1.name; });
                                metadata = column.metadata;
                                rawColumnExpr_1 =
                                    metadata.rawColumnName &&
                                        applyAggregation(metadata.rawColumnName);
                            }
                            _this.setState({ isSelected: expr_1 });
                            var r = new __1.DragData.DataExpression(table, expr_1, type, metadata, rawColumnExpr_1, scaleID, allowSelectValue);
                            return r;
                        }, renderDragElement: function () { return [
                            React.createElement("span", { className: "dragging-table-cell" }, element.mappings[key].expression),
                            { x: -10, y: -8 },
                        ]; } },
                        React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(element.classID).iconPath) }),
                        React.createElement("span", { className: "el-text" }, element.properties.name + "." + _this.getPropertyDisplayName(key)))));
            }
        }; }; };
        scales = scales.sort(function (a, b) {
            if (a.properties.name < b.properties.name) {
                return -1;
            }
            if (a.properties.name > b.properties.name) {
                return 1;
            }
            return 0;
        });
        // Collect all used scales and object with properties into one list
        var propertyList = scales.flatMap(function (scale) {
            return [0]
                .map(function () {
                return {
                    scale: scale,
                    mark: null,
                    property: null,
                    glyph: null,
                };
            })
                .concat(
            // take all chart elements
            store.chart.elements
                // filter elements by scale
                .filter(filterElementByScalePredicate(scale._id))
                .flatMap(function (mark) {
                // Take all properties of object/element where scale was used and map them into {property, element, scale} object/element
                return filterElementProperties(scale._id, mark).map(function (property) {
                    return {
                        property: property,
                        mark: mark,
                        scale: scale,
                        glyph: null,
                    };
                });
            }))
                .concat(store.chart.glyphs
                // map all glyphs into {glyph & marks} group
                .flatMap(function (glyph) {
                return glyph.marks.map(function (mark) {
                    return {
                        glyph: glyph,
                        mark: mark,
                    };
                });
            })
                // filter elements by scale
                .filter(function (_a) {
                var mark = _a.mark;
                return filterElementByScalePredicate(scale._id)(mark);
            })
                // Take all properties of object/element where scale was used and map them into {property, element, scale} object/element
                .flatMap(function (_a) {
                var mark = _a.mark, glyph = _a.glyph;
                return filterElementProperties(scale._id, mark).map(function (property) {
                    return {
                        property: property,
                        mark: mark,
                        scale: scale,
                        glyph: glyph,
                    };
                });
            }));
        });
        return (React.createElement("div", { className: "charticulator__object-list-editor charticulator__object-scales" },
            React.createElement(object_list_editor_1.ReorderListView, { restrict: true, enabled: true, onReorder: function (IndexA, IndexB) {
                    // Drag properties item only
                    if (!propertyList[IndexA].property || IndexA === IndexB) {
                        return;
                    }
                    // Find next scale in the list
                    if (IndexB > 0) {
                        IndexB--;
                    }
                    while (IndexB > 0 &&
                        !propertyList[IndexB] &&
                        propertyList[IndexB].property != null) {
                        IndexB--;
                    }
                    store.dispatcher.dispatch(new __1.Actions.SetObjectMappingScale(propertyList[IndexA].mark, propertyList[IndexA].property, propertyList[IndexB].scale._id));
                } }, propertyList.map(function (el) {
                return mapToUI(el.scale)(el.glyph, el.mark)(el.property);
            }))));
    };
    return ScalesPanel;
}(context_component_1.ContextedComponent));
exports.ScalesPanel = ScalesPanel;
//# sourceMappingURL=scales_panel.js.map