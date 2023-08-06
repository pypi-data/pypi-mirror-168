"use strict";
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
exports.Director = exports.MenuItemBuilder = void 0;
var core_1 = require("../../../core");
var react_1 = require("@fluentui/react");
var common_1 = require("./common");
var scale_editor_1 = require("../panels/scale_editor");
var fluent_mapping_editor_1 = require("../panels/widgets/fluent_mapping_editor");
var strings_1 = require("../../../strings");
var specification_1 = require("../../../core/specification");
var fluentui_customized_components_1 = require("../panels/widgets/controls/fluentui_customized_components");
var collapsiblePanel_1 = require("../panels/widgets/controls/collapsiblePanel");
var React = require("react");
var DELIMITER = "-";
var DERIVED_COLUMNS_KEY_PREFIX = "_derived";
var MenuItemsCreator = /** @class */ (function () {
    function MenuItemsCreator() {
        this.menuItems = [];
        this.nullDescription = strings_1.strings.core.none;
        this.fields = [];
        this.nullSelectable = true;
        this.onClick = function () {
            alert();
        };
        this.useAggregation = false;
        this.useDerivedColumns = false;
        this.isDerivedColumns = false;
        this.derivedColumnsIdx = [];
        this.selectedKey = null;
        this.defaultValue = null;
    }
    MenuItemsCreator.prototype.onToggleSelect = function (field, ev, item) {
        ev && ev.preventDefault && ev.preventDefault();
        if (item && field) {
            this.selectedKey = field.columnName + DELIMITER + item.key;
        }
    };
    MenuItemsCreator.prototype.onToggleDerivedSelect = function (field, derivedField, ev, item) {
        ev && ev.preventDefault();
        if (derivedField && field && item) {
            this.selectedKey =
                field.columnName + DELIMITER + derivedField + DELIMITER + item.key;
        }
    };
    MenuItemsCreator.prototype.setFieds = function (datasetStore, table, kinds, types) {
        this.fields = this.getTableFields(datasetStore, table, kinds, types);
    };
    MenuItemsCreator.prototype.getTableFields = function (store, table, kinds, types) {
        var storeTable = store
            .getTables()
            .filter(function (storeTable) { return storeTable.name == table || table == null; })[0];
        var imagesTable = store
            .getTables()
            .filter(function (storeTable) { return storeTable.name.endsWith("Images"); })[0];
        var columns = core_1.deepClone(storeTable.columns);
        //append image column
        if (imagesTable) {
            var imageColumn = imagesTable.columns.filter(function (column) { return column.type === specification_1.DataType.Image; })[0];
            columns.push(imageColumn);
        }
        var columnFilters = [];
        columnFilters.push(function (x) { return !x.metadata.isRaw; });
        if (table) {
            columnFilters.push(function (x) { return x.table == table; });
        }
        if (kinds) {
            columnFilters.push(function (x) { return x.metadata != null && common_1.isKindAcceptable(x.metadata.kind, kinds); });
        }
        if (types) {
            columnFilters.push(function (x) { return x.metadata != null && types.indexOf(x.type) >= 0; });
        }
        var columnFilter = function (x) {
            var e_1, _a;
            try {
                for (var columnFilters_1 = __values(columnFilters), columnFilters_1_1 = columnFilters_1.next(); !columnFilters_1_1.done; columnFilters_1_1 = columnFilters_1.next()) {
                    var f = columnFilters_1_1.value;
                    if (!f(x)) {
                        return false;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (columnFilters_1_1 && !columnFilters_1_1.done && (_a = columnFilters_1.return)) _a.call(columnFilters_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return true;
        };
        var candidates = columns.map(function (c) {
            var e_2, _a;
            var r = {
                selectable: true,
                table: storeTable.name,
                columnName: c.name,
                expression: core_1.Expression.variable(c.name).toString(),
                rawExpression: core_1.Expression.variable(c.metadata.rawColumnName || c.name).toString(),
                type: c.type,
                displayName: c.name,
                metadata: c.metadata,
                derived: [],
            };
            // Compute derived columns.
            var derivedColumns = common_1.type2DerivedColumns[r.type];
            if (derivedColumns) {
                try {
                    for (var derivedColumns_1 = __values(derivedColumns), derivedColumns_1_1 = derivedColumns_1.next(); !derivedColumns_1_1.done; derivedColumns_1_1 = derivedColumns_1.next()) {
                        var item = derivedColumns_1_1.value;
                        var ditem = {
                            table: storeTable.name,
                            columnName: null,
                            expression: core_1.Expression.functionCall(item.function, core_1.Expression.parse(r.expression)).toString(),
                            rawExpression: core_1.Expression.functionCall(item.function, core_1.Expression.parse(r.rawExpression)).toString(),
                            type: item.type,
                            metadata: item.metadata,
                            displayName: item.name,
                            selectable: true,
                        };
                        if (columnFilter(ditem)) {
                            r.derived.push(ditem);
                        }
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (derivedColumns_1_1 && !derivedColumns_1_1.done && (_a = derivedColumns_1.return)) _a.call(derivedColumns_1);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
            r.selectable = columnFilter(r);
            return r;
        });
        // Make sure we only show good ones
        candidates = candidates.filter(function (x) { return (x.derived.length > 0 || x.selectable) && !x.metadata.isRaw; });
        return candidates;
    };
    MenuItemsCreator.prototype.transformField = function (item, aggregation) {
        var _a;
        if (aggregation === void 0) { aggregation = null; }
        if (aggregation == null) {
            aggregation = core_1.Expression.getDefaultAggregationFunction(item.type, (_a = item.metadata) === null || _a === void 0 ? void 0 : _a.kind);
        }
        var r = {
            table: item.table,
            expression: item.expression,
            rawExpression: item.rawExpression,
            columnName: item.columnName,
            type: item.type,
            metadata: item.metadata,
        };
        if (this.useAggregation) {
            r.expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.expression)).toString();
            r.rawExpression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.rawExpression)).toString();
        }
        return r;
    };
    MenuItemsCreator.prototype.transformDerivedField = function (item, expression, aggregation) {
        var _a;
        if (aggregation === void 0) { aggregation = null; }
        if (aggregation == null) {
            aggregation = core_1.Expression.getDefaultAggregationFunction(item.type, (_a = item.metadata) === null || _a === void 0 ? void 0 : _a.kind);
        }
        var r = {
            table: item.table,
            expression: item.expression + expression,
            rawExpression: item.rawExpression + expression,
            columnName: item.columnName,
            type: item.type,
            metadata: item.metadata,
        };
        if (this.useAggregation) {
            r.expression = expression;
            r.rawExpression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(item.rawExpression)).toString();
        }
        return r;
    };
    MenuItemsCreator.prototype.checkSelection = function (key) {
        return key.localeCompare(this.selectedKey) === 0;
    };
    MenuItemsCreator.prototype.buildMenuFieldsItems = function () {
        var _this = this;
        var _a, _b, _c;
        // if useAggregation == true -> create sub menu
        var mapping = (_c = (_b = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent) === null || _c === void 0 ? void 0 : _c.getAttributeMapping(this.attribute);
        this.menuItems = this.fields.map(function (field, idx) {
            var onClickFn = function (ev, item) {
                var transformedField = _this.transformField(field, item === null || item === void 0 ? void 0 : item.key);
                if ((mapping === null || mapping === void 0 ? void 0 : mapping.type) === specification_1.MappingType.text) {
                    _this.textMappingOnClick(transformedField.expression, field);
                }
                else {
                    _this.onClick(transformedField);
                }
                _this.onToggleSelect(field, ev, item);
            };
            var subMenuCheckedItem = null;
            var derivedColumns = common_1.type2DerivedColumns[field.type];
            if (derivedColumns) {
                _this.isDerivedColumns = true;
                _this.derivedColumnsIdx.push([idx, field]);
            }
            var subMenuProps = _this.useAggregation
                ? {
                    items: core_1.Expression.getCompatibleAggregationFunctionsByDataKind(field.metadata.kind).map(function (subMenuItem) {
                        var selectionKey = field.columnName + DELIMITER + subMenuItem.name;
                        var isSelected = _this.checkSelection(selectionKey);
                        if (isSelected) {
                            subMenuCheckedItem = subMenuItem.displayName;
                        }
                        var mappingConfig = _this.scaleEditorMenu(isSelected);
                        return {
                            key: subMenuItem.name,
                            text: subMenuItem.displayName,
                            isChecked: isSelected,
                            canCheck: true,
                            onClick: onClickFn,
                            split: mappingConfig.isMappingEditor,
                            subMenuProps: mappingConfig.scaleEditorSubMenuProps,
                        };
                    }),
                }
                : null;
            var selectionKey = field.columnName + DELIMITER + field.columnName;
            var itemText = field.columnName +
                (subMenuProps && subMenuCheckedItem && mapping ? "" : "");
            return {
                key: field.columnName + (derivedColumns ? DERIVED_COLUMNS_KEY_PREFIX : ""),
                text: itemText,
                subMenuProps: subMenuProps,
                canCheck: subMenuProps ? null : true,
                isChecked: _this.checkSelection(selectionKey),
                onClick: subMenuProps ? null : onClickFn,
                data: subMenuCheckedItem,
            };
        });
    };
    MenuItemsCreator.prototype.renderScaleEditor = function (parent, store) {
        var _a, _b;
        var mapping = (_b = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent.getAttributeMapping(this.attribute);
        if (mapping && mapping.type == specification_1.MappingType.scale) {
            var scaleMapping = mapping;
            if (scaleMapping.scale) {
                var scaleObject = core_1.getById(this.store.chart.scales, scaleMapping.scale);
                return (React.createElement(scale_editor_1.ScaleEditor, { scale: scaleObject, scaleMapping: scaleMapping, store: store, plotSegment: fluent_mapping_editor_1.parentOfType(parent.props.parent.objectClass.parent, "plot-segment") }));
            }
            return null;
        }
        return null;
    };
    MenuItemsCreator.prototype.produceScaleEditor = function (store, attribute, parent) {
        this.attribute = attribute;
        this.parent = parent;
        this.store = store;
    };
    MenuItemsCreator.prototype.appendNull = function () {
        var _this = this;
        this.menuItems = __spread([
            {
                key: this.nullDescription,
                text: this.nullDescription,
                onClick: function () { return _this.onClick(null); },
            }
        ], this.menuItems);
    };
    MenuItemsCreator.prototype.scaleEditorMenu = function (isSelected) {
        var _this = this;
        var _a, _b, _c;
        var mapping = (_c = (_b = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent) === null || _c === void 0 ? void 0 : _c.getAttributeMapping(this.attribute);
        var isMappingEditor = !!(mapping &&
            mapping.type == specification_1.MappingType.scale &&
            mapping.scale);
        var scaleEditorSubMenuProps = isSelected && isMappingEditor
            ? {
                items: [
                    {
                        key: "mapping",
                        onRender: function () { return _this.renderScaleEditor(_this.parent, _this.store); },
                    },
                ],
            }
            : null;
        return { scaleEditorSubMenuProps: scaleEditorSubMenuProps, isMappingEditor: isMappingEditor };
    };
    MenuItemsCreator.prototype.textMappingOnClick = function (menuExpr, field) {
        var _a, _b, _c, _d, _e, _f;
        var newValue = "${" + menuExpr + "}";
        if (core_1.Expression.parseTextExpression(newValue).isTrivialString()) {
            (_c = (_b = (_a = this === null || this === void 0 ? void 0 : this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent) === null || _c === void 0 ? void 0 : _c.onEditMappingHandler(this.attribute, {
                type: "value",
                value: newValue,
            });
        }
        else {
            (_f = (_e = (_d = this === null || this === void 0 ? void 0 : this.parent) === null || _d === void 0 ? void 0 : _d.props) === null || _e === void 0 ? void 0 : _e.parent) === null || _f === void 0 ? void 0 : _f.onEditMappingHandler(this.attribute, {
                type: "text",
                table: field.table,
                textExpression: newValue,
            });
        }
    };
    MenuItemsCreator.prototype.getDerivedColumnExpression = function (derivedColumn, field, aggregationMenuItem) {
        var expr = core_1.Expression.functionCall(derivedColumn.function, core_1.Expression.variable(field.columnName)).toString();
        return aggregationMenuItem.name + "(" + expr + ")";
    };
    /**
     * Add DerivedColumn
     * @see derivedColumnsIdx
     */
    // eslint-disable-next-line max-lines-per-function
    MenuItemsCreator.prototype.appendDerivedColumn = function () {
        var _this = this;
        var _a, _b, _c;
        var mapping = (_c = (_b = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent) === null || _c === void 0 ? void 0 : _c.getAttributeMapping(this.attribute);
        if (this.useAggregation && this.isDerivedColumns) {
            var _loop_1 = function (i) {
                var menuIdx = this_1.derivedColumnsIdx[i][0];
                var field = this_1.derivedColumnsIdx[i][1];
                var derivedColumns = common_1.type2DerivedColumns[field.type];
                var subMenuCheckedItem = null;
                var subMenuProps = this_1.useAggregation
                    ? {
                        items: derivedColumns.map(function (derivedColumn) {
                            var subMenuProps = _this.useAggregation
                                ? {
                                    items: core_1.Expression.getCompatibleAggregationFunctionsByDataKind(derivedColumn.metadata.kind).map(function (aggregationMenuItem) {
                                        var _a, _b, _c;
                                        var onClickFn = function (ev, item) {
                                            var menuExpr = _this.getDerivedColumnExpression(derivedColumn, field, aggregationMenuItem);
                                            if ((mapping === null || mapping === void 0 ? void 0 : mapping.type) === specification_1.MappingType.text ||
                                                (mapping === null || mapping === void 0 ? void 0 : mapping.type) === specification_1.MappingType.value) {
                                                _this.textMappingOnClick(menuExpr, field);
                                            }
                                            else {
                                                _this.onClick(_this.transformDerivedField(field, menuExpr, item === null || item === void 0 ? void 0 : item.key));
                                            }
                                            //update selection key
                                            _this.onToggleDerivedSelect(field, derivedColumn.name, ev, item);
                                        };
                                        var selectionKey = field.columnName +
                                            DELIMITER +
                                            derivedColumn.name +
                                            DELIMITER +
                                            aggregationMenuItem.name;
                                        var isSelected = _this.checkSelection(selectionKey);
                                        if (isSelected) {
                                            subMenuCheckedItem =
                                                derivedColumn.displayName +
                                                    DELIMITER +
                                                    aggregationMenuItem.displayName;
                                        }
                                        //function for mapping renderer
                                        var mapping = (_c = (_b = (_a = _this.parent) === null || _a === void 0 ? void 0 : _a.props) === null || _b === void 0 ? void 0 : _b.parent) === null || _c === void 0 ? void 0 : _c.getAttributeMapping(_this.attribute);
                                        var mappingConfig = _this.scaleEditorMenu(isSelected);
                                        return {
                                            key: aggregationMenuItem.name,
                                            text: aggregationMenuItem.displayName,
                                            isChecked: isSelected,
                                            canCheck: true,
                                            onClick: onClickFn,
                                            split: mappingConfig.isMappingEditor,
                                            subMenuProps: mappingConfig.scaleEditorSubMenuProps,
                                        };
                                    }),
                                }
                                : null;
                            return {
                                key: derivedColumn.name,
                                text: derivedColumn.displayName,
                                canCheck: true,
                                subMenuProps: subMenuProps,
                            };
                        }),
                    }
                    : null;
                //key for no aggregation option
                var selectionKey = field.columnName + DELIMITER + field.columnName;
                var itemText = field.columnName +
                    strings_1.strings.objects.derivedColumns.menuSuffix +
                    (subMenuProps && subMenuCheckedItem && mapping ? "" : "");
                var derivedColumnsField = {
                    key: field.columnName,
                    text: itemText,
                    subMenuProps: subMenuProps,
                    canCheck: subMenuProps ? null : true,
                    isChecked: this_1.checkSelection(selectionKey),
                    data: subMenuCheckedItem,
                };
                //add derived column field to menu
                this_1.menuItems.splice(menuIdx + 1, 0, derivedColumnsField);
            };
            var this_1 = this;
            for (var i = 0; i < this.derivedColumnsIdx.length; i++) {
                _loop_1(i);
            }
            //we need clear array between renders
            this.derivedColumnsIdx = [];
        }
    };
    MenuItemsCreator.prototype.buildMenu = function () {
        this.buildMenuFieldsItems();
        if (this.useDerivedColumns) {
            this.appendDerivedColumn();
        }
        this.appendNull();
    };
    MenuItemsCreator.prototype.parseDerivedColumnsExpression = function (expression) {
        var DATE_DERIVED_PREDIX = "date.";
        if (expression.startsWith(DATE_DERIVED_PREDIX)) {
            //data.year(DATE) -> DATE-year
            return (expression.match(/\(([^)]+)\)/)[1] +
                DELIMITER +
                expression.match(/\.([^(]+)\(/)[1]);
        }
        return expression;
    };
    //todo: defaultValue without Aggregation
    MenuItemsCreator.prototype.produceDefaultValue = function (defaultValue) {
        var _a, _b;
        var mappingType = defaultValue === null || defaultValue === void 0 ? void 0 : defaultValue.type;
        this.defaultValue = defaultValue;
        var expression = null;
        var expressionAggregation = null;
        if (defaultValue != null) {
            if (defaultValue.expression != null) {
                var parsed = void 0;
                if (mappingType === specification_1.MappingType.text) {
                    parsed = (_b = (_a = core_1.Expression.parseTextExpression(defaultValue.expression)) === null || _a === void 0 ? void 0 : _a.parts[0]) === null || _b === void 0 ? void 0 : _b.expression;
                }
                else {
                    parsed = core_1.Expression.parse(defaultValue.expression);
                }
                if (parsed instanceof core_1.Expression.FunctionCall) {
                    expression = parsed.args[0].toString();
                    expressionAggregation = parsed.name;
                    expression = expression === null || expression === void 0 ? void 0 : expression.split("`").join("");
                    //need to provide date.year() etc.
                    expression = this.parseDerivedColumnsExpression(expression);
                }
            }
            var value = (expression ? expression + DELIMITER : "") + expressionAggregation;
            if (value) {
                this.selectedKey = value;
            }
        }
    };
    return MenuItemsCreator;
}());
var MenuItemBuilder = /** @class */ (function () {
    function MenuItemBuilder() {
        this.reset();
    }
    MenuItemBuilder.prototype.produceScaleEditor = function (store, attribute, parent) {
        this.menuItemsCreator.produceScaleEditor(store, attribute, parent);
    };
    MenuItemBuilder.prototype.produceDerivedColumns = function () {
        this.menuItemsCreator.useDerivedColumns = true;
    };
    MenuItemBuilder.prototype.produceOnChange = function (fn) {
        this.menuItemsCreator.onClick = fn;
    };
    MenuItemBuilder.prototype.getMenuItems = function () {
        return this.menuItemsCreator.menuItems;
    };
    MenuItemBuilder.prototype.reset = function () {
        this.menuItemsCreator = new MenuItemsCreator();
    };
    MenuItemBuilder.prototype.produceNullDescription = function (nullDescription) {
        this.menuItemsCreator.nullDescription = nullDescription;
    };
    MenuItemBuilder.prototype.produceUsingAggregation = function (useAggregation) {
        this.menuItemsCreator.useAggregation = useAggregation;
    };
    MenuItemBuilder.prototype.produceFields = function (datasetStore, table, kinds, types) {
        this.menuItemsCreator.setFieds(datasetStore, table, kinds, types);
    };
    MenuItemBuilder.prototype.produceDefaultValue = function (dafaultValue) {
        this.menuItemsCreator.produceDefaultValue(dafaultValue);
    };
    MenuItemBuilder.prototype.buildMenu = function () {
        return this.menuItemsCreator.buildMenu();
    };
    return MenuItemBuilder;
}());
exports.MenuItemBuilder = MenuItemBuilder;
var Director = /** @class */ (function () {
    function Director() {
    }
    Director.prototype.setBuilder = function (builder) {
        this.builder = builder;
    };
    Director.prototype.buildNullMenu = function () {
        this.builder.buildMenu();
        return this.builder.getMenuItems();
    };
    Director.prototype.buildFieldsMenu = function (onClick, defaultValue, datasetStore, parent, attribute, table, kinds, types) {
        // console.log(datasetStore, table, kinds, types)
        this.builder.produceFields(datasetStore, table, kinds, types);
        this.builder.produceOnChange(onClick);
        this.builder.produceUsingAggregation(true);
        this.builder.produceDefaultValue(defaultValue);
        this.builder.produceScaleEditor(datasetStore, attribute, parent);
        this.builder.produceDerivedColumns();
        this.builder.buildMenu();
        return this.builder.getMenuItems();
    };
    Director.prototype.buildSectionHeaderFieldsMenu = function (onClick, defaultValue, datasetStore, table, kinds, types) {
        this.builder.produceFields(datasetStore, table, kinds, types);
        this.builder.produceOnChange(onClick);
        this.builder.produceUsingAggregation(true);
        this.builder.produceDefaultValue(defaultValue);
        this.builder.buildMenu();
        return this.builder.getMenuItems();
    };
    Director.prototype.getMenuRender = function () {
        var theme = react_1.getTheme();
        var CustomMenuRender = function (_a) {
            var item = _a.item, defaultKey = _a.defaultKey;
            var currentFunction;
            if (item.subMenuProps) {
                currentFunction = item.subMenuProps.items.find(function (i) { return i.isChecked; });
                if (currentFunction) {
                    defaultKey = currentFunction.key;
                }
            }
            return (React.createElement(fluentui_customized_components_1.FluentDataBindingMenuItem, { key: item.key, backgroundColor: currentFunction
                    ? theme.semanticColors.buttonBackgroundChecked
                    : null, backgroundColorHover: theme.semanticColors.buttonBackgroundHovered },
                React.createElement(fluentui_customized_components_1.FluentDataBindingMenuLabel, null,
                    React.createElement(react_1.Label, { onClick: function (e) {
                            var _a;
                            var agr = (_a = item.subMenuProps) === null || _a === void 0 ? void 0 : _a.items.find(function (item) { return item.key === defaultKey; });
                            if (agr) {
                                agr.onClick(e, agr);
                            }
                            else {
                                item.onClick(e, item);
                            }
                        }, styles: fluentui_customized_components_1.defaultLabelStyle }, item.text)),
                item.subMenuProps ? (React.createElement(react_1.Dropdown, { styles: __assign(__assign({}, fluentui_customized_components_1.defaultStyle), { title: __assign(__assign({}, fluentui_customized_components_1.defaultStyle.title), { lineHeight: fluentui_customized_components_1.defultBindButtonSize.height, borderWidth: "0px" }), dropdownOptionText: {
                            boxSizing: "unset",
                            lineHeight: fluentui_customized_components_1.defultBindButtonSize.height,
                        }, callout: {
                            minWidth: 180,
                        } }), selectedKey: defaultKey, options: item.subMenuProps.items.map(function (i) { return ({
                        key: i.key,
                        text: i.text,
                    }); }), onChange: function (e, opt) {
                        var agr = item.subMenuProps.items.find(function (item) { return item.key === opt.key; });
                        if (agr) {
                            agr.onClick(e, agr);
                        }
                        else {
                            item.onClick(e, item);
                        }
                    } })) : null));
        };
        return function (props) {
            var calloutKey = "mappingMenuAnchor";
            // find current mapping
            var mapping = null;
            var currentColumn = props.items
                .filter(function (item) { return item.subMenuProps; }) // exclude None
                .flatMap(function (items) {
                if (items.subMenuProps &&
                    items.subMenuProps.items.find(function (i) { return i.key === "year"; })) {
                    return items.subMenuProps.items;
                }
                else {
                    return items;
                }
            })
                .find(function (item) {
                return item.subMenuProps.items.filter(function (i) { return i.isChecked && i.subMenuProps; })
                    .length > 0;
            }); // Exclude unselected columns
            if (currentColumn) {
                var aggregationFunction = currentColumn.subMenuProps.items.find(function (i) { return i.isChecked && i.subMenuProps; });
                var currentMapping = aggregationFunction.subMenuProps.items.find(function (i) { return i.key === "mapping"; }); // Select mapping of column
                // set current mapping
                mapping = currentMapping;
            }
            return (React.createElement("div", { id: calloutKey },
                mapping ? (React.createElement(react_1.Callout, { target: "#" + calloutKey, directionalHint: react_1.DirectionalHint.leftCenter }, mapping.onRender(mapping, function () { return null; }))) : null,
                !props.items.find(function (item) { return item.key === "first" || item.key === "avg"; }) ? (React.createElement(React.Fragment, null, props.items.map(function (item) {
                    var _a, _b;
                    if ((_a = item.subMenuProps) === null || _a === void 0 ? void 0 : _a.items.find(function (i) { return i.key === "year"; })) {
                        var expand = item.subMenuProps.items.find(function (columns) {
                            return columns.subMenuProps.items.find(function (func) { return func.isChecked; });
                        });
                        return (React.createElement(collapsiblePanel_1.CollapsiblePanel, { key: item.key, header: function () { return (React.createElement(react_1.Label, { styles: fluentui_customized_components_1.defaultLabelStyle }, item.text)); }, isCollapsed: expand === null, widgets: item.subMenuProps.items.map(function (item) {
                                var _a;
                                var currentKey = (_a = item.subMenuProps) === null || _a === void 0 ? void 0 : _a.items[0].key;
                                return (React.createElement(CustomMenuRender, { key: item.key, item: item, defaultKey: currentKey }));
                            }) }));
                    }
                    else {
                        var currentKey = (_b = item.subMenuProps) === null || _b === void 0 ? void 0 : _b.items[0].key;
                        return (React.createElement(CustomMenuRender, { key: item.key, item: item, defaultKey: currentKey }));
                    }
                }))) : (React.createElement(react_1.ContextualMenu, __assign({}, props)))));
        };
    };
    return Director;
}());
exports.Director = Director;
//# sourceMappingURL=data_field_binding_builder.js.map