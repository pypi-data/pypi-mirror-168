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
exports.ImportDataView = exports.FileUploader = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var R = require("../../resources");
var globals = require("../../globals");
var config_1 = require("../../config");
var core_1 = require("../../../core");
var utils_1 = require("../../utils");
var index_1 = require("../../components/index");
var icons_1 = require("../../components/icons");
var table_view_1 = require("../dataset/table_view");
var controllers_1 = require("../../controllers");
var dataset_1 = require("../../../core/dataset");
var stores_1 = require("../../stores");
var actions_1 = require("../../actions/actions");
var strings_1 = require("../../../strings");
var react_1 = require("@fluentui/react");
var FileUploader = /** @class */ (function (_super) {
    __extends(FileUploader, _super);
    function FileUploader(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            draggingOver: false,
            filename: props.filename,
        };
        return _this;
    }
    FileUploader.prototype.reset = function () {
        this.inputElement.value = null;
        this.setState({
            filename: null,
        });
    };
    FileUploader.prototype.onInputChange = function () {
        if (this.inputElement.files.length == 1) {
            this.setState({
                filename: this.inputElement.files[0].name,
            });
            if (this.props.onChange) {
                this.props.onChange(this.inputElement.files[0]);
            }
        }
    };
    FileUploader.prototype.showOpenFile = function () {
        this.reset();
        this.inputElement.click();
    };
    FileUploader.prototype.isDataTransferValid = function (dt) {
        if (dt && dt.items.length == 1) {
            if (dt.items[0].kind == "file") {
                return true;
            }
        }
        return false;
    };
    FileUploader.prototype.getFileFromDataTransfer = function (dt) {
        if (dt && dt.items.length == 1) {
            if (dt.items[0].kind == "file") {
                var file = dt.items[0].getAsFile();
                var ext = utils_1.getExtensionFromFileName(file.name);
                if (this.props.extensions.indexOf(ext) >= 0) {
                    return file;
                }
                else {
                    return null;
                }
            }
        }
        if (dt && dt.files.length == 1) {
            return dt.files[0];
        }
        return null;
    };
    FileUploader.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { tabIndex: 0, className: utils_1.classNames("charticulator__file-uploader", ["is-dragging-over", this.state.draggingOver], ["is-active", this.state.filename != null]), onClick: function () { return _this.showOpenFile(); }, onKeyPress: function (e) {
                if (e.key === "Enter") {
                    _this.showOpenFile();
                }
            }, onDragOver: function (e) {
                e.preventDefault();
                if (_this.isDataTransferValid(e.dataTransfer)) {
                    _this.setState({
                        draggingOver: true,
                    });
                }
            }, onDragLeave: function () {
                _this.setState({
                    draggingOver: false,
                });
            }, onDragExit: function () {
                _this.setState({
                    draggingOver: false,
                });
            }, onDrop: function (e) {
                e.preventDefault();
                _this.setState({
                    draggingOver: false,
                });
                var file = _this.getFileFromDataTransfer(e.dataTransfer);
                if (file != null) {
                    _this.setState({
                        filename: file.name,
                    });
                    if (_this.props.onChange) {
                        _this.props.onChange(file);
                    }
                }
            } },
            React.createElement("input", { style: { display: "none" }, accept: this.props.extensions.map(function (x) { return "." + x; }).join(","), ref: function (e) { return (_this.inputElement = e); }, type: "file", onChange: function () { return _this.onInputChange(); } }),
            this.state.filename == null ? (React.createElement("span", { className: "charticulator__file-uploader-prompt" },
                React.createElement(icons_1.SVGImageIcon, { url: R.getSVGIcon("toolbar/import") }),
                strings_1.strings.fileImport.fileUpload)) : (React.createElement("span", { className: "charticulator__file-uploader-filename" }, this.state.filename))));
    };
    return FileUploader;
}(React.Component));
exports.FileUploader = FileUploader;
var ImportDataView = /** @class */ (function (_super) {
    __extends(ImportDataView, _super);
    function ImportDataView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            dataTable: null,
            imagesTable: null,
            linkTable: null,
            dataTableOrigin: null,
            linkTableOrigin: null,
        };
        _this.props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () {
            if (_this.isComponentMounted) {
                _this.forceUpdate();
            }
        });
        return _this;
    }
    ImportDataView.prototype.componentDidMount = function () {
        this.isComponentMounted = true;
    };
    ImportDataView.prototype.componentWillUnmount = function () {
        this.isComponentMounted = false;
    };
    ImportDataView.prototype.loadFileAsTable = function (file) {
        var _this = this;
        return utils_1.readFileAsString(file).then(function (contents) {
            var localeFileFormat = _this.props.store.getLocaleFileFormat();
            var ext = utils_1.getExtensionFromFileName(file.name);
            var filename = utils_1.getFileNameWithoutExtension(file.name);
            var loader = new core_1.Dataset.DatasetLoader();
            switch (ext) {
                case "csv": {
                    var table_1 = loader.loadDSVFromContents(filename, contents, localeFileFormat);
                    // if table contains images split to separate table
                    var keyAndImageColumns_1 = table_1.columns.filter(function (column) {
                        return column.name === core_1.ImageKeyColumn ||
                            column.type === core_1.Dataset.DataType.Image;
                    });
                    if (keyAndImageColumns_1.length === 2) {
                        var imagesIds = table_1.rows.map(function (row) { return row === null || row === void 0 ? void 0 : row[core_1.ImageKeyColumn]; });
                        var uniqueIds = __spread(new Set(imagesIds));
                        var rows = uniqueIds.map(function (imageId) {
                            return table_1.rows.find(function (row) { return row[core_1.ImageKeyColumn] === imageId; });
                        });
                        var imageTable = __assign(__assign({}, table_1), { name: table_1.name + "Images", displayName: table_1.displayName + "Images", columns: keyAndImageColumns_1, rows: rows.map(function (row) {
                                var imageRow = {
                                    _id: row["_id"],
                                };
                                keyAndImageColumns_1.forEach(function (column) {
                                    imageRow[column.name] = row[column.name];
                                });
                                return imageRow;
                            }) });
                        table_1.columns = table_1.columns.filter(function (column) {
                            return column.type !== core_1.Dataset.DataType.Image &&
                                column.displayName !== core_1.ImageKeyColumn;
                        });
                        return [table_1, imageTable];
                    }
                    return [table_1, null];
                }
                case "tsv": {
                    return [
                        loader.loadDSVFromContents(filename, contents, {
                            delimiter: "\t",
                            numberFormat: localeFileFormat.numberFormat,
                            currency: null,
                            group: null,
                            utcTimeZone: true,
                        }),
                        null,
                    ];
                }
            }
        });
    };
    ImportDataView.prototype.renderTable = function (table, onTypeChange) {
        return (React.createElement("div", { className: "wide-content" },
            React.createElement(table_view_1.TableView, { table: table, maxRows: 5, onTypeChange: onTypeChange })));
    };
    // eslint-disable-next-line
    ImportDataView.prototype.render = function () {
        var _this = this;
        var sampleDatasetDiv;
        var sampleDatasets = config_1.getConfig().SampleDatasets;
        return (React.createElement("div", { className: "charticulator__import-data-view" },
            sampleDatasets != null ? (React.createElement("div", { ref: function (e) { return (sampleDatasetDiv = e); } },
                React.createElement(index_1.ButtonRaised, { text: strings_1.strings.fileImport.loadSample, onClick: function () {
                        globals.popupController.popupAt(function (context) {
                            return (React.createElement(controllers_1.PopupView, { context: context },
                                React.createElement("div", { className: "charticulator__sample-dataset-list" }, sampleDatasets.map(function (dataset) {
                                    return (React.createElement("div", { className: "charticulator__sample-dataset-list-item", key: dataset.name, onClick: function () {
                                            Promise.all(dataset.tables.map(function (table, index) {
                                                var loader = new core_1.Dataset.DatasetLoader();
                                                return loader
                                                    .loadDSVFromURL(table.url, _this.props.store.getLocaleFileFormat())
                                                    .then(function (r) {
                                                    r.name = table.name;
                                                    r.displayName = table.name;
                                                    r.type =
                                                        index == 0
                                                            ? dataset_1.TableType.Main
                                                            : dataset_1.TableType.Links; // assumes there are two tables only
                                                    return r;
                                                });
                                            })).then(function (tables) {
                                                context.close();
                                                var ds = {
                                                    name: dataset.name,
                                                    tables: tables,
                                                };
                                                _this.props.onConfirmImport(ds);
                                            });
                                        } },
                                        React.createElement("div", { className: "el-title" }, dataset.name),
                                        React.createElement("div", { className: "el-description" }, dataset.description)));
                                }))));
                        }, { anchor: sampleDatasetDiv });
                    } }))) : null,
            React.createElement("h2", null,
                "Data",
                this.state.dataTable ? ": " + this.state.dataTable.name : null),
            this.state.dataTable ? (React.createElement(React.Fragment, null,
                React.createElement("div", { className: "charticulator__import-data-view-table" },
                    this.renderTable(this.state.dataTable, function (column, type) {
                        var dataColumn = _this.state.dataTable.columns.find(function (col) { return col.name === column; });
                        var dataTableError = utils_1.convertColumns(_this.state.dataTable, dataColumn, _this.state.dataTableOrigin, type);
                        if (dataTableError) {
                            _this.props.store.dispatcher.dispatch(new actions_1.AddMessage("parsingDataError", {
                                text: dataTableError,
                            }));
                        }
                        else {
                            _this.setState({
                                dataTable: _this.state.dataTable,
                            });
                            dataColumn.type = type;
                            dataColumn.metadata.kind = utils_1.getPreferredDataKind(type);
                        }
                    }),
                    React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileImport.removeButtonText, iconProps: {
                            iconName: "ChromeClose",
                        }, styles: core_1.primaryButtonStyles, title: strings_1.strings.fileImport.removeButtonTitle, onClick: function () {
                            _this.setState({
                                dataTable: null,
                                dataTableOrigin: null,
                            });
                        } })),
                this.state.imagesTable ? (React.createElement("div", { className: "charticulator__import-data-view-table" }, this.renderTable(this.state.imagesTable, function (column, type) {
                    var dataColumn = _this.state.imagesTable.columns.find(function (col) { return col.name === column; });
                    var dataTableError = utils_1.convertColumns(_this.state.imagesTable, dataColumn, _this.state.dataTableOrigin, type);
                    if (dataTableError) {
                        _this.props.store.dispatcher.dispatch(new actions_1.AddMessage("parsingDataError", {
                            text: dataTableError,
                        }));
                    }
                    else {
                        _this.setState({
                            imagesTable: _this.state.imagesTable,
                        });
                        dataColumn.type = type;
                        dataColumn.metadata.kind = utils_1.getPreferredDataKind(type);
                    }
                }))) : null)) : (React.createElement(FileUploader, { extensions: ["csv", "tsv"], onChange: function (file) {
                    _this.loadFileAsTable(file).then(function (_a) {
                        var _b = __read(_a, 2), table = _b[0], imageTable = _b[1];
                        table.type = dataset_1.TableType.Main;
                        if (imageTable) {
                            imageTable.type = dataset_1.TableType.Image;
                        }
                        _this.checkKeyColumn(table, _this.state.linkTable);
                        _this.setState({
                            dataTable: table,
                            dataTableOrigin: core_1.deepClone(table),
                            imagesTable: imageTable,
                        });
                    });
                } })),
            React.createElement("h2", null,
                strings_1.strings.fileImport.links,
                this.state.linkTable ? ": " + this.state.linkTable.name : null),
            this.state.linkTable ? (React.createElement("div", { className: "charticulator__import-data-view-table" },
                this.renderTable(this.state.linkTable, function (column, type) {
                    var dataColumn = _this.state.linkTable.columns.find(function (col) { return col.name === column; });
                    var linkTableError = utils_1.convertColumns(_this.state.linkTable, dataColumn, _this.state.dataTableOrigin, type);
                    if (linkTableError) {
                        _this.props.store.dispatcher.dispatch(new actions_1.AddMessage("parsingDataError", {
                            text: linkTableError,
                        }));
                    }
                    _this.setState({
                        linkTable: _this.state.linkTable,
                        linkTableOrigin: _this.state.linkTable,
                    });
                }),
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileImport.removeButtonText, iconProps: {
                        iconName: "ChromeClose",
                    }, title: strings_1.strings.fileImport.removeButtonTitle, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.setState({
                            linkTable: null,
                            linkTableOrigin: null,
                        });
                        _this.checkSourceAndTargetColumns(null);
                        _this.checkKeyColumn(_this.state.dataTable, null);
                    } }))) : (React.createElement(FileUploader, { extensions: ["csv", "tsv"], onChange: function (file) {
                    _this.loadFileAsTable(file).then(function (_a) {
                        var _b = __read(_a, 1), table = _b[0];
                        table.type = dataset_1.TableType.Links;
                        _this.checkSourceAndTargetColumns(table);
                        _this.checkKeyColumn(_this.state.dataTable, table);
                        _this.setState({
                            linkTable: table,
                            linkTableOrigin: core_1.deepClone(table),
                        });
                    });
                } })),
            React.createElement("div", { className: "el-actions" },
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileImport.doneButtonText, iconProps: {
                        iconName: "CheckMark",
                    }, styles: core_1.primaryButtonStyles, title: strings_1.strings.fileImport.doneButtonTitle, disabled: this.state.dataTable == null ||
                        this.props.store.messageState.get("noID") !== undefined ||
                        this.props.store.messageState.get("noSourceOrTargetID") !==
                            undefined, onClick: function () {
                        if (_this.state.dataTable != null &&
                            _this.props.store.messageState.get("noID") === undefined &&
                            _this.props.store.messageState.get("noSourceOrTargetID") ===
                                undefined) {
                            var dataset = {
                                name: _this.state.dataTable.name,
                                tables: [_this.state.dataTable, _this.state.imagesTable].filter(function (table) { return table != null; }),
                            };
                            if (_this.state.linkTable != null) {
                                dataset.tables.push(_this.state.linkTable);
                            }
                            _this.props.onConfirmImport(dataset);
                        }
                    } })),
            React.createElement("div", { className: "charticulator__credits" },
                React.createElement("p", { dangerouslySetInnerHTML: {
                        __html: config_1.getConfig().LegalNotices &&
                            config_1.getConfig().LegalNotices.privacyStatementHTML,
                    } }))));
    };
    ImportDataView.prototype.checkSourceAndTargetColumns = function (table) {
        var countOfKeyColumns = table &&
            table.columns.filter(function (column) {
                return column.name === core_1.LinkSourceKeyColumn ||
                    column.name === core_1.LinkTargetKeyColumn;
            }).length;
        if (table && countOfKeyColumns < 2) {
            this.props.store.dispatcher.dispatch(new actions_1.AddMessage("noSourceOrTargetID", {
                text: strings_1.strings.fileImport.messageNoSourceOrTargetID(core_1.LinkSourceKeyColumn, core_1.LinkTargetKeyColumn),
            }));
        }
        else {
            this.props.store.dispatcher.dispatch(new actions_1.RemoveMessage("noSourceOrTargetID"));
        }
    };
    ImportDataView.prototype.checkKeyColumn = function (mainTable, linksTable) {
        var isKeyColumn = mainTable &&
            mainTable.columns.find(function (column) { return column.name === core_1.KeyColumn; });
        if (!isKeyColumn && linksTable) {
            this.props.store.dispatcher.dispatch(new actions_1.AddMessage("noID", {
                text: strings_1.strings.fileImport.messageNoID(core_1.KeyColumn),
            }));
        }
        else {
            this.props.store.dispatcher.dispatch(new actions_1.RemoveMessage("noID"));
        }
    };
    return ImportDataView;
}(React.Component));
exports.ImportDataView = ImportDataView;
//# sourceMappingURL=import_data_view.js.map