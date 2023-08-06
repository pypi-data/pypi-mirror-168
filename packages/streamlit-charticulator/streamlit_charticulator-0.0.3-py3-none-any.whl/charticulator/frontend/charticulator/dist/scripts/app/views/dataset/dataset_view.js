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
exports.ColumnView = exports.ColumnViewState = exports.ColumnViewProps = exports.ColumnsView = exports.DatasetView = void 0;
/**
 * See {@link DatasetView} or {@link TableView}
 * @packageDocumentation
 * @preferred
 */
var React = require("react");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var controllers_1 = require("../../controllers");
var globals = require("../../globals");
var R = require("../../resources");
var stores_1 = require("../../stores");
var utils_1 = require("../../utils");
var controls_1 = require("../panels/widgets/controls");
var common_1 = require("./common");
var table_view_1 = require("./table_view");
var dataset_1 = require("../../../core/dataset");
var specification_1 = require("../../../core/specification");
var template_1 = require("../../template");
var container_1 = require("../../../container");
var import_view_1 = require("../file_view/import_view");
var strings_1 = require("../../../strings");
var app_store_1 = require("../../stores/app_store");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("../panels/widgets/controls/fluentui_customized_components");
/**
 * Component for displaying dataset on the left side of app
 *
 * ![Mark widgets](media://dataset_view.png)
 */
