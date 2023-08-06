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
exports.MenuBar = exports.HelpButton = void 0;
var React = require("react");
var ReactDOM = require("react-dom");
var globals = require("../globals");
var R = require("../resources");
var react_1 = require("@fluentui/react");
var core_1 = require("../../core");
var actions_1 = require("../actions");
var components_1 = require("../components");
var context_component_1 = require("../context_component");
var controllers_1 = require("../controllers");
var file_view_1 = require("./file_view");
var stores_1 = require("../stores");
var utils_1 = require("../utils");
var container_1 = require("../../container");
var dataset_1 = require("../../core/dataset");
var import_view_1 = require("./file_view/import_view");
var strings_1 = require("../../strings");
var main_view_1 = require("../main_view");
var config_1 = require("../config");
var app_store_1 = require("../stores/app_store");
var delete_dialog_1 = require("./panels/delete_dialog");
var HelpButton = /** @class */ (function (_super) {
    __extends(HelpButton, _super);
    function HelpButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HelpButton.prototype.render = function () {
        var _this = this;
        var _a;
        var contactUsLinkProps = {
            onClick: (_a = this.props.handlers) === null || _a === void 0 ? void 0 : _a.onContactUsLink,
        };
        if (!contactUsLinkProps.onClick) {
            contactUsLinkProps.href =
                config_1.getConfig().ContactUsHref || "mailto:charticulator@microsoft.com";
        }
        return (React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/help"), title: strings_1.strings.menuBar.help, ref: "helpButton", onClick: function () {
                globals.popupController.popupAt(function (context) {
                    return (React.createElement(controllers_1.PopupView, { context: context, className: "charticulator__menu-popup" },
                        React.createElement("div", { className: "charticulator__menu-dropdown", onClick: function () { return context.close(); } },
                            React.createElement("div", { className: "el-item" },
                                React.createElement("a", { target: "_blank", href: "https://charticulator.com/docs/getting-started.html" }, strings_1.strings.help.gettingStarted)),
                            React.createElement("div", { className: "el-item" },
                                React.createElement("a", { target: "_blank", href: "https://charticulator.com/gallery/index.html" }, strings_1.strings.help.gallery)),
                            _this.props.hideReportIssues ? null : (React.createElement("div", { className: "el-item" },
                                React.createElement("a", { target: "_blank", href: "https://github.com/Microsoft/charticulator/issues/new" }, strings_1.strings.help.issues))),
                            React.createElement("div", { className: "el-item" },
                                React.createElement("a", { target: "_blank", href: "https://charticulator.com/" }, strings_1.strings.help.home)),
                            React.createElement("div", { className: "el-item" },
                                React.createElement("a", __assign({}, contactUsLinkProps), strings_1.strings.help.contact)),
                            React.createElement("div", { className: "el-item-version" }, strings_1.strings.help.version(CHARTICULATOR_PACKAGE.version)))));
                }, {
                    anchor: ReactDOM.findDOMNode(_this.refs.helpButton),
                    alignX: controllers_1.PopupAlignment.EndInner,
                });
            } }));
    };
    return HelpButton;
}(React.Component));
exports.HelpButton = HelpButton;
var MenuBar = /** @class */ (function (_super) {
    __extends(MenuBar, _super);
    function MenuBar(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.popupController = new controllers_1.PopupController();
        _this.keyboardMap = {
            "ctrl-z": "undo",
            "ctrl-y": "redo",
            "ctrl-s": "save",
            "ctrl-shift-s": "export",
            "ctrl-n": "new",
            "ctrl-o": "open",
            backspace: "delete",
            delete: "delete",
            escape: "escape",
        };
        _this.onKeyDown = function (e) {
            if (e.target == document.body) {
                var prefix = "";
                if (e.shiftKey) {
                    prefix = "shift-" + prefix;
                }
                if (e.ctrlKey || e.metaKey) {
                    prefix = "ctrl-" + prefix;
                }
                var name_1 = ("" + prefix + e.key).toLowerCase();
                if (_this.keyboardMap[name_1]) {
                    var command = _this.keyboardMap[name_1];
                    switch (command) {
                        case "new":
                            {
                                _this.showFileModalWindow(file_view_1.MainTabs.open);
                            }
                            break;
                        case "open":
                            {
                                _this.showFileModalWindow(file_view_1.MainTabs.open);
                            }
                            break;
                        case "save":
                            {
                                if (_this.context.store.editorType == app_store_1.EditorType.Nested ||
                                    _this.context.store.editorType == app_store_1.EditorType.Embedded ||
                                    _this.context.store.editorType == app_store_1.EditorType.NestedEmbedded) {
                                    _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_EDIT);
                                }
                                else {
                                    if (_this.context.store.currentChartID) {
                                        _this.dispatch(new actions_1.Actions.Save());
                                    }
                                    else {
                                        _this.showFileModalWindow(file_view_1.MainTabs.save);
                                    }
                                }
                            }
                            break;
                        case "export":
                            {
                                _this.showFileModalWindow(file_view_1.MainTabs.export);
                            }
                            break;
                        case "undo":
                            {
                                new actions_1.Actions.Undo().dispatch(_this.context.store.dispatcher);
                            }
                            break;
                        case "redo":
                            {
                                new actions_1.Actions.Redo().dispatch(_this.context.store.dispatcher);
                            }
                            break;
                        case "delete":
                            {
                                _this.store.deleteSelection();
                            }
                            break;
                        case "escape":
                            {
                                _this.store.handleEscapeKey();
                            }
                            break;
                    }
                    e.preventDefault();
                }
            }
        };
        _this.state = {
            showSaveDialog: false,
        };
        return _this;
    }
    MenuBar.prototype.componentDidMount = function () {
        var _this = this;
        window.addEventListener("keydown", this.onKeyDown);
        this.editor = this.context.store.addListener(stores_1.AppStore.EVENT_IS_NESTED_EDITOR, function () { return _this.forceUpdate(); });
        this.graphics = this.context.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); });
    };
    MenuBar.prototype.componentWillUnmount = function () {
        window.removeEventListener("keydown", this.onKeyDown);
        this.editor.remove();
        this.graphics.remove();
    };
    MenuBar.prototype.hideFileModalWindow = function () {
        globals.popupController.reset();
    };
    MenuBar.prototype.showFileModalWindow = function (defaultTab) {
        var _this = this;
        if (defaultTab === void 0) { defaultTab = file_view_1.MainTabs.open; }
        if (this.context.store.disableFileView) {
            return;
        }
        globals.popupController.showModal(function (context) {
            return (React.createElement(controllers_1.ModalView, { context: context },
                React.createElement(file_view_1.FileView, { backend: _this.context.store.backend, defaultTab: defaultTab, store: _this.context.store, onClose: function () { return context.close(); } })));
        }, { anchor: null });
    };
    MenuBar.prototype.renderSaveNested = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null,
            React.createElement(react_1.Dialog, { dialogContentProps: {
                    title: strings_1.strings.dialogs.saveChanges.saveChangesTitle,
                    subText: strings_1.strings.dialogs.saveChanges.saveChanges("chart"),
                }, hidden: !this.state.showSaveDialog, minWidth: "80%", onDismiss: function () {
                    _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_CLOSE);
                } },
                React.createElement(react_1.DialogFooter, null,
                    React.createElement(react_1.PrimaryButton, { styles: container_1.primaryButtonStyles, onClick: function () {
                            _this.setState({
                                showSaveDialog: false,
                            });
                            _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_EDIT);
                            setTimeout(function () {
                                return _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_CLOSE);
                            });
                        }, text: strings_1.strings.menuBar.saveButton }),
                    React.createElement(react_1.DefaultButton, { onClick: function () {
                            _this.setState({
                                showSaveDialog: false,
                            });
                            _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_CLOSE);
                        }, text: strings_1.strings.menuBar.dontSaveButton }))),
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/save"), text: strings_1.strings.menuBar.saveNested, title: strings_1.strings.menuBar.save, onClick: function () {
                    _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_EDIT);
                    _this.setState({
                        showSaveDialog: false,
                    });
                } }),
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/cross"), text: strings_1.strings.menuBar.closeNested, title: strings_1.strings.menuBar.closeNested, onClick: function () {
                    if (_this.store.chartManager.hasUnsavedChanges()) {
                        _this.setState({
                            showSaveDialog: true,
                        });
                    }
                    else {
                        _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_CLOSE);
                        _this.setState({
                            showSaveDialog: false,
                        });
                    }
                } }),
            React.createElement("span", { className: "charticulator__menu-bar-separator" })));
    };
    // eslint-disable-next-line
    MenuBar.prototype.renderImportButton = function (props) {
        var _this = this;
        var _a;
        return (React.createElement(React.Fragment, null,
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/import-template"), text: "", title: strings_1.strings.menuBar.importTemplate, onClick: ((_a = props.handlers) === null || _a === void 0 ? void 0 : _a.onImportTemplateClick) ||
                    // eslint-disable-next-line
                    (function () {
                        var inputElement = document.createElement("input");
                        inputElement.type = "file";
                        var file = null;
                        inputElement.accept = ["tmplt", "json"]
                            .map(function (x) { return "." + x; })
                            .join(",");
                        // eslint-disable-next-line
                        inputElement.onchange = function () {
                            if (inputElement.files.length == 1) {
                                file = inputElement.files[0];
                                if (file) {
                                    // eslint-disable-next-line
                                    utils_1.readFileAsString(file).then(function (str) {
                                        var data = JSON.parse(str);
                                        var unmappedColumns = [];
                                        data.tables[0].columns.forEach(function (column) {
                                            unmappedColumns = unmappedColumns.concat(_this.store.checkColumnsMapping(column, dataset_1.TableType.Main, _this.store.dataset));
                                        });
                                        if (data.tables[1]) {
                                            data.tables[1].columns.forEach(function (column) {
                                                unmappedColumns = unmappedColumns.concat(_this.store.checkColumnsMapping(column, dataset_1.TableType.Links, _this.store.dataset));
                                            });
                                        }
                                        var tableMapping = new Map();
                                        tableMapping.set(data.tables[0].name, _this.store.dataset.tables[0].name);
                                        if (data.tables[1] && _this.store.dataset.tables[1]) {
                                            tableMapping.set(data.tables[1].name, _this.store.dataset.tables[1].name);
                                        }
                                        var loadTemplateIntoState = function (tableMapping, columnMapping) {
                                            var e_1, _a, e_2, _b;
                                            var template = new container_1.ChartTemplate(data);
                                            try {
                                                for (var _c = __values(template.getDatasetSchema()), _d = _c.next(); !_d.done; _d = _c.next()) {
                                                    var table = _d.value;
                                                    template.assignTable(table.name, tableMapping.get(table.name) || table.name);
                                                    try {
                                                        for (var _e = (e_2 = void 0, __values(table.columns)), _f = _e.next(); !_f.done; _f = _e.next()) {
                                                            var column = _f.value;
                                                            template.assignColumn(table.name, column.name, columnMapping.get(column.name) || column.name);
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
                                            var instance = template.instantiate(_this.store.dataset, false // no scale inference
                                            );
                                            _this.store.dispatcher.dispatch(new actions_1.Actions.ImportChartAndDataset(instance.chart, _this.store.dataset, {}));
                                            _this.store.dispatcher.dispatch(new actions_1.Actions.ReplaceDataset(_this.store.dataset));
                                        };
                                        if (unmappedColumns.length > 0) {
                                            // mapping show dialog then call loadTemplateIntoState
                                            _this.popupController.showModal(function (context) {
                                                return (React.createElement(controllers_1.ModalView, { context: context },
                                                    React.createElement("div", { onClick: function (e) { return e.stopPropagation(); } },
                                                        React.createElement(import_view_1.FileViewImport, { mode: import_view_1.MappingMode.ImportTemplate, tables: data.tables, datasetTables: _this.store.dataset.tables, tableMapping: tableMapping, unmappedColumns: unmappedColumns, onSave: function (mapping) {
                                                                loadTemplateIntoState(tableMapping, mapping);
                                                                context.close();
                                                            }, onClose: function () {
                                                                context.close();
                                                            } }))));
                                            }, { anchor: null });
                                        }
                                        else {
                                            loadTemplateIntoState(tableMapping, new Map());
                                        }
                                    });
                                }
                            }
                        };
                        inputElement.click();
                    }) })));
    };
    MenuBar.prototype.renderExportButton = function (props) {
        var _this = this;
        var _a;
        return (React.createElement(React.Fragment, null,
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/export-template"), text: "", title: strings_1.strings.menuBar.exportTemplate, onClick: ((_a = props.handlers) === null || _a === void 0 ? void 0 : _a.onExportTemplateClick) ||
                    (function () {
                        var e_3, _a;
                        var template = core_1.deepClone(_this.store.buildChartTemplate());
                        var target = _this.store.createExportTemplateTarget(strings_1.strings.menuBar.defaultTemplateName, template);
                        var targetProperties = {};
                        try {
                            for (var _b = __values(target.getProperties()), _c = _b.next(); !_c.done; _c = _b.next()) {
                                var property = _c.value;
                                targetProperties[property.name] =
                                    _this.store.getPropertyExportName(property.name) ||
                                        property.default;
                            }
                        }
                        catch (e_3_1) { e_3 = { error: e_3_1 }; }
                        finally {
                            try {
                                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                            }
                            finally { if (e_3) throw e_3.error; }
                        }
                        _this.dispatch(new actions_1.Actions.ExportTemplate("", target, targetProperties));
                    }) })));
    };
    MenuBar.prototype.renderCopyToClipboard = function (props) {
        var _a;
        return (React.createElement(React.Fragment, null,
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("Copy"), text: "", title: strings_1.strings.menuBar.copyTemplate, onClick: (_a = props.handlers) === null || _a === void 0 ? void 0 : _a.onCopyToClipboardClick })));
    };
    MenuBar.prototype.renderSaveEmbedded = function () {
        var _this = this;
        var hasUnsavedChanges = this.store.chartManager.hasUnsavedChanges();
        return (React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/save"), text: strings_1.strings.menuBar.saveButton, disabled: !hasUnsavedChanges, title: strings_1.strings.menuBar.save, onClick: function () {
                _this.context.store.dispatcher.dispatch(new actions_1.Actions.UpdatePlotSegments());
                _this.context.store.dispatcher.dispatch(new actions_1.Actions.UpdateDataAxis());
                _this.context.store.emit(stores_1.AppStore.EVENT_NESTED_EDITOR_EDIT);
            } }));
    };
    MenuBar.prototype.renderDelete = function () {
        return React.createElement(delete_dialog_1.DeleteDialog, { context: this.context });
    };
    MenuBar.prototype.renderNewOpenSave = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null,
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/new"), title: strings_1.strings.menuBar.new, onClick: function () {
                    _this.showFileModalWindow(file_view_1.MainTabs.new);
                } }),
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/open"), title: strings_1.strings.menuBar.open, onClick: function () {
                    _this.showFileModalWindow(file_view_1.MainTabs.open);
                } }),
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/save"), title: strings_1.strings.menuBar.save, text: strings_1.strings.menuBar.saveButton, onClick: function () {
                    if (_this.context.store.currentChartID) {
                        _this.dispatch(new actions_1.Actions.Save());
                    }
                    else {
                        _this.showFileModalWindow(file_view_1.MainTabs.save);
                    }
                } }),
            this.renderImportButton(this.props),
            React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/export"), title: strings_1.strings.menuBar.export, onClick: function () {
                    _this.showFileModalWindow(file_view_1.MainTabs.export);
                } })));
    };
    MenuBar.prototype.toolbarButtons = function (props) {
        var _this = this;
        return (React.createElement(React.Fragment, null,
            this.context.store.editorType === app_store_1.EditorType.Chart
                ? this.renderNewOpenSave()
                : null,
            this.context.store.editorType === app_store_1.EditorType.Embedded &&
                props.alignSaveButton === props.alignButtons
                ? this.renderSaveEmbedded()
                : null,
            this.context.store.editorType === app_store_1.EditorType.Embedded ||
                this.context.store.editorType === app_store_1.EditorType.NestedEmbedded ? (React.createElement(React.Fragment, null,
                React.createElement("span", { className: "charticulator__menu-bar-separator" }),
                this.renderImportButton(props),
                this.renderExportButton(props),
                this.renderCopyToClipboard(props))) : null,
            React.createElement("span", { className: "charticulator__menu-bar-separator" }),
            this.props.undoRedoLocation === main_view_1.UndoRedoLocation.MenuBar ? (React.createElement(React.Fragment, null,
                React.createElement(components_1.MenuButton, { url: R.getSVGIcon("Undo"), title: strings_1.strings.menuBar.undo, disabled: this.context.store.historyManager.statesBefore.length === 0, onClick: function () {
                        return new actions_1.Actions.Undo().dispatch(_this.context.store.dispatcher);
                    } }),
                React.createElement(components_1.MenuButton, { url: R.getSVGIcon("Redo"), title: strings_1.strings.menuBar.redo, disabled: this.context.store.historyManager.statesAfter.length === 0, onClick: function () {
                        return new actions_1.Actions.Redo().dispatch(_this.context.store.dispatcher);
                    } }))) : null,
            React.createElement("span", { className: "charticulator__menu-bar-separator" }),
            this.renderDelete()));
    };
    MenuBar.prototype.toolbarTabButtons = function (props) {
        var _a;
        return (React.createElement(React.Fragment, null, (_a = props.tabButtons) === null || _a === void 0 ? void 0 : _a.map(function (button) {
            return (React.createElement(React.Fragment, null,
                React.createElement("span", { className: "charticulator__menu-bar-separator" }),
                React.createElement(components_1.MenuButton, { url: R.getSVGIcon(button.icon), title: button.tooltip, onClick: button.onClick, text: button.text, disabled: !button.active })));
        })));
    };
    MenuBar.prototype.render = function () {
        var _this = this;
        var _a;
        return (React.createElement(React.Fragment, null,
            React.createElement(controllers_1.PopupContainer, { controller: this.popupController }),
            React.createElement("section", { className: "charticulator__menu-bar" },
                React.createElement("div", { className: "charticulator__menu-bar-left" },
                    this.context.store.editorType === app_store_1.EditorType.Embedded ||
                        this.context.store.editorType ===
                            app_store_1.EditorType.NestedEmbedded ? null : (React.createElement(components_1.AppButton, { name: this.props.name, title: strings_1.strings.menuBar.home, onClick: function () { return _this.showFileModalWindow(file_view_1.MainTabs.open); } })),
                    this.props.alignButtons === main_view_1.PositionsLeftRight.Left ? (React.createElement(React.Fragment, null,
                        React.createElement("span", { className: "charticulator__menu-bar-separator" }),
                        this.toolbarButtons(this.props))) : null,
                    this.context.store.editorType === app_store_1.EditorType.Embedded &&
                        this.props.alignSaveButton == main_view_1.PositionsLeftRight.Left &&
                        this.props.alignSaveButton !== this.props.alignButtons
                        ? this.renderSaveEmbedded()
                        : null,
                    this.context.store.editorType === app_store_1.EditorType.Embedded &&
                        this.props.tabButtons
                        ? this.toolbarTabButtons(this.props)
                        : null,
                    this.context.store.editorType === app_store_1.EditorType.Nested ||
                        this.context.store.editorType === app_store_1.EditorType.NestedEmbedded
                        ? this.renderSaveNested()
                        : null),
                React.createElement("div", { className: "charticulator__menu-bar-center el-text" },
                    React.createElement("p", { className: utils_1.classNames("charticulator__menu-bar-center", [
                            "nested-chart",
                            this.context.store.editorType === app_store_1.EditorType.NestedEmbedded,
                        ]) }, "" + ((_a = this.context.store.chart) === null || _a === void 0 ? void 0 : _a.properties.name) + (this.context.store.editorType === app_store_1.EditorType.Embedded ||
                        this.context.store.editorType === app_store_1.EditorType.NestedEmbedded
                        ? " - " + this.props.name || strings_1.strings.app.name
                        : ""))),
                React.createElement("div", { className: "charticulator__menu-bar-right" },
                    this.props.alignButtons === main_view_1.PositionsLeftRight.Right ? (React.createElement(React.Fragment, null,
                        this.toolbarButtons(this.props),
                        React.createElement("span", { className: "charticulator__menu-bar-separator" }))) : null,
                    (this.context.store.editorType === app_store_1.EditorType.Embedded ||
                        this.context.store.editorType === app_store_1.EditorType.NestedEmbedded) &&
                        this.props.alignSaveButton == main_view_1.PositionsLeftRight.Right &&
                        this.props.alignSaveButton !== this.props.alignButtons
                        ? this.renderSaveEmbedded()
                        : null,
                    React.createElement(HelpButton, { handlers: this.props.handlers, hideReportIssues: false })))));
    };
    return MenuBar;
}(context_component_1.ContextedComponent));
exports.MenuBar = MenuBar;
//# sourceMappingURL=menubar.js.map