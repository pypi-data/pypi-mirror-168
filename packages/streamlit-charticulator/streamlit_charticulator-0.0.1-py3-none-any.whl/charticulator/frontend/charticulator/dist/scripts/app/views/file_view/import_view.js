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
Object.defineProperty(exports, "__esModule", { value: true });
exports.FileViewImport = exports.MappingMode = void 0;
var React = require("react");
var components_1 = require("../../components");
var context_component_1 = require("../../context_component");
var controls_1 = require("../panels/widgets/controls");
var dataset_1 = require("../../../core/dataset/dataset");
var strings_1 = require("../../../strings");
var MappingMode;
(function (MappingMode) {
    MappingMode[MappingMode["ImportTemplate"] = 0] = "ImportTemplate";
    MappingMode[MappingMode["ImportDataset"] = 1] = "ImportDataset";
})(MappingMode = exports.MappingMode || (exports.MappingMode = {}));
var FileViewImport = /** @class */ (function (_super) {
    __extends(FileViewImport, _super);
    function FileViewImport() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            columnMappings: new Map(),
        };
        return _this;
    }
    // eslint-disable-next-line
    FileViewImport.prototype.render = function () {
        var _this = this;
        var tables = this.props.tables;
        var newMapping = new Map(this.state.columnMappings);
        var getDefaultValue = function (name) { return function () {
            var mapped = newMapping.get(name);
            if (mapped) {
                return mapped;
            }
            return strings_1.strings.templateImport.unmapped;
        }; };
        var onChange = function (columnName) { return function (value) {
            newMapping.set(columnName, value);
            _this.setState({
                columnMappings: newMapping,
            });
        }; };
        tables.forEach(function (table, tableIndex) {
            var _a;
            var filteredByTableColumns = (_a = _this.props.datasetTables[tableIndex]) === null || _a === void 0 ? void 0 : _a.columns;
            if (!filteredByTableColumns) {
                return;
            }
            var usedColumns = new Set();
            // match columns by name and type
            table.columns.forEach(function (column) {
                filteredByTableColumns.forEach(function (pbiColumn) {
                    if (pbiColumn.displayName === column.name &&
                        (column.type === pbiColumn.type ||
                            column.type === dataset_1.DataType.String) &&
                        !newMapping.get(column.name)) {
                        newMapping.set(column.name, pbiColumn.name);
                        usedColumns.add(pbiColumn);
                    }
                });
            });
            // match columns by type
            table.columns.forEach(function (column) {
                // Set default column by type
                if (!newMapping.get(column.name)) {
                    filteredByTableColumns.forEach(function (pbiColumn) {
                        if (column.type === pbiColumn.type && !usedColumns.has(pbiColumn)) {
                            newMapping.set(column.name, pbiColumn.name);
                            usedColumns.add(pbiColumn);
                        }
                    });
                }
            });
        });
        return (React.createElement(components_1.FloatingPanel, { floatInCenter: true, scroll: true, peerGroup: "import", title: strings_1.strings.templateImport.title, closeButtonIcon: "ChromeClose", height: 600, width: 800, onClose: this.props.onClose },
            React.createElement("section", { className: "charticulator__file-view-mapping_view" },
                React.createElement("section", null,
                    tables &&
                        tables.map(function (table) {
                            return (React.createElement("div", { className: "charticulator__file-view-mapping_table", key: table.name },
                                React.createElement("h4", null, _this.props.mode === MappingMode.ImportTemplate
                                    ? strings_1.strings.templateImport.usbtitleImportTemplate
                                    : strings_1.strings.templateImport.usbtitleImportData),
                                React.createElement("table", { className: "charticulator__file-view-mapping_table" },
                                    React.createElement("thead", null,
                                        React.createElement("tr", { className: "charticulator__file-view-mapping_rows" },
                                            React.createElement("th", { className: "charticulator__file-view-mapping_row_item" }, _this.props.mode === MappingMode.ImportTemplate
                                                ? strings_1.strings.templateImport.columnNameTemplate
                                                : strings_1.strings.templateImport.columnNameChart),
                                            React.createElement("th", { className: "charticulator__file-view-mapping_row_item" }, strings_1.strings.templateImport.dataType),
                                            React.createElement("th", { className: "charticulator__file-view-mapping_row_item" }, strings_1.strings.templateImport.examples),
                                            React.createElement("th", { className: "charticulator__file-view-mapping_row_item" }, strings_1.strings.templateImport.mapped))),
                                    React.createElement("tbody", null, table.columns.map(function (column) {
                                        var datasetTable = _this.props.datasetTables.find(function (t) {
                                            return t.name ===
                                                (_this.props.tableMapping.get(table.name) ||
                                                    table.name);
                                        });
                                        var optionValues = (datasetTable === null || datasetTable === void 0 ? void 0 : datasetTable.columns.filter(function (pbiColumn) {
                                            return pbiColumn.type === column.type ||
                                                column.type === dataset_1.DataType.String;
                                        }).map(function (pbiColumn) {
                                            return pbiColumn.displayName;
                                        })) || [];
                                        return (React.createElement(React.Fragment, { key: table.name + "-" + column.name },
                                            React.createElement("tr", { className: "charticulator__file-view-mapping_rows" },
                                                " ",
                                                React.createElement("td", { className: "charticulator__file-view-mapping_row_item" }, column.name),
                                                React.createElement("td", { className: "charticulator__file-view-mapping_row_item" }, strings_1.strings.typeDisplayNames[column.type]),
                                                React.createElement("td", { className: "charticulator__file-view-mapping_row_item" }, column.metadata.examples),
                                                React.createElement("td", { className: "charticulator__file-view-mapping_row_item" },
                                                    React.createElement(controls_1.Select, { labels: optionValues, icons: null, options: optionValues, value: getDefaultValue(column.name)().toString(), showText: true, onChange: onChange(column.name) })))));
                                    })))));
                        }),
                    React.createElement("div", { className: "charticulator__file-view-mapping_row_button_toolbar" },
                        React.createElement(components_1.ButtonRaised, { onClick: function () {
                                _this.props.onClose();
                            }, text: strings_1.strings.button.cancel }),
                        React.createElement(components_1.ButtonRaised, { onClick: function () {
                                if (_this.props.unmappedColumns.filter(function (unmapped) {
                                    return _this.state.columnMappings.get(unmapped.name) ===
                                        undefined;
                                }).length === 0) {
                                    _this.props.onSave(_this.state.columnMappings);
                                }
                            }, text: strings_1.strings.templateImport.save, disabled: this.props.unmappedColumns.filter(function (unmapped) {
                                return _this.state.columnMappings.get(unmapped.name) === undefined;
                            }).length !== 0 }))))));
    };
    return FileViewImport;
}(context_component_1.ContextedComponent));
exports.FileViewImport = FileViewImport;
//# sourceMappingURL=import_view.js.map