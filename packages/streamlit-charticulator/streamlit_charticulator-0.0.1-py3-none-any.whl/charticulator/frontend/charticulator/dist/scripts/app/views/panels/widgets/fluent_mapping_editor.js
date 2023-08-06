"use strict";
/* eslint-disable max-lines-per-function */
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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.parentOfType = exports.DataMappAndScaleEditor = exports.FluentMappingEditor = void 0;
var React = require("react");
var core_1 = require("../../../../core");
var actions_1 = require("../../../actions");
var fluentui_color_picker_1 = require("../../../components/fluentui_color_picker");
var context_component_1 = require("../../../context_component");
var common_1 = require("../../dataset/common");
var scale_editor_1 = require("../scale_editor");
var types_1 = require("./types");
var scale_value_selector_1 = require("../scale_value_selector");
var fluentui_value_editor_1 = require("./fluentui_value_editor");
var fluentui_input_expression_1 = require("./controls/fluentui_input_expression");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var fluent_ui_data_field_selector_1 = require("../../dataset/fluent_ui_data_field_selector");
var data_field_binding_builder_1 = require("../../dataset/data_field_binding_builder");
var strings_1 = require("../../../../strings");
var specification_1 = require("../../../../core/specification");
var fluentui_empty_mapping_1 = require("./controls/fluentui_empty_mapping");
var utils_1 = require("./utils");
var FluentMappingEditor = /** @class */ (function (_super) {
    __extends(FluentMappingEditor, _super);
    function FluentMappingEditor(props) {
        var _this = _super.call(this, props) || this;
        _this.updateEvents = new core_1.EventEmitter();
        _this.state = {
            showNoneAsValue: false,
            isDataFieldValueSelectionOpen: false,
            isColorPickerOpen: false,
        };
        _this.director = null;
        _this.director = new data_field_binding_builder_1.Director();
        _this.director.setBuilder(new data_field_binding_builder_1.MenuItemBuilder());
        return _this;
    }
    FluentMappingEditor.prototype.changeDataFieldValueSelectionState = function () {
        this.setState(__assign(__assign({}, this.state), { isDataFieldValueSelectionOpen: !this.state.isDataFieldValueSelectionOpen }));
    };
    FluentMappingEditor.prototype.changeColorPickerState = function () {
        this.setState(__assign(__assign({}, this.state), { isColorPickerOpen: !this.state.isColorPickerOpen }));
    };
    FluentMappingEditor.prototype.openDataFieldValueSelection = function () {
        var _this = this;
        var parent = this.props.parent;
        var attribute = this.props.attribute;
        var mapping = parent.getAttributeMapping(attribute);
        var scaleMapping = mapping;
        if (scaleMapping === null || scaleMapping === void 0 ? void 0 : scaleMapping.scale) {
            var scaleObject = core_1.getById(this.props.store.chart.scales, scaleMapping.scale);
            return (React.createElement(React.Fragment, null, this.state.isDataFieldValueSelectionOpen && (React.createElement(react_1.Callout, { target: "#dataFieldValueSelection", onDismiss: function () { return _this.changeDataFieldValueSelectionState(); } },
                React.createElement(scale_value_selector_1.ScaleValueSelector, { scale: scaleObject, scaleMapping: mapping, store: this.props.store, onSelect: function (index) {
                        var paresedExpression = core_1.Expression.parse(scaleMapping.expression);
                        // change the second param of get function
                        paresedExpression.args[1].value = index;
                        scaleMapping.expression = paresedExpression.toString();
                        _this.props.parent.onEditMappingHandler(_this.props.attribute, scaleMapping);
                        _this.changeDataFieldValueSelectionState();
                    } })))));
        }
        return null;
    };
    FluentMappingEditor.prototype.initiateValueEditor = function () {
        switch (this.props.type) {
            case "number":
            case "font-family":
            case "text":
                {
                    this.setState(__assign(__assign({}, this.state), { showNoneAsValue: true }));
                }
                break;
            case "color":
                {
                    if (this.noneLabel == null) {
                        return;
                    }
                    this.changeColorPickerState();
                }
                break;
        }
    };
    FluentMappingEditor.prototype.setValueMapping = function (value) {
        this.props.parent.onEditMappingHandler(this.props.attribute, {
            type: "value",
            value: value,
        });
    };
    FluentMappingEditor.prototype.clearMapping = function () {
        this.props.parent.onEditMappingHandler(this.props.attribute, null);
        this.setState(__assign(__assign({}, this.state), { showNoneAsValue: false }));
    };
    FluentMappingEditor.prototype.mapData = function (data, hints) {
        this.props.parent.onMapDataHandler(this.props.attribute, data, hints);
    };
    FluentMappingEditor.prototype.componentDidUpdate = function () {
        this.updateEvents.emit("update");
    };
    FluentMappingEditor.prototype.getTableOrDefault = function () {
        if (this.props.options.table) {
            return this.props.options.table;
        }
        else {
            return this.props.parent.store.getTables()[0].name;
        }
    };
    FluentMappingEditor.prototype.renderValueEditor = function (value) {
        var _this = this;
        var placeholderText = this.props.options.defaultAuto
            ? strings_1.strings.core.auto
            : strings_1.strings.core.none;
        if (this.props.options.defaultValue != null) {
            placeholderText = this.props.options.defaultValue.toString();
        }
        var parent = this.props.parent;
        var attribute = this.props.attribute;
        var options = this.props.options;
        var mapping = parent.getAttributeMapping(attribute);
        var table = mapping ? mapping.table : options.table;
        var builderProps = getMenuProps.bind(this)(parent, attribute, options);
        var mainMenuItems = this.director.buildFieldsMenu(builderProps.onClick, builderProps.defaultValue, parent.store, this, attribute, table, options.acceptKinds);
        var menuRender = this.director.getMenuRender();
        return (React.createElement(React.Fragment, null,
            React.createElement(fluentui_value_editor_1.FluentValueEditor, { label: this.props.options.label, value: value, type: this.props.type, placeholder: placeholderText, onClear: function () { return _this.clearMapping(); }, onEmitValue: function (value) { return _this.setValueMapping(value); }, onEmitMapping: function (mapping) {
                    return _this.props.parent.onEditMappingHandler(_this.props.attribute, mapping);
                }, onBeginDataFieldSelection: function () {
                    if (_this.mappingButton) {
                        _this.mappingButton.click();
                    }
                }, getTable: function () { return _this.getTableOrDefault(); }, hints: this.props.options.hints, numberOptions: this.props.options.numberOptions, stopPropagation: this.props.options.stopPropagation, mainMenuItems: mainMenuItems, menuRender: menuRender })));
    };
    FluentMappingEditor.prototype.renderColorPicker = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null, this.state.isColorPickerOpen && (React.createElement(react_1.Callout, { target: "#id_" + this.props.options.label, onDismiss: function () { return _this.changeColorPickerState(); } },
            React.createElement(fluentui_color_picker_1.ColorPicker, { store: this.props.store, defaultValue: null, allowNull: true, onPick: function (color) {
                    if (color == null) {
                        _this.clearMapping();
                    }
                    else {
                        _this.setValueMapping(color);
                    }
                }, closePicker: function () {
                    _this.changeColorPickerState();
                }, parent: this })))));
    };
    FluentMappingEditor.prototype.renderCurrentAttributeMapping = function () {
        var _this = this;
        var parent = this.props.parent;
        var attribute = this.props.attribute;
        var options = this.props.options;
        var mapping = parent.getAttributeMapping(attribute);
        if (!mapping) {
            if (options.defaultValue != undefined) {
                return this.renderValueEditor(options.defaultValue);
            }
            else {
                var alwaysShowNoneAsValue = false;
                if (this.props.type == core_1.Specification.AttributeType.Number ||
                    this.props.type == core_1.Specification.AttributeType.Enum ||
                    this.props.type == core_1.Specification.AttributeType.Image) {
                    alwaysShowNoneAsValue = true;
                }
                if (this.state.showNoneAsValue || alwaysShowNoneAsValue) {
                    return this.renderValueEditor(null);
                }
                else {
                    var onClick = function () {
                        if (!mapping || mapping.valueIndex == undefined) {
                            _this.initiateValueEditor();
                        }
                    };
                    return (React.createElement(fluentui_empty_mapping_1.EmptyMapping, { options: options, onClick: onClick.bind(this), renderColorPicker: this.renderColorPicker.bind(this), type: this.props.type }));
                }
            }
        }
        else {
            switch (mapping.type) {
                case core_1.Specification.MappingType.value: {
                    var valueMapping = mapping;
                    return this.renderValueEditor(valueMapping.value);
                }
                case core_1.Specification.MappingType.text: {
                    var textMapping_1 = mapping;
                    return (React.createElement(fluentui_input_expression_1.FluentInputExpression, { label: this.props.options.label, defaultValue: textMapping_1.textExpression, textExpression: true, value: textMapping_1.textExpression, validate: function (value) {
                            return parent.store.verifyUserExpressionWithTable(value, textMapping_1.table, { textExpression: true, expectedTypes: ["string"] });
                        }, allowNull: true, onEnter: function (newValue) {
                            if (newValue == null || newValue.trim() == "") {
                                _this.clearMapping();
                            }
                            else {
                                if (core_1.Expression.parseTextExpression(newValue).isTrivialString()) {
                                    _this.props.parent.onEditMappingHandler(_this.props.attribute, {
                                        type: core_1.Specification.MappingType.value,
                                        value: newValue,
                                    });
                                }
                                else {
                                    _this.props.parent.onEditMappingHandler(_this.props.attribute, {
                                        type: core_1.Specification.MappingType.text,
                                        table: textMapping_1.table,
                                        textExpression: newValue,
                                    });
                                }
                            }
                            return true;
                        } }));
                }
                case core_1.Specification.MappingType.scale: {
                    var scaleMapping_1 = mapping;
                    var table = mapping ? mapping.table : options.table;
                    var builderProps = getMenuProps.bind(this)(parent, attribute, options);
                    var mainMenuItems = this.director.buildFieldsMenu(builderProps.onClick, builderProps.defaultValue, parent.store, this, attribute, table, options.acceptKinds);
                    var menuRender = this.director.getMenuRender();
                    if (scaleMapping_1.scale) {
                        return (React.createElement(React.Fragment, null,
                            this.props.options.label ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, this.props.options.label)) : null,
                            React.createElement(fluentui_customized_components_1.FluentActionButton, null,
                                React.createElement(react_1.ActionButton, { elementRef: function (e) { return (_this.mappingButton = e); }, styles: {
                                        menuIcon: __assign({ display: "none !important" }, fluentui_customized_components_1.defultComponentsHeight),
                                        root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                                    }, title: strings_1.strings.mappingEditor.bindData, menuProps: {
                                        items: mainMenuItems,
                                        onRenderMenuList: menuRender,
                                        onMenuOpened: function () {
                                            var _a;
                                            var currentMapping = parent.getAttributeMapping(attribute);
                                            FluentMappingEditor.openEditor((_a = currentMapping) === null || _a === void 0 ? void 0 : _a.expression, false, _this.mappingButton);
                                        },
                                    }, text: scaleMapping_1.expression, iconProps: {
                                        iconName: "ColumnFunction",
                                    }, onMenuClick: function (event) {
                                        if (scaleMapping_1.expression.startsWith("get")) {
                                            event.preventDefault();
                                            _this.changeDataFieldValueSelectionState();
                                        }
                                    } }))));
                    }
                    else {
                        return (React.createElement(React.Fragment, null,
                            this.props.options.label ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, this.props.options.label)) : null,
                            React.createElement(fluentui_customized_components_1.FluentActionButton, null,
                                React.createElement(react_1.ActionButton, { text: scaleMapping_1.expression, elementRef: function (e) { return (_this.mappingButton = e); }, iconProps: {
                                        iconName: "ColumnFunction",
                                    } }))));
                    }
                }
                case core_1.Specification.MappingType.expressionScale:
                    {
                        var scaleMapping_2 = mapping;
                        var table = mapping ? scaleMapping_2.table : options.table;
                        var builderProps = getMenuProps.bind(this)(parent, attribute, options);
                        var mainMenuItems = this.director.buildFieldsMenu(builderProps.onClick, builderProps.defaultValue, parent.store, this, attribute, table, options.acceptKinds);
                        var menuRender = this.director.getMenuRender();
                        return (React.createElement(React.Fragment, null,
                            this.props.options.label ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, this.props.options.label)) : null,
                            React.createElement(fluentui_customized_components_1.FluentRowLayout, null,
                                React.createElement(fluentui_customized_components_1.FluentActionButton, { style: {
                                        flex: 1,
                                        marginRight: "2px",
                                    } },
                                    React.createElement(react_1.ActionButton, { elementRef: function (e) { return (_this.mappingButton = e); }, styles: {
                                            menuIcon: __assign({ display: "none !important" }, fluentui_customized_components_1.defultComponentsHeight),
                                            root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                                        }, title: strings_1.strings.mappingEditor.keyColumnExpression, 
                                        // menuProps={{
                                        //   items: mainMenuItems,
                                        //   onRenderMenuList: menuRender,
                                        //   onMenuOpened: () => {
                                        //     const currentMapping = parent.getAttributeMapping(
                                        //       attribute
                                        //     );
                                        //     FluentMappingEditor.openEditor(
                                        //       (currentMapping as Specification.ScaleValueExpressionMapping)
                                        //         ?.expression,
                                        //       false,
                                        //       this.mappingButton
                                        //     );
                                        //   },
                                        // }}
                                        text: scaleMapping_2.expression, iconProps: {
                                            iconName: "ColumnFunction",
                                        }, onMenuClick: function (event) {
                                            if (scaleMapping_2.expression.startsWith("get")) {
                                                event.preventDefault();
                                                _this.changeDataFieldValueSelectionState();
                                            }
                                        } })),
                                React.createElement(fluentui_customized_components_1.FluentActionButton, { style: {
                                        flex: 1,
                                    } },
                                    React.createElement(react_1.ActionButton, { elementRef: function (e) { return (_this.mappingButton = e); }, styles: {
                                            menuIcon: __assign({ display: "none !important" }, fluentui_customized_components_1.defultComponentsHeight),
                                            root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                                        }, title: strings_1.strings.mappingEditor.bindData, menuProps: {
                                            items: mainMenuItems,
                                            onRenderMenuList: menuRender,
                                            onMenuOpened: function () {
                                                var _a;
                                                var currentMapping = parent.getAttributeMapping(attribute);
                                                FluentMappingEditor.openEditor((_a = currentMapping) === null || _a === void 0 ? void 0 : _a.valueExpression, false, _this.mappingButton);
                                            },
                                        }, text: scaleMapping_2.valueExpression, iconProps: {
                                            iconName: "ColumnFunction",
                                        }, onMenuClick: function (event) {
                                            if (scaleMapping_2.expression.startsWith("get")) {
                                                event.preventDefault();
                                                _this.changeDataFieldValueSelectionState();
                                            }
                                        } })))));
                    }
                    break;
                default: {
                    return React.createElement("span", null, "(...)");
                }
            }
        }
    };
    FluentMappingEditor.prototype.render = function () {
        var _this = this;
        var parent = this.props.parent;
        var attribute = this.props.attribute;
        var options = this.props.options;
        var currentMapping = parent.getAttributeMapping(attribute);
        // If there is a mapping, also not having default or using auto
        var shouldShowBindData = parent.onMapDataHandler != null;
        var isDataMapping = currentMapping != null &&
            (currentMapping.type == "scale" || currentMapping.type == "value");
        var valueIndex = currentMapping && currentMapping.valueIndex;
        if (this.props.options.openMapping) {
            setTimeout(function () {
                var _a;
                FluentMappingEditor.openEditor((_a = currentMapping) === null || _a === void 0 ? void 0 : _a.expression, true, _this.mappingButton);
            }, 0);
        }
        var table = currentMapping
            ? currentMapping.table
            : options.table;
        var builderProps = getMenuProps.bind(this)(parent, attribute, options);
        var mainMenuItems = this.director.buildFieldsMenu(builderProps.onClick, builderProps.defaultValue, parent.store, this, attribute, table, options.acceptKinds);
        var menuRender = this.director.getMenuRender();
        var acceptTables = utils_1.getDropzoneAcceptTables(this.props.parent, options.acceptLinksTable);
        return (React.createElement("div", { ref: function (e) { return (_this.noneLabel = e); }, key: attribute },
            React.createElement(types_1.DropZoneView, { filter: function (data) {
                    var _a;
                    if (acceptTables.length > 0 &&
                        !acceptTables.includes((_a = data.table) === null || _a === void 0 ? void 0 : _a.name)) {
                        return false;
                    }
                    if (!shouldShowBindData) {
                        return false;
                    }
                    if (data instanceof actions_1.DragData.DataExpression) {
                        return common_1.isKindAcceptable(data.metadata.kind, options.acceptKinds);
                    }
                    else {
                        return false;
                    }
                }, onDrop: function (data, point, modifiers) {
                    if (!options.hints) {
                        options.hints = {};
                    }
                    options.hints.newScale = modifiers.shiftKey;
                    options.hints.scaleID = data.scaleID;
                    var parsedExpression = core_1.Expression.parse(data.expression);
                    if (data.allowSelectValue && parsedExpression.name !== "get") {
                        data.expression = "get(" + data.expression + ", 0)";
                    }
                    // because original mapping allowed it
                    if (parsedExpression.name === "get") {
                        data.allowSelectValue = true;
                    }
                    _this.mapData(data, __assign(__assign({}, options.hints), { allowSelectValue: data.allowSelectValue }));
                }, className: "charticulator__widget-control-mapping-editor" }, parent.styledHorizontal({
                alignItems: "start",
            }, [1, 0], this.renderCurrentAttributeMapping(), React.createElement("span", null,
                isDataMapping ? (React.createElement(fluentui_customized_components_1.FluentButton, null,
                    React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "EraseTool",
                        }, styles: {
                            root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                        }, checked: false, title: strings_1.strings.mappingEditor.remove, onClick: function () {
                            if (parent.getAttributeMapping(attribute)) {
                                _this.clearMapping();
                            }
                            _this.setState(__assign(__assign({}, _this.state), { showNoneAsValue: false }));
                        } }))) : null,
                (valueIndex === undefined || valueIndex === null) &&
                    shouldShowBindData ? (React.createElement(React.Fragment, null,
                    React.createElement(fluentui_customized_components_1.FluentButton, null,
                        React.createElement(react_1.DefaultButton, { elementRef: function (e) { return (_this.mappingButton = e); }, iconProps: {
                                iconName: "Link",
                            }, styles: {
                                menuIcon: {
                                    display: "none !important",
                                },
                                root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                            }, title: strings_1.strings.mappingEditor.bindData, checked: isDataMapping, menuProps: {
                                items: mainMenuItems,
                                onRenderMenuList: menuRender,
                            } })))) : null,
                valueIndex !== undefined && valueIndex !== null ? (React.createElement(fluentui_customized_components_1.FluentButton, null,
                    React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "Link",
                        }, id: "dataFieldValueSelection", styles: {
                            root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                        }, title: strings_1.strings.mappingEditor.bindDataValue, elementRef: function (e) { return (_this.mappingButton = e); }, onClick: function () {
                            _this.changeDataFieldValueSelectionState();
                        }, checked: isDataMapping }))) : null,
                this.openDataFieldValueSelection())))));
    };
    FluentMappingEditor.menuKeyClick = function (derivedExpression) {
        setTimeout(function () {
            var aggContainer = document.querySelector("body :last-child.ms-Layer");
            var button = aggContainer === null || aggContainer === void 0 ? void 0 : aggContainer.querySelector("button.ms-ContextualMenu-splitMenu");
            if (button == null) {
                var derColumnsContainer = document.querySelector("body :last-child.ms-Layer");
                var derColumnsContainerXpath = "//ul//span[text()=\"" + derivedExpression + "\"]";
                var derMenuItem_1 = document.evaluate(derColumnsContainerXpath, derColumnsContainer, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                setTimeout(function () {
                    derMenuItem_1 === null || derMenuItem_1 === void 0 ? void 0 : derMenuItem_1.click();
                    setTimeout(function () {
                        var aggContainer = document.querySelector("body :last-child.ms-Layer");
                        var splitButton = aggContainer === null || aggContainer === void 0 ? void 0 : aggContainer.querySelector("button.ms-ContextualMenu-splitMenu");
                        splitButton === null || splitButton === void 0 ? void 0 : splitButton.click();
                    }, 100);
                }, 100);
            }
            else {
                button === null || button === void 0 ? void 0 : button.click();
            }
        }, 100);
    };
    FluentMappingEditor.openEditor = function (expressionString, clickOnButton, mappingButton) {
        setTimeout(function () {
            if (clickOnButton) {
                mappingButton === null || mappingButton === void 0 ? void 0 : mappingButton.click();
            }
            setTimeout(function () {
                var _a;
                var expression = null;
                var expressionAggregation = null;
                var derivedExpression = null;
                if (expressionString != null) {
                    var parsed = core_1.Expression.parse(expressionString);
                    if (parsed instanceof core_1.Expression.FunctionCall) {
                        expression = parsed.args[0].toString();
                        expressionAggregation = parsed.name;
                        //dataFieldValueSelection
                        if (expressionAggregation.startsWith("get")) {
                            return;
                        }
                        //derived columns
                        if (expression.startsWith("date.")) {
                            derivedExpression = (_a = common_1.type2DerivedColumns.date.find(function (item) {
                                return expression.startsWith(item.function);
                            })) === null || _a === void 0 ? void 0 : _a.displayName;
                        }
                    }
                    expression = expression === null || expression === void 0 ? void 0 : expression.split("`").join("");
                    try {
                        var aggContainer = document.querySelector("body :last-child.ms-Layer");
                        var xpath = "//ul//span[contains(text(), \"" + expression + "\")]";
                        var menuItem_1 = document.evaluate(xpath, aggContainer, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (menuItem_1 == null) {
                            var derSubXpath = "//ul//span[contains(text(), \"" + derivedExpression + "\")]";
                            var derElement_1 = document.evaluate(derSubXpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            setTimeout(function () {
                                derElement_1 === null || derElement_1 === void 0 ? void 0 : derElement_1.click();
                                FluentMappingEditor.menuKeyClick(derivedExpression);
                            });
                        }
                        else {
                            setTimeout(function () {
                                menuItem_1 === null || menuItem_1 === void 0 ? void 0 : menuItem_1.click();
                                FluentMappingEditor.menuKeyClick(derivedExpression);
                            }, 0);
                        }
                    }
                    catch (e) {
                        console.log(e);
                    }
                }
            }, 0);
        });
    };
    return FluentMappingEditor;
}(React.Component));
exports.FluentMappingEditor = FluentMappingEditor;
var DataMappAndScaleEditor = /** @class */ (function (_super) {
    __extends(DataMappAndScaleEditor, _super);
    function DataMappAndScaleEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            currentMapping: _this.props.defaultMapping,
        };
        return _this;
    }
    DataMappAndScaleEditor.prototype.componentDidMount = function () {
        var _this = this;
        this.tokens = [
            this.props.parent.updateEvents.addListener("update", function () {
                _this.setState({
                    currentMapping: _this.props.parent.props.parent.getAttributeMapping(_this.props.attribute),
                });
            }),
        ];
    };
    DataMappAndScaleEditor.prototype.componentWillUnmount = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.tokens), _c = _b.next(); !_c.done; _c = _b.next()) {
                var t = _c.value;
                t.remove();
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    DataMappAndScaleEditor.prototype.renderScaleEditor = function () {
        var mapping = this.state.currentMapping;
        if (mapping && mapping.type == "scale") {
            var scaleMapping = mapping;
            if (scaleMapping.scale) {
                var scaleObject = core_1.getById(this.store.chart.scales, scaleMapping.scale);
                return (React.createElement(scale_editor_1.ScaleEditor, { scale: scaleObject, scaleMapping: scaleMapping, store: this.store, plotSegment: this.props.plotSegment }));
            }
        }
        return null;
    };
    DataMappAndScaleEditor.prototype.renderDataPicker = function () {
        var _this = this;
        var options = this.props.options;
        var currentExpression = null;
        var mapping = this.state.currentMapping;
        if (mapping != null && mapping.type == "scale") {
            currentExpression = mapping.expression;
        }
        return (React.createElement("div", null,
            React.createElement(fluent_ui_data_field_selector_1.DataFieldSelector, { table: mapping ? mapping.table : options.table, datasetStore: this.store, kinds: options.acceptKinds, useAggregation: true, defaultValue: currentExpression
                    ? { table: options.table, expression: currentExpression }
                    : null, nullDescription: strings_1.strings.core.none, nullNotHighlightable: true, onChange: function (value) {
                    if (value != null) {
                        _this.props.parent.mapData(new actions_1.DragData.DataExpression(_this.store.getTable(value.table), value.expression, value.type, value.metadata, value.rawExpression), options.hints);
                    }
                    else {
                        _this.props.parent.clearMapping();
                        _this.props.onClose();
                    }
                } })));
    };
    DataMappAndScaleEditor.prototype.render = function () {
        var scaleElement = this.renderScaleEditor();
        if (scaleElement) {
            return (React.createElement("div", { className: "charticulator__data-mapping-and-scale-editor" },
                React.createElement("div", { className: this.props.alignLeft ? "el-scale-editor-left" : "el-scale-editor" }, scaleElement),
                React.createElement("div", { className: "el-data-picker" }, this.renderDataPicker())));
        }
        else {
            return (React.createElement("div", { className: "charticulator__data-mapping-and-scale-editor" },
                React.createElement("div", { className: "el-data-picker" }, this.renderDataPicker())));
        }
    };
    return DataMappAndScaleEditor;
}(context_component_1.ContextedComponent));
exports.DataMappAndScaleEditor = DataMappAndScaleEditor;
function parentOfType(p, typeSought) {
    while (p) {
        if (core_1.Prototypes.isType(p.object.classID, typeSought)) {
            return p;
        }
        p = p.parent;
    }
}
exports.parentOfType = parentOfType;
function getMenuProps(parent, attribute, options) {
    var _this = this;
    var _a;
    var currentMapping = parent.getAttributeMapping(attribute);
    var table = currentMapping ? currentMapping.table : options.table;
    var onClick = function (value) {
        if (value != null) {
            _this.mapData(new actions_1.DragData.DataExpression(_this.props.store.getTable(value.table), value.expression, value.type, value.metadata, value.rawExpression), options.hints);
        }
        else {
            _this.clearMapping();
        }
    };
    var mapping = parent.getAttributeMapping(attribute);
    var currentExpression = null;
    if (mapping != null) {
        if (mapping.type == specification_1.MappingType.text) {
            currentExpression = mapping.textExpression;
        }
        if (mapping.type == specification_1.MappingType.scale) {
            currentExpression = mapping.expression;
        }
    }
    var defaultValue = currentExpression
        ? {
            table: (_a = options === null || options === void 0 ? void 0 : options.table) !== null && _a !== void 0 ? _a : table,
            expression: currentExpression,
            type: mapping === null || mapping === void 0 ? void 0 : mapping.type,
        }
        : null;
    return {
        onClick: onClick,
        defaultValue: defaultValue,
    };
}
//# sourceMappingURL=fluent_mapping_editor.js.map