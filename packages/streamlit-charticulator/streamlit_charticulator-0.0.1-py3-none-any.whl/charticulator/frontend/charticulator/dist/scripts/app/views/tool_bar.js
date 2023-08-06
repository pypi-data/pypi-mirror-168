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
exports.CheckboxButton = exports.LegendButton = exports.LinkButton = exports.ScaffoldButton = exports.MultiObjectButton = exports.ObjectButton = exports.Toolbar = void 0;
var React = require("react");
var ReactDOM = require("react-dom");
var globals = require("../globals");
var R = require("../resources");
var actions_1 = require("../actions");
var components_1 = require("../components");
var context_component_1 = require("../context_component");
var controllers_1 = require("../controllers");
var utils_1 = require("../utils");
var link_creator_1 = require("./panels/link_creator");
var legend_creator_1 = require("./panels/legend_creator");
var stores_1 = require("../stores");
var strings_1 = require("../../strings");
var main_view_1 = require("../main_view");
var app_store_1 = require("../stores/app_store");
var minWidthToColapseButtons = Object.freeze({
    guides: 1090,
    plotSegments: 1120,
    scaffolds: 1211,
});
var Toolbar = /** @class */ (function (_super) {
    __extends(Toolbar, _super);
    function Toolbar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            innerWidth: window.innerWidth,
        };
        return _this;
    }
    Toolbar.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.store.addListener(stores_1.AppStore.EVENT_CURRENT_TOOL, function () {
            _this.forceUpdate();
        });
        this.resizeListener = function () {
            _this.setState({
                innerWidth: window.innerWidth,
            });
        };
        window.addEventListener("resize", this.resizeListener);
    };
    Toolbar.prototype.componentWillUnmount = function () {
        this.token.remove();
        window.removeEventListener("resize", this.resizeListener);
    };
    Toolbar.prototype.renderGuidesButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "guide-y",
                    title: strings_1.strings.toolbar.guideY,
                    icon: "guide/x",
                },
                {
                    classID: "guide-x",
                    title: strings_1.strings.toolbar.guideX,
                    icon: "guide/y",
                },
                {
                    classID: "guide-coordinator-x",
                    title: strings_1.strings.toolbar.guideX,
                    icon: "guide/coordinator-x",
                },
                {
                    classID: "guide-coordinator-y",
                    title: strings_1.strings.toolbar.guideY,
                    icon: "guide/coordinator-y",
                },
                {
                    classID: "guide-coordinator-polar",
                    title: strings_1.strings.toolbar.guidePolar,
                    icon: "plot-segment/polar",
                },
            ] }));
    };
    Toolbar.prototype.renderPlotSegmentsButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "plot-segment.cartesian",
                    title: strings_1.strings.toolbar.region2D,
                    icon: "plot/region",
                    noDragging: true,
                },
                {
                    classID: "plot-segment.line",
                    title: strings_1.strings.toolbar.line,
                    icon: "plot/line",
                    noDragging: true,
                },
            ] }));
    };
    Toolbar.prototype.renderMarksButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "mark.rect",
                    title: strings_1.strings.toolbar.rectangle,
                    icon: "mark/rect",
                    options: '{"shape":"rectangle"}',
                },
                {
                    classID: "mark.rect",
                    title: strings_1.strings.toolbar.ellipse,
                    icon: "mark/ellipse",
                    options: '{"shape":"ellipse"}',
                },
                {
                    classID: "mark.rect",
                    title: strings_1.strings.toolbar.triangle,
                    icon: "mark/triangle",
                    options: '{"shape":"triangle"}',
                },
            ] }));
    };
    Toolbar.prototype.renderSymbolButton = function () {
        return (React.createElement(ObjectButton, { classID: "mark.symbol", title: "Symbol", icon: "mark/symbol" }));
    };
    Toolbar.prototype.renderLineButton = function () {
        return React.createElement(ObjectButton, { classID: "mark.line", title: "Line", icon: "mark/line" });
    };
    Toolbar.prototype.renderTextButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "mark.text",
                    title: strings_1.strings.toolbar.text,
                    icon: "mark/text",
                },
                {
                    classID: "mark.textbox",
                    title: strings_1.strings.toolbar.textbox,
                    icon: "mark/textbox",
                },
            ] }));
    };
    Toolbar.prototype.renderIconButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "mark.icon",
                    title: strings_1.strings.toolbar.icon,
                    icon: "mark/icon",
                },
                {
                    classID: "mark.image",
                    title: strings_1.strings.toolbar.image,
                    icon: "FileImage",
                },
            ] }));
    };
    Toolbar.prototype.renderDataAxisButton = function () {
        return (React.createElement(ObjectButton, { classID: "mark.data-axis", title: strings_1.strings.toolbar.dataAxis, icon: "mark/data-axis" }));
    };
    Toolbar.prototype.renderScaffoldButton = function () {
        return (React.createElement(MultiObjectButton, { compact: this.props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "scaffold/cartesian-x",
                    title: strings_1.strings.toolbar.lineH,
                    icon: "scaffold/cartesian-x",
                    noDragging: false,
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-x"); },
                },
                {
                    classID: "scaffold/cartesian-y",
                    title: strings_1.strings.toolbar.lineV,
                    icon: "scaffold/cartesian-y",
                    noDragging: false,
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-y"); },
                },
                {
                    classID: "scaffold/circle",
                    title: strings_1.strings.toolbar.polar,
                    icon: "scaffold/circle",
                    noDragging: false,
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("polar"); },
                },
                {
                    classID: "scaffold/curve",
                    title: strings_1.strings.toolbar.curve,
                    icon: "scaffold/curve",
                    noDragging: false,
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("curve"); },
                },
            ] }));
    };
    Toolbar.prototype.getGlyphToolItems = function (labels) {
        var _this = this;
        if (labels === void 0) { labels = true; }
        return [
            React.createElement(React.Fragment, null,
                React.createElement(React.Fragment, null,
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                    labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, strings_1.strings.toolbar.marks)),
                    this.renderMarksButton(),
                    this.renderSymbolButton(),
                    this.renderLineButton(),
                    this.renderTextButton(),
                    this.renderIconButton(),
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                    this.renderDataAxisButton(),
                    this.context.store.editorType === app_store_1.EditorType.Embedded ? (React.createElement(ObjectButton, { classID: "mark.nested-chart", title: strings_1.strings.toolbar.nestedChart, icon: "mark/nested-chart" })) : null,
                    this.props.undoRedoLocation === main_view_1.UndoRedoLocation.ToolBar ? (React.createElement(React.Fragment, null,
                        React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                        React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.undo, icon: R.getSVGIcon("Undo"), disabled: this.context.store.historyManager.statesBefore.length === 0, onClick: function () {
                                return new actions_1.Actions.Undo().dispatch(_this.context.store.dispatcher);
                            } }),
                        React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.redo, icon: R.getSVGIcon("Redo"), disabled: this.context.store.historyManager.statesAfter.length === 0, onClick: function () {
                                return new actions_1.Actions.Redo().dispatch(_this.context.store.dispatcher);
                            } }))) : null)),
        ];
    };
    Toolbar.prototype.getChartToolItems = function (labels) {
        var _this = this;
        if (labels === void 0) { labels = true; }
        return [
            React.createElement(React.Fragment, null,
                this.props.undoRedoLocation === main_view_1.UndoRedoLocation.ToolBar ? (React.createElement(React.Fragment, null,
                    React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.undo, icon: R.getSVGIcon("toolbar/undo"), disabled: this.context.store.historyManager.statesBefore.length === 0, onClick: function () {
                            return new actions_1.Actions.Undo().dispatch(_this.context.store.dispatcher);
                        } }),
                    React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.redo, icon: R.getSVGIcon("toolbar/redo"), disabled: this.context.store.historyManager.statesAfter.length === 0, onClick: function () {
                            return new actions_1.Actions.Redo().dispatch(_this.context.store.dispatcher);
                        } }),
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }))) : null,
                React.createElement(LinkButton, { label: true }),
                React.createElement(LegendButton, null),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                        ? "charticulator__toolbar-vertical-label"
                        : "charticulator__toolbar-label" }, strings_1.strings.toolbar.guides)),
                this.renderGuidesButton(),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                labels && (React.createElement(React.Fragment, null,
                    React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, this.props.layout === main_view_1.LayoutDirection.Vertical
                        ? strings_1.strings.toolbar.plot
                        : strings_1.strings.toolbar.plotSegments))),
                this.renderPlotSegmentsButton(),
                React.createElement(React.Fragment, null,
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                    labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, strings_1.strings.toolbar.scaffolds)),
                    this.renderScaffoldButton())),
        ];
    };
    // eslint-disable-next-line
    Toolbar.prototype.getToolItems = function (labels, innerWidth) {
        var _this = this;
        if (labels === void 0) { labels = true; }
        if (innerWidth === void 0) { innerWidth = window.innerWidth; }
        return (React.createElement(React.Fragment, null,
            this.props.undoRedoLocation === main_view_1.UndoRedoLocation.ToolBar ? (React.createElement(React.Fragment, null,
                React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.undo, icon: R.getSVGIcon("Undo"), disabled: this.context.store.historyManager.statesBefore.length === 0, onClick: function () {
                        return new actions_1.Actions.Undo().dispatch(_this.context.store.dispatcher);
                    } }),
                React.createElement(components_1.ToolButton, { title: strings_1.strings.menuBar.redo, icon: R.getSVGIcon("Redo"), disabled: this.context.store.historyManager.statesAfter.length === 0, onClick: function () {
                        return new actions_1.Actions.Redo().dispatch(_this.context.store.dispatcher);
                    } }),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }))) : null,
            labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.marks)),
            this.renderMarksButton(),
            this.renderSymbolButton(),
            this.renderLineButton(),
            this.renderTextButton(),
            this.renderIconButton(),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            this.renderDataAxisButton(),
            React.createElement(ObjectButton, { classID: "mark.nested-chart", title: strings_1.strings.toolbar.nestedChart, icon: "BarChartVerticalFilter" }),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            React.createElement(LinkButton, { label: labels }),
            React.createElement(LegendButton, null),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.guides)),
            innerWidth > minWidthToColapseButtons.guides ? (React.createElement(React.Fragment, null,
                React.createElement(ObjectButton, { classID: "guide-y", title: strings_1.strings.toolbar.guideY, icon: "guide/x" }),
                React.createElement(ObjectButton, { classID: "guide-x", title: strings_1.strings.toolbar.guideX, icon: "guide/y" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-x", title: strings_1.strings.toolbar.guideX, icon: "guide/coordinator-x" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-y", title: strings_1.strings.toolbar.guideY, icon: "guide/coordinator-y" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-polar", title: strings_1.strings.toolbar.guidePolar, icon: "plot-segment/polar" }))) : (this.renderGuidesButton()),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement(React.Fragment, null,
                React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                        ? "charticulator__toolbar-vertical-label"
                        : "charticulator__toolbar-label" }, this.props.layout === main_view_1.LayoutDirection.Vertical
                    ? strings_1.strings.toolbar.plot
                    : strings_1.strings.toolbar.plotSegments))),
            innerWidth > minWidthToColapseButtons.plotSegments ? (React.createElement(React.Fragment, null,
                React.createElement(ObjectButton, { classID: "plot-segment.cartesian", title: strings_1.strings.toolbar.region2D, icon: "plot/region", noDragging: true }),
                React.createElement(ObjectButton, { classID: "plot-segment.line", title: strings_1.strings.toolbar.line, icon: "plot/line", noDragging: true }))) : (this.renderPlotSegmentsButton()),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement("span", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.scaffolds)),
            innerWidth > minWidthToColapseButtons.scaffolds ? (React.createElement(React.Fragment, null,
                React.createElement(ScaffoldButton, { type: "cartesian-x", title: strings_1.strings.toolbar.lineH, icon: "scaffold/cartesian-x", currentTool: this.store.currentTool }),
                React.createElement(ScaffoldButton, { type: "cartesian-y", title: strings_1.strings.toolbar.lineV, icon: "scaffold/cartesian-y", currentTool: this.store.currentTool }),
                React.createElement(ScaffoldButton, { type: "polar", title: strings_1.strings.toolbar.polar, icon: "scaffold/circle", currentTool: this.store.currentTool }),
                React.createElement(ScaffoldButton, { type: "curve", title: strings_1.strings.toolbar.curve, icon: "scaffold/curve", currentTool: this.store.currentTool }))) : (this.renderScaffoldButton())));
    };
    Toolbar.prototype.render = function () {
        var _this = this;
        var _a;
        var tooltipsItems = [];
        if (this.context.store.editorType === app_store_1.EditorType.Embedded ||
            this.context.store.editorType === app_store_1.EditorType.NestedEmbedded) {
            var chartToolItems = this.getChartToolItems(this.props.toolbarLabels);
            var glyphToolItems = this.getGlyphToolItems(this.props.toolbarLabels);
            tooltipsItems = __spread(chartToolItems, glyphToolItems);
        }
        else {
            tooltipsItems = [
                this.getToolItems(this.props.toolbarLabels, (_a = this.state) === null || _a === void 0 ? void 0 : _a.innerWidth),
            ];
        }
        return (React.createElement(React.Fragment, null,
            React.createElement("div", { className: this.props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical"
                    : "charticulator__toolbar-horizontal" },
                React.createElement("div", { className: "charticulator__toolbar-buttons-align-left" }, tooltipsItems.map(function (item, index) {
                    return (React.createElement(React.Fragment, { key: index },
                        React.createElement("div", { key: index, className: _this.props.layout === main_view_1.LayoutDirection.Vertical
                                ? "charticulator__toolbar-vertical-group"
                                : "charticulator__toolbar-horizontal-group" }, item)));
                })))));
    };
    return Toolbar;
}(context_component_1.ContextedComponent));
exports.Toolbar = Toolbar;
var ObjectButton = /** @class */ (function (_super) {
    __extends(ObjectButton, _super);
    function ObjectButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ObjectButton.prototype.getIsActive = function () {
        return (this.store.currentTool == this.props.classID &&
            this.store.currentToolOptions == this.props.options);
    };
    ObjectButton.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.context.store.addListener(stores_1.AppStore.EVENT_CURRENT_TOOL, function () {
            _this.forceUpdate();
        });
    };
    ObjectButton.prototype.componentWillUnmount = function () {
        this.token.remove();
    };
    ObjectButton.prototype.render = function () {
        var _this = this;
        return (React.createElement(components_1.ToolButton, { icon: R.getSVGIcon(this.props.icon), active: this.getIsActive(), title: this.props.title, text: this.props.text, compact: this.props.compact, onClick: function () {
                _this.dispatch(new actions_1.Actions.SetCurrentTool(_this.props.classID, _this.props.options));
                if (_this.props.onClick) {
                    _this.props.onClick();
                }
            }, dragData: this.props.noDragging
                ? null
                : this.props.onDrag
                    ? this.props.onDrag
                    : function () {
                        return new actions_1.DragData.ObjectType(_this.props.classID, _this.props.options);
                    } }));
    };
    return ObjectButton;
}(context_component_1.ContextedComponent));
exports.ObjectButton = ObjectButton;
var MultiObjectButton = /** @class */ (function (_super) {
    __extends(MultiObjectButton, _super);
    function MultiObjectButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            currentSelection: {
                classID: _this.props.tools[0].classID,
                options: _this.props.tools[0].options,
            },
        };
        return _this;
    }
    MultiObjectButton.prototype.isActive = function () {
        var e_1, _a;
        var store = this.store;
        try {
            for (var _b = __values(this.props.tools), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (item.classID == store.currentTool &&
                    item.options == store.currentToolOptions) {
                    return true;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return false;
    };
    MultiObjectButton.prototype.getSelectedTool = function () {
        var e_2, _a;
        try {
            for (var _b = __values(this.props.tools), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (item.classID == this.state.currentSelection.classID &&
                    item.options == this.state.currentSelection.options) {
                    return item;
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return this.props.tools[0];
    };
    MultiObjectButton.prototype.componentDidMount = function () {
        var _this = this;
        this.token = this.store.addListener(stores_1.AppStore.EVENT_CURRENT_TOOL, function () {
            var e_3, _a;
            try {
                for (var _b = __values(_this.props.tools), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    // If the tool is within the tools defined here, we update the current selection
                    if (_this.store.currentTool == item.classID &&
                        _this.store.currentToolOptions == item.options) {
                        _this.setState({
                            currentSelection: {
                                classID: item.classID,
                                options: item.options,
                            },
                        });
                        break;
                    }
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_3) throw e_3.error; }
            }
            _this.forceUpdate();
        });
    };
    MultiObjectButton.prototype.componentWillUnmount = function () {
        this.token.remove();
    };
    MultiObjectButton.prototype.render = function () {
        var _this = this;
        var openContextMenu = function () {
            globals.popupController.popupAt(function (context) {
                return (React.createElement(controllers_1.PopupView, { context: context }, _this.props.tools.map(function (tool, index) { return (React.createElement("div", { key: index, className: "charticulator__button-multi-tool-dropdown" },
                    React.createElement(ObjectButton, __assign({}, tool, { noDragging: tool.noDragging !== undefined ? tool.noDragging : true, onClick: function () { return context.close(); } })))); })));
            }, {
                anchor: ReactDOM.findDOMNode(_this.refButton),
                alignX: controllers_1.PopupAlignment.EndOuter,
                alignY: controllers_1.PopupAlignment.StartInner,
            });
        };
        var onClick = function () {
            if (_this.props.compact) {
                openContextMenu();
            }
        };
        var onClickContextMenu = function () {
            if (!_this.props.compact) {
                openContextMenu();
            }
        };
        return (React.createElement("div", { className: utils_1.classNames("charticulator__button-multi-tool", [
                "is-active",
                this.isActive(),
            ]) },
            React.createElement(ObjectButton, __assign({ ref: function (e) { return (_this.refButton = e); } }, this.getSelectedTool(), { onClick: onClick, compact: this.props.compact })),
            React.createElement("span", { className: "el-dropdown", ref: function (e) {
                    if (_this.props.compact) {
                        return;
                    }
                    _this.refButton = e;
                }, onClick: onClickContextMenu }, this.props.compact ? null : (React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("ChevronDown") })))));
    };
    return MultiObjectButton;
}(context_component_1.ContextedComponent));
exports.MultiObjectButton = MultiObjectButton;
var ScaffoldButton = /** @class */ (function (_super) {
    __extends(ScaffoldButton, _super);
    function ScaffoldButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ScaffoldButton.prototype.render = function () {
        var _this = this;
        return (React.createElement(components_1.ToolButton, { icon: R.getSVGIcon(this.props.icon), active: this.props.currentTool == this.props.type, title: this.props.title, onClick: function () {
                // this.dispatch(new Actions.SetCurrentTool(this.props.type));
            }, dragData: function () {
                return new actions_1.DragData.ScaffoldType(_this.props.type);
            } }));
    };
    return ScaffoldButton;
}(context_component_1.ContextedComponent));
exports.ScaffoldButton = ScaffoldButton;
var LinkButton = /** @class */ (function (_super) {
    __extends(LinkButton, _super);
    function LinkButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LinkButton.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { ref: function (e) { return (_this.container = e); } },
            React.createElement(components_1.ToolButton, { title: strings_1.strings.toolbar.links, text: this.props.label ? strings_1.strings.toolbar.links : "", icon: R.getSVGIcon("CharticulatorLine"), active: this.store.currentTool == "link", onClick: function () {
                    globals.popupController.popupAt(function (context) { return (React.createElement(controllers_1.PopupView, { context: context },
                        React.createElement(link_creator_1.LinkCreationPanel, { onFinish: function () { return context.close(); } }))); }, { anchor: _this.container });
                } })));
    };
    return LinkButton;
}(context_component_1.ContextedComponent));
exports.LinkButton = LinkButton;
var LegendButton = /** @class */ (function (_super) {
    __extends(LegendButton, _super);
    function LegendButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LegendButton.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { ref: function (e) { return (_this.container = e); } },
            React.createElement(components_1.ToolButton, { title: strings_1.strings.toolbar.legend, icon: R.getSVGIcon("CharticulatorLegend"), active: this.store.currentTool == "legend", onClick: function () {
                    globals.popupController.popupAt(function (context) { return (React.createElement(controllers_1.PopupView, { context: context },
                        React.createElement(legend_creator_1.LegendCreationPanel, { onFinish: function () { return context.close(); } }))); }, { anchor: _this.container });
                } })));
    };
    return LegendButton;
}(context_component_1.ContextedComponent));
exports.LegendButton = LegendButton;
var CheckboxButton = /** @class */ (function (_super) {
    __extends(CheckboxButton, _super);
    function CheckboxButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CheckboxButton.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { className: "charticulator__toolbar-checkbox", onClick: function () {
                var nv = !_this.props.value;
                if (_this.props.onChange) {
                    _this.props.onChange(nv);
                }
            } },
            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(this.props.value ? "checkbox/checked" : "checkbox/empty") }),
            React.createElement("span", { className: "el-label" }, this.props.text)));
    };
    return CheckboxButton;
}(React.Component));
exports.CheckboxButton = CheckboxButton;
//# sourceMappingURL=tool_bar.js.map