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
exports.SingleMarkView = exports.MarkEditorView = void 0;
var React = require("react");
var globals = require("../../globals");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var renderer_1 = require("../../renderer");
var stores_1 = require("../../stores");
var utils_1 = require("../../utils");
var controls_1 = require("../panels/widgets/controls");
var bounding_box_1 = require("./bounding_box");
var creating_component_1 = require("./creating_component");
var dropzone_1 = require("./dropzone");
var handles_1 = require("./handles");
var mark_1 = require("./snapping/mark");
var move_1 = require("./snapping/move");
var context_component_1 = require("../../context_component");
var guides_1 = require("../../../core/prototypes/guides");
var strings_1 = require("../../../strings");
var specification_1 = require("../../../core/specification");
var prototypes_1 = require("../../../core/prototypes");
/**
 * Editor view for glyph
 * ![Mark widgets](media://glyph_editor.png)
 */
var MarkEditorView = /** @class */ (function (_super) {
    __extends(MarkEditorView, _super);
    function MarkEditorView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.subs = [];
        _this.state = {
            currentCreation: null,
            width: 300,
            height: 300,
        };
        _this.resize = function () {
            var bbox = _this.refContainer.getBoundingClientRect();
            _this.setState({
                width: bbox.width,
                height: _this.props.height != null ? _this.props.height : bbox.height,
            });
        };
        return _this;
    }
    MarkEditorView.prototype.componentDidMount = function () {
        var _this = this;
        var chartStore = this.store;
        this.subs.push(chartStore.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); }));
        this.subs.push(chartStore.addListener(stores_1.AppStore.EVENT_SELECTION, function () { return _this.forceUpdate(); }));
        this.subs.push(chartStore.addListener(stores_1.AppStore.EVENT_CURRENT_TOOL, function () {
            _this.setState({
                currentCreation: chartStore.currentTool,
                currentCreationOptions: chartStore.currentToolOptions,
            });
        }));
        this.resizeListenerHandle = globals.resizeListeners.addListener(this.refContainer, this.resize);
        this.resize();
    };
    MarkEditorView.prototype.componentWillUnmount = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.subs), _c = _b.next(); !_c.done; _c = _b.next()) {
                var sub = _c.value;
                sub.remove();
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.subs = [];
        globals.resizeListeners.removeListener(this.refContainer, this.resizeListenerHandle);
    };
    MarkEditorView.prototype.getGlyphState = function (glyph) {
        var chartStore = this.store;
        // Find the plot segment's index
        var layoutIndex = core_1.indexOf(chartStore.chart.elements, function (e) {
            return core_1.Prototypes.isType(e.classID, "plot-segment") &&
                e.glyph == glyph._id;
        });
        if (layoutIndex == -1) {
            // Cannot find plot segment, return null
            return null;
        }
        else {
            // Find the selected glyph
            var plotSegmentState = chartStore.chartState.elements[layoutIndex];
            var glyphIndex = chartStore.getSelectedGlyphIndex(chartStore.chart.elements[layoutIndex]._id);
            // If found, use the glyph, otherwise fallback to the first glyph
            if (glyphIndex < 0) {
                return plotSegmentState.glyphs[0];
            }
            else {
                return plotSegmentState.glyphs[glyphIndex];
            }
        }
    };
    MarkEditorView.prototype.render = function () {
        var _this = this;
        var currentGlyph = this.store.currentGlyph;
        if (currentGlyph == null ||
            this.store.chart.glyphs.indexOf(currentGlyph) < 0) {
            currentGlyph = this.store.chart.glyphs[0];
        }
        return (React.createElement("div", { className: "mark-editor-view", ref: function (e) { return (_this.refContainer = e); } },
            currentGlyph ? (React.createElement(SingleMarkView, { ref: function (e) {
                    _this.refSingleMarkView = e;
                }, glyph: currentGlyph, glyphState: this.getGlyphState(currentGlyph), parent: this, width: this.state.width, height: this.state.height - 30 })) : (React.createElement("div", { className: "mark-editor-single-view" },
                React.createElement("div", { className: "mark-view-container", style: {
                        width: this.state.width + "px",
                        height: this.state.height - 24 + "px",
                    } },
                    React.createElement("div", { className: "mark-view-container-notice" }, "No glyph to edit")))),
            React.createElement("div", { className: "canvas-controls" },
                React.createElement("div", { className: "canvas-controls-left" },
                    React.createElement("span", { className: "glyph-tabs" }, this.store.chart.glyphs.map(function (glyph) { return (React.createElement("span", { tabIndex: 0, className: utils_1.classNames("el-item", [
                            "is-active",
                            glyph == currentGlyph,
                        ]), key: glyph._id, onClick: function () {
                            _this.dispatch(new actions_1.Actions.SelectGlyph(null, glyph));
                        }, onKeyPress: function (e) {
                            if (e.key === "Enter") {
                                _this.dispatch(new actions_1.Actions.SelectGlyph(null, glyph));
                            }
                        } }, glyph.properties.name)); })),
                    React.createElement(controls_1.Button, { icon: "general/plus", title: strings_1.strings.canvas.newGlyph, onClick: function () {
                            _this.dispatch(new actions_1.Actions.AddGlyph("glyph.rectangle"));
                        } })),
                React.createElement("div", { className: "canvas-controls-right" },
                    React.createElement(controls_1.Button, { icon: "ZoomIn", title: strings_1.strings.canvas.zoomIn, onClick: function () {
                            _this.refSingleMarkView.doZoom(1.1);
                        } }),
                    React.createElement(controls_1.Button, { icon: "ZoomOut", title: strings_1.strings.canvas.zoomOut, onClick: function () {
                            _this.refSingleMarkView.doZoom(1 / 1.1);
                        } }),
                    React.createElement(controls_1.Button, { icon: "ZoomToFit", title: strings_1.strings.canvas.zoomAuto, onClick: function () {
                            _this.refSingleMarkView.doZoomAuto();
                        } }),
                    React.createElement(controls_1.Button, { icon: "rect-zoom", title: "Rectangle zoom", onClick: function () {
                            _this.dispatch(new actions_1.Actions.SetCurrentTool("rectangle-zoom"));
                        } })))));
    };
    MarkEditorView.prototype.getCurrentCreation = function () {
        return this.state.currentCreation;
    };
    MarkEditorView.prototype.getCurrentCreationOptions = function () {
        return this.state.currentCreationOptions;
    };
    return MarkEditorView;
}(context_component_1.ContextedComponent));
exports.MarkEditorView = MarkEditorView;
var SingleMarkView = /** @class */ (function (_super) {
    __extends(SingleMarkView, _super);
    function SingleMarkView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.tokens = [];
        return _this;
    }
    SingleMarkView.prototype.getDefaultState = function () {
        return {
            showIndicator: false,
            showIndicatorActive: false,
            dataForDropZones: false,
            selectedElement: null,
            snappingCandidates: null,
            zoom: {
                centerX: this.props.width / 2,
                centerY: this.props.height / 2,
                scale: 1,
            },
        };
    };
    SingleMarkView.prototype.doZoom = function (factor) {
        var _a = this.state.zoom, scale = _a.scale, centerX = _a.centerX, centerY = _a.centerY;
        var fixPoint = core_1.Geometry.unapplyZoom(this.state.zoom, {
            x: this.props.width / 2,
            y: this.props.height / 2,
        });
        var newScale = scale * factor;
        newScale = Math.min(20, Math.max(0.05, newScale));
        this.setState({
            zoom: {
                centerX: centerX + (scale - newScale) * fixPoint.x,
                centerY: centerY + (scale - newScale) * fixPoint.y,
                scale: newScale,
            },
        });
    };
    SingleMarkView.prototype.doCustomZoom = function (cx, cy, width, height) {
        var newCX = this.props.width / 2 - cx;
        var newCY = this.props.height / 2 + cy;
        var newScale = this.props.width > this.props.height
            ? this.props.height / height
            : this.props.width / width;
        this.setState({
            zoom: {
                centerX: newCX,
                centerY: newCY,
                scale: 1,
            },
        });
        this.doZoom(newScale);
    };
    SingleMarkView.prototype.doZoomAuto = function () {
        var newZoom = this.getFitViewZoom(this.props.width, this.props.height);
        if (!newZoom) {
            return;
        }
        this.setState({
            zoom: newZoom,
        });
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.getFitViewZoom = function (width, height) {
        var e_2, _a;
        var glyphState = this.props.glyphState;
        if (!glyphState) {
            return null;
        }
        var manager = this.store.chartManager;
        // First we compute the maximum bounding box for marks in the glyph
        var boundingRects = [];
        try {
            // Get bounding box for each element
            for (var _b = __values(glyphState.marks), _c = _b.next(); !_c.done; _c = _b.next()) {
                var markState = _c.value;
                var cls = manager.getMarkClass(markState);
                var bbox = cls.getBoundingBox();
                if (bbox) {
                    var xBounds = [];
                    var yBounds = [];
                    switch (bbox.type) {
                        case "anchored-rectangle":
                            {
                                var bboxRect = bbox;
                                var cos = Math.cos(core_1.Geometry.degreesToRadians(bboxRect.rotation));
                                var sin = Math.sin(core_1.Geometry.degreesToRadians(bboxRect.rotation));
                                xBounds = [
                                    bboxRect.anchorX +
                                        bboxRect.cx +
                                        (bboxRect.width / 2) * cos +
                                        (bboxRect.height / 2) * sin,
                                    bboxRect.anchorX +
                                        bboxRect.cx -
                                        (bboxRect.width / 2) * cos +
                                        (bboxRect.height / 2) * sin,
                                    bboxRect.anchorX +
                                        bboxRect.cx +
                                        (bboxRect.width / 2) * cos -
                                        (bboxRect.height / 2) * sin,
                                    bboxRect.anchorX +
                                        bboxRect.cx -
                                        (bboxRect.width / 2) * cos -
                                        (bboxRect.height / 2) * sin,
                                ];
                                yBounds = [
                                    bboxRect.anchorY +
                                        bboxRect.cy +
                                        (bboxRect.width / 2) * -sin +
                                        (bboxRect.height / 2) * cos,
                                    bboxRect.anchorY +
                                        bboxRect.cy -
                                        (bboxRect.width / 2) * -sin +
                                        (bboxRect.height / 2) * cos,
                                    bboxRect.anchorY +
                                        bboxRect.cy +
                                        (bboxRect.width / 2) * -sin -
                                        (bboxRect.height / 2) * cos,
                                    bboxRect.anchorY +
                                        bboxRect.cy -
                                        (bboxRect.width / 2) * -sin -
                                        (bboxRect.height / 2) * cos,
                                ];
                            }
                            break;
                        case "rectangle":
                            {
                                var bboxRect = bbox;
                                xBounds = [
                                    bboxRect.cx + bboxRect.width / 2,
                                    bboxRect.cx - bboxRect.width / 2,
                                ];
                                yBounds = [
                                    bboxRect.cy + bboxRect.height / 2,
                                    bboxRect.cy - bboxRect.height / 2,
                                ];
                            }
                            break;
                        case "circle":
                            {
                                var bboxCircle = bbox;
                                xBounds = [
                                    bboxCircle.cx - bboxCircle.radius,
                                    bboxCircle.cx + bboxCircle.radius,
                                ];
                                yBounds = [
                                    bboxCircle.cy - bboxCircle.radius,
                                    bboxCircle.cy + bboxCircle.radius,
                                ];
                            }
                            break;
                        case "line": {
                            var bboxLine = bbox;
                            xBounds = [bboxLine.x1, bboxLine.x2];
                            yBounds = [bboxLine.y1, bboxLine.y2];
                        }
                    }
                    if (xBounds.length > 0) {
                        // y is the same size
                        boundingRects.push([
                            Math.min.apply(Math, __spread(xBounds)),
                            Math.max.apply(Math, __spread(xBounds)),
                            Math.min.apply(Math, __spread(yBounds)),
                            Math.max.apply(Math, __spread(yBounds)),
                        ]);
                    }
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
        // If there's no bounding rect found
        if (boundingRects.length == 0) {
            var cx = 0;
            var cy = 0;
            var _d = glyphState.attributes, x1 = _d.x1, x2 = _d.x2, y1 = _d.y1, y2 = _d.y2;
            var overshoot = 0.4;
            var scale1 = width / (1 + Math.abs(x2 - x1) * (1 + overshoot));
            var scale2 = height / (1 + Math.abs(y2 - y1) * (1 + overshoot));
            var scale = Math.min(scale1, scale2);
            var zoom = {
                centerX: width / 2 - cx * scale,
                centerY: height / 2 + cy * scale,
                scale: scale,
            };
            return zoom;
        }
        else {
            var x1 = Math.min.apply(Math, __spread(boundingRects.map(function (b) { return b[0]; })));
            var x2 = Math.max.apply(Math, __spread(boundingRects.map(function (b) { return b[1]; })));
            var y1 = Math.min.apply(Math, __spread(boundingRects.map(function (b) { return b[2]; })));
            var y2 = Math.max.apply(Math, __spread(boundingRects.map(function (b) { return b[3]; })));
            var cx = (x1 + x2) / 2;
            var cy = (y1 + y2) / 2;
            var overshoot = 0.4;
            var scale1 = width / (1 + Math.abs(x2 - x1) * (1 + overshoot));
            var scale2 = height / (1 + Math.abs(y2 - y1) * (1 + overshoot));
            var scale = Math.min(scale1, scale2);
            var zoom = {
                centerX: width / 2 - cx * scale,
                centerY: height / 2 + cy * scale,
                scale: scale,
            };
            return zoom;
        }
    };
    SingleMarkView.prototype.doAutoFit = function () {
        var newZoom = this.getFitViewZoom(this.props.width, this.props.height);
        if (!newZoom) {
            return;
        }
        this.setState({
            zoom: newZoom,
        });
    };
    SingleMarkView.prototype.scheduleAutoFit = function () {
        var _this = this;
        var token = this.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () {
            _this.doAutoFit();
            token.remove();
        });
    };
    SingleMarkView.prototype.getRelativePoint = function (point) {
        var r = this.refs.canvas.getBoundingClientRect();
        return {
            x: point.x - r.left,
            y: point.y - r.top,
        };
    };
    SingleMarkView.prototype.onDragEnter = function (ctx) {
        var _this = this;
        this.dispatch(new actions_1.Actions.SetCurrentTool(null));
        var data = ctx.data;
        if (data instanceof actions_1.DragData.ObjectType) {
            if (core_1.Prototypes.isType(data.classID, "mark") ||
                core_1.Prototypes.isType(data.classID, "guide")) {
                this.setState({
                    showIndicatorActive: true,
                });
                ctx.onLeave(function () {
                    _this.setState({
                        showIndicatorActive: false,
                    });
                });
                ctx.onDrop(function (point) {
                    point = _this.getRelativePoint(point);
                    var attributes = {};
                    var opt = JSON.parse(data.options);
                    _this.scheduleAutoFit();
                    for (var key in opt) {
                        if (Object.prototype.hasOwnProperty.call(opt, key)) {
                            attributes[key] = opt[key];
                        }
                    }
                    _this.dispatch(new actions_1.Actions.AddMarkToGlyph(_this.props.glyph, data.classID, core_1.Geometry.unapplyZoom(_this.state.zoom, point), {}, attributes));
                });
                return true;
            }
        }
        // if (data instanceof DragData.DropZoneData) {
        //     this.setState({
        //         dataForDropZones: data
        //     });
        //     ctx.onLeave(() => {
        //         this.setState({
        //             dataForDropZones: false
        //         });
        //     });
        //     return true;
        // }
        return false;
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.canvasInteraction);
        this.hammer.add(new Hammer.Tap());
        var pan = new Hammer.Pan();
        var pinch = new Hammer.Pinch();
        pinch.recognizeWith(pan);
        this.hammer.add([pinch]);
        this.hammer.on("tap", function () {
            _this.dispatch(new actions_1.Actions.SelectGlyph(null, _this.props.glyph));
        });
        var cX = null, cY = 0, cScale = 0;
        var dX0, dY0;
        var fixPoint = null;
        var lastDeltaX, lastDeltaY;
        var lastEventScale = 1;
        this.hammer.on("pinchstart panstart", function (e) {
            fixPoint = core_1.Geometry.unapplyZoom(_this.state.zoom, _this.getRelativePoint({ x: e.center.x, y: e.center.y }));
            cX = _this.state.zoom.centerX;
            cY = _this.state.zoom.centerY;
            cScale = _this.state.zoom.scale;
            dX0 = 0;
            dY0 = 0;
            lastDeltaX = 0;
            lastDeltaY = 0;
            lastEventScale = 1;
        });
        this.hammer.on("pinch pan", function (e) {
            if (e.type == "pan") {
                e.scale = lastEventScale;
            }
            lastEventScale = e.scale;
            var newScale = cScale * e.scale;
            newScale = Math.min(20, Math.max(0.05, newScale));
            _this.setState({
                zoom: {
                    centerX: cX + e.deltaX - dX0 + (cScale - newScale) * fixPoint.x,
                    centerY: cY + e.deltaY - dY0 + (cScale - newScale) * fixPoint.y,
                    scale: newScale,
                },
            });
            lastDeltaX = e.deltaX;
            lastDeltaY = e.deltaY;
        });
        this.refs.canvas.onwheel = function (e) {
            var fixPoint = core_1.Geometry.unapplyZoom(_this.state.zoom, _this.getRelativePoint({ x: e.pageX, y: e.pageY }));
            var _a = _this.state.zoom, centerX = _a.centerX, centerY = _a.centerY, scale = _a.scale;
            var delta = -e.deltaY;
            if (e.deltaMode == e.DOM_DELTA_LINE) {
                delta *= 33.3;
            }
            var newScale = scale * Math.exp(delta / 1000);
            newScale = Math.min(20, Math.max(0.05, newScale));
            _this.setState({
                zoom: {
                    centerX: centerX + (scale - newScale) * fixPoint.x,
                    centerY: centerY + (scale - newScale) * fixPoint.y,
                    scale: newScale,
                },
            });
            cX = _this.state.zoom.centerX;
            cY = _this.state.zoom.centerY;
            dX0 = lastDeltaX;
            dY0 = lastDeltaY;
            cScale = _this.state.zoom.scale;
            e.stopPropagation();
            e.preventDefault();
        };
        globals.dragController.registerDroppable(this, this.refs.canvas);
        this.tokens.push(globals.dragController.addListener("sessionstart", function () {
            var session = globals.dragController.getSession();
            if (session && session.data instanceof actions_1.DragData.DropZoneData) {
                _this.setState({
                    dataForDropZones: session.data,
                });
            }
            if (session && session.data instanceof actions_1.DragData.ObjectType) {
                if (core_1.Prototypes.isType(session.data.classID, "mark") ||
                    core_1.Prototypes.isType(session.data.classID, "guide")) {
                    _this.setState({
                        showIndicator: true,
                    });
                }
            }
        }));
        this.tokens.push(globals.dragController.addListener("sessionend", function () {
            _this.setState({
                dataForDropZones: false,
                showIndicator: false,
            });
        }));
    };
    SingleMarkView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        globals.dragController.unregisterDroppable(this);
        this.tokens.forEach(function (token) { return token.remove(); });
        this.tokens = [];
    };
    SingleMarkView.prototype.renderElementDefs = function (element, elementState) {
        var chartStore = this.store;
        var elementClass = chartStore.chartManager.getMarkClass(elementState);
        var graphics = elementClass.getGraphics(new core_1.Graphics.CartesianCoordinates(), { x: 0, y: 0 }, 0, chartStore.chartManager);
        if (!graphics) {
            return null;
        }
        return renderer_1.renderSVGDefs(graphics);
    };
    SingleMarkView.prototype.renderElement = function (element, elementState) {
        var chartStore = this.store;
        var elementClass = chartStore.chartManager.getMarkClass(elementState);
        var graphics = elementClass.getGraphics(new core_1.Graphics.CartesianCoordinates(), { x: 0, y: 0 }, 0, chartStore.chartManager);
        if (!graphics) {
            return null;
        }
        return renderer_1.renderGraphicalElementSVG(graphics);
    };
    SingleMarkView.prototype.renderDropIndicator = function () {
        if (!this.state.showIndicator) {
            return null;
        }
        return (React.createElement("rect", { x: 0, y: 0, width: this.props.width, height: this.props.height, className: utils_1.classNames("drop-indicator", [
                "active",
                this.state.showIndicatorActive,
            ]) }));
    };
    SingleMarkView.prototype.getSnappingGuides = function () {
        var e_3, _a;
        var guides;
        var chartStore = this.store;
        var glyphState = this.props.glyphState;
        if (!glyphState) {
            return [];
        }
        guides = chartStore.chartManager
            .getGlyphClass(glyphState)
            .getAlignmentGuides()
            .map(function (g) {
            return { element: null, guide: g };
        });
        var _loop_1 = function (element, elementState) {
            var elementClass = chartStore.chartManager.getMarkClass(elementState);
            guides = guides.concat(elementClass.getSnappingGuides().map(function (g) {
                return { element: element, guide: g };
            }));
        };
        try {
            for (var _b = __values(core_1.zip(this.props.glyph.marks, glyphState.marks)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var _d = __read(_c.value, 2), element = _d[0], elementState = _d[1];
                _loop_1(element, elementState);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return guides;
    };
    SingleMarkView.prototype.renderHandles = function () {
        return (React.createElement("g", null, this.renderElementHandles()));
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.renderBoundsGuides = function () {
        var _this = this;
        // eslint-disable-next-line
        return this.getSnappingGuides().map(function (info, idx) {
            var theGuide = info.guide;
            if (theGuide.visible) {
                if (theGuide.type == "x") {
                    var guide = theGuide;
                    return (React.createElement("line", { className: utils_1.classNames("mark-guide", [
                            "coordinator",
                            info.guide.visualType ===
                                prototypes_1.SnappingGuidesVisualTypes.Coordinator,
                        ], [
                            "single",
                            info.guide.visualType === prototypes_1.SnappingGuidesVisualTypes.Guide,
                        ]), key: "k" + idx, x1: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, x2: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, y1: 0, y2: _this.props.height }));
                }
                if (theGuide.type == "y") {
                    var guide = theGuide;
                    return (React.createElement("line", { className: utils_1.classNames("mark-guide", [
                            "coordinator",
                            info.guide.visualType ===
                                prototypes_1.SnappingGuidesVisualTypes.Coordinator,
                        ], [
                            "single",
                            info.guide.visualType === prototypes_1.SnappingGuidesVisualTypes.Guide,
                        ]), key: "k" + idx, x1: 0, x2: _this.props.width, y1: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY, y2: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY }));
                }
                if (theGuide.type == "point") {
                    var axisGuide = theGuide;
                    return (React.createElement(React.Fragment, null,
                        React.createElement("circle", { className: "mark-guide", key: "ck" + idx, cx: axisGuide.angle * _this.state.zoom.scale +
                                _this.state.zoom.centerX, cy: -axisGuide.radius * _this.state.zoom.scale +
                                _this.state.zoom.centerY, r: Math.abs(3 * _this.state.zoom.scale) }),
                        React.createElement("circle", { className: "mark-guide", key: "ck" + idx + "display", cx: axisGuide.cx * _this.state.zoom.scale + _this.state.zoom.centerX, cy: -axisGuide.cy * _this.state.zoom.scale +
                                _this.state.zoom.centerY, r: Math.abs(axisGuide.visibleRadius * _this.state.zoom.scale) }),
                        React.createElement("line", { key: "lk" + idx + "display", className: "mark-guide", x1: axisGuide.cx * _this.state.zoom.scale + _this.state.zoom.centerX, y1: -axisGuide.cy * _this.state.zoom.scale +
                                _this.state.zoom.centerY, x2: axisGuide.angle * _this.state.zoom.scale +
                                _this.state.zoom.centerX, y2: -axisGuide.radius * _this.state.zoom.scale +
                                _this.state.zoom.centerY })));
                }
            }
        });
    };
    SingleMarkView.prototype.renderMarkHandles = function () {
        var _this = this;
        var chartStore = this.store;
        var glyphState = this.props.glyphState;
        var markClass = chartStore.chartManager.getGlyphClass(glyphState);
        var handles = markClass.getHandles();
        return handles.map(function (handle, index) {
            return (React.createElement(handles_1.HandlesView, { key: "m" + index, handles: handles, zoom: _this.state.zoom, active: false, onDragStart: function (bound, ctx) {
                    var session = new move_1.MoveSnappingSession(bound);
                    ctx.onDrag(function (e) {
                        session.handleDrag(e);
                    });
                    ctx.onEnd(function (e) {
                        var updates = session.getUpdates(session.handleEnd(e));
                        if (updates) {
                            _this.dispatch(new actions_1.Actions.UpdateGlyphAttribute(_this.props.glyph, updates));
                        }
                    });
                } }));
        });
    };
    SingleMarkView.prototype.renderAnchorHandles = function () {
        var _this = this;
        return core_1.zipArray(this.props.glyph.marks, this.props.glyphState.marks)
            .filter(function (x) { return x[0].classID == "mark.anchor"; })
            .map(function (_a) {
            var _b = __read(_a, 2), element = _b[0], elementState = _b[1];
            var elementClass = _this.store.chartManager.getMarkClass(elementState);
            var bounds = elementClass.getHandles();
            return (React.createElement(handles_1.HandlesView, { key: "m" + element._id, handles: bounds, zoom: _this.state.zoom, active: _this.state.selectedElement == element, onDragStart: function (bound, ctx) {
                    var guides = _this.getSnappingGuides();
                    var session = new mark_1.MarkSnappingSession(guides, _this.props.glyph, element, elementState, bound, 10 / _this.state.zoom.scale, bound.options && bound.options.snapToClosestPoint);
                    ctx.onDrag(function (e) {
                        session.handleDrag(e);
                        _this.setState({
                            snappingCandidates: session.getCurrentCandidates(),
                        });
                    });
                    ctx.onEnd(function (e) {
                        _this.setState({
                            snappingCandidates: null,
                        });
                        var action = session.getActions(session.handleEnd(e));
                        if (action) {
                            _this.dispatch(action);
                        }
                    });
                } }));
        });
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.renderElementHandles = function () {
        var _this = this;
        return (core_1.zipArray(this.props.glyph.marks, this.props.glyphState.marks)
            .filter(function (x) { return x[0].classID != "mark.anchor"; })
            .sort(function (a, b) {
            var aSelected = _this.store.currentSelection instanceof stores_1.MarkSelection &&
                _this.store.currentSelection.mark == a[0];
            var bSelected = _this.store.currentSelection instanceof stores_1.MarkSelection &&
                _this.store.currentSelection.mark == b[0];
            if (aSelected) {
                return +1;
            }
            if (bSelected) {
                return -1;
            }
            return (_this.props.glyph.marks.indexOf(a[0]) -
                _this.props.glyph.marks.indexOf(b[0]));
        })
            // eslint-disable-next-line
            .map(function (_a) {
            var _b = __read(_a, 2), element = _b[0], elementState = _b[1];
            var elementClass = _this.store.chartManager.getMarkClass(elementState);
            var shouldRenderHandles = _this.store.currentSelection instanceof stores_1.MarkSelection &&
                _this.store.currentSelection.mark == element;
            if (!shouldRenderHandles) {
                var bbox_1 = elementClass.getBoundingBox();
                if (bbox_1) {
                    return (React.createElement(bounding_box_1.BoundingBoxView, { key: "m" + element._id, zoom: _this.state.zoom, boundingBox: bbox_1, onClick: function () {
                            _this.dispatch(new actions_1.Actions.SelectMark(null, _this.props.glyph, element));
                        } }));
                }
            }
            var handles = elementClass.getHandles();
            var bbox = elementClass.getBoundingBox();
            return (React.createElement("g", { key: "m" + element._id },
                bbox ? (React.createElement(bounding_box_1.BoundingBoxView, { zoom: _this.state.zoom, boundingBox: bbox, active: true })) : null,
                React.createElement(handles_1.HandlesView, { handles: handles, zoom: _this.state.zoom, active: false, visible: shouldRenderHandles, isAttributeSnapped: function (attribute) {
                        var e_4, _a;
                        if (element.mappings[attribute] != null) {
                            return true;
                        }
                        try {
                            for (var _b = __values(_this.props.glyph.constraints), _c = _b.next(); !_c.done; _c = _b.next()) {
                                var constraint = _c.value;
                                if (constraint.type == "snap") {
                                    if (constraint.attributes.element == element._id &&
                                        constraint.attributes.attribute == attribute) {
                                        return true;
                                    }
                                    if (constraint.attributes.targetElement == element._id &&
                                        constraint.attributes.targetAttribute == attribute) {
                                        return true;
                                    }
                                }
                            }
                        }
                        catch (e_4_1) { e_4 = { error: e_4_1 }; }
                        finally {
                            try {
                                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                            }
                            finally { if (e_4) throw e_4.error; }
                        }
                        return false;
                    }, onDragStart: function (handle, ctx) {
                        var guides = _this.getSnappingGuides();
                        var session = new mark_1.MarkSnappingSession(guides, _this.props.glyph, element, elementState, handle, 10 / _this.state.zoom.scale, handle.options && handle.options.snapToClosestPoint);
                        ctx.onDrag(function (e) {
                            session.handleDrag(e);
                            _this.setState({
                                snappingCandidates: session.getCurrentCandidates(),
                            });
                        });
                        ctx.onEnd(function (e) {
                            _this.setState({
                                snappingCandidates: null,
                            });
                            // if (handle.type == "text-input") {
                            //     let textInput = handle as Prototypes.Handles.TextInput;
                            //     ctx.onEnd(e => {
                            //         let updates: { [name: string]: Specification.Mapping }
                            //         new Actions.SetMarkAttribute(this.props.store.mark, element, textInput.attribute, { type: "value", value: e.newValue } as Specification.ValueMapping).dispatch(this.props.store.dispatcher);
                            //     })
                            // } else if (handle.type == "text-alignment") {
                            //     let textAlignment = handle as Prototypes.Handles.TextAlignment;
                            //     ctx.onEnd(e => {
                            //         new Actions.SetObjectProperty(element, textAlignment.propertyAlignment, null, e.newAlignment).dispatch(this.props.store.dispatcher);
                            //         new Actions.SetObjectProperty(element, textAlignment.propertyRotation, null, e.newRotation).dispatch(this.props.store.dispatcher);
                            //     })
                            // } else {
                            var action = session.getActions(session.handleEnd(e));
                            if (action) {
                                _this.dispatch(action);
                            }
                            // }
                        });
                    } })));
            // } else {
            //     let bbox = elementClass.getBoundingBox();
            //     if (bbox) {
            //         return (
            //             <BoundingBoxView
            //                 key={`m${element._id}`}
            //                 zoom={this.state.zoom}
            //                 boundingBox={bbox}
            //                 onClick={() => {
            //                     new Actions.SelectElement(this.props.store.mark, element).dispatch(this.props.store.dispatcher);
            //                 }}
            //             />
            //         );
            //     } else {
            //         let handles = elementClass.getHandles();
            //         return (
            //             <HandlesView
            //                 key={`m${element._id}`}
            //                 handles={handles}
            //                 zoom={this.state.zoom}
            //                 active={true}
            //                 visible={false}
            //                 onDragStart={(handle, ctx) => {
            //                     let guides = this.getSnappingGuides();
            //                     let session = new MarkSnappingSession(guides, this.props.store.mark, element, elementState, handle, 10 / this.state.zoom.scale);
            //                     ctx.onDrag((e) => {
            //                         session.handleDrag(e);
            //                         this.setState({
            //                             snappingCandidates: session.getCurrentCandidates()
            //                         });
            //                     });
            //                     ctx.onEnd((e) => {
            //                         this.setState({
            //                             snappingCandidates: null
            //                         });
            //                         let action = session.getActions(session.handleEnd(e));
            //                         if (action) {
            //                             action.dispatch(this.props.store.dispatcher);
            //                         }
            //                     });
            //                 }}
            //             />
            //         );
            //     }
            // }
        }));
    };
    SingleMarkView.prototype.renderDropZoneForElement = function (data, element, state) {
        var _this = this;
        var cls = this.store.chartManager.getMarkClass(state);
        return cls
            .getDropZones()
            .map(function (zone, idx) {
            if (zone.accept) {
                if (zone.accept.table) {
                    if (data.table.name != zone.accept.table) {
                        return null;
                    }
                }
                if (zone.accept.kind) {
                    if (data.metadata.kind != zone.accept.kind) {
                        return null;
                    }
                }
            }
            return (React.createElement(dropzone_1.DropZoneView, { key: "m" + idx, onDragEnter: function (data) {
                    if (data instanceof actions_1.DragData.DataExpression) {
                        if (zone.accept) {
                            if (zone.accept.table) {
                                if (data.table.name != zone.accept.table) {
                                    return null;
                                }
                            }
                            if (zone.accept.kind) {
                                if (data.metadata.kind != zone.accept.kind) {
                                    return null;
                                }
                            }
                        }
                        if (zone.dropAction.scaleInference) {
                            return function (point, modifiers) {
                                if (!zone.dropAction.scaleInference.hints) {
                                    zone.dropAction.scaleInference.hints = {};
                                }
                                zone.dropAction.scaleInference.hints.newScale =
                                    modifiers.shiftKey;
                                _this.dispatch(new actions_1.Actions.MapDataToMarkAttribute(_this.props.glyph, element, zone.dropAction.scaleInference.attribute, zone.dropAction.scaleInference.attributeType, data.expression, data.valueType, data.metadata, zone.dropAction.scaleInference.hints, data.table.name));
                                return true;
                            };
                        }
                        if (zone.dropAction.axisInference) {
                            return function () {
                                _this.dispatch(new actions_1.Actions.BindDataToAxis(element, zone.dropAction.axisInference.property, zone.dropAction.axisInference.appendToProperty, data, false));
                                return true;
                            };
                        }
                    }
                }, zone: zone, zoom: _this.state.zoom }));
        });
    };
    SingleMarkView.prototype.renderSnappingGuidesLabels = function () {
        var e_5, _a, e_6, _b;
        var _this = this;
        var allLabels = [];
        try {
            for (var _c = __values(core_1.zip(this.props.glyph.marks, this.props.glyphState.marks)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), elementState = _e[1];
                var elementClass = this.store.chartManager.getMarkClass(elementState);
                var guides = elementClass.getSnappingGuides();
                try {
                    for (var guides_2 = (e_6 = void 0, __values(guides)), guides_2_1 = guides_2.next(); !guides_2_1.done; guides_2_1 = guides_2.next()) {
                        var item = guides_2_1.value;
                        if (item.type == "label" || item.type == "point") {
                            allLabels.push(item);
                        }
                    }
                }
                catch (e_6_1) { e_6 = { error: e_6_1 }; }
                finally {
                    try {
                        if (guides_2_1 && !guides_2_1.done && (_b = guides_2.return)) _b.call(guides_2);
                    }
                    finally { if (e_6) throw e_6.error; }
                }
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_5) throw e_5.error; }
        }
        if (allLabels.length == 0) {
            return null;
        }
        return (React.createElement("g", null, allLabels.map(function (guide, i) {
            switch (guide.type) {
                case "point": {
                    var axisGuide = guide;
                    return (React.createElement(React.Fragment, null,
                        React.createElement("circle", { className: "snapping-guide", key: "k" + i, cx: axisGuide.angle * _this.state.zoom.scale +
                                _this.state.zoom.centerX, cy: -axisGuide.radius * _this.state.zoom.scale +
                                _this.state.zoom.centerY, r: Math.abs(5 * _this.state.zoom.scale) })));
                }
                case "label": {
                    var label = guide;
                    var x = label.x * _this.state.zoom.scale + _this.state.zoom.centerX;
                    var y = -label.y * _this.state.zoom.scale + _this.state.zoom.centerY;
                    return (React.createElement("g", { transform: "translate(" + x + "," + y + ")", className: "snapping-guide-label", key: i },
                        React.createElement("circle", { cx: 0, cy: 0, r: 2 }),
                        React.createElement("text", { x: 5, y: 5, transform: "rotate(45)" }, label.text)));
                }
            }
        })));
    };
    SingleMarkView.prototype.renderSnappingGuides = function () {
        var _this = this;
        var guides = this.state.snappingCandidates;
        if (!guides || guides.length == 0) {
            return null;
        }
        return guides.map(function (guide, idx) {
            var key = "m" + idx;
            switch (guide.guide.type) {
                case "x": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", x1: axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerX, x2: axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerX, y1: 0, y2: _this.props.height }));
                }
                case "y": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", y1: -axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerY, y2: -axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerY, x1: 0, x2: _this.props.width }));
                }
            }
        });
    };
    SingleMarkView.prototype.renderMarkGuides = function () {
        var _this = this;
        var markClass = this.store.chartManager.getGlyphClass(this.props.glyphState);
        var markGuides = markClass.getAlignmentGuides();
        return markGuides.map(function (theGuide, idx) {
            if (theGuide.type == "x") {
                var guide = theGuide;
                return (React.createElement("line", { className: "mark-guide", key: "k" + idx, x1: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, x2: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, y1: 0, y2: _this.props.height }));
            }
            if (theGuide.type == "y") {
                var guide = theGuide;
                return (React.createElement("line", { className: "mark-guide", key: "k" + idx, y1: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY, y2: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY, x1: 0, x2: _this.props.width }));
            }
        });
    };
    SingleMarkView.prototype.renderAnchor = function () {
        var _a = this.props, glyph = _a.glyph, glyphState = _a.glyphState;
        var anchorIndex = core_1.indexOf(glyph.marks, function (x) { return x.classID == "mark.anchor"; });
        var pt = {
            x: glyphState.marks[anchorIndex].attributes.x,
            y: -glyphState.marks[anchorIndex].attributes.y,
        };
        pt = core_1.Geometry.applyZoom(this.state.zoom, pt);
        return (React.createElement("path", { d: "M" + (pt.x - 5) + "," + pt.y + "L" + pt.x + "," + (pt.y - 5) + "L" + (pt.x + 5) + "," + pt.y + "L" + pt.x + "," + (pt.y + 5) + "Z", className: "mark-anchor" }));
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.renderCreatingComponent = function () {
        var _this = this;
        var currentCreation = this.props.parent.getCurrentCreation();
        var currentCreationOptions = this.props.parent.getCurrentCreationOptions();
        if (currentCreation == null) {
            return null;
        }
        var metadata = core_1.Prototypes.ObjectClasses.GetMetadata(currentCreation);
        if (metadata && metadata.creatingInteraction) {
            var classID_1 = currentCreation;
            return (React.createElement(creating_component_1.CreatingComponentFromCreatingInteraction, { width: this.props.width, height: this.props.height, zoom: this.state.zoom, guides: this.getSnappingGuides(), description: metadata.creatingInteraction, onCreate: function (mappings, attributes) {
                    _this.dispatch(new actions_1.Actions.SetCurrentTool(null));
                    var opt = JSON.parse(currentCreationOptions);
                    for (var key in opt) {
                        if (Object.prototype.hasOwnProperty.call(opt, key)) {
                            attributes[key] = opt[key];
                        }
                    }
                    _this.dispatch(new actions_1.Actions.AddMarkToGlyph(_this.props.glyph, classID_1, { x: 0, y: 0 }, mappings, attributes));
                }, onCancel: function () {
                    _this.dispatch(new actions_1.Actions.SetCurrentTool(null));
                } }));
        }
        else {
            var onCreate_1 = null;
            var mode = "point";
            var addGuide_1 = function (arg, axis, outerAttr, lowAttr, highAttr, baselineLow, baselineMid, baselineHigh) {
                var pos = arg[0];
                var outer = +_this.props.glyphState.attributes[outerAttr];
                var low = +_this.props.glyphState.attributes[lowAttr];
                var high = +_this.props.glyphState.attributes[highAttr];
                var quarter = outer / 4;
                var rel;
                var baseline;
                if (pos < low + quarter) {
                    // relative to low
                    baseline = baselineLow;
                    rel = pos - low;
                }
                else if (pos < quarter) {
                    // relative to mid
                    baseline = baselineMid;
                    rel = pos;
                }
                else {
                    // relative to high
                    baseline = baselineHigh;
                    rel = pos - high;
                }
                var value = [rel, arg[1]];
                var guideProperties = {
                    axis: axis,
                    baseline: baseline,
                };
                _this.dispatch(new actions_1.Actions.AddMarkToGlyph(_this.props.glyph, "guide.guide", { x: 0, y: 0 }, {
                    value: [
                        value[0],
                        {
                            type: specification_1.MappingType.value,
                            value: value[0],
                        },
                    ],
                }, guideProperties));
            };
            switch (currentCreation) {
                case "guide-x":
                    {
                        mode = "vline";
                        onCreate_1 = function (x) {
                            return addGuide_1(x, "x", "width", "ix1", "ix2", "left", "center", "right");
                        };
                    }
                    break;
                case "guide-y":
                    {
                        mode = "hline";
                        onCreate_1 = function (y) {
                            return addGuide_1(y, "y", "height", "iy1", "iy2", "bottom", "middle", "top");
                        };
                    }
                    break;
                case "guide-coordinator-x":
                    {
                        mode = "line";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            _this.dispatch(new actions_1.Actions.AddMarkToGlyph(_this.props.glyph, "guide.guide-coordinator", { x: 0, y: 0 }, { x1: x1, y1: y1, x2: x2, y2: y2 }, {
                                axis: "x",
                                count: guides_1.GuideCoordinatorClass.defaultAttributes.count,
                            }));
                        };
                    }
                    break;
                case "guide-coordinator-y":
                    {
                        mode = "line";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            _this.dispatch(new actions_1.Actions.AddMarkToGlyph(_this.props.glyph, "guide.guide-coordinator", { x: 0, y: 0 }, { x1: x1, y1: y1, x2: x2, y2: y2 }, {
                                axis: "y",
                                count: guides_1.GuideCoordinatorClass.defaultAttributes.count,
                            }));
                        };
                    }
                    break;
                // Uncomment to allow polar guide coordinates in mark/glyph editor
                // case "guide-coordinator-polar":
                //   {
                //     mode = "rectangle";
                //     onCreate = (x1, y1, x2, y2) => {
                //       this.dispatch(
                //         new Actions.AddMarkToGlyph(
                //           this.props.glyph,
                //           "guide.guide-coordinator-polar",
                //           { x: 0, y: 0 },
                //           { x1, y1, x2, y2 },
                //           {
                //             axis: "xy",
                //             angularGuidesCount: 4,
                //             radialGuidesCount: 2,
                //             startAngle: 45,
                //             endAngle: 405,
                //             innerRatio: 0.0,
                //             outerRatio: 1,
                //           }
                //         )
                //       );
                //     };
                //   }
                //   break;
                case "rectangle-zoom":
                    {
                        mode = "rectangle";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            var width = Math.abs(x2[0] - x1[0]);
                            var height = Math.abs(y2[0] - y1[0]);
                            var centerX = Math.min(x2[0], x1[0]) + width / 2;
                            var centerY = Math.min(y2[0], y1[0]) + height / 2;
                            _this.doCustomZoom(centerX, centerY, width, height);
                        };
                    }
                    break;
            }
            return (React.createElement(creating_component_1.CreatingComponent, { width: this.props.width, height: this.props.height, zoom: this.state.zoom, mode: mode, key: mode, guides: this.getSnappingGuides(), onCreate: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this.dispatch(new actions_1.Actions.SetCurrentTool(null));
                    if (onCreate_1) {
                        onCreate_1.apply(void 0, __spread(args));
                    }
                }, onCancel: function () {
                    _this.dispatch(new actions_1.Actions.SetCurrentTool(null));
                } }));
        }
    };
    // eslint-disable-next-line
    SingleMarkView.prototype.render = function () {
        var _this = this;
        var _a = this.props, glyph = _a.glyph, glyphState = _a.glyphState;
        var transform = "translate(" + this.state.zoom.centerX + "," + this.state.zoom.centerY + ") scale(" + this.state.zoom.scale + ")";
        if (!glyphState) {
            return (React.createElement("div", { className: "mark-editor-single-view" },
                React.createElement("div", { className: "mark-view-container" },
                    React.createElement("svg", { className: "canvas-view canvas-view-mark", ref: "canvas", x: 0, y: 0, width: this.props.width - 4, height: this.props.height },
                        React.createElement("rect", { ref: "canvasInteraction", className: "interaction-handler", x: 0, y: 0, width: this.props.width, height: this.props.height })),
                    React.createElement("div", { className: "mark-view-container-notice" }, strings_1.strings.canvas.markContainer))));
        }
        return (React.createElement("div", { className: "mark-editor-single-view" },
            React.createElement("div", { className: "mark-view-container", style: {
                    width: this.props.width,
                    height: this.props.height,
                } },
                React.createElement("svg", { className: "canvas-view canvas-view-mark", ref: "canvas", x: 0, y: 0, width: this.props.width - 4, height: this.props.height },
                    React.createElement("defs", null, core_1.zipArray(glyph.marks, glyphState.marks).map(function (_a) {
                        var _b = __read(_a, 2), elements = _b[0], elementState = _b[1];
                        return (React.createElement(React.Fragment, { key: "SVGDefs-" + elements._id }, _this.renderElementDefs(elements, elementState)));
                    })),
                    React.createElement("rect", { ref: "canvasInteraction", className: "interaction-handler", x: 0, y: 0, width: this.props.width, height: this.props.height }),
                    this.renderBoundsGuides(),
                    React.createElement("g", { ref: "zoomable", transform: transform, className: "graphics" }, core_1.zipArray(glyph.marks, glyphState.marks).map(function (_a) {
                        var _b = __read(_a, 2), elements = _b[0], elementState = _b[1];
                        return (React.createElement("g", { key: "m" + elements._id }, _this.renderElement(elements, elementState)));
                    })),
                    this.renderSnappingGuides(),
                    this.renderSnappingGuidesLabels(),
                    React.createElement("g", null, !this.state.dataForDropZones ? this.renderHandles() : null),
                    React.createElement("g", null, this.state.dataForDropZones
                        ? core_1.zipArray(glyph.marks, glyphState.marks).map(function (_a) {
                            var _b = __read(_a, 2), elements = _b[0], elementState = _b[1];
                            return (React.createElement("g", { key: "m" + elements._id }, _this.renderDropZoneForElement(_this.state.dataForDropZones, elements, elementState)));
                        })
                        : null),
                    React.createElement("g", null, this.renderDropIndicator()),
                    this.renderCreatingComponent()))));
    };
    return SingleMarkView;
}(context_component_1.ContextedComponent));
exports.SingleMarkView = SingleMarkView;
//# sourceMappingURL=mark_editor.js.map