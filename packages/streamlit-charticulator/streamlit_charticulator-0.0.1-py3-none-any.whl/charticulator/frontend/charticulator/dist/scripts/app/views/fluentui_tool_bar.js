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
exports.CheckboxButton = exports.LegendButton = exports.LinkButton = exports.ScaffoldButton = exports.MultiObjectButton = exports.ObjectButton = exports.FluentUIToolbar = void 0;
var React = require("react");
var R = require("../resources");
var actions_1 = require("../actions");
var components_1 = require("../components");
var context_component_1 = require("../context_component");
var link_creator_1 = require("./panels/link_creator");
var legend_creator_1 = require("./panels/legend_creator");
var stores_1 = require("../stores");
var strings_1 = require("../../strings");
var main_view_1 = require("../main_view");
var react_1 = require("react");
var react_2 = require("@fluentui/react");
var resources_1 = require("../resources");
var app_store_1 = require("../stores/app_store");
var react_3 = require("react");
var react_4 = require("react");
var Icon_1 = require("@fluentui/react/lib/Icon");
var minWidthToColapseButtons = Object.freeze({
    guides: 1090,
    plotSegments: 1120,
    scaffolds: 1211,
});
exports.FluentUIToolbar = function (props) {
    var store = react_1.useContext(context_component_1.MainReactContext).store;
    var _a = __read(react_3.useState(window.innerWidth), 2), innerWidth = _a[0], setInnerWidth = _a[1];
    var resizeListener = function () {
        setInnerWidth(window.innerWidth);
    };
    react_4.useEffect(function () {
        setInnerWidth(window.innerWidth);
        window.addEventListener("resize", resizeListener);
        return function () {
            window.removeEventListener("resize", resizeListener);
        };
    }, [setInnerWidth]);
    var getGlyphToolItems = function (labels) {
        if (labels === void 0) { labels = true; }
        return [
            React.createElement(React.Fragment, null,
                React.createElement(React.Fragment, null,
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                    labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, strings_1.strings.toolbar.marks)),
                    React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                            {
                                classID: "mark.rect",
                                title: strings_1.strings.toolbar.rectangle,
                                icon: "RectangleShape",
                                options: '{"shape":"rectangle"}',
                            },
                            {
                                classID: "mark.rect",
                                title: strings_1.strings.toolbar.ellipse,
                                icon: "Ellipse",
                                options: '{"shape":"ellipse"}',
                            },
                            {
                                classID: "mark.rect",
                                title: strings_1.strings.toolbar.triangle,
                                icon: "TriangleShape",
                                options: '{"shape":"triangle"}',
                            },
                        ] }),
                    React.createElement(ObjectButton, { classID: "mark.symbol", title: strings_1.strings.toolbar.symbol, icon: "Shapes" }),
                    React.createElement(ObjectButton, { classID: "mark.line", title: strings_1.strings.toolbar.line, icon: "Line" }),
                    React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                            {
                                classID: "mark.text",
                                title: strings_1.strings.toolbar.text,
                                icon: "FontColorA",
                            },
                            {
                                classID: "mark.textbox",
                                title: strings_1.strings.toolbar.textbox,
                                icon: "TextField",
                            },
                        ] }),
                    React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                            {
                                classID: "mark.icon",
                                title: strings_1.strings.toolbar.icon,
                                icon: "ImagePixel",
                            },
                            {
                                classID: "mark.image",
                                title: strings_1.strings.toolbar.image,
                                icon: "FileImage",
                            },
                        ] }),
                    React.createElement(ObjectButton, { classID: "mark.data-axis", title: strings_1.strings.toolbar.dataAxis, icon: "mark/data-axis" }),
                    store.editorType === app_store_1.EditorType.Embedded ? (React.createElement(ObjectButton, { classID: "mark.nested-chart", title: strings_1.strings.toolbar.nestedChart, icon: "BarChartVerticalFilter" })) : null,
                    props.undoRedoLocation === main_view_1.UndoRedoLocation.ToolBar ? (React.createElement(React.Fragment, null,
                        React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                        React.createElement(components_1.FluentToolButton, { title: strings_1.strings.menuBar.undo, disabled: store.historyManager.statesBefore.length === 0, icon: "Undo", onClick: function () { return new actions_1.Actions.Undo().dispatch(store.dispatcher); } }),
                        React.createElement(components_1.FluentToolButton, { title: strings_1.strings.menuBar.redo, disabled: store.historyManager.statesAfter.length === 0, icon: "Redo", onClick: function () { return new actions_1.Actions.Redo().dispatch(store.dispatcher); } }))) : null)),
        ];
    };
    // eslint-disable-next-line max-lines-per-function
    var getChartToolItems = function (labels) {
        if (labels === void 0) { labels = true; }
        return [
            React.createElement(React.Fragment, null,
                React.createElement(exports.LinkButton, { label: true }),
                React.createElement(exports.LegendButton, null),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                        ? "charticulator__toolbar-vertical-label"
                        : "charticulator__toolbar-label" }, strings_1.strings.toolbar.guides)),
                React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                        {
                            classID: "guide-y",
                            title: strings_1.strings.toolbar.guideY,
                            icon: "guide/x",
                            options: '{"shape":"rectangle"}',
                        },
                        {
                            classID: "guide-x",
                            title: strings_1.strings.toolbar.guideX,
                            icon: "guide/y",
                            options: '{"shape":"ellipse"}',
                        },
                        {
                            classID: "guide-coordinator-x",
                            title: strings_1.strings.toolbar.guideX,
                            icon: "CharticulatorGuideX",
                            options: '{"shape":"triangle"}',
                        },
                        {
                            classID: "guide-coordinator-y",
                            title: strings_1.strings.toolbar.guideY,
                            icon: "CharticulatorGuideY",
                            options: '{"shape":"triangle"}',
                        },
                        {
                            classID: "guide-coordinator-polar",
                            title: strings_1.strings.toolbar.guidePolar,
                            icon: "CharticulatorGuideCoordinator",
                            options: "",
                        },
                    ] }),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                labels && (React.createElement(React.Fragment, null,
                    React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, props.layout === main_view_1.LayoutDirection.Vertical
                        ? strings_1.strings.toolbar.plot
                        : strings_1.strings.toolbar.plotSegments))),
                React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                        {
                            classID: "plot-segment.cartesian",
                            title: strings_1.strings.toolbar.region2D,
                            icon: "BorderDot",
                            noDragging: true,
                        },
                        {
                            classID: "plot-segment.line",
                            title: strings_1.strings.toolbar.line,
                            icon: "Line",
                            noDragging: true,
                        },
                    ] }),
                React.createElement(React.Fragment, null,
                    React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
                    labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-label"
                            : "charticulator__toolbar-label" }, strings_1.strings.toolbar.scaffolds)),
                    React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                            {
                                classID: "scaffold/cartesian-x",
                                title: strings_1.strings.toolbar.lineH,
                                icon: "scaffold/cartesian-x",
                                onClick: function () { return null; },
                                onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-x"); },
                            },
                            {
                                classID: "scaffold/cartesian-y",
                                title: strings_1.strings.toolbar.lineV,
                                icon: "scaffold/cartesian-y",
                                onClick: function () { return null; },
                                onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-y"); },
                            },
                            {
                                classID: "scaffold/circle",
                                title: strings_1.strings.toolbar.polar,
                                icon: "scaffold/circle",
                                onClick: function () { return null; },
                                onDrag: function () { return new actions_1.DragData.ScaffoldType("polar"); },
                            },
                            {
                                classID: "scaffold/curve",
                                title: strings_1.strings.toolbar.curve,
                                icon: "scaffold/curve",
                                onClick: function () { return null; },
                                onDrag: function () { return new actions_1.DragData.ScaffoldType("curve"); },
                            },
                        ] }))),
        ];
    };
    var renderScaffoldButton = function () {
        return (React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "scaffold/cartesian-x",
                    title: strings_1.strings.toolbar.lineH,
                    icon: "scaffold/cartesian-x",
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-x"); },
                },
                {
                    classID: "scaffold/cartesian-y",
                    title: strings_1.strings.toolbar.lineV,
                    icon: "scaffold/cartesian-y",
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("cartesian-y"); },
                },
                {
                    classID: "scaffold/circle",
                    title: strings_1.strings.toolbar.polar,
                    icon: "scaffold/circle",
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("polar"); },
                },
                {
                    classID: "scaffold/curve",
                    title: strings_1.strings.toolbar.curve,
                    icon: "scaffold/curve",
                    onClick: function () { return null; },
                    onDrag: function () { return new actions_1.DragData.ScaffoldType("curve"); },
                },
            ] }));
    };
    var renderGuidesButton = function () {
        return (React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                {
                    classID: "guide-y",
                    title: strings_1.strings.toolbar.guideY,
                    icon: "guide/x",
                },
                {
                    classID: "guide-x",
                    title: strings_1.strings.toolbar.guideX,
                    icon: "guide/y",
                    options: "",
                },
                {
                    classID: "guide-coordinator-x",
                    title: strings_1.strings.toolbar.guideX,
                    icon: "CharticulatorGuideX",
                    options: "",
                },
                {
                    classID: "guide-coordinator-y",
                    title: strings_1.strings.toolbar.guideY,
                    icon: "CharticulatorGuideY",
                    options: "",
                },
                {
                    classID: "guide-coordinator-polar",
                    title: strings_1.strings.toolbar.guidePolar,
                    icon: "CharticulatorGuideCoordinator",
                    options: "",
                },
            ] }));
    };
    // eslint-disable-next-line max-lines-per-function
    var getToolItems = function (labels, innerWidth) {
        if (labels === void 0) { labels = true; }
        if (innerWidth === void 0) { innerWidth = window.innerWidth; }
        return (React.createElement(React.Fragment, null,
            props.undoRedoLocation === main_view_1.UndoRedoLocation.ToolBar ? (React.createElement(React.Fragment, null,
                React.createElement(components_1.FluentToolButton, { title: strings_1.strings.menuBar.undo, disabled: store.historyManager.statesBefore.length === 0, icon: "Undo", onClick: function () { return new actions_1.Actions.Undo().dispatch(store.dispatcher); } }),
                React.createElement(components_1.FluentToolButton, { title: strings_1.strings.menuBar.redo, disabled: store.historyManager.statesAfter.length === 0, icon: "Redo", onClick: function () { return new actions_1.Actions.Redo().dispatch(store.dispatcher); } }),
                React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }))) : null,
            labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.marks)),
            React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                    {
                        classID: "mark.rect",
                        title: strings_1.strings.toolbar.rectangle,
                        icon: "RectangleShape",
                        options: '{"shape":"rectangle"}',
                    },
                    {
                        classID: "mark.rect",
                        title: strings_1.strings.toolbar.ellipse,
                        icon: "Ellipse",
                        options: '{"shape":"ellipse"}',
                    },
                    {
                        classID: "mark.rect",
                        title: strings_1.strings.toolbar.triangle,
                        icon: "TriangleShape",
                        options: '{"shape":"triangle"}',
                    },
                ] }),
            React.createElement(ObjectButton, { classID: "mark.symbol", title: "Symbol", icon: "Shapes" }),
            React.createElement(ObjectButton, { classID: "mark.line", title: "Line", icon: "Line" }),
            React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                    {
                        classID: "mark.text",
                        title: strings_1.strings.toolbar.text,
                        icon: "FontColorA",
                    },
                    {
                        classID: "mark.textbox",
                        title: strings_1.strings.toolbar.textbox,
                        icon: "TextField",
                    },
                ] }),
            React.createElement(MultiObjectButton, { compact: props.layout === main_view_1.LayoutDirection.Vertical, tools: [
                    {
                        classID: "mark.icon",
                        title: strings_1.strings.toolbar.icon,
                        icon: "ImagePixel",
                    },
                    {
                        classID: "mark.image",
                        title: strings_1.strings.toolbar.image,
                        icon: "FileImage",
                    },
                ] }),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            React.createElement(ObjectButton, { classID: "mark.data-axis", title: strings_1.strings.toolbar.dataAxis, icon: "mark/data-axis" }),
            React.createElement(ObjectButton, { classID: "mark.nested-chart", title: strings_1.strings.toolbar.nestedChart, icon: "BarChartVerticalFilter" }),
            React.createElement(exports.LegendButton, null),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            React.createElement(exports.LinkButton, { label: labels }),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.guides)),
            innerWidth > minWidthToColapseButtons.guides ? (React.createElement(React.Fragment, null,
                React.createElement(ObjectButton, { classID: "guide-y", title: strings_1.strings.toolbar.guideY, icon: "guide/x" }),
                React.createElement(ObjectButton, { classID: "guide-x", title: strings_1.strings.toolbar.guideX, icon: "guide/y" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-x", title: strings_1.strings.toolbar.guideX, icon: "CharticulatorGuideX" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-y", title: strings_1.strings.toolbar.guideY, icon: "CharticulatorGuideY" }),
                React.createElement(ObjectButton, { classID: "guide-coordinator-polar", title: strings_1.strings.toolbar.guidePolar, icon: "CharticulatorGuideCoordinator" }))) : (renderGuidesButton()),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement(React.Fragment, null,
                React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                        ? "charticulator__toolbar-vertical-label"
                        : "charticulator__toolbar-label" }, props.layout === main_view_1.LayoutDirection.Vertical
                    ? strings_1.strings.toolbar.plot
                    : strings_1.strings.toolbar.plotSegments))),
            React.createElement(ObjectButton, { classID: "plot-segment.cartesian", title: strings_1.strings.toolbar.region2D, icon: "BorderDot", noDragging: true }),
            React.createElement(ObjectButton, { classID: "plot-segment.line", title: strings_1.strings.toolbar.line, icon: "Line", noDragging: true }),
            React.createElement("span", { className: "charticulator__toolbar-horizontal-separator" }),
            labels && (React.createElement("span", { className: props.layout === main_view_1.LayoutDirection.Vertical
                    ? "charticulator__toolbar-vertical-label"
                    : "charticulator__toolbar-label" }, strings_1.strings.toolbar.scaffolds)),
            innerWidth > minWidthToColapseButtons.scaffolds ? (React.createElement(React.Fragment, null,
                React.createElement(exports.ScaffoldButton, { type: "cartesian-x", title: strings_1.strings.toolbar.lineH, icon: "scaffold/cartesian-x", currentTool: store.currentTool }),
                React.createElement(exports.ScaffoldButton, { type: "cartesian-y", title: strings_1.strings.toolbar.lineV, icon: "scaffold/cartesian-y", currentTool: store.currentTool }),
                React.createElement(exports.ScaffoldButton, { type: "polar", title: strings_1.strings.toolbar.polar, icon: "scaffold/circle", currentTool: store.currentTool }),
                React.createElement(exports.ScaffoldButton, { type: "curve", title: strings_1.strings.toolbar.curve, icon: "scaffold/curve", currentTool: store.currentTool }))) : (renderScaffoldButton())));
    };
    var tooltipsItems = [];
    if (store.editorType === "embedded") {
        var chartToolItems = getChartToolItems(props.toolbarLabels);
        var glyphToolItems = getGlyphToolItems(props.toolbarLabels);
        tooltipsItems = __spread(chartToolItems, glyphToolItems);
    }
    else {
        tooltipsItems = [getToolItems(props.toolbarLabels, innerWidth)];
    }
    return (React.createElement(React.Fragment, null,
        React.createElement("div", { className: props.layout === main_view_1.LayoutDirection.Vertical
                ? "charticulator__toolbar-vertical"
                : "charticulator__toolbar-horizontal" },
            React.createElement("div", { className: "charticulator__toolbar-buttons-align-left" }, tooltipsItems.map(function (item, index) {
                return (React.createElement(React.Fragment, { key: index },
                    React.createElement("div", { key: index, className: props.layout === main_view_1.LayoutDirection.Vertical
                            ? "charticulator__toolbar-vertical-group"
                            : "charticulator__toolbar-horizontal-group" }, item)));
            })))));
};
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
        return (React.createElement(React.Fragment, null,
            React.createElement(components_1.DraggableElement, { dragData: this.props.noDragging
                    ? null
                    : this.props.onDrag
                        ? this.props.onDrag
                        : function () {
                            return new actions_1.DragData.ObjectType(_this.props.classID, _this.props.options);
                        }, onDragStart: function () { return _this.setState({ dragging: true }); }, onDragEnd: function () { return _this.setState({ dragging: false }); }, renderDragElement: function () {
                    return [
                        React.createElement(components_1.SVGImageIcon, { url: resources_1.getSVGIcon(_this.props.icon), width: 32, height: 32 }),
                        { x: -16, y: -16 },
                    ];
                } },
                React.createElement(react_2.IconButton, { iconProps: {
                        iconName: this.props.icon,
                    }, title: this.props.title, text: this.props.text, checked: this.getIsActive(), onClick: function () {
                        _this.dispatch(new actions_1.Actions.SetCurrentTool(_this.props.classID, _this.props.options));
                        if (_this.props.onClick) {
                            _this.props.onClick();
                        }
                    } }))));
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
            dragging: false,
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
        var currentTool = this.getSelectedTool();
        return (React.createElement(components_1.DraggableElement, { dragData: function () {
                if (currentTool === null || currentTool === void 0 ? void 0 : currentTool.onDrag) {
                    return currentTool === null || currentTool === void 0 ? void 0 : currentTool.onDrag();
                }
                return new actions_1.DragData.ObjectType(currentTool.classID, currentTool.options);
            }, onDragStart: function () { return _this.setState({ dragging: true }); }, onDragEnd: function () { return _this.setState({ dragging: false }); }, renderDragElement: function () {
                return [
                    React.createElement(Icon_1.Icon, { iconName: currentTool.icon, "aria-hidden": "true" }),
                    { x: 16, y: 16 },
                ];
            } },
            React.createElement(react_2.IconButton, { split: true, menuProps: {
                    items: this.props.tools.map(function (tool, index) {
                        return {
                            key: tool.classID + index,
                            data: {
                                classID: tool.classID,
                                options: tool.options,
                            },
                            text: tool.title,
                            iconProps: { iconName: tool.icon },
                        };
                    }),
                    onItemClick: function (ev, item) {
                        if (item.data) {
                            _this.dispatch(new actions_1.Actions.SetCurrentTool(item.data.classID, item.data.options));
                        }
                    },
                }, iconProps: {
                    iconName: currentTool.icon,
                }, onMenuClick: function () {
                    if (currentTool) {
                        _this.dispatch(new actions_1.Actions.SetCurrentTool(currentTool.classID, currentTool.options));
                    }
                } })));
    };
    return MultiObjectButton;
}(context_component_1.ContextedComponent));
exports.MultiObjectButton = MultiObjectButton;
exports.ScaffoldButton = function (props) {
    return (React.createElement(components_1.FluentToolButton, { icon: props.icon, active: props.currentTool == props.type, title: props.title, onClick: function () {
            // this.dispatch(new Actions.SetCurrentTool(this.props.type));
        }, dragData: function () {
            return new actions_1.DragData.ScaffoldType(props.type);
        } }));
};
exports.LinkButton = function (props) {
    var store = React.useContext(context_component_1.MainReactContext).store;
    var _a = __read(React.useState(false), 2), isOpen = _a[0], openDialog = _a[1];
    return (React.createElement("span", { id: "linkCreator" },
        React.createElement(react_2.IconButton, { title: strings_1.strings.toolbar.link, text: props.label ? strings_1.strings.toolbar.link : "", iconProps: {
                iconName: "CharticulatorLine",
            }, checked: store.currentTool == "link", onClick: function () {
                openDialog(true);
            } }),
        isOpen ? (React.createElement(react_2.Callout, { target: "#linkCreator", hidden: !isOpen, onDismiss: function () { return openDialog(false); } },
            React.createElement(link_creator_1.LinkCreationPanel, { onFinish: function () { return openDialog(false); } }))) : null));
};
exports.LegendButton = function () {
    var store = React.useContext(context_component_1.MainReactContext).store;
    var _a = __read(React.useState(false), 2), isOpen = _a[0], setOpen = _a[1];
    React.useEffect(function () {
        return function () {
            setOpen(false);
        };
    }, [setOpen]);
    return (React.createElement("span", { id: "createLegend" },
        React.createElement(react_2.IconButton, { title: strings_1.strings.toolbar.legend, iconProps: {
                iconName: "CharticulatorLegend",
            }, checked: store.currentTool == "legend", onClick: function () {
                setOpen(!isOpen);
            } }),
        isOpen ? (React.createElement(react_2.Callout, { onDismiss: function () { return setOpen(false); }, target: "#createLegend", directionalHint: react_2.DirectionalHint.bottomLeftEdge },
            React.createElement(legend_creator_1.LegendCreationPanel, { onFinish: function () { return setOpen(false); } }))) : null));
};
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
//# sourceMappingURL=fluentui_tool_bar.js.map