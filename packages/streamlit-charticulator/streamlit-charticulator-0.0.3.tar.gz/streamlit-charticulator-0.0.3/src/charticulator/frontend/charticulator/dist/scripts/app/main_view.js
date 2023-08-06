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
exports.MainView = exports.LayoutDirection = exports.PositionsLeftRightTop = exports.PositionsLeftRight = exports.UndoRedoLocation = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var globals = require("./globals");
var components_1 = require("./components");
var controllers_1 = require("./controllers");
var stores_1 = require("./stores");
var views_1 = require("./views");
var menubar_1 = require("./views/menubar");
var object_list_editor_1 = require("./views/panels/object_list_editor");
var scales_panel_1 = require("./views/panels/scales_panel");
var strings_1 = require("../strings");
var fluentui_tool_bar_1 = require("./views/fluentui_tool_bar");
var context_component_1 = require("./context_component");
var UndoRedoLocation;
(function (UndoRedoLocation) {
    UndoRedoLocation["MenuBar"] = "menubar";
    UndoRedoLocation["ToolBar"] = "toolbar";
})(UndoRedoLocation = exports.UndoRedoLocation || (exports.UndoRedoLocation = {}));
var PositionsLeftRight;
(function (PositionsLeftRight) {
    PositionsLeftRight["Left"] = "left";
    PositionsLeftRight["Right"] = "right";
})(PositionsLeftRight = exports.PositionsLeftRight || (exports.PositionsLeftRight = {}));
var PositionsLeftRightTop;
(function (PositionsLeftRightTop) {
    PositionsLeftRightTop["Left"] = "left";
    PositionsLeftRightTop["Right"] = "right";
    PositionsLeftRightTop["Top"] = "top";
})(PositionsLeftRightTop = exports.PositionsLeftRightTop || (exports.PositionsLeftRightTop = {}));
var LayoutDirection;
(function (LayoutDirection) {
    LayoutDirection["Vertical"] = "vertical";
    LayoutDirection["Horizontal"] = "horizontal";
})(LayoutDirection = exports.LayoutDirection || (exports.LayoutDirection = {}));
var MainView = /** @class */ (function (_super) {
    __extends(MainView, _super);
    function MainView(props) {
        var _this = _super.call(this, props) || this;
        if (!props.viewConfiguration) {
            _this.viewConfiguration = {
                ColumnsPosition: PositionsLeftRight.Left,
                EditorPanelsPosition: PositionsLeftRight.Left,
                ToolbarPosition: PositionsLeftRightTop.Top,
                MenuBarButtons: PositionsLeftRight.Left,
                MenuBarSaveButtons: PositionsLeftRight.Left,
                ToolbarLabels: true,
                UndoRedoLocation: UndoRedoLocation.MenuBar,
            };
        }
        else {
            _this.viewConfiguration = props.viewConfiguration;
        }
        _this.state = {
            glyphViewMaximized: false,
            layersViewMaximized: false,
            attributeViewMaximized: false,
            scaleViewMaximized: false,
            currentFocusComponentIndex: 0,
        };
        props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); });
        return _this;
    }
    MainView.prototype.shortcutKeyHandler = function (e) {
        if (e.ctrlKey && e.key === "F6") {
            var focusableComponents = this.getFocusableComponents();
            var newIndex = this.state.currentFocusComponentIndex;
            focusableComponents[newIndex].setAttribute("tabIndex", null);
            if (e.shiftKey) {
                newIndex = this.state.currentFocusComponentIndex - 1;
            }
            else {
                newIndex = this.state.currentFocusComponentIndex + 1;
            }
            if (newIndex >= focusableComponents.length) {
                newIndex = 0;
            }
            if (newIndex < 0) {
                newIndex = focusableComponents.length - 1;
            }
            this.setState({
                currentFocusComponentIndex: newIndex,
            });
            focusableComponents[newIndex].setAttribute("tabIndex", "0");
            focusableComponents[newIndex].focus();
            console.log("current index", newIndex);
        }
    };
    MainView.prototype.componentDidMount = function () {
        document.addEventListener("keydown", this.shortcutKeyHandler.bind(this));
    };
    MainView.prototype.getFocusableComponents = function () {
        return document.querySelectorAll(".charticulator__menu-bar,.charticulator__toolbar-horizontal,.minimizable-pane,.charticulator__floating-panel");
    };
    MainView.prototype.componentWillUnmount = function () {
        document.removeEventListener("keydown", this.shortcutKeyHandler);
    };
    MainView.prototype.getChildContext = function () {
        return {
            store: this.props.store,
        };
    };
    // eslint-disable-next-line
    MainView.prototype.render = function () {
        var _this = this;
        var toolBarCreator = function (config) {
            return (React.createElement("div", { className: "charticulator__panel-editor-toolbar-" + config.layout },
                React.createElement(fluentui_tool_bar_1.FluentUIToolbar, { toolbarLabels: config.toolbarLabels, undoRedoLocation: config.undoRedoLocation, layout: config.layout })));
        };
        var datasetPanel = function () {
            return (React.createElement("div", { className: "charticulator__panel charticulator__panel-dataset" },
                React.createElement(components_1.MinimizablePanelView, null,
                    React.createElement(components_1.MinimizablePane, { title: strings_1.strings.mainView.datasetPanelTitle, scroll: true, hideHeader: true },
                        React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                            React.createElement(views_1.DatasetView, { store: _this.props.store }))),
                    _this.state.scaleViewMaximized ? null : (React.createElement(components_1.MinimizablePane, { title: strings_1.strings.mainView.scalesPanelTitle, scroll: true, onMaximize: function () { return _this.setState({ scaleViewMaximized: true }); } },
                        React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                            React.createElement(scales_panel_1.ScalesPanel, { store: _this.props.store })))))));
        };
        var editorPanels = function () {
            return (React.createElement("div", { className: "charticulator__panel-editor-panel charticulator__panel-editor-panel-panes", style: {
                    display: _this.state.glyphViewMaximized &&
                        _this.state.attributeViewMaximized &&
                        _this.state.layersViewMaximized
                        ? "none"
                        : undefined,
                } },
                React.createElement(components_1.MinimizablePanelView, null,
                    _this.state.glyphViewMaximized ? null : (React.createElement(components_1.MinimizablePane, { title: strings_1.strings.mainView.glyphPaneltitle, scroll: false, onMaximize: function () { return _this.setState({ glyphViewMaximized: true }); } },
                        React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                            React.createElement(views_1.MarkEditorView, { height: 300 })))),
                    _this.state.layersViewMaximized ? null : (React.createElement(components_1.MinimizablePane, { title: strings_1.strings.mainView.layersPanelTitle, scroll: true, maxHeight: 200, onMaximize: function () { return _this.setState({ layersViewMaximized: true }); } },
                        React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                            React.createElement(object_list_editor_1.ObjectListEditor, null)))),
                    _this.state.attributeViewMaximized ? null : (React.createElement(components_1.MinimizablePane, { title: strings_1.strings.mainView.attributesPaneltitle, scroll: true, onMaximize: function () {
                            return _this.setState({ attributeViewMaximized: true });
                        } },
                        React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                            React.createElement(views_1.AttributePanel, { store: _this.props.store })))))));
        };
        var chartPanel = function () {
            return (React.createElement("div", { className: "charticulator__panel-editor-panel charticulator__panel-editor-panel-chart" },
                React.createElement(components_1.ErrorBoundary, { telemetryRecorder: _this.props.telemetry },
                    React.createElement(views_1.ChartEditorView, { store: _this.props.store }))));
        };
        return (React.createElement("div", { className: "charticulator__application", onDragOver: function (e) { return e.preventDefault(); }, onDrop: function (e) { return e.preventDefault(); } },
            React.createElement(context_component_1.MainReactContext.Provider, { value: {
                    store: this.props.store,
                } },
                React.createElement(components_1.TelemetryContext.Provider, { value: this.props.telemetry },
                    React.createElement(menubar_1.MenuBar, { alignButtons: this.viewConfiguration.MenuBarButtons, alignSaveButton: this.viewConfiguration.MenuBarSaveButtons, undoRedoLocation: this.viewConfiguration.UndoRedoLocation, name: this.viewConfiguration.Name, ref: function (e) { return (_this.refMenuBar = e); }, handlers: this.props.menuBarHandlers, tabButtons: this.props.tabButtons }),
                    this.viewConfiguration.ToolbarPosition ==
                        PositionsLeftRightTop.Top &&
                        toolBarCreator({
                            layout: LayoutDirection.Horizontal,
                            toolbarLabels: this.viewConfiguration.ToolbarLabels,
                            undoRedoLocation: this.viewConfiguration.UndoRedoLocation,
                        }),
                    React.createElement("section", { className: "charticulator__panel-container" },
                        this.viewConfiguration.ColumnsPosition ==
                            PositionsLeftRight.Left && datasetPanel(),
                        React.createElement("div", { className: "charticulator__panel charticulator__panel-editor" },
                            React.createElement("div", { className: "charticulator__panel-editor-panel-container" },
                                this.viewConfiguration.EditorPanelsPosition ==
                                    PositionsLeftRight.Left && editorPanels(),
                                this.viewConfiguration.ToolbarPosition ==
                                    PositionsLeftRightTop.Left &&
                                    toolBarCreator({
                                        layout: LayoutDirection.Vertical,
                                        toolbarLabels: this.viewConfiguration.ToolbarLabels,
                                        undoRedoLocation: this.viewConfiguration.UndoRedoLocation,
                                    }),
                                chartPanel(),
                                this.viewConfiguration.ToolbarPosition ==
                                    PositionsLeftRightTop.Right &&
                                    toolBarCreator({
                                        layout: LayoutDirection.Vertical,
                                        toolbarLabels: this.viewConfiguration.ToolbarLabels,
                                        undoRedoLocation: this.viewConfiguration.UndoRedoLocation,
                                    }),
                                this.viewConfiguration.EditorPanelsPosition ==
                                    PositionsLeftRight.Right && editorPanels())),
                        this.viewConfiguration.ColumnsPosition ==
                            PositionsLeftRight.Right && datasetPanel()),
                    React.createElement("div", { className: "charticulator__floating-panels" },
                        this.state.glyphViewMaximized ? (React.createElement(components_1.FloatingPanel, { peerGroup: "panels", title: strings_1.strings.mainView.glyphPaneltitle, onClose: function () { return _this.setState({ glyphViewMaximized: false }); } },
                            React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                React.createElement(views_1.MarkEditorView, null)))) : null,
                        this.state.layersViewMaximized ? (React.createElement(components_1.FloatingPanel, { scroll: true, peerGroup: "panels", title: strings_1.strings.mainView.layersPanelTitle, onClose: function () { return _this.setState({ layersViewMaximized: false }); } },
                            React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                React.createElement(object_list_editor_1.ObjectListEditor, null)))) : null,
                        this.state.attributeViewMaximized ? (React.createElement(components_1.FloatingPanel, { scroll: true, peerGroup: "panels", title: strings_1.strings.mainView.attributesPaneltitle, onClose: function () {
                                return _this.setState({ attributeViewMaximized: false });
                            } },
                            React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                React.createElement(views_1.AttributePanel, { store: this.props.store })),
                            React.createElement(controllers_1.PopupContainer, { controller: globals.popupController }))) : null,
                        this.props.store.messageState.size ? (React.createElement("div", { className: "charticulator__floating-panels_errors" },
                            React.createElement(components_1.FloatingPanel, { floatInCenter: true, scroll: true, peerGroup: "messages", title: strings_1.strings.mainView.errorsPanelTitle, closeButtonIcon: "ChromeClose", height: 200, width: 350 },
                                React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                    React.createElement(components_1.MessagePanel, { store: this.props.store }))))) : null,
                        this.state.scaleViewMaximized ? (React.createElement(components_1.FloatingPanel, { scroll: true, peerGroup: "panels", title: strings_1.strings.mainView.scalesPanelTitle, onClose: function () { return _this.setState({ scaleViewMaximized: false }); } },
                            React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                React.createElement(scales_panel_1.ScalesPanel, { store: this.props.store })))) : null),
                    React.createElement(controllers_1.PopupContainer, { controller: globals.popupController }),
                    this.props.store.messageState.size ? (React.createElement("div", { className: "charticulator__floating-panels_errors" },
                        React.createElement(components_1.FloatingPanel, { floatInCenter: true, scroll: true, peerGroup: "messages", title: strings_1.strings.mainView.errorsPanelTitle, closeButtonIcon: "general/cross", height: 200, width: 350 },
                            React.createElement(components_1.ErrorBoundary, { telemetryRecorder: this.props.telemetry },
                                React.createElement(components_1.MessagePanel, { store: this.props.store }))))) : null,
                    React.createElement(controllers_1.DragStateView, { controller: globals.dragController })))));
    };
    MainView.childContextTypes = {
        store: function (s) { return s instanceof stores_1.AppStore; },
    };
    return MainView;
}(React.Component));
exports.MainView = MainView;
//# sourceMappingURL=main_view.js.map