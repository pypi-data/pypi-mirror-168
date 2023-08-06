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
Object.defineProperty(exports, "__esModule", { value: true });
exports.PlotSegmentSelector = exports.LinkCreationPanel = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var R = require("../../resources");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var context_component_1 = require("../../context_component");
var utils_1 = require("../../utils");
var data_field_selector_1 = require("../dataset/data_field_selector");
var object_list_editor_1 = require("./object_list_editor");
var radio_control_1 = require("./radio_control");
var specification_1 = require("../../../core/specification");
var react_1 = require("@fluentui/react");
var links_1 = require("../../../core/prototypes/links");
var LinkCreationPanel = /** @class */ (function (_super) {
    __extends(LinkCreationPanel, _super);
    function LinkCreationPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        return _this;
    }
    LinkCreationPanel.prototype.getDefaultState = function () {
        var plotSegments = this.store.chart.elements;
        plotSegments = plotSegments.filter(function (x) {
            return core_1.Prototypes.isType(x.classID, "plot-segment");
        });
        var selectedPlotSegments = plotSegments.map(function (x) { return x._id; });
        var linkMode = "link-through";
        if (selectedPlotSegments.length == 1) {
            linkMode = this.isLinkDataPresent() ? "link-table" : "link-through";
        }
        else {
            linkMode = "link-between";
        }
        return {
            linkType: "line",
            linkMode: linkMode,
            plotSegments: plotSegments,
            selectedPlotSegments: selectedPlotSegments,
            errorReport: null,
        };
    };
    LinkCreationPanel.prototype.isLinkDataPresent = function () {
        return this.store.dataset.tables.length > 1;
    };
    LinkCreationPanel.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__link-type-table" },
            React.createElement("div", { className: "el-row" },
                React.createElement("h2", null, "Link using:"),
                React.createElement(radio_control_1.PanelRadioControl, { options: ["line", "band"], icons: ["link/line", "link/band"], labels: ["Line", "Band"], value: this.state.linkType, onChange: function (newValue) {
                        return _this.setState({ linkType: newValue });
                    }, showText: true })),
            this.state.plotSegments.length > 1 ? (React.createElement("div", { className: "el-row" },
                React.createElement("h2", null, "Plot Segment(s):"),
                React.createElement(PlotSegmentSelector, { items: this.state.plotSegments, defaultSelection: this.state.selectedPlotSegments, onChange: function (newSelection) {
                        var linkMode = _this.state.linkMode;
                        if (newSelection.length == 1) {
                            linkMode = _this.isLinkDataPresent()
                                ? "link-table"
                                : "link-through";
                        }
                        else {
                            linkMode = "link-between";
                        }
                        _this.setState({
                            linkMode: linkMode,
                            selectedPlotSegments: newSelection,
                        });
                    } }))) : null,
            this.state.selectedPlotSegments.length == 1 &&
                this.isLinkDataPresent() ? (React.createElement("div", { className: "el-row" },
                React.createElement("h2", null, "Link Mode:"),
                React.createElement(radio_control_1.PanelRadioControl, { options: ["link-through", "link-table"], icons: ["link/through", "link/table"], labels: ["Sequentially", "By Link Data"], value: this.state.linkMode, onChange: function (newValue) { return _this.setState({ linkMode: newValue }); }, showText: true, asList: true }))) : null,
            this.state.linkMode == "link-through" ? (React.createElement("div", null,
                React.createElement("h2", null, "Connect by:"),
                React.createElement("div", { className: "el-row" },
                    React.createElement(data_field_selector_1.DataFieldSelector, { ref: function (e) { return (_this.groupBySelector = e); }, kinds: [core_1.Specification.DataKind.Categorical], datasetStore: this.store, nullDescription: "(link all items)" })))) : null,
            React.createElement("div", { className: "el-row" },
                React.createElement(react_1.PrimaryButton, { text: "Create Links", onClick: function () {
                        var links = _this.getLinkObject();
                        if (links != null) {
                            _this.dispatch(new actions_1.Actions.AddLinks(links));
                            if (_this.props.onFinish) {
                                _this.props.onFinish();
                            }
                        }
                        else {
                            _this.setState({
                                errorReport: "Cannot Create Link!",
                            });
                        }
                    } }),
                this.state.errorReport ? (React.createElement("span", null, this.state.errorReport)) : null)));
    };
    // eslint-disable-next-line
    LinkCreationPanel.prototype.getDefaultAnchor = function (manager, linkMode, cs, glyph1, glyphState1, 
    // eslint-disable-next-line
    glyph2, glyphState2) {
        var e_1, _a, e_2, _b;
        // Default color and opacity
        var color;
        var opacity;
        switch (this.state.linkType) {
            case "line":
                {
                    color = {
                        type: specification_1.MappingType.value,
                        value: { r: 0, g: 0, b: 0 },
                    };
                    opacity = {
                        type: specification_1.MappingType.value,
                        value: 1,
                    };
                }
                break;
            case "band":
                {
                    color = {
                        type: specification_1.MappingType.value,
                        value: { r: 0, g: 0, b: 0 },
                    };
                    opacity = {
                        type: specification_1.MappingType.value,
                        value: 0.5,
                    };
                }
                break;
        }
        // Get anchor candidates
        var candidates1 = [];
        var candidates2 = [];
        try {
            for (var _c = __values(glyphState1.marks), _d = _c.next(); !_d.done; _d = _c.next()) {
                var mark = _d.value;
                var c = manager.getMarkClass(mark);
                if (c.getLinkAnchors) {
                    candidates1 = candidates1.concat(c.getLinkAnchors("begin"));
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
        try {
            for (var _e = __values(glyphState2.marks), _f = _e.next(); !_f.done; _f = _e.next()) {
                var mark = _f.value;
                var c = manager.getMarkClass(mark);
                if (c.getLinkAnchors) {
                    candidates2 = candidates2.concat(c.getLinkAnchors("end"));
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_2) throw e_2.error; }
        }
        // Filter based on link type
        switch (this.state.linkType) {
            case "line":
                {
                    candidates1 = candidates1.filter(function (x) { return x.points.length == 1; });
                    candidates2 = candidates2.filter(function (x) { return x.points.length == 1; });
                }
                break;
            case "band": {
                candidates1 = candidates1.filter(function (x) { return x.points.length == 2; });
                candidates2 = candidates2.filter(function (x) { return x.points.length == 2; });
            }
        }
        var glyphAttributes1 = glyphState1.attributes;
        var glyphAttributes2 = glyphState2.attributes;
        var determineRelationship = function (a1, a2, b1, b2) {
            var _a, _b;
            // Make sure order is correct
            _a = __read([Math.min(a1, a2), Math.max(a1, a2)], 2), a1 = _a[0], a2 = _a[1];
            _b = __read([Math.min(b1, b2), Math.max(b1, b2)], 2), b1 = _b[0], b2 = _b[1];
            if (a2 <= b1) {
                return "after";
            }
            else if (a1 >= b2) {
                return "before";
            }
            else {
                return "overlap";
            }
        };
        // Determine relative position
        var xRelationship = determineRelationship(glyphAttributes1.x1, glyphAttributes1.x2, glyphAttributes2.x1, glyphAttributes2.x2);
        var yRelationship = determineRelationship(glyphAttributes1.y1, glyphAttributes1.y2, glyphAttributes2.y1, glyphAttributes2.y2);
        var meanPoint = function (points) {
            var e_3, _a;
            var x = 0, y = 0;
            try {
                for (var points_1 = __values(points), points_1_1 = points_1.next(); !points_1_1.done; points_1_1 = points_1.next()) {
                    var pt = points_1_1.value;
                    x += pt.x;
                    y += pt.y;
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (points_1_1 && !points_1_1.done && (_a = points_1.return)) _a.call(points_1);
                }
                finally { if (e_3) throw e_3.error; }
            }
            return {
                x: x / points.length,
                y: y / points.length,
            };
        };
        var c1 = null, c2 = null;
        if (xRelationship == "after") {
            if (linkMode == "link-table") {
                c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).y; })];
                c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).y; })];
            }
            else {
                c1 = candidates1[core_1.argMax(candidates1, function (c) { return meanPoint(c.points).x; })];
                c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).x; })];
            }
        }
        else if (xRelationship == "before") {
            if (linkMode == "link-table") {
                c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).y; })];
                c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).y; })];
            }
            else {
                c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).x; })];
                c2 = candidates2[core_1.argMax(candidates2, function (c) { return meanPoint(c.points).x; })];
            }
        }
        else {
            if (yRelationship == "after") {
                if (linkMode == "link-table") {
                    c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).x; })];
                    c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).x; })];
                }
                else {
                    c1 = candidates1[core_1.argMax(candidates1, function (c) { return meanPoint(c.points).y; })];
                    c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).y; })];
                }
            }
            else if (yRelationship == "before") {
                if (linkMode == "link-table") {
                    c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).x; })];
                    c2 = candidates2[core_1.argMin(candidates2, function (c) { return meanPoint(c.points).x; })];
                }
                else {
                    c1 = candidates1[core_1.argMin(candidates1, function (c) { return meanPoint(c.points).y; })];
                    c2 = candidates2[core_1.argMax(candidates2, function (c) { return meanPoint(c.points).y; })];
                }
            }
            else {
                c1 =
                    candidates1[core_1.argMin(candidates1, function (c) { return Math.abs(meanPoint(c.points).y); })];
                c2 =
                    candidates2[core_1.argMin(candidates2, function (c) { return Math.abs(meanPoint(c.points).y); })];
            }
        }
        switch (this.state.linkType) {
            case "line":
                {
                    if (c1 == null) {
                        c1 = {
                            element: null,
                            points: [
                                {
                                    xAttribute: "icx",
                                    yAttribute: "icy",
                                    x: 0,
                                    y: 0,
                                    direction: { x: 0, y: 0 },
                                },
                            ],
                        };
                    }
                    if (c2 == null) {
                        c2 = {
                            element: null,
                            points: [
                                {
                                    xAttribute: "icx",
                                    yAttribute: "icy",
                                    x: 0,
                                    y: 0,
                                    direction: { x: 0, y: 0 },
                                },
                            ],
                        };
                    }
                }
                break;
            case "band":
                {
                    if (c1 == null) {
                        c1 = {
                            element: null,
                            points: [
                                {
                                    xAttribute: "icx",
                                    yAttribute: "iy1",
                                    x: 0,
                                    y: 0,
                                    direction: { x: 1, y: 0 },
                                },
                                {
                                    xAttribute: "icx",
                                    yAttribute: "iy2",
                                    x: 0,
                                    y: 0,
                                    direction: { x: 1, y: 0 },
                                },
                            ],
                        };
                    }
                    if (c2 == null) {
                        c2 = {
                            element: null,
                            points: [
                                {
                                    xAttribute: "icx",
                                    yAttribute: "iy1",
                                    x: 0,
                                    y: 0,
                                    direction: { x: -1, y: 0 },
                                },
                                {
                                    xAttribute: "icx",
                                    yAttribute: "iy2",
                                    x: 0,
                                    y: 0,
                                    direction: { x: -1, y: 0 },
                                },
                            ],
                        };
                    }
                }
                break;
        }
        var anchor1 = c1.points.map(function (pt) {
            return {
                x: { element: c1.element, attribute: pt.xAttribute },
                y: { element: c1.element, attribute: pt.yAttribute },
                direction: pt.direction,
            };
        });
        var anchor2 = c2.points.map(function (pt) {
            return {
                x: { element: c2.element, attribute: pt.xAttribute },
                y: { element: c2.element, attribute: pt.yAttribute },
                direction: pt.direction,
            };
        });
        if (linkMode != "link-table") {
            if (c1.element != null) {
                var element1 = core_1.getById(glyph1.marks, c1.element);
                switch (element1.classID) {
                    case "mark.symbol":
                        {
                            if (element1.mappings.fill != null) {
                                color = element1.mappings.fill;
                            }
                        }
                        break;
                    case "mark.rect":
                        {
                            if (element1.mappings.fill != null) {
                                color = element1.mappings.fill;
                            }
                        }
                        break;
                }
            }
        }
        var interpolationType = "line";
        if (cs instanceof core_1.Graphics.PolarCoordinates) {
            interpolationType = "bezier";
        }
        else {
            interpolationType = "line";
        }
        // If directions are the same direction, switch line to circle.
        if (core_1.Geometry.vectorDot(anchor1[0].direction, anchor2[0].direction) > 0) {
            if (interpolationType == "line") {
                interpolationType = "circle";
            }
        }
        return {
            linkType: this.state.linkType,
            interpolationType: interpolationType,
            anchor1: anchor1,
            anchor2: anchor2,
            color: color,
            opacity: opacity,
        };
    };
    // eslint-disable-next-line
    LinkCreationPanel.prototype.getLinkObject = function () {
        var manager = this.store.chartManager;
        var plotSegmentIDs = this.state.selectedPlotSegments;
        var plotSegmentClasses = plotSegmentIDs.map(function (x) { return manager.getClassById(x); });
        var glyphs = plotSegmentClasses.map(function (c) { return manager.getObjectById(c.object.glyph); });
        switch (this.state.linkMode) {
            case "link-through": {
                // Find the first pair of glyphs
                var plotSegmentClass = plotSegmentClasses[0];
                var glyph = glyphs[0];
                var facetBy = this.groupBySelector
                    ? this.groupBySelector.value
                        ? [
                            this.groupBySelector.value
                                .expression,
                        ]
                        : []
                    : [];
                var facets = core_1.Prototypes.Links.facetRows(manager.dataflow.getTable(plotSegmentClass.object.table), plotSegmentClass.state.dataRowIndices, facetBy.map(function (x) { return manager.dataflow.cache.parse(x); }));
                var layoutState = plotSegmentClass.state;
                var rowToMarkState = new Map();
                for (var i = 0; i < layoutState.dataRowIndices.length; i++) {
                    rowToMarkState.set(layoutState.dataRowIndices[i].join(","), layoutState.glyphs[i]);
                }
                var _a = this.getDefaultAnchor(manager, "link-through", plotSegmentClass.getCoordinateSystem(), glyph, rowToMarkState.get(facets[0][0].join(",")), glyph, rowToMarkState.get(facets[0][1] ? facets[0][1].join(",") : facets[0][0].join(","))), linkType = _a.linkType, interpolationType = _a.interpolationType, anchor1 = _a.anchor1, anchor2 = _a.anchor2, color = _a.color, opacity = _a.opacity;
                var links = {
                    _id: core_1.uniqueID(),
                    classID: "links.through",
                    mappings: {
                        color: color,
                        opacity: opacity,
                    },
                    properties: {
                        name: "Link",
                        linkMarkType: "",
                        visible: true,
                        linkType: linkType,
                        interpolationType: interpolationType,
                        anchor1: anchor1,
                        anchor2: anchor2,
                        linkThrough: {
                            plotSegment: this.state.selectedPlotSegments[0],
                            facetExpressions: facetBy,
                        },
                        curveness: 30,
                        closeLink: false,
                        beginArrowType: links_1.ArrowType.NO_ARROW,
                        endArrowType: links_1.ArrowType.NO_ARROW,
                    },
                };
                return links;
            }
            case "link-between": {
                // Find the first pair of glyphs
                var firstGlyphs = plotSegmentClasses.map(function (x) { return x.state.glyphs[0]; });
                var _b = this.getDefaultAnchor(manager, "link-between", new core_1.Graphics.CartesianCoordinates(), glyphs[0], firstGlyphs[0], glyphs[1], firstGlyphs[1]), linkType = _b.linkType, interpolationType = _b.interpolationType, anchor1 = _b.anchor1, anchor2 = _b.anchor2, color = _b.color, opacity = _b.opacity;
                var links = {
                    _id: core_1.uniqueID(),
                    classID: "links.between",
                    mappings: {
                        color: color,
                        opacity: opacity,
                    },
                    properties: {
                        name: "Link",
                        linkMarkType: "",
                        visible: true,
                        linkType: linkType,
                        interpolationType: interpolationType,
                        anchor1: anchor1,
                        anchor2: anchor2,
                        linkBetween: {
                            plotSegments: plotSegmentIDs,
                        },
                        curveness: 30,
                        closeLink: false,
                        beginArrowType: links_1.ArrowType.NO_ARROW,
                        endArrowType: links_1.ArrowType.NO_ARROW,
                    },
                };
                return links;
            }
            case "link-table": {
                // Find the first pair of glyphs
                var firstGlyphs = plotSegmentClasses[0].state.glyphs;
                var _c = this.getDefaultAnchor(manager, "link-table", plotSegmentClasses[0].getCoordinateSystem(), glyphs[0], firstGlyphs[0], glyphs[0], firstGlyphs[1]), linkType = _c.linkType, interpolationType = _c.interpolationType, anchor1 = _c.anchor1, anchor2 = _c.anchor2, color = _c.color, opacity = _c.opacity;
                var links = {
                    _id: core_1.uniqueID(),
                    classID: "links.table",
                    mappings: {
                        color: color,
                        opacity: opacity,
                    },
                    properties: {
                        name: "Link",
                        linkMarkType: "",
                        visible: true,
                        linkType: linkType,
                        interpolationType: interpolationType,
                        anchor1: anchor1,
                        anchor2: anchor2,
                        linkTable: {
                            table: this.store.dataset.tables[1].name,
                            plotSegments: [
                                plotSegmentClasses[0].object._id,
                                plotSegmentClasses[0].object._id,
                            ],
                        },
                        curveness: 30,
                        closeLink: false,
                        beginArrowType: links_1.ArrowType.NO_ARROW,
                        endArrowType: links_1.ArrowType.NO_ARROW,
                    },
                };
                return links;
            }
        }
    };
    return LinkCreationPanel;
}(context_component_1.ContextedComponent));
exports.LinkCreationPanel = LinkCreationPanel;
var PlotSegmentSelector = /** @class */ (function (_super) {
    __extends(PlotSegmentSelector, _super);
    function PlotSegmentSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        return _this;
    }
    PlotSegmentSelector.prototype.getInitialState = function () {
        var plotSegments = this.props.items;
        return {
            order: plotSegments.map(function (x) { return x._id; }),
            selection: this.props.defaultSelection || plotSegments.map(function (x) { return x._id; }),
        };
    };
    PlotSegmentSelector.prototype.notify = function () {
        if (this.props.onChange) {
            this.props.onChange(this.state.selection);
        }
    };
    PlotSegmentSelector.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__plot-segment-selector charticulator-panel-list-view is-list" },
            React.createElement(object_list_editor_1.ReorderListView, { enabled: true, onReorder: function (a, b) {
                    var newOrder = _this.state.order.slice();
                    object_list_editor_1.ReorderListView.ReorderArray(newOrder, a, b);
                    var newSelection = _this.state.order.filter(function (x) { return _this.state.selection.indexOf(x) >= 0; });
                    _this.setState({
                        order: newOrder,
                        selection: newSelection,
                    }, function () { return _this.notify(); });
                } }, this.state.order.map(function (id) {
                var item = core_1.getById(_this.props.items, id);
                return (React.createElement("div", { key: id, className: utils_1.classNames("el-item", [
                        "is-active",
                        _this.state.selection.indexOf(id) >= 0,
                    ]), onClick: function (e) {
                        if (e.shiftKey) {
                            var newSelection = _this.state.order.filter(function (x) { return x == id || _this.state.selection.indexOf(x) >= 0; });
                            _this.setState({
                                selection: newSelection,
                            }, function () { return _this.notify(); });
                        }
                        else {
                            _this.setState({
                                selection: [id],
                            }, function () { return _this.notify(); });
                        }
                    } },
                    React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(item.classID).iconPath) }),
                    React.createElement("span", { className: "el-text" }, item.properties.name)));
            }))));
    };
    return PlotSegmentSelector;
}(context_component_1.ContextedComponent));
exports.PlotSegmentSelector = PlotSegmentSelector;
//# sourceMappingURL=link_creator.js.map