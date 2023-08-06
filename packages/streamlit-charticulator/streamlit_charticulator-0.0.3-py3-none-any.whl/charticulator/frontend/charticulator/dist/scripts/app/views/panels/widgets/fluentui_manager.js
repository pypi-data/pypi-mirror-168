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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
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
exports.DetailsButtonInner = exports.FluentDetailsButton = exports.DropZoneView = exports.FluentUIWidgetManager = void 0;
var React = require("react");
var ReactDOM = require("react-dom");
var globals = require("../../../globals");
var R = require("../../../resources");
var core_1 = require("../../../../core");
var actions_1 = require("../../../actions");
var components_1 = require("../../../components");
var icons_1 = require("../../../components/icons");
var controllers_1 = require("../../../controllers");
var index_1 = require("../../../utils/index");
var object_list_editor_1 = require("../object_list_editor");
var controls_1 = require("./controls");
var groupby_editor_1 = require("./groupby_editor");
var container_1 = require("../../../../container");
var expression_1 = require("../../../../core/expression");
var datetime_1 = require("../../../../core/dataset/datetime");
var scale_value_selector_1 = require("../scale_value_selector");
var react_1 = require("@fluentui/react");
var fluent_mapping_editor_1 = require("./fluent_mapping_editor");
var fluentui_input_color_1 = require("./controls/fluentui_input_color");
var fluentui_input_expression_1 = require("./controls/fluentui_input_expression");
var fluentui_customized_components_1 = require("./controls/fluentui_customized_components");
var fluentui_input_number_1 = require("./controls/fluentui_input_number");
var merge_styles_1 = require("@fluentui/merge-styles");
var strings_1 = require("../../../../strings");
var fluentui_image_1 = require("./controls/fluentui_image");
var fluentui_image_2_1 = require("./controls/fluentui_image_2");
var data_field_binding_builder_1 = require("../../dataset/data_field_binding_builder");
var fluentui_input_format_1 = require("./controls/fluentui_input_format");
var collapsiblePanel_1 = require("./controls/collapsiblePanel");
var actions_2 = require("../../../actions/actions");
var fluentui_filter_1 = require("./fluentui_filter");
var observer_1 = require("./observer");
var fluent_ui_gradient_picker_1 = require("../../../components/fluent_ui_gradient_picker");
var types_1 = require("../../../../core/specification/types");
var custom_collapsible_panel_1 = require("./controls/custom_collapsible_panel");
var fluentui_reorder_string_value_1 = require("./controls/fluentui_reorder_string_value");
var input_gradient_1 = require("./controls/input_gradient");
var styles_1 = require("./styles");
var utils_1 = require("./utils");
var app_store_1 = require("../../../stores/app_store");
var FluentUIWidgetManager = /** @class */ (function () {
    function FluentUIWidgetManager(store, objectClass, ignoreSearch) {
        if (ignoreSearch === void 0) { ignoreSearch = false; }
        this.store = store;
        this.objectClass = objectClass;
        this.ignoreSearch = ignoreSearch;
        this.director = new data_field_binding_builder_1.Director();
        this.director.setBuilder(new data_field_binding_builder_1.MenuItemBuilder());
        this.eventManager = new observer_1.EventManager();
        this.eventListener = new observer_1.UIManagerListener(this);
        this.eventManager.subscribe(observer_1.EventType.UPDATE_FIELD, this.eventListener);
    }
    FluentUIWidgetManager.prototype.getKeyFromProperty = function (property) {
        var _a;
        return (property === null || property === void 0 ? void 0 : property.property) + "-" + ((_a = property === null || property === void 0 ? void 0 : property.field) === null || _a === void 0 ? void 0 : _a.toString());
    };
    FluentUIWidgetManager.prototype.searchInput = function (options) {
        var _this = this;
        var _a, _b;
        if (options === void 0) { options = {}; }
        return (React.createElement(react_1.TextField, { styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { field: __assign(__assign({}, fluentui_customized_components_1.defaultStyle.field), { height: null, padding: "unset" }), root: {
                    marginBottom: 5,
                    marginTop: 5,
                }, prefix: {
                    backgroundColor: "unset",
                } }), placeholder: options.placeholder, label: options.label, disabled: options.disabled, onRenderLabel: fluentui_customized_components_1.labelRender, onChange: function (event, value) {
                var newValue = "";
                if ((value === null || value === void 0 ? void 0 : value.length) > 0) {
                    newValue = value.trim();
                }
                _this.store.dispatcher.dispatch(new actions_1.Actions.SearchUpdated(newValue));
            }, type: "text", underlined: (_a = options.underline) !== null && _a !== void 0 ? _a : false, borderless: (_b = options.borderless) !== null && _b !== void 0 ? _b : false, style: options.styles, prefix: "", onRenderPrefix: function () {
                return React.createElement(react_1.FontIcon, { "aria-label": "Search", iconName: "Search" });
            }, autoComplete: "off", defaultValue: this.store.searchString }));
    };
    FluentUIWidgetManager.prototype.searchWrapper = function (options) {
        var widgets = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            widgets[_i - 1] = arguments[_i];
        }
        var searchStings = options.searchPattern;
        var searchString = this.store.searchString;
        if ((searchString === null || searchString === void 0 ? void 0 : searchString.length) != 0 && searchStings.length >= 0) {
            if (!searchStings.some(function (value) {
                return value && (value === null || value === void 0 ? void 0 : value.toUpperCase().includes(searchString === null || searchString === void 0 ? void 0 : searchString.toUpperCase()));
            })) {
                return;
            }
        }
        return (React.createElement(React.Fragment, null, widgets.map(function (x, id) { return (React.createElement(React.Fragment, { key: "search-" + id + "-" + core_1.getRandomNumber() }, Array.isArray(x)
            ? x.map(function (w) { return (React.createElement(React.Fragment, { key: "search-" + id + "-" + core_1.getRandomNumber() }, w)); })
            : x)); })));
    };
    FluentUIWidgetManager.prototype.mappingEditor = function (name, attribute, options) {
        var _this = this;
        var _a;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([name], searchSections))) {
            return;
        }
        var objectClass = this.objectClass;
        var info = objectClass.attributes[attribute];
        if (options.defaultValue == null) {
            options.defaultValue = info.defaultValue;
        }
        options.acceptLinksTable = (_a = options.acceptLinksTable) !== null && _a !== void 0 ? _a : false;
        var openMapping = options.openMapping || attribute === this.store.currentAttributeFocus;
        if (openMapping) {
            setTimeout(function () {
                document
                    .querySelectorAll(".ms-GroupHeader-expand")
                    .forEach(function (expand) {
                    if (expand.querySelector("i").classList.contains("is-collapsed")) {
                        expand.click();
                    }
                });
                _this.store.dispatcher.dispatch(new actions_1.Actions.FocusToMarkAttribute(null));
            }, 0);
        }
        return (React.createElement(fluent_mapping_editor_1.FluentMappingEditor, { key: name + attribute, store: this.store, parent: this, attribute: attribute, type: info.type, options: __assign(__assign({}, options), { label: name, openMapping: openMapping }) }));
    };
    FluentUIWidgetManager.prototype.getAttributeMapping = function (attribute) {
        return this.objectClass.object.mappings[attribute];
    };
    FluentUIWidgetManager.prototype.getPropertyValue = function (property) {
        var prop = this.objectClass.object.properties[property.property];
        var value;
        if (property.field != null) {
            value = core_1.getField(prop, property.field);
        }
        else {
            value = prop;
        }
        return value;
    };
    FluentUIWidgetManager.prototype.getDateFormat = function (property) {
        try {
            var prop = this.objectClass.object.properties[property.property];
            var expressionString = prop.expression;
            var expression = expression_1.TextExpression.Parse("${" + expressionString + "}");
            // const table = this.store.chartManager.dataflow.getTable((this.objectClass.object as any).table);
            var functionCallpart = expression.parts.find(function (part) {
                if (part.expression instanceof expression_1.FunctionCall) {
                    return part.expression.args.find(function (arg) { return arg instanceof expression_1.Variable; });
                }
            }).expression;
            if (functionCallpart) {
                var variable = functionCallpart.args.find(function (arg) { return arg instanceof expression_1.Variable; });
                var columnName_1 = variable.name;
                var tableName_1 = this.objectClass.object.table;
                var table = this.store.dataset.tables.find(function (table) { return table.name === tableName_1; });
                var column = table.columns.find(function (column) { return column.name === columnName_1; });
                if (column.metadata.format) {
                    return column.metadata.format;
                }
                var rawColumnName = column.metadata.rawColumnName;
                if (rawColumnName &&
                    (column.metadata.kind === core_1.Specification.DataKind.Temporal ||
                        column.type === core_1.Specification.DataType.Boolean)) {
                    var value = (table.rows[0][rawColumnName] || core_1.refineColumnName(rawColumnName)).toString();
                    return datetime_1.getDateFormat(value);
                }
            }
        }
        catch (ex) {
            console.warn(ex);
            return null;
        }
        return null;
    };
    FluentUIWidgetManager.prototype.emitSetProperty = function (property, value) {
        new actions_1.Actions.SetObjectProperty(this.objectClass.object, property.property, property.field, value, property.noUpdateState, property.noComputeLayout).dispatch(this.store.dispatcher);
    };
    FluentUIWidgetManager.prototype.emitUpdateProperty = function (event, property, prevKey, newKey) {
        event.preventDefault();
        event.stopPropagation();
        var validatedKey = newKey.length === 0 ? " " : newKey;
        var oldPropertyValue = this.getPropertyValue(property);
        var changedValue = oldPropertyValue;
        var newValue = Object.keys(changedValue).reduce(function (obj, key) {
            obj[key === prevKey ? validatedKey : key] = oldPropertyValue[key];
            return obj;
        }, {});
        new actions_1.Actions.SetObjectProperty(this.objectClass.object, property.property, property.field, newValue, property.noUpdateState, property.noComputeLayout).dispatch(this.store.dispatcher);
    };
    FluentUIWidgetManager.prototype.inputFormat = function (property, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        return (React.createElement(fluentui_input_format_1.FluentInputFormat, { label: options.label, defaultValue: this.getPropertyValue(property), validate: function (value) {
                if (value && value.trim() !== "") {
                    try {
                        container_1.getFormat()(value === null || value === void 0 ? void 0 : value.replace(container_1.tickFormatParserExpression(), "$1"));
                        return {
                            pass: true,
                            formatted: value,
                        };
                    }
                    catch (ex) {
                        try {
                            core_1.applyDateFormat(new Date(), value === null || value === void 0 ? void 0 : value.replace(container_1.tickFormatParserExpression(), "$1"));
                            return {
                                pass: true,
                                formatted: value,
                            };
                        }
                        catch (ex) {
                            return {
                                pass: false,
                                error: strings_1.strings.objects.invalidFormat,
                            };
                        }
                    }
                }
                return {
                    pass: true,
                };
            }, placeholder: options.blank || strings_1.strings.core.none, onEnter: function (value) {
                if (!value || value.trim() == "") {
                    _this.emitSetProperty(property, null);
                }
                else {
                    _this.emitSetProperty(property, value);
                }
                return true;
            }, allowNull: options.allowNull }));
    };
    FluentUIWidgetManager.prototype.inputNumber = function (property, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var value = this.getPropertyValue(property);
        return (React.createElement(fluentui_input_number_1.FluentInputNumber, __assign({}, options, { key: this.getKeyFromProperty(property), defaultValue: value, placeholder: options.placeholder, onEnter: function (value) {
                var _a, _b, _c, _d, _e;
                if (value == null) {
                    _this.emitSetProperty(property, null);
                }
                else {
                    _this.emitSetProperty(property, value);
                }
                if ((_a = options.observerConfig) === null || _a === void 0 ? void 0 : _a.isObserver) {
                    if (((_b = options.observerConfig) === null || _b === void 0 ? void 0 : _b.properties) instanceof Array) {
                        (_c = options.observerConfig) === null || _c === void 0 ? void 0 : _c.properties.forEach(function (property) {
                            var _a;
                            return _this.eventManager.notify(observer_1.EventType.UPDATE_FIELD, property, (_a = options.observerConfig) === null || _a === void 0 ? void 0 : _a.value);
                        });
                    }
                    else {
                        _this.eventManager.notify(observer_1.EventType.UPDATE_FIELD, (_d = options.observerConfig) === null || _d === void 0 ? void 0 : _d.properties, (_e = options.observerConfig) === null || _e === void 0 ? void 0 : _e.value);
                    }
                }
                return true;
            } })));
    };
    FluentUIWidgetManager.prototype.inputDate = function (property, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var value = this.getPropertyValue(property);
        var format = this.getDateFormat(property);
        return (React.createElement(fluentui_customized_components_1.FluentDatePickerWrapper, null,
            React.createElement(react_1.DatePicker, { key: this.getKeyFromProperty(property), firstDayOfWeek: react_1.DayOfWeek.Sunday, placeholder: options.placeholder, ariaLabel: options.placeholder, defaultValue: format, value: new Date(value), label: options.label, onSelectDate: function (value) {
                    if (value == null) {
                        _this.emitSetProperty(property, null);
                        return true;
                    }
                    else {
                        _this.emitSetProperty(property, value);
                        return true;
                    }
                } })));
    };
    FluentUIWidgetManager.prototype.inputText = function (property, options) {
        var _this = this;
        var _a, _b, _c;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var prevKey = (_a = options.value) !== null && _a !== void 0 ? _a : "";
        return (React.createElement(react_1.TextField, { styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { field: __assign(__assign({}, fluentui_customized_components_1.defaultStyle.field), { height: null }) }), key: this.getKeyFromProperty(property), value: options.value
                ? options.value
                : this.getPropertyValue(property), placeholder: options.placeholder, label: options.label, disabled: options.disabled, onRenderLabel: fluentui_customized_components_1.labelRender, onChange: function (event, value) {
                options.updateProperty
                    ? _this.emitUpdateProperty(event, property, prevKey, value)
                    : _this.emitSetProperty(property, value);
                prevKey = value;
                if (options.emitMappingAction) {
                    new actions_1.Actions.SetCurrentMappingAttribute(value).dispatch(_this.store.dispatcher);
                }
            }, onClick: function () {
                if (options.emitMappingAction) {
                    new actions_1.Actions.SetCurrentMappingAttribute(prevKey).dispatch(_this.store.dispatcher);
                }
            }, type: "text", underlined: (_b = options.underline) !== null && _b !== void 0 ? _b : false, borderless: (_c = options.borderless) !== null && _c !== void 0 ? _c : false, style: options.styles }));
    };
    FluentUIWidgetManager.prototype.inputFontFamily = function (property, options) {
        var _this = this;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        return (React.createElement(controls_1.FluentComboBoxFontFamily, { key: this.getKeyFromProperty(property), label: options.label, defaultValue: this.getPropertyValue(property), onEnter: function (value) {
                _this.emitSetProperty(property, value);
                return true;
            } }));
    };
    FluentUIWidgetManager.prototype.inputComboBox = function (property, options) {
        var _this = this;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        return (React.createElement(react_1.ComboBox, { styles: fluentui_customized_components_1.defaultStyle, key: this.getKeyFromProperty(property), selectedKey: this.getPropertyValue(property), label: options.label, autoComplete: "on", options: options.defaultRange.map(function (rangeValue) {
                return {
                    key: rangeValue,
                    text: rangeValue,
                };
            }), onChange: function (event, value) {
                _this.emitSetProperty(property, value.key);
                return true;
            } }));
    };
    FluentUIWidgetManager.prototype.inputSelect = function (property, options) {
        var _this = this;
        var _a;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var theme = react_1.getTheme();
        var isLocalIcons = (_a = options.isLocalIcons) !== null && _a !== void 0 ? _a : false;
        if (options.type == "dropdown") {
            return (React.createElement(react_1.Dropdown, { key: this.getKeyFromProperty(property) + "-" + options.label + "-" + options.type, selectedKey: this.getPropertyValue(property), defaultValue: this.getPropertyValue(property), label: options.label, onRenderLabel: fluentui_customized_components_1.labelRender, onRenderOption: styles_1.onRenderOption, onRenderTitle: styles_1.onRenderTitle, options: options.options.map(function (rangeValue, index) {
                    var _a;
                    return {
                        key: rangeValue,
                        text: options.labels[index],
                        data: {
                            icon: (_a = options.icons) === null || _a === void 0 ? void 0 : _a[index],
                            iconStyles: {
                                stroke: "gray",
                            },
                            isLocalIcons: isLocalIcons,
                        },
                    };
                }), onChange: function (event, value) {
                    _this.emitSetProperty(property, value.key);
                    _this.defaultNotification(options.observerConfig);
                    if (options.onChange) {
                        options.onChange(value);
                    }
                    return true;
                }, styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), styles_1.dropdownStyles(options)) }));
        }
        else {
            return (React.createElement(React.Fragment, { key: this.getKeyFromProperty(property) + "-" + options.label + "-" + options.type },
                options.label && options.label.length > 0 ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, options.label)) : null,
                options.options.map(function (option, index) {
                    return (React.createElement(react_1.IconButton, { key: _this.getKeyFromProperty(property) + "-" + options.label + "-" + options.type + "-" + index, iconProps: {
                            iconName: options.icons[index],
                        }, style: {
                            stroke: theme.palette.themePrimary + " !important",
                        }, styles: {
                            label: null,
                            root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                        }, title: options.labels[index], checked: option === _this.getPropertyValue(property), onClick: function () {
                            _this.emitSetProperty(property, option);
                        } }));
                })));
        }
    };
    FluentUIWidgetManager.prototype.inputBoolean = function (properties, options) {
        var _this = this;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([
                options.label,
                options.headerLabel
            ], searchSections))) {
            return;
        }
        var property = properties instanceof Array ? properties[0] : properties;
        switch (options.type) {
            case "checkbox-fill-width":
            case "checkbox": {
                return (React.createElement(React.Fragment, { key: this.getKeyFromProperty(property) },
                    options.headerLabel ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, options.headerLabel)) : null,
                    React.createElement(fluentui_customized_components_1.FluentCheckbox, { style: options.styles },
                        React.createElement(react_1.Checkbox, { checked: this.getPropertyValue(property), label: options.label, styles: __assign({ label: fluentui_customized_components_1.defaultLabelStyle, root: __assign({}, fluentui_customized_components_1.defultComponentsHeight) }, options.checkBoxStyles), onChange: function (ev, v) {
                                if (properties instanceof Array) {
                                    properties.forEach(function (property) {
                                        return _this.emitSetProperty(property, v);
                                    });
                                }
                                else {
                                    _this.emitSetProperty(property, v);
                                }
                                _this.defaultNotification(options.observerConfig);
                                if (options.onChange && !v) {
                                    options.onChange(v);
                                }
                            } }))));
            }
            case "highlight": {
                return (React.createElement(react_1.IconButton, { key: this.getKeyFromProperty(property), iconProps: {
                        iconName: options.icon,
                    }, title: options.label, label: options.label, styles: __assign(__assign({}, fluentui_customized_components_1.defultBindButtonSize), { label: fluentui_customized_components_1.defaultLabelStyle, root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize) }), text: options.label, ariaLabel: options.label, checked: this.getPropertyValue(property), onClick: function () {
                        _this.defaultNotification(options.observerConfig);
                        var v = _this.getPropertyValue(property);
                        _this.emitSetProperty(property, !v);
                    } }));
            }
        }
    };
    FluentUIWidgetManager.prototype.defaultNotification = function (observerConfig) {
        var _this = this;
        if (observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.isObserver) {
            if ((observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.properties) instanceof Array) {
                observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.properties.forEach(function (property) {
                    return _this.eventManager.notify(observer_1.EventType.UPDATE_FIELD, property, observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.value);
                });
            }
            else {
                this.eventManager.notify(observer_1.EventType.UPDATE_FIELD, observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.properties, observerConfig === null || observerConfig === void 0 ? void 0 : observerConfig.value);
            }
        }
    };
    FluentUIWidgetManager.prototype.inputExpression = function (property, options) {
        var _this = this;
        var _a;
        if (options === void 0) { options = {}; }
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var value = this.getPropertyValue(property);
        var inputExpression = (React.createElement(fluentui_input_expression_1.FluentInputExpression, { key: this.getKeyFromProperty(property), label: options.label, value: value, defaultValue: value, validate: function (value) {
                if (value && value.trim() !== "") {
                    return _this.store.verifyUserExpressionWithTable(value, options.table);
                }
                return {
                    pass: true,
                };
            }, placeholder: (_a = options.placeholder) !== null && _a !== void 0 ? _a : strings_1.strings.core.none, onEnter: function (value) {
                if (!value || value.trim() == "") {
                    _this.emitSetProperty(property, null);
                }
                else {
                    _this.emitSetProperty(property, value);
                    _this.store.updateDataAxes();
                    _this.store.updatePlotSegments();
                }
                return true;
            }, allowNull: options.allowNull }));
        if (options.dropzone) {
            var className = options.noLineHeight
                ? "charticulator__widget-section-header-no-height charticulator__widget-section-header-dropzone"
                : "charticulator__widget-section-header charticulator__widget-section-header-dropzone";
            return (React.createElement(DropZoneView, { key: options.label, filter: function (data) { return data instanceof actions_1.DragData.DataExpression; }, onDrop: function (data) {
                    var _a, _b, _c, _d;
                    if (options.dropzone.type === "axis-data-binding") {
                        new actions_1.Actions.BindDataToAxis(_this.objectClass.object, options.dropzone.property, null, data, true).dispatch(_this.store.dispatcher);
                    }
                    else {
                        var newValue = data.expression;
                        try {
                            if ((_a = data.metadata) === null || _a === void 0 ? void 0 : _a.columnName) {
                                if (((_b = data.metadata) === null || _b === void 0 ? void 0 : _b.columnName.split(" ").length) > 1) {
                                    newValue = "`" + ((_c = data.metadata) === null || _c === void 0 ? void 0 : _c.columnName) + "`";
                                }
                                else {
                                    newValue = (_d = data.metadata) === null || _d === void 0 ? void 0 : _d.columnName;
                                }
                            }
                            else {
                                newValue = data.expression;
                            }
                            _this.emitSetProperty(property, newValue);
                        }
                        catch (ex) {
                            //put data.expression value
                            _this.emitSetProperty(property, newValue);
                        }
                    }
                }, className: className, draggingHint: function () {
                    var _a;
                    return (React.createElement("span", { className: "el-dropzone-hint" }, (_a = options.dropzone) === null || _a === void 0 ? void 0 : _a.prompt));
                } }, inputExpression));
        }
        else {
            return inputExpression;
        }
    };
    FluentUIWidgetManager.prototype.inputColor = function (property, options) {
        var _this = this;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([options.label], searchSections))) {
            return;
        }
        var color = this.getPropertyValue(property);
        return (React.createElement(fluentui_input_color_1.FluentInputColor, { key: this.getKeyFromProperty(property), label: options.label, store: this.store, defaultValue: color, allowNull: options.allowNull, noDefaultMargin: options.noDefaultMargin, labelKey: options.labelKey, onEnter: function (value) {
                _this.emitSetProperty(property, value);
                return true;
            }, width: options.width, underline: options.underline, pickerBeforeTextField: options.pickerBeforeTextField, styles: options.styles }));
    };
    FluentUIWidgetManager.prototype.inputColorGradient = function (property, inline) {
        var _this = this;
        if (inline === void 0) { inline = false; }
        //aAAAA
        var gradient = this.getPropertyValue(property);
        if (inline) {
            return (React.createElement("span", { className: "charticulator__widget-control-input-color-gradient-inline" },
                React.createElement(fluent_ui_gradient_picker_1.FluentUIGradientPicker, { key: this.getKeyFromProperty(property), defaultValue: gradient, onPick: function (value) {
                        _this.emitSetProperty(property, value);
                    } })));
        }
        else {
            return (React.createElement(input_gradient_1.InputColorGradient, { key: this.getKeyFromProperty(property), defaultValue: gradient, onEnter: function (value) {
                    _this.emitSetProperty(property, value);
                    return true;
                } }));
        }
    };
    FluentUIWidgetManager.prototype.inputImage = function (property) {
        var _this = this;
        return (React.createElement(fluentui_image_1.InputImage, { key: this.getKeyFromProperty(property), value: this.getPropertyValue(property), onChange: function (image) {
                _this.emitSetProperty(property, image);
                return true;
            } }));
    };
    FluentUIWidgetManager.prototype.inputImageProperty = function (property) {
        var _this = this;
        return (React.createElement(fluentui_image_2_1.InputImageProperty, { key: this.getKeyFromProperty(property), value: this.getPropertyValue(property), onChange: function (image) {
                _this.emitSetProperty(property, image);
                return true;
            } }));
    };
    FluentUIWidgetManager.prototype.clearButton = function (property, icon, isHeader, styles) {
        var _this = this;
        return (React.createElement(fluentui_customized_components_1.FluentButton, { key: this.getKeyFromProperty(property), marginTop: isHeader ? "0px" : null, style: styles },
            React.createElement(react_1.DefaultButton, { styles: {
                    root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                }, iconProps: {
                    iconName: icon || "EraseTool",
                }, onClick: function () {
                    _this.emitSetProperty(property, null);
                } })));
    };
    FluentUIWidgetManager.prototype.setButton = function (property, value, icon, text) {
        var _this = this;
        if (!this.shouldDrawComponent([text])) {
            return;
        }
        return (React.createElement(react_1.DefaultButton, { key: this.getKeyFromProperty(property), iconProps: {
                iconName: icon,
            }, text: text, onClick: function () {
                _this.emitSetProperty(property, value);
            } }));
    };
    FluentUIWidgetManager.prototype.scaleEditor = function (attribute, text) {
        var _this = this;
        if (!this.shouldDrawComponent([text])) {
            return;
        }
        var mappingButton = null;
        var objectClass = this.objectClass;
        var mapping = objectClass.object.mappings[attribute];
        var scaleObject = core_1.getById(this.store.chart.scales, mapping.scale);
        return (React.createElement(components_1.ButtonRaised, { key: attribute, ref: function (e) { return (mappingButton = ReactDOM.findDOMNode(e)); }, text: text, onClick: function () {
                globals.popupController.popupAt(function (context) {
                    return (React.createElement(controllers_1.PopupView, { context: context },
                        React.createElement(scale_value_selector_1.ScaleValueSelector, { scale: scaleObject, scaleMapping: mapping, store: _this.store })));
                }, { anchor: mappingButton });
            } }));
    };
    FluentUIWidgetManager.prototype.orderByWidget = function (property, options) {
        var _this = this;
        var onClick = function (value) {
            if (value != null) {
                _this.emitSetProperty(property, {
                    expression: value.expression,
                });
            }
            else {
                _this.emitSetProperty(property, null);
            }
        };
        var currentExpression = null;
        var currentSortBy = this.getPropertyValue(property);
        if (currentSortBy != null) {
            currentExpression = currentSortBy.expression;
        }
        var defaultValue = currentExpression
            ? { table: options.table, expression: currentExpression }
            : null;
        var menu = this.director.buildSectionHeaderFieldsMenu(onClick, defaultValue, this.store);
        var menuRender = this.director.getMenuRender();
        return (React.createElement(DropZoneView, { key: this.getKeyFromProperty(property), filter: function (data) { return data instanceof actions_1.DragData.DataExpression; }, onDrop: function (data) {
                _this.emitSetProperty(property, { expression: data.expression });
            }, className: "" },
            React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px" },
                React.createElement(react_1.IconButton, { styles: {
                        root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                        label: null,
                    }, key: property.property, checked: this.getPropertyValue(property) != null, iconProps: {
                        iconName: "SortLines",
                    }, menuProps: {
                        items: menu,
                        gapSpace: options.shiftCallout ? options.shiftCallout : 0,
                        onMenuOpened: function () {
                            fluent_mapping_editor_1.FluentMappingEditor.openEditor(currentExpression, false, null);
                        },
                        onRenderMenuList: menuRender,
                    } }))));
    };
    FluentUIWidgetManager.prototype.reorderWidget = function (property, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var container;
        return (React.createElement(fluentui_customized_components_1.FluentButton, { ref: function (e) { return (container = e); }, key: this.getKeyFromProperty(property), marginTop: "1px", paddingRight: "0px" },
            React.createElement(react_1.DefaultButton, { styles: {
                    root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight),
                }, iconProps: {
                    iconName: "SortLines",
                }, onClick: function () {
                    globals.popupController.popupAt(function (context) {
                        var items = options.items
                            ? options.items
                            : _this.getPropertyValue(property);
                        return (React.createElement(controllers_1.PopupView, { context: context },
                            React.createElement(fluentui_reorder_string_value_1.FluentUIReorderStringsValue, __assign({ items: items, onConfirm: function (items, customOrder, sortOrder) {
                                    _this.emitSetProperty(property, items);
                                    if (customOrder) {
                                        _this.emitSetProperty({
                                            property: property.property,
                                            field: "orderMode",
                                        }, types_1.OrderMode.order);
                                        _this.emitSetProperty({
                                            property: property.property,
                                            field: "order",
                                        }, items);
                                    }
                                    else {
                                        if (sortOrder) {
                                            _this.emitSetProperty({
                                                property: property.property,
                                                field: "orderMode",
                                            }, types_1.OrderMode.alphabetically);
                                        }
                                        else {
                                            _this.emitSetProperty({
                                                property: property.property,
                                                field: "orderMode",
                                            }, types_1.OrderMode.order);
                                            _this.emitSetProperty({
                                                property: property.property,
                                                field: "order",
                                            }, items);
                                        }
                                    }
                                    context.close();
                                }, onReset: function () {
                                    var axisDataBinding = __assign({}, _this.objectClass.object.properties[property.property]);
                                    axisDataBinding.table = _this.store.chartManager.getTable(_this.objectClass.object.table);
                                    axisDataBinding.metadata = {
                                        kind: axisDataBinding.dataKind,
                                        orderMode: "order",
                                    };
                                    var groupBy = _this.store.getGroupingExpression(_this.objectClass.object);
                                    var values = _this.store.chartManager.getGroupedExpressionVector(_this.objectClass.object.table, groupBy, axisDataBinding.expression);
                                    var categories = _this.store.getCategoriesForDataBinding(axisDataBinding.metadata, axisDataBinding.type, values).categories;
                                    return categories;
                                } }, options))));
                    }, { anchor: container });
                } })));
    };
    FluentUIWidgetManager.prototype.arrayWidget = function (property, renderItem, options) {
        var _this = this;
        if (options === void 0) { options = {
            allowDelete: true,
            allowReorder: true,
        }; }
        var items = this.getPropertyValue(property).slice();
        return (React.createElement("div", { className: "charticulator__widget-array-view", key: this.getKeyFromProperty(property) },
            React.createElement(object_list_editor_1.ReorderListView, { enabled: options.allowReorder, onReorder: function (dragIndex, dropIndex) {
                    object_list_editor_1.ReorderListView.ReorderArray(items, dragIndex, dropIndex);
                    _this.emitSetProperty(property, items);
                } }, items.map(function (item, index) {
                return (React.createElement("div", { key: index, className: "charticulator__widget-array-view-item" },
                    options.allowReorder ? (React.createElement("span", { className: "charticulator__widget-array-view-control charticulator__widget-array-view-order" },
                        React.createElement(react_1.FontIcon, { className: merge_styles_1.mergeStyles({
                                fontSize: "20px",
                                margin: "5px",
                            }), iconName: "CheckListText" }))) : null,
                    React.createElement("span", { className: "charticulator__widget-array-view-content" }, renderItem({
                        property: property.property,
                        field: property.field
                            ? property.field instanceof Array
                                ? __spread(property.field, [index]) : [property.field, index]
                            : index,
                    })),
                    options.allowDelete ? (React.createElement("span", { className: "charticulator__widget-array-view-control" },
                        React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px" },
                            React.createElement(react_1.DefaultButton, { styles: {
                                    root: {
                                        minWidth: "unset",
                                    },
                                }, iconProps: {
                                    iconName: "Delete",
                                }, onClick: function () {
                                    items.splice(index, 1);
                                    _this.emitSetProperty(property, items);
                                } })))) : null));
            }))));
    };
    FluentUIWidgetManager.prototype.dropTarget = function (options, widget) {
        var _this = this;
        return (React.createElement(DropZoneView, { key: this.getKeyFromProperty(options === null || options === void 0 ? void 0 : options.property) + options.label, filter: function (data) { return data instanceof actions_1.DragData.DataExpression; }, onDrop: function (data) {
                _this.emitSetProperty(options.property, {
                    expression: data.expression,
                });
            }, className: index_1.classNames("charticulator__widget-control-drop-target"), draggingHint: function () { return (React.createElement("span", { className: "el-dropzone-hint" }, options.label)); } }, widget));
    };
    // Label and text
    FluentUIWidgetManager.prototype.icon = function (icon) {
        return (React.createElement("span", { className: "charticulator__widget-label", key: icon },
            React.createElement(icons_1.SVGImageIcon, { url: R.getSVGIcon(icon) })));
    };
    FluentUIWidgetManager.prototype.label = function (title, options) {
        var searchSections = Array.isArray(options === null || options === void 0 ? void 0 : options.searchSection)
            ? options === null || options === void 0 ? void 0 : options.searchSection : [options === null || options === void 0 ? void 0 : options.searchSection];
        if (!(options === null || options === void 0 ? void 0 : options.ignoreSearch) && !this.shouldDrawComponent(searchSections)) {
            return;
        }
        return (React.createElement(fluentui_customized_components_1.FluentLabelHeader, { key: title, marginBottom: (options === null || options === void 0 ? void 0 : options.addMargins) ? "5px" : "0px", marginTop: (options === null || options === void 0 ? void 0 : options.addMargins) ? "5px" : "0px" },
            React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, title)));
    };
    FluentUIWidgetManager.prototype.text = function (title, align) {
        if (align === void 0) { align = "left"; }
        return (React.createElement("span", { className: "charticulator__widget-text", style: { textAlign: align }, key: title + align }, title));
    };
    FluentUIWidgetManager.prototype.sep = function () {
        return React.createElement("span", { className: "charticulator__widget-sep" });
    };
    // Layout elements
    FluentUIWidgetManager.prototype.sectionHeader = function (title, widget, options) {
        var _this = this;
        var _a;
        if (options === void 0) { options = {}; }
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([title], searchSections))) {
            return;
        }
        this.director.setBuilder(new data_field_binding_builder_1.MenuItemBuilder());
        if (options.dropzone && options.dropzone.type == "axis-data-binding") {
            var current = this.getPropertyValue({
                property: options.dropzone.property,
            });
            var onClick = function (value) {
                if (!value) {
                    _this.emitSetProperty({ property: options.dropzone.property }, null);
                }
                else {
                    var data = new actions_1.DragData.DataExpression(_this.store.getTable(value.table), value.expression, value.type, value.metadata, value.rawExpression);
                    new actions_1.Actions.BindDataToAxis(_this.objectClass.object, options.dropzone.property, null, data, false).dispatch(_this.store.dispatcher);
                }
            };
            var defaultValue = current && current.expression
                ? { table: null, expression: current.expression }
                : null;
            var menu = this.director.buildSectionHeaderFieldsMenu(onClick, defaultValue, this.store);
            var menuRender = this.director.getMenuRender();
            var className = options.noLineHeight
                ? "charticulator__widget-section-header-no-height charticulator__widget-section-header-dropzone"
                : "charticulator__widget-section-header charticulator__widget-section-header-dropzone";
            var acceptTables_1 = utils_1.getDropzoneAcceptTables(this, (_a = options.acceptLinksTable) !== null && _a !== void 0 ? _a : false);
            return (React.createElement(DropZoneView, { key: title, filter: function (data) {
                    var _a;
                    if (acceptTables_1.length > 0 &&
                        !acceptTables_1.includes((_a = data.table) === null || _a === void 0 ? void 0 : _a.name)) {
                        return false;
                    }
                    return data instanceof actions_1.DragData.DataExpression;
                }, onDrop: function (data) {
                    new actions_1.Actions.BindDataToAxis(_this.objectClass.object, options.dropzone.property, null, data, true).dispatch(_this.store.dispatcher);
                }, className: className, draggingHint: function () { return (React.createElement("span", { className: "el-dropzone-hint" }, options.dropzone.prompt)); } },
                title ? (React.createElement(fluentui_customized_components_1.FluentLabelHeader, null,
                    React.createElement(react_1.Label, null, title))) : null,
                widget,
                React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px", marginLeft: "6px" },
                    React.createElement(react_1.DefaultButton, { key: title, iconProps: {
                            iconName: "Link",
                        }, menuProps: {
                            items: menu,
                            onRenderMenuList: menuRender,
                        }, styles: {
                            menuIcon: {
                                display: "none !important",
                            },
                            root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultBindButtonSize),
                        } }))));
        }
        else {
            return (React.createElement("div", { className: "charticulator__widget-section-header" },
                React.createElement(fluentui_customized_components_1.FluentLabelHeader, null,
                    React.createElement(react_1.Label, null, title)),
                widget));
        }
    };
    FluentUIWidgetManager.prototype.horizontal = function (cols) {
        var widgets = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            widgets[_i - 1] = arguments[_i];
        }
        return (React.createElement("div", { className: "charticulator__widget-horizontal", key: "widget-horizontal" }, widgets.map(function (x, id) { return (React.createElement("span", { className: "el-layout-item el-layout-item-col-" + cols[id], key: "horizontal-" + id }, x)); })));
    };
    FluentUIWidgetManager.prototype.styledHorizontal = function (styles, cols) {
        var widgets = [];
        for (var _i = 2; _i < arguments.length; _i++) {
            widgets[_i - 2] = arguments[_i];
        }
        return (React.createElement("div", { className: "charticulator__widget-horizontal", style: styles }, widgets.map(function (x, id) { return (React.createElement("span", { className: "el-layout-item el-layout-item-col-" + cols[id], key: id }, x)); })));
    };
    FluentUIWidgetManager.prototype.filterEditor = function (options) {
        var filterText = strings_1.strings.filter.filterBy;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([
                filterText
            ], searchSections, [
                strings_1.strings.objects.axes.data,
            ]))) {
            return;
        }
        return (React.createElement(fluentui_filter_1.FilterPanel, { key: options.key, options: __assign({}, options), text: filterText, manager: this }));
    };
    FluentUIWidgetManager.prototype.groupByEditor = function (options) {
        var _this = this;
        var button;
        var text = strings_1.strings.objects.plotSegment.groupBy;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!options.ignoreSearch &&
            !this.shouldDrawComponent(__spread([
                text
            ], searchSections, [
                strings_1.strings.objects.axes.data,
            ]))) {
            return;
        }
        var getControl = function () {
            var _a, _b;
            switch (options.mode) {
                case "button" /* Button */:
                    if (options.value) {
                        if (options.value.expression) {
                            text =
                                strings_1.strings.objects.plotSegment.groupByCategory +
                                    options.value.expression;
                        }
                    }
                    return (React.createElement(fluentui_customized_components_1.FluentButton, { marginTop: "0px", key: _this.getKeyFromProperty((_a = options.target) === null || _a === void 0 ? void 0 : _a.property) + (options === null || options === void 0 ? void 0 : options.table) + (options === null || options === void 0 ? void 0 : options.value) },
                        React.createElement(react_1.DefaultButton, { styles: {
                                root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight),
                            }, text: text, elementRef: function (e) { return (button = e); }, iconProps: {
                                iconName: "RowsGroup",
                            }, onClick: function () {
                                globals.popupController.popupAt(function (context) {
                                    return (React.createElement(controllers_1.PopupView, { context: context },
                                        React.createElement(groupby_editor_1.GroupByEditor, { manager: _this, value: options.value, options: options })));
                                }, { anchor: button });
                            } })));
                case "panel" /* Panel */:
                    return (React.createElement(groupby_editor_1.GroupByEditor, { key: _this.getKeyFromProperty((_b = options === null || options === void 0 ? void 0 : options.target) === null || _b === void 0 ? void 0 : _b.property) +
                            options.table + (options === null || options === void 0 ? void 0 : options.value), manager: _this, value: options.value, options: options }));
            }
        };
        return (React.createElement("div", { key: options.key, style: { display: "inline" }, ref: function (e) { return (button = e); } }, getControl()));
    };
    FluentUIWidgetManager.prototype.nestedChartEditor = function (property, options) {
        var _this = this;
        var editNestedChartText = strings_1.strings.menuBar.editNestedChart;
        var importTemplate = strings_1.strings.menuBar.importTemplate;
        var searchSections = Array.isArray(options.searchSection)
            ? options.searchSection
            : [options.searchSection];
        if (!this.shouldDrawComponent(__spread([
            editNestedChartText,
            importTemplate
        ], searchSections))) {
            return;
        }
        return (React.createElement(React.Fragment, { key: this.getKeyFromProperty(property) }, this.vertical(React.createElement(fluentui_customized_components_1.NestedChartButtonsWrapper, null,
            React.createElement(components_1.ButtonRaised, { text: editNestedChartText, onClick: function () {
                    _this.store.dispatcher.dispatch(new actions_2.OpenNestedEditor(_this.objectClass.object, property, options));
                } })), React.createElement(fluentui_customized_components_1.NestedChartButtonsWrapper, null,
            React.createElement(components_1.ButtonRaised, { text: importTemplate, onClick: function () { return __awaiter(_this, void 0, void 0, function () {
                    var file, str, data, template, _a, _b, table, tTable, _c, _d, column, instance;
                    var e_1, _e, e_2, _f;
                    return __generator(this, function (_g) {
                        switch (_g.label) {
                            case 0: return [4 /*yield*/, index_1.showOpenFileDialog(["tmplt", "json"])];
                            case 1:
                                file = _g.sent();
                                return [4 /*yield*/, index_1.readFileAsString(file)];
                            case 2:
                                str = _g.sent();
                                data = JSON.parse(str);
                                template = new container_1.ChartTemplate(data);
                                try {
                                    for (_a = __values(options.dataset.tables), _b = _a.next(); !_b.done; _b = _a.next()) {
                                        table = _b.value;
                                        tTable = template.getDatasetSchema()[0];
                                        template.assignTable(tTable.name, table.name);
                                        try {
                                            for (_c = (e_2 = void 0, __values(tTable.columns)), _d = _c.next(); !_d.done; _d = _c.next()) {
                                                column = _d.value;
                                                template.assignColumn(tTable.name, column.name, column.name);
                                            }
                                        }
                                        catch (e_2_1) { e_2 = { error: e_2_1 }; }
                                        finally {
                                            try {
                                                if (_d && !_d.done && (_f = _c.return)) _f.call(_c);
                                            }
                                            finally { if (e_2) throw e_2.error; }
                                        }
                                    }
                                }
                                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                                finally {
                                    try {
                                        if (_b && !_b.done && (_e = _a.return)) _e.call(_a);
                                    }
                                    finally { if (e_1) throw e_1.error; }
                                }
                                instance = template.instantiate(options.dataset, false // no scale inference
                                );
                                this.emitSetProperty(property, instance.chart);
                                return [2 /*return*/];
                        }
                    });
                }); } })))));
    };
    FluentUIWidgetManager.prototype.row = function (title, widget) {
        return (React.createElement("div", { className: "charticulator__widget-row", key: title },
            title != null ? (React.createElement("span", { className: "charticulator__widget-row-label el-layout-item" }, title)) : // <Label>{title}</Label>
                null,
            widget));
    };
    FluentUIWidgetManager.prototype.vertical = function () {
        var widgets = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            widgets[_i] = arguments[_i];
        }
        return (React.createElement("div", { className: "charticulator__widget-vertical" }, widgets.map(function (x, id) { return (React.createElement("span", { className: "el-layout-item", key: id }, x)); })));
    };
    FluentUIWidgetManager.prototype.styledVertical = function (styles) {
        var widgets = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            widgets[_i - 1] = arguments[_i];
        }
        return (React.createElement("div", { className: "charticulator__widget-vertical", style: styles }, widgets.map(function (x, id) { return (React.createElement("span", { className: "el-layout-item", key: id }, x)); })));
    };
    FluentUIWidgetManager.prototype.verticalGroup = function (options, widgets) {
        if (widgets.filter(function (widget) { return (Array.isArray(widget) ? widget === null || widget === void 0 ? void 0 : widget[0] : widget); })
            .length == 0) {
            return null;
        }
        return (React.createElement("div", null,
            React.createElement(collapsiblePanel_1.CollapsiblePanel, { header: options.header, widgets: widgets, isCollapsed: options.isCollapsed, alignVertically: options.alignVertically, store: this.store })));
    };
    FluentUIWidgetManager.prototype.table = function (rows) {
        return (React.createElement("table", { className: "charticulator__widget-table" },
            React.createElement("tbody", null, rows.map(function (row, index) { return (React.createElement("tr", { key: index }, row.map(function (x, i) { return (React.createElement("td", { key: i },
                React.createElement("span", { className: "el-layout-item" }, x))); }))); }))));
    };
    FluentUIWidgetManager.prototype.scrollList = function (widgets, options) {
        if (options === void 0) { options = {}; }
        return (React.createElement("div", { className: "charticulator__widget-scroll-list", style: {
                maxHeight: options.maxHeight ? options.maxHeight + "px" : undefined,
                height: options.height ? options.height + "px" : undefined,
            } }, widgets.map(function (widget, i) { return (React.createElement("div", { className: "charticulator__widget-scroll-list-item", key: i, style: options.styles }, widget)); })));
    };
    FluentUIWidgetManager.prototype.tooltip = function (widget, tooltipContent) {
        return React.createElement(react_1.TooltipHost, { content: tooltipContent }, widget);
    };
    FluentUIWidgetManager.prototype.customCollapsiblePanel = function (widgets, options) {
        if (options === void 0) { options = {}; }
        if (widgets.filter(function (widget) { return (Array.isArray(widget) ? widget === null || widget === void 0 ? void 0 : widget[0] : widget); })
            .length == 0) {
            return null;
        }
        return (React.createElement(custom_collapsible_panel_1.CustomCollapsiblePanel, { widgets: widgets, styles: options.styles, header: options.header, store: this.store }));
    };
    FluentUIWidgetManager.prototype.reorderByAnotherColumnWidget = function (property, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var container;
        return (React.createElement(fluentui_customized_components_1.FluentButton, { ref: function (e) { return (container = e); }, key: this.getKeyFromProperty(property), marginTop: "0px", paddingRight: "0px" },
            React.createElement(react_1.DefaultButton, { styles: {
                    root: __assign({ minWidth: "unset" }, fluentui_customized_components_1.defultComponentsHeight),
                }, iconProps: {
                    iconName: "SortLines",
                }, onClick: function () {
                    globals.popupController.popupAt(function (context) {
                        var items = options.items
                            ? options.items
                            : _this.getPropertyValue(property);
                        return (React.createElement(controllers_1.PopupView, { context: context },
                            React.createElement(fluentui_reorder_string_value_1.FluentUIReorderStringsValue, __assign({ items: items, onConfirm: function (items) {
                                    _this.emitSetProperty(property, items);
                                    if (options.onConfirmClick) {
                                        options.onConfirmClick(items);
                                    }
                                    _this.emitSetProperty({
                                        property: property.property,
                                        field: "orderMode",
                                    }, types_1.OrderMode.order);
                                    if (options.onConfirmClick) {
                                        options.onConfirmClick(items);
                                    }
                                    context.close();
                                }, onReset: function () {
                                    if (options.onResetCategories) {
                                        return options.onResetCategories;
                                    }
                                    var axisDataBinding = __assign({}, _this.objectClass.object.properties[property.property]);
                                    axisDataBinding.table = _this.store.chartManager.getTable(_this.objectClass.object.table);
                                    axisDataBinding.metadata = {
                                        kind: axisDataBinding.dataKind,
                                        orderMode: "order",
                                    };
                                    var groupBy = _this.store.getGroupingExpression(_this.objectClass.object);
                                    var values = _this.store.chartManager.getGroupedExpressionVector(_this.objectClass.object.table, groupBy, axisDataBinding.expression);
                                    var categories = _this.store.getCategoriesForDataBinding(axisDataBinding.metadata, axisDataBinding.type, values).categories;
                                    return categories;
                                } }, options))));
                    }, {
                        anchor: container,
                        alignX: _this.store.editorType == app_store_1.EditorType.Embedded
                            ? controllers_1.PopupAlignment.EndInner
                            : controllers_1.PopupAlignment.StartInner,
                    });
                } })));
    };
    FluentUIWidgetManager.prototype.shouldDrawComponent = function (options) {
        var searchString = this.store.searchString;
        //remove null values
        var componentStings = options.filter(function (value) { return value != undefined; });
        if (this.ignoreSearch) {
            return true;
        }
        if ((searchString === null || searchString === void 0 ? void 0 : searchString.length) != 0 && componentStings.length >= 0) {
            if (!componentStings.some(function (value) {
                return value && (value === null || value === void 0 ? void 0 : value.toUpperCase().includes(searchString === null || searchString === void 0 ? void 0 : searchString.toUpperCase()));
            })) {
                return false;
            }
        }
        return true;
    };
    return FluentUIWidgetManager;
}());
exports.FluentUIWidgetManager = FluentUIWidgetManager;
var DropZoneView = /** @class */ (function (_super) {
    __extends(DropZoneView, _super);
    function DropZoneView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isInSession: false,
            isDraggingOver: false,
            data: null,
        };
        return _this;
    }
    DropZoneView.prototype.componentDidMount = function () {
        var _this = this;
        globals.dragController.registerDroppable(this, this.dropContainer);
        this.tokens = [
            globals.dragController.addListener("sessionstart", function () {
                var session = globals.dragController.getSession();
                if (_this.props.filter(session.data)) {
                    _this.setState({
                        isInSession: true,
                    });
                }
            }),
            globals.dragController.addListener("sessionend", function () {
                _this.setState({
                    isInSession: false,
                });
            }),
        ];
    };
    DropZoneView.prototype.componentWillUnmount = function () {
        globals.dragController.unregisterDroppable(this);
        this.tokens.forEach(function (x) { return x.remove(); });
    };
    DropZoneView.prototype.onDragEnter = function (ctx) {
        var _this = this;
        var data = ctx.data;
        var judge = this.props.filter(data);
        if (judge) {
            this.setState({
                isDraggingOver: true,
                data: data,
            });
            ctx.onLeave(function () {
                _this.setState({
                    isDraggingOver: false,
                    data: null,
                });
            });
            ctx.onDrop(function (point, modifiers) {
                _this.props.onDrop(data, point, modifiers);
            });
            return true;
        }
    };
    DropZoneView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: index_1.classNames(this.props.className, ["is-in-session", this.state.isInSession], ["is-dragging-over", this.state.isDraggingOver]), onClick: this.props.onClick, ref: function (e) { return (_this.dropContainer = e); } }, this.props.draggingHint == null
            ? this.props.children
            : this.state.isInSession
                ? this.props.draggingHint()
                : this.props.children));
    };
    return DropZoneView;
}(React.Component));
exports.DropZoneView = DropZoneView;
var FluentDetailsButton = /** @class */ (function (_super) {
    __extends(FluentDetailsButton, _super);
    function FluentDetailsButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FluentDetailsButton.prototype.componentDidUpdate = function () {
        if (this.inner) {
            this.inner.forceUpdate();
        }
    };
    FluentDetailsButton.prototype.render = function () {
        var _this = this;
        var btn;
        return (React.createElement(React.Fragment, null,
            this.props.label ? (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, this.props.label)) : null,
            React.createElement(react_1.DefaultButton, { iconProps: {
                    iconName: "More",
                }, componentRef: function (e) {
                    return (btn = ReactDOM.findDOMNode(e));
                }, onClick: function () {
                    globals.popupController.popupAt(function (context) {
                        return (React.createElement(controllers_1.PopupView, { context: context },
                            React.createElement(DetailsButtonInner, { parent: _this, ref: function (e) { return (_this.inner = e); } })));
                    }, {
                        anchor: btn,
                        alignX: controllers_1.getAlignment(btn).alignX,
                    });
                } })));
    };
    return FluentDetailsButton;
}(React.Component));
exports.FluentDetailsButton = FluentDetailsButton;
var DetailsButtonInner = /** @class */ (function (_super) {
    __extends(DetailsButtonInner, _super);
    function DetailsButtonInner() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsButtonInner.prototype.render = function () {
        var _a;
        var parent = this.props.parent;
        return (React.createElement("div", { className: "charticulator__widget-popup-details" }, (_a = parent.props.manager).vertical.apply(_a, __spread(parent.props.widgets))));
    };
    return DetailsButtonInner;
}(React.Component));
exports.DetailsButtonInner = DetailsButtonInner;
//# sourceMappingURL=fluentui_manager.js.map