var DatasetView = /** @class */ (function (_super) {
    __extends(DatasetView, _super);
    function DatasetView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DatasetView.prototype.componentDidMount = function () {
        var _this = this;
        this.props.store.addListener(stores_1.AppStore.EVENT_DATASET, function () {
            return _this.forceUpdate();
        });
    };
    DatasetView.prototype.render = function () {
        var _this = this;
        var tables = this.props.store.getTables();
        var mainTables = [dataset_1.TableType.Main, dataset_1.TableType.Links, dataset_1.TableType.Image];
        return (React.createElement("div", { className: "charticulator__dataset-view" }, tables
            .filter(function (table) { return mainTables.find(function (m) { return m === table.type; }); })
            .map(function (table, idx) { return (React.createElement(ColumnsView, { key: "t" + idx, table: table, store: _this.props.store })); })));
    };
    DatasetView.prototype.onImportConnections = function () {
        alert(strings_1.strings.error.notImplemented);
    };
    return DatasetView;
}(React.Component));
exports.DatasetView = DatasetView;
var buttonStyles = {
    root: {
        height: fluentui_customized_components_1.defultBindButtonSize + "px",
        width: fluentui_customized_components_1.defultBindButtonSize + "px",
        minWidth: fluentui_customized_components_1.defultBindButtonSize + "px",
        padding: "0px",
        border: "none",
    },
};
var ColumnsView = /** @class */ (function (_super) {
    __extends(ColumnsView, _super);
    function ColumnsView(props) {
        var _this = _super.call(this, props) || this;
        _this.popupController = new controllers_1.PopupController();
        _this.state = {
            selectedColumn: null,
            tableViewIsOpened: false,
        };
        return _this;
    }
    // eslint-disable-next-line
    ColumnsView.prototype.render = function () {
        var _this = this;
        var table = this.props.table;
        return (React.createElement(React.Fragment, null,
            React.createElement(controllers_1.PopupContainer, { controller: this.popupController }),
            React.createElement("div", { className: "charticulator__dataset-view-columns" },
                React.createElement("h2", { className: "el-title" },
                    React.createElement("span", { className: "el-text" }, dataset_1.tableTypeName[this.props.table.type]),
                    this.props.store.editorType === app_store_1.EditorType.Chart ? (React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "general/replace",
                        }, styles: buttonStyles, title: strings_1.strings.dataset.replaceWithCSV, 
                        // eslint-disable-next-line
                        onClick: function () {
                            // eslint-disable-next-line
                            utils_1.showOpenFileDialog(["csv"]).then(function (file) {
                                var loader = new core_1.Dataset.DatasetLoader();
                                var reader = new FileReader();
                                // eslint-disable-next-line
                                reader.onload = function () {
                                    var newTable = loader.loadDSVFromContents(table.name, reader.result, _this.props.store.getLocaleFileFormat());
                                    newTable.displayName = utils_1.getFileNameWithoutExtension(file.name);
                                    newTable.name = table.name;
                                    newTable.type = table.type;
                                    var store = _this.props.store;
                                    var newDataset = {
                                        name: store.dataset.name,
                                        tables: store.dataset.tables.map(function (x) {
                                            if (x.name == table.name) {
                                                return newTable;
                                            }
                                            else {
                                                return x;
                                            }
                                        }),
                                    };
                                    {
                                        var builder = new template_1.ChartTemplateBuilder(store.chart, store.dataset, store.chartManager, CHARTICULATOR_PACKAGE.version);
                                        var template_2 = builder.build();
                                        var unmappedColumns_1 = [];
                                        template_2.tables[0].columns.forEach(function (column) {
                                            unmappedColumns_1 = unmappedColumns_1.concat(store.checkColumnsMapping(column, dataset_1.TableType.Main, newDataset));
                                        });
                                        if (template_2.tables[1]) {
                                            template_2.tables[1].columns.forEach(function (column) {
                                                unmappedColumns_1 = unmappedColumns_1.concat(store.checkColumnsMapping(column, dataset_1.TableType.Links, newDataset));
                                            });
                                        }
                                        var tableMapping_1 = new Map();
                                        tableMapping_1.set(template_2.tables[0].name, store.dataset.tables[0].name);
                                        if (template_2.tables[1] && store.dataset.tables[1]) {
                                            tableMapping_1.set(template_2.tables[1].name, store.dataset.tables[1].name);
                                        }
                                        // eslint-disable-next-line
                                        var loadTemplateIntoState_1 = function (store, tableMapping, columnMapping, template) {
                                            var e_1, _a, e_2, _b;
                                            var templateInstance = new container_1.ChartTemplate(template);
                                            try {
                                                for (var _c = __values(templateInstance.getDatasetSchema()), _d = _c.next(); !_d.done; _d = _c.next()) {
                                                    var table_1 = _d.value;
                                                    templateInstance.assignTable(table_1.name, tableMapping.get(table_1.name) || table_1.name);
                                                    try {
                                                        for (var _e = (e_2 = void 0, __values(table_1.columns)), _f = _e.next(); !_f.done; _f = _e.next()) {
                                                            var column = _f.value;
                                                            templateInstance.assignColumn(table_1.name, column.name, columnMapping.get(column.name) || column.name);
                                                        }
                                                    }
                                                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                                                    finally {
                                                        try {
                                                            if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                                                        }
                                                        finally { if (e_2) throw e_2.error; }
                                                    }
                                                }
                                            }
                                            catch (e_1_1) { e_1 = { error: e_1_1 }; }
                                            finally {
                                                try {
                                                    if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                                                }
                                                finally { if (e_1) throw e_1.error; }
                                            }
                                            var instance = templateInstance.instantiate(newDataset, false // no scale inference
                                            );
                                            store.dispatcher.dispatch(new actions_1.Actions.ImportChartAndDataset(instance.chart, newDataset, {}));
                                            store.dispatcher.dispatch(new actions_1.Actions.ReplaceDataset(newDataset));
                                        };
                                        if (unmappedColumns_1.length > 0) {
                                            _this.popupController.showModal(function (context) {
                                                return (React.createElement(controllers_1.ModalView, { context: context },
                                                    React.createElement("div", { onClick: function (e) { return e.stopPropagation(); } },
                                                        React.createElement(import_view_1.FileViewImport, { mode: import_view_1.MappingMode.ImportDataset, tables: template_2.tables, datasetTables: newDataset.tables, tableMapping: tableMapping_1, unmappedColumns: unmappedColumns_1, onSave: function (mapping) {
                                                                loadTemplateIntoState_1(store, tableMapping_1, mapping, template_2);
                                                                // TODO check mappings
                                                                context.close();
                                                            }, onClose: function () {
                                                                context.close();
                                                            } }))));
                                            }, { anchor: null });
                                        }
                                        else {
                                            store.dispatcher.dispatch(new actions_1.Actions.ReplaceDataset(newDataset));
                                        }
                                    }
                                };
                                reader.readAsText(file);
                            });
                        } })) : null,
                    React.createElement(react_1.DefaultButton, { iconProps: {
                            iconName: "More",
                        }, styles: buttonStyles, id: "charticulator__dataset-view-detail-" + this.props.table.displayName, title: strings_1.strings.dataset.showDataValues, 
                        // ={false}
                        onClick: function () {
                            _this.setState({
                                tableViewIsOpened: !_this.state.tableViewIsOpened,
                            });
                        } }),
                    this.state.tableViewIsOpened ? (React.createElement(react_1.Callout, { target: "#charticulator__dataset-view-detail-" + this.props.table.displayName, onDismiss: function () {
                            _this.setState({
                                tableViewIsOpened: false,
                            });
                        } },
                        React.createElement("div", { className: "charticulator__dataset-view-detail" },
                            React.createElement("h2", null, table.displayName || table.name),
                            React.createElement("p", null, strings_1.strings.dataset.dimensions(table.rows.length, table.columns.length)),
                            React.createElement(table_view_1.TableView, { table: table, onTypeChange: this.props.store.editorType === app_store_1.EditorType.Chart
                                    ? function (column, type) {
                                        var store = _this.props.store;
                                        store.dispatcher.dispatch(new actions_1.Actions.ConvertColumnDataType(table.name, column, type));
                                    }
                                    : null })))) : null),
                React.createElement("p", { className: "el-details" }, table.displayName || table.name),
                table.columns
                    .filter(function (c) { return !c.metadata.isRaw; })
                    .map(function (c, idx) { return (React.createElement(ColumnView, { key: "t" + idx, store: _this.props.store, table: _this.props.table, column: c })); }))));
    };
    return ColumnsView;
}(React.Component));
exports.ColumnsView = ColumnsView;
var ColumnViewProps = /** @class */ (function () {
    function ColumnViewProps() {
    }
    return ColumnViewProps;
}());
exports.ColumnViewProps = ColumnViewProps;
var ColumnViewState = /** @class */ (function () {
    function ColumnViewState() {
    }
    return ColumnViewState;
}());
exports.ColumnViewState = ColumnViewState;
var ColumnView = /** @class */ (function (_super) {
    __extends(ColumnView, _super);
    function ColumnView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isSelected: null,
            isExpanded: false,
        };
        return _this;
    }
    ColumnView.prototype.renderDerivedColumns = function () {
        var _this = this;
        var c = this.props.column;
        var derivedColumns = common_1.type2DerivedColumns[c.type];
        if (!derivedColumns) {
            return null;
        }
        return (React.createElement("div", { className: "charticulator__dataset-view-derived-fields" }, derivedColumns.map(function (desc) {
            var expr = core_1.Expression.functionCall(desc.function, core_1.Expression.variable(_this.props.column.name)).toString();
            var lambdaExpr = core_1.Expression.lambda(["x"], core_1.Expression.functionCall(desc.function, core_1.Expression.fields(core_1.Expression.variable("x"), _this.props.column.name))).toString();
            var type = desc.type;
            return _this.renderColumnControl(desc.name, R.getSVGIcon(common_1.kind2Icon[desc.metadata.kind]), expr, lambdaExpr, type, null, desc.metadata, undefined, expr, desc.displayName);
        })));
    };
    ColumnView.prototype.applyAggregation = function (expr, type, kind) {
        var aggregation = core_1.Expression.getDefaultAggregationFunction(type, kind);
        return core_1.Expression.functionCall(aggregation, core_1.Expression.parse(expr)).toString();
    };
    // eslint-disable-next-line max-lines-per-function
    ColumnView.prototype.renderColumnControl = function (label, icon, expr, lambdaExpr, type, additionalElement, metadata, onColumnKindChanged, rawColumnExpr, displayLabel) {
        var _this = this;
        if (additionalElement === void 0) { additionalElement = null; }
        var anchor;
        var onClickHandler = function () {
            if (!onColumnKindChanged) {
                return;
            }
            globals.popupController.popupAt(function (context) { return (React.createElement(controllers_1.PopupView, { key: label, context: context },
                React.createElement("div", null,
                    React.createElement(controls_1.DropdownListView, { selected: type, list: utils_1.getConvertableDataKind(type).map(function (type) {
                            return {
                                name: type.toString(),
                                text: type.toString(),
                                url: R.getSVGIcon(common_1.kind2Icon[type]),
                            };
                        }), context: context, onClick: function (value) {
                            onColumnKindChanged(label, value);
                        }, onClose: function () {
                            anchor === null || anchor === void 0 ? void 0 : anchor.focus();
                        } })))); }, {
                anchor: anchor,
                alignX: controllers_1.PopupAlignment.Outer,
                alignY: controllers_1.PopupAlignment.StartInner,
            });
        };
        return (React.createElement("div", { tabIndex: 0, key: label, className: "click-handler", ref: function (e) { return (anchor = e); }, onClick: onClickHandler, onKeyPress: function (e) {
                if (e.key === "Enter") {
                    onClickHandler();
                }
            } },
            React.createElement(components_1.DraggableElement, { key: expr, className: utils_1.classNames("charticulator__dataset-view-column", [
                    "is-active",
                    this.state.isSelected == expr,
                ]), onDragStart: function () { return _this.setState({ isSelected: expr }); }, onDragEnd: function () { return _this.setState({ isSelected: null }); }, dragData: function () {
                    _this.setState({ isSelected: expr });
                    var r = new actions_1.DragData.DataExpression(_this.props.table, _this.applyAggregation(expr, type, metadata.kind), type, __assign(__assign({}, metadata), { columnName: displayLabel !== null && displayLabel !== void 0 ? displayLabel : label }), rawColumnExpr
                        ? _this.applyAggregation(rawColumnExpr, specification_1.DataType.String, metadata.kind)
                        : _this.applyAggregation(expr, type, metadata.kind));
                    return r;
                }, renderDragElement: function () { return [
                    React.createElement("span", { className: "dragging-table-cell" }, expr),
                    { x: -10, y: -8 },
                ]; } },
                React.createElement(components_1.SVGImageIcon, { url: icon }),
                React.createElement("span", { className: "el-text" }, displayLabel !== null && displayLabel !== void 0 ? displayLabel : label),
                additionalElement)));
    };
    // eslint-disable-next-line
    ColumnView.prototype.render = function () {
        var _this = this;
        var c = this.props.column;
        var derivedColumnsControl = this.renderDerivedColumns();
        if (derivedColumnsControl != null) {
            return (React.createElement("div", null,
                this.renderColumnControl(c.name, R.getSVGIcon(common_1.kind2Icon[c.metadata.kind]), core_1.Expression.variable(c.name).toString(), core_1.Expression.lambda(["x"], core_1.Expression.fields(core_1.Expression.variable("x"), c.name)).toString(), c.type, React.createElement(components_1.ButtonFlat, { title: strings_1.strings.dataset.showDerivedFields, stopPropagation: true, url: this.state.isExpanded
                        ? R.getSVGIcon("ChevronDown")
                        : R.getSVGIcon("ChevronLeft"), onClick: function () {
                        _this.setState({ isExpanded: !_this.state.isExpanded });
                    } }), c.metadata, function (column, type) {
                    c.metadata.kind = type;
                    _this.forceUpdate();
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.UpdatePlotSegments());
                }, core_1.Expression.variable(c.metadata.rawColumnName || c.name).toString(), c.displayName),
                this.state.isExpanded ? derivedColumnsControl : null));
        }
        else {
            return this.renderColumnControl(c.name, R.getSVGIcon(common_1.kind2Icon[c.metadata.kind]), core_1.Expression.variable(c.name).toString(), core_1.Expression.lambda(["x"], core_1.Expression.fields(core_1.Expression.variable("x"), c.name)).toString(), c.type, null, c.metadata, function (column, type) {
                c.metadata.kind = type;
                _this.props.store.dispatcher.dispatch(new actions_1.Actions.UpdatePlotSegments());
                _this.forceUpdate();
            }, core_1.Expression.variable(c.metadata.rawColumnName || c.name).toString(), c.displayName);
        }
    };
    return ColumnView;
}(React.Component));
exports.ColumnView = ColumnView;
//# sourceMappingURL=dataset_view.js.map