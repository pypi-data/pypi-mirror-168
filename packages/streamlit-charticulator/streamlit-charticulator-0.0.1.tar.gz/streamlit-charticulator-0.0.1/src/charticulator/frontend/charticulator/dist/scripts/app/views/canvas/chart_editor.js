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
exports.ChartEditorView = void 0;
var React = require("react");
var R = require("../../resources");
var globals = require("../../globals");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var renderer_1 = require("../../renderer");
var stores_1 = require("../../stores");
var controls_1 = require("../panels/widgets/controls");
var bounding_box_1 = require("./bounding_box");
var creating_component_1 = require("./creating_component");
var dropzone_1 = require("./dropzone");
var editing_link_1 = require("./editing_link");
var handles_1 = require("./handles");
var resize_1 = require("./handles/resize");
var chart_1 = require("./snapping/chart");
var move_1 = require("./snapping/move");
var guides_1 = require("../../../core/prototypes/guides");
var strings_1 = require("../../../strings");
var specification_1 = require("../../../core/specification");
var prototypes_1 = require("../../../core/prototypes");
var utils_1 = require("../../utils");
var fluentui_manager_1 = require("../panels/widgets/fluentui_manager");
var react_1 = require("@fluentui/react");
/**
 * Editor view for chart
 * ![Mark widgets](media://chart_editor.png)
 */
var ChartEditorView = /** @class */ (function (_super) {
    __extends(ChartEditorView, _super);
    function ChartEditorView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            zoom: {
                centerX: 50,
                centerY: 50,
                scale: 1,
            },
            snappingCandidates: null,
            graphics: _this.getGraphics(),
            currentCreation: null,
            currentSelection: _this.props.store.currentSelection,
            dropZoneData: false,
            viewWidth: 100,
            viewHeight: 100,
            isSolving: false,
            canvasToolbar: true,
        };
        _this.tokens = [];
        return _this;
    }
    ChartEditorView.prototype.getRelativePoint = function (point) {
        var r = this.refs.canvas.getBoundingClientRect();
        return {
            x: point.x - r.left,
            y: point.y - r.top,
        };
    };
    ChartEditorView.prototype.getFitViewZoom = function (width, height) {
        var chartState = this.props.store.chartState;
        var x1 = chartState.attributes.x1;
        var y1 = chartState.attributes.y1;
        var x2 = chartState.attributes.x2;
        var y2 = chartState.attributes.y2;
        var overshoot = 0.4;
        var scale1 = width / (Math.abs(x2 - x1) * (1 + overshoot));
        var scale2 = height / (Math.abs(y2 - y1) * (1 + overshoot));
        var zoom = {
            centerX: width / 2,
            centerY: height / 2,
            scale: Math.min(scale1, scale2),
        };
        return zoom;
    };
    // eslint-disable-next-line
    ChartEditorView.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.canvasInteraction);
        this.hammer.add(new Hammer.Tap());
        var pan = new Hammer.Pan();
        var pinch = new Hammer.Pinch();
        pinch.recognizeWith(pan);
        this.hammer.add([pinch]);
        this.hammer.on("tap", function () {
            new actions_1.Actions.ClearSelection().dispatch(_this.props.store.dispatcher);
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
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, this.updateGraphics.bind(this)));
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_SELECTION, this.updateSelection.bind(this)));
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_CURRENT_TOOL, function () {
            _this.setState({
                currentCreation: _this.props.store.currentTool,
                currentCreationOptions: _this.props.store.currentToolOptions,
            });
        }));
        // We display the working icon after 200ms.
        var newStateTimer = null;
        this.tokens.push(this.props.store.addListener(stores_1.AppStore.EVENT_SOLVER_STATUS, function () {
            var newState = _this.props.store.solverStatus.solving;
            if (newState) {
                if (!newStateTimer) {
                    newStateTimer = setTimeout(function () {
                        _this.setState({ isSolving: true });
                    }, 500);
                }
            }
            else {
                if (newStateTimer) {
                    clearTimeout(newStateTimer);
                    newStateTimer = null;
                }
                _this.setState({ isSolving: false });
            }
        }));
        var doResize = function () {
            if (!_this.refs.canvasContainer) {
                return;
            }
            var rect = _this.refs.canvasContainer.getBoundingClientRect();
            var width = rect.width;
            var height = rect.height;
            _this.setState({
                viewWidth: width,
                viewHeight: height,
                zoom: _this.getFitViewZoom(width, height),
            });
        };
        globals.resizeListeners.addListener(this.refs.canvasContainer, doResize);
        doResize();
        this.tokens.push(globals.dragController.addListener("sessionstart", function () {
            var session = globals.dragController.getSession();
            if (session && session.data instanceof actions_1.DragData.DropZoneData) {
                _this.setState({
                    dropZoneData: { data: session.data },
                });
            }
        }));
        this.tokens.push(globals.dragController.addListener("sessionend", function () {
            _this.setState({
                dropZoneData: false,
            });
        }));
    };
    ChartEditorView.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
        this.tokens.forEach(function (t) { return t.remove(); });
        globals.dragController.unregisterDroppable(this);
    };
    ChartEditorView.prototype.onDragEnter = function (ctx) {
        var _this = this;
        new actions_1.Actions.SetCurrentTool(null).dispatch(this.props.store.dispatcher);
        var data = ctx.data;
        if (data instanceof actions_1.DragData.ScaffoldType) {
            this.setState({
                dropZoneData: { layout: data },
            });
            ctx.onLeave(function () {
                _this.setState({
                    dropZoneData: false,
                });
            });
            return true;
        }
        return false;
    };
    ChartEditorView.prototype.getGraphics = function () {
        var renderer = new core_1.Graphics.ChartRenderer(this.props.store.chartManager, this.props.store.renderEvents);
        return renderer.render();
    };
    ChartEditorView.prototype.updateSelection = function () {
        this.setState({ currentSelection: this.props.store.currentSelection });
        this.setState({
            canvasToolbar: true,
        });
    };
    ChartEditorView.prototype.updateGraphics = function () {
        this.setState({ graphics: this.getGraphics() });
    };
    ChartEditorView.prototype.renderGraphics = function () {
        var renderer = new core_1.Graphics.ChartRenderer(this.props.store.chartManager, this.props.store.renderEvents);
        return (React.createElement(React.Fragment, { key: "graphics" },
            React.createElement(renderer_1.GraphicalElementDisplay, { element: this.state.graphics }),
            React.createElement("g", { className: "canvas-chart-controls" }, renderer.renderControls(this.props.store.chart, this.props.store.chartState, this.state.zoom))));
    };
    ChartEditorView.prototype.renderEditingLink = function () {
        var store = this.props.store;
        if (store.currentSelection instanceof stores_1.ChartElementSelection) {
            var element = store.currentSelection.chartElement;
            if (core_1.Prototypes.isType(element.classID, "links")) {
                return (React.createElement(editing_link_1.EditingLink, { width: this.state.viewWidth, height: this.state.viewHeight, zoom: this.state.zoom, store: store, link: element }));
            }
        }
        return null;
    };
    // eslint-disable-next-line
    ChartEditorView.prototype.renderCreatingComponent = function () {
        var _this = this;
        if (this.state.currentCreation == null) {
            return null;
        }
        var metadata = core_1.Prototypes.ObjectClasses.GetMetadata(this.state.currentCreation);
        if (metadata && metadata.creatingInteraction) {
            var classID_1 = this.state.currentCreation;
            var options_1 = this.state.currentCreationOptions;
            return (React.createElement(creating_component_1.CreatingComponentFromCreatingInteraction, { width: this.state.viewWidth, height: this.state.viewHeight, zoom: this.state.zoom, guides: this.getSnappingGuides(), description: metadata.creatingInteraction, onCreate: function (mappings, attributes) {
                    new actions_1.Actions.SetCurrentTool(null).dispatch(_this.props.store.dispatcher);
                    var opt = JSON.parse(options_1);
                    for (var key in opt) {
                        if (Object.prototype.hasOwnProperty.call(opt, key)) {
                            attributes[key] = opt[key];
                        }
                    }
                    new actions_1.Actions.AddChartElement(classID_1, mappings, attributes).dispatch(_this.props.store.dispatcher);
                }, onCancel: function () {
                    new actions_1.Actions.SetCurrentTool(null).dispatch(_this.props.store.dispatcher);
                } }));
        }
        else {
            var onCreate_1 = null;
            var mode = "point";
            var addGuide_1 = function (arg, axis, outerAttr, lowMarginAttr, highMarginAttr, baselineLow, baselineMid, baselineHigh) {
                var outer = +_this.props.store.chartState.attributes[outerAttr];
                var lowMargin = +_this.props.store.chartState.attributes[lowMarginAttr];
                var highMargin = +_this.props.store.chartState.attributes[highMarginAttr];
                var fromCenter = arg[0];
                var abs = outer / 2 + fromCenter;
                var inner = outer - lowMargin - highMargin;
                var half = inner / 2;
                var quarter = half / 2;
                var lowAbs = lowMargin;
                var halfAbs = lowMargin + half;
                var highAbs = outer - highMargin;
                var rel;
                var baseline;
                if (abs < lowAbs + quarter) {
                    // relative to low
                    baseline = baselineLow;
                    rel = abs - lowAbs;
                }
                else if (abs < halfAbs + quarter) {
                    // relative to mid
                    baseline = baselineMid;
                    rel = abs - halfAbs;
                }
                else {
                    // relative to high
                    baseline = baselineHigh;
                    rel = abs - highAbs;
                }
                var value = [rel, arg[1]];
                var guideProperties = {
                    axis: axis,
                    baseline: baseline,
                };
                new actions_1.Actions.AddChartElement("guide.guide", {
                    value: [
                        value[0],
                        {
                            type: specification_1.MappingType.value,
                            value: value[0],
                        },
                    ],
                }, guideProperties).dispatch(_this.props.store.dispatcher);
            };
            switch (this.state.currentCreation) {
                case "guide-x":
                    {
                        mode = "vline";
                        onCreate_1 = function (x) {
                            return addGuide_1(x, "x", "width", "marginLeft", "marginRight", "left", "center", "right");
                        };
                    }
                    break;
                case "guide-y":
                    {
                        mode = "hline";
                        onCreate_1 = function (y) {
                            return addGuide_1(y, "y", "height", "marginBottom", "marginTop", "bottom", "middle", "top");
                        };
                    }
                    break;
                case "guide-coordinator-x":
                    {
                        mode = "line";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            new actions_1.Actions.AddChartElement("guide.guide-coordinator", { x1: x1, y1: y1, x2: x2, y2: y2 }, {
                                axis: "x",
                                count: guides_1.GuideCoordinatorClass.defaultAttributes.count,
                            }).dispatch(_this.props.store.dispatcher);
                        };
                    }
                    break;
                case "guide-coordinator-y":
                    {
                        mode = "line";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            new actions_1.Actions.AddChartElement("guide.guide-coordinator", { x1: x1, y1: y1, x2: x2, y2: y2 }, {
                                axis: "y",
                                count: guides_1.GuideCoordinatorClass.defaultAttributes.count,
                            }).dispatch(_this.props.store.dispatcher);
                        };
                    }
                    break;
                case "guide-coordinator-polar":
                    {
                        mode = "rectangle";
                        onCreate_1 = function (x1, y1, x2, y2) {
                            new actions_1.Actions.AddChartElement("guide.guide-coordinator-polar", { x1: x1, y1: y1, x2: x2, y2: y2 }, {
                                axis: "xy",
                                angularGuidesCount: 4,
                                radialGuidesCount: 1,
                                startAngle: 0,
                                endAngle: 360,
                                innerRatio: 0.0,
                                outerRatio: 1,
                            }).dispatch(_this.props.store.dispatcher);
                        };
                    }
                    break;
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
            return (React.createElement(creating_component_1.CreatingComponent, { width: this.state.viewWidth, height: this.state.viewHeight, zoom: this.state.zoom, mode: mode, key: mode, guides: this.getSnappingGuides(), 
                // tslint:disable-next-line
                onCreate: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    new actions_1.Actions.SetCurrentTool(null).dispatch(_this.props.store.dispatcher);
                    // let newArgs = args.map(([value, mapping]) => {
                    //     return [value, mapping || { type: "value", value: value } as Specification.ValueMapping]
                    // }) as [number, Specification.Mapping][];
                    if (onCreate_1) {
                        onCreate_1.apply(void 0, __spread(args));
                    }
                }, onCancel: function () {
                    new actions_1.Actions.SetCurrentTool(null).dispatch(_this.props.store.dispatcher);
                } }));
        }
    };
    ChartEditorView.prototype.doCustomZoom = function (cx, cy, width, height) {
        var width_main = this.state.viewWidth;
        var height_main = this.state.viewHeight;
        var newCX = width_main / 2 - cx;
        var newCY = height_main / 2 + cy;
        var newScale = width_main > height_main ? height_main / height : width_main / width;
        this.setState({
            zoom: {
                centerX: newCX,
                centerY: newCY,
                scale: 1,
            },
        });
        this.doZoom(newScale);
    };
    ChartEditorView.prototype.renderBoundsGuides = function () {
        var _this = this;
        // let chartClass = this.props.store.chartManager.getChartClass(this.props.store.chartState);
        // let boundsGuides = chartClass.getSnappingGuides();
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
                        ]), key: "k" + idx, x1: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, x2: guide.value * _this.state.zoom.scale + _this.state.zoom.centerX, y1: 0, y2: _this.state.viewHeight }));
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
                        ]), key: "k" + idx, x1: 0, x2: _this.state.viewWidth, y1: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY, y2: -guide.value * _this.state.zoom.scale + _this.state.zoom.centerY }));
                }
                if (theGuide.type == "point") {
                    var axisGuide = theGuide;
                    return (React.createElement(React.Fragment, { key: "fk" + idx },
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
    ChartEditorView.prototype.getSnappingGuides = function () {
        var _this = this;
        var chartClass = this.props.store.chartManager.getChartClass(this.props.store.chartState);
        var boundsGuides = chartClass.getSnappingGuides();
        var chartGuides = boundsGuides.map(function (bounds) {
            return {
                element: null,
                guide: bounds,
            };
        });
        var elements = this.props.store.chart.elements;
        var elementStates = this.props.store.chartState.elements;
        core_1.zipArray(elements, elementStates).forEach(function (_a) {
            var _b = __read(_a, 2), layout = _b[0], layoutState = _b[1];
            var layoutClass = _this.props.store.chartManager.getChartElementClass(layoutState);
            chartGuides = chartGuides.concat(layoutClass.getSnappingGuides().map(function (bounds) {
                return {
                    element: layout,
                    guide: bounds,
                };
            }));
        });
        return chartGuides;
    };
    ChartEditorView.prototype.renderChartHandles = function () {
        var _this = this;
        var chartClass = this.props.store.chartManager.getChartClass(this.props.store.chartState);
        var handles = chartClass.getHandles();
        return handles.map(function (handle, index) {
            return (React.createElement(handles_1.HandlesView, { key: "m" + index, handles: handles, zoom: _this.state.zoom, active: false, onDragStart: function (bound, ctx) {
                    var session = new move_1.MoveSnappingSession(bound);
                    ctx.onDrag(function (e) {
                        session.handleDrag(e);
                    });
                    ctx.onEnd(function (e) {
                        var updates = session.getUpdates(session.handleEnd(e));
                        if (updates) {
                            for (var name_1 in updates) {
                                if (!Object.prototype.hasOwnProperty.call(updates, name_1)) {
                                    continue;
                                }
                                new actions_1.Actions.SetChartAttribute(name_1, {
                                    type: specification_1.MappingType.value,
                                    value: updates[name_1],
                                }).dispatch(_this.props.store.dispatcher);
                            }
                        }
                    });
                } }));
        });
    };
    ChartEditorView.prototype.renderMarkHandlesInPlotSegment = function (plotSegment, plotSegmentState) {
        var _this = this;
        var bboxViews = [];
        var cs = this.props.store.chartManager
            .getPlotSegmentClass(plotSegmentState)
            .getCoordinateSystem();
        var glyph = core_1.getById(this.props.store.chart.glyphs, plotSegment.glyph);
        plotSegmentState.glyphs.forEach(function (glyphState, glyphIndex) {
            var offsetX = glyphState.attributes.x;
            var offsetY = glyphState.attributes.y;
            glyphState.marks.forEach(function (markState, markIndex) {
                var mark = glyph.marks[markIndex];
                var markClass = _this.props.store.chartManager.getMarkClass(markState);
                if (core_1.Prototypes.isType(mark.classID, guides_1.GuideCoordinatorClass.classID)) {
                    return;
                }
                var bbox = markClass.getBoundingBox();
                var isMarkSelected = false;
                if (_this.props.store.currentSelection instanceof stores_1.MarkSelection) {
                    if (_this.props.store.currentSelection.plotSegment == plotSegment &&
                        _this.props.store.currentSelection.glyph == glyph &&
                        _this.props.store.currentSelection.mark == mark) {
                        if (glyphIndex ==
                            _this.props.store.getSelectedGlyphIndex(plotSegment._id)) {
                            isMarkSelected = true;
                        }
                    }
                }
                if (bbox) {
                    bboxViews.push(React.createElement(bounding_box_1.BoundingBoxView, { key: glyphIndex + "/" + markIndex, boundingBox: bbox, coordinateSystem: cs, offset: { x: offsetX, y: offsetY }, zoom: _this.state.zoom, active: isMarkSelected, onClick: function () {
                            new actions_1.Actions.SelectMark(plotSegment, glyph, mark, glyphIndex).dispatch(_this.props.store.dispatcher);
                        } }));
                }
            });
        });
        return React.createElement("g", null, bboxViews);
    };
    // eslint-disable-next-line
    ChartEditorView.prototype.renderLayoutHandles = function () {
        var _this = this;
        var elements = this.props.store.chart.elements;
        var elementStates = this.props.store.chartState.elements;
        return core_1.stableSortBy(core_1.zipArray(elements, elementStates), function (x) {
            var _a = __read(x, 1), layout = _a[0];
            var shouldRenderHandles = _this.state.currentSelection instanceof stores_1.ChartElementSelection &&
                _this.state.currentSelection.chartElement == layout;
            return shouldRenderHandles ? 1 : 0;
        }).map(
        // eslint-disable-next-line
        function (_a) {
            var _b = __read(_a, 2), layout = _b[0], layoutState = _b[1];
            var layoutClass = _this.props.store.chartManager.getChartElementClass(layoutState);
            // Render handles if the chart element is selected
            var shouldRenderHandles = _this.state.currentSelection instanceof stores_1.ChartElementSelection &&
                _this.state.currentSelection.chartElement == layout;
            var bbox = layoutClass.getBoundingBox();
            if (!shouldRenderHandles) {
                if (bbox) {
                    var bboxView = (React.createElement(bounding_box_1.BoundingBoxView, { key: layout._id, boundingBox: bbox, zoom: _this.state.zoom, onClick: function () {
                            new actions_1.Actions.SelectChartElement(layout, null).dispatch(_this.props.store.dispatcher);
                            _this.props.store.dispatcher.dispatch(new actions_1.Actions.SearchUpdated(""));
                        } }));
                    if (core_1.Prototypes.isType(layout.classID, "plot-segment")) {
                        return (React.createElement("g", { key: layout._id },
                            _this.renderMarkHandlesInPlotSegment(layout, layoutState),
                            bboxView));
                    }
                    else {
                        return bboxView;
                    }
                }
            }
            var handles = layoutClass.getHandles();
            return (React.createElement("g", { key: "m" + layout._id },
                bbox ? (React.createElement(bounding_box_1.BoundingBoxView, { zoom: _this.state.zoom, boundingBox: bbox, active: true })) : null,
                core_1.Prototypes.isType(layout.classID, "plot-segment")
                    ? _this.renderMarkHandlesInPlotSegment(layout, layoutState)
                    : null,
                React.createElement(handles_1.HandlesView, { handles: handles, zoom: _this.state.zoom, active: false, visible: shouldRenderHandles, isAttributeSnapped: function (attribute) {
                        var e_1, _a;
                        if (layout.mappings[attribute] != null) {
                            return true;
                        }
                        try {
                            for (var _b = __values(_this.props.store.chart.constraints), _c = _b.next(); !_c.done; _c = _b.next()) {
                                var constraint = _c.value;
                                if (constraint.type == "snap") {
                                    if (constraint.attributes.element == layout._id &&
                                        constraint.attributes.attribute == attribute) {
                                        return true;
                                    }
                                    if (constraint.attributes.targetElement == layout._id &&
                                        constraint.attributes.targetAttribute == attribute) {
                                        return true;
                                    }
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
                    }, onDragStart: function (handle, ctx) {
                        var guides = _this.getSnappingGuides();
                        var session = new chart_1.ChartSnappingSession(guides, layout, handle, 10 / _this.state.zoom.scale, handle.options && handle.options.snapToClosestPoint);
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
                                action.forEach(function (a) {
                                    return a.dispatch(_this.props.store.dispatcher);
                                });
                            }
                        });
                    } })));
        });
    };
    ChartEditorView.prototype.renderHandles = function () {
        return (React.createElement("g", null,
            this.renderChartHandles(),
            this.renderLayoutHandles()));
    };
    ChartEditorView.prototype.renderControls = function () {
        var _this = this;
        var elements = this.props.store.chart.elements;
        var elementStates = this.props.store.chartState.elements;
        return (React.createElement("div", { className: "canvas-popups" }, core_1.zipArray(elements, elementStates)
            .filter(function (_a) {
            var _b = __read(_a, 1), element = _b[0];
            return core_1.Prototypes.isType(element.classID, "plot-segment");
        })
            .map(function (_a, index) {
            var _b = __read(_a, 2), layout = _b[0], layoutState = _b[1];
            if (_this.state.currentSelection instanceof stores_1.ChartElementSelection &&
                _this.state.currentSelection.chartElement == layout) {
                var layoutClass = _this.props.store.chartManager.getPlotSegmentClass(layoutState);
                var manager = new fluentui_manager_1.FluentUIWidgetManager(_this.props.store, layoutClass);
                var controls = layoutClass.getPopupEditor(manager);
                if (!controls) {
                    return null;
                }
                var pt = core_1.Geometry.applyZoom(_this.state.zoom, {
                    x: controls.anchor.x,
                    y: -controls.anchor.y,
                });
                if (pt.x < 0 || pt.y < 0 || !_this.state.canvasToolbar) {
                    return null;
                }
                return (React.createElement(React.Fragment, { key: "canvas" },
                    React.createElement("div", { className: "charticulator__canvas-popup", key: "m" + index, id: "anchor" + index, style: {
                            left: pt.x.toFixed(0) + "px",
                            bottom: (_this.state.viewHeight - pt.y + 5).toFixed(0) + "px",
                        } }),
                    React.createElement(react_1.Callout, { target: "#anchor" + index, directionalHint: react_1.DirectionalHint.topLeftEdge, styles: {
                            root: {
                                padding: 10,
                            },
                            calloutMain: {
                                overflow: "hidden",
                            },
                        }, onDismiss: function () {
                            return _this.setState({
                                canvasToolbar: false,
                            });
                        } }, manager.horizontal.apply(manager, __spread([controls.widgets.map(function () { return 0; })], controls.widgets)))));
            }
        })));
    };
    // eslint-disable-next-line
    ChartEditorView.prototype.renderSnappingGuides = function () {
        var _this = this;
        var guides = this.state.snappingCandidates;
        if (!guides || guides.length == 0) {
            return null;
        }
        // eslint-disable-next-line
        return guides.map(function (guide, idx) {
            var key = "m" + idx;
            switch (guide.guide.type) {
                case "x": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", x1: axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerX, x2: axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerX, y1: 0, y2: _this.state.viewHeight }));
                }
                case "y": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", y1: -axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerY, y2: -axisGuide.value * _this.state.zoom.scale +
                            _this.state.zoom.centerY, x1: 0, x2: _this.state.viewWidth }));
                }
                case "point": {
                    var axisGuide = guide.guide;
                    return (React.createElement(React.Fragment, { key: "snapping-guid-" + idx },
                        axisGuide.visibleRadius ? (React.createElement("circle", { className: "snapping-guide", key: "ck" + idx + "display", cx: axisGuide.cx * _this.state.zoom.scale +
                                _this.state.zoom.centerX, cy: -axisGuide.cy * _this.state.zoom.scale +
                                _this.state.zoom.centerY, r: Math.abs(axisGuide.visibleRadius * _this.state.zoom.scale) })) : (React.createElement(React.Fragment, { key: "snapping-link-" + idx },
                            React.createElement("line", { key: "lk" + idx + "display1", className: "snapping-guide", x1: axisGuide.cx * _this.state.zoom.scale +
                                    _this.state.zoom.centerX, y1: -(axisGuide.cy - 10) * _this.state.zoom.scale +
                                    _this.state.zoom.centerY, x2: axisGuide.cx * _this.state.zoom.scale +
                                    _this.state.zoom.centerX, y2: -(axisGuide.cy + 10) * _this.state.zoom.scale +
                                    _this.state.zoom.centerY }),
                            React.createElement("line", { key: "lk" + idx + "display1", className: "snapping-guide", x1: (axisGuide.cx - 10) * _this.state.zoom.scale +
                                    _this.state.zoom.centerX, y1: -axisGuide.cy * _this.state.zoom.scale +
                                    _this.state.zoom.centerY, x2: (axisGuide.cx + 10) * _this.state.zoom.scale +
                                    _this.state.zoom.centerX, y2: -axisGuide.cy * _this.state.zoom.scale +
                                    _this.state.zoom.centerY }))),
                        React.createElement("line", { key: "lk" + idx + "display", className: "snapping-guide", x1: axisGuide.cx * _this.state.zoom.scale + _this.state.zoom.centerX, y1: -axisGuide.cy * _this.state.zoom.scale +
                                _this.state.zoom.centerY, x2: axisGuide.angle * _this.state.zoom.scale +
                                _this.state.zoom.centerX, y2: -axisGuide.radius * _this.state.zoom.scale +
                                _this.state.zoom.centerY })));
                }
            }
        });
    };
    ChartEditorView.prototype.renderChartCanvas = function () {
        var _this = this;
        var chartState = this.props.store.chartState;
        var p1 = {
            x: -chartState.attributes.width / 2,
            y: -chartState.attributes.height / 2,
        };
        var p2 = {
            x: +chartState.attributes.width / 2,
            y: +chartState.attributes.height / 2,
        };
        var p1t = core_1.Geometry.applyZoom(this.state.zoom, p1);
        var p2t = core_1.Geometry.applyZoom(this.state.zoom, p2);
        var cornerInnerRadius = 8;
        var cornerOuterRadius = cornerInnerRadius + 1;
        var shadowSize = cornerOuterRadius - cornerInnerRadius;
        var getRoundedRectPath = function (x1, y1, x2, y2, radius) {
            return "m" + (Math.min(x1, x2) + cornerInnerRadius) + "," + Math.min(y1, y2) + " \n      h" + (Math.abs(x2 - x1) - radius * 2) + " \n      a" + radius + "," + radius + " 0 0 1 " + radius + "," + radius + " \n      v" + (Math.abs(y2 - y1) - radius * 2) + " \n      a" + radius + "," + radius + " 0 0 1 -" + radius + "," + radius + " \n      h-" + (Math.abs(x2 - x1) - radius * 2) + " \n      a" + radius + "," + radius + " 0 0 1 -" + radius + ",-" + radius + " \n      v-" + (Math.abs(y2 - y1) - radius * 2) + " \n      a" + radius + "," + radius + " 0 0 1 " + radius + ",-" + radius + " \n      z";
        };
        return (React.createElement("g", null,
            React.createElement("path", { className: "canvas-region-outer", d: getRoundedRectPath(p1t.x - shadowSize, p1t.y - shadowSize, p2t.x + shadowSize, p2t.y + shadowSize, cornerInnerRadius) }),
            React.createElement("path", { className: "canvas-region", d: getRoundedRectPath(p1t.x, p1t.y, p2t.x, p2t.y, cornerInnerRadius) }),
            React.createElement(resize_1.ResizeHandleView, { zoom: this.state.zoom, cx: (p1.x + p2.x) / 2, cy: (p1.y + p2.y) / 2, width: Math.abs(p2.x - p1.x), height: Math.abs(p2.y - p1.y), onResize: function (newWidth, newHeight) {
                    new actions_1.Actions.SetChartSize(newWidth, newHeight).dispatch(_this.props.store.dispatcher);
                } })));
    };
    ChartEditorView.prototype.renderDropZoneForMarkLayout = function (layout, state) {
        var _this = this;
        var cls = this.props.store.chartManager.getPlotSegmentClass(state);
        return cls
            .getDropZones()
            .filter(function (zone) {
            // We don't allow scale data mapping right now
            if (zone.dropAction.scaleInference) {
                return false;
            }
            if (_this.state.dropZoneData) {
                // Process dropzone filter
                if (zone.accept) {
                    if (zone.accept.table != null) {
                        if (_this.state.dropZoneData.data instanceof actions_1.DragData.DataExpression) {
                            var data = _this.state.dropZoneData
                                .data;
                            if (data.table.name != zone.accept.table) {
                                return false;
                            }
                        }
                        else {
                            return false;
                        }
                    }
                    if (zone.accept.scaffolds) {
                        if (_this.state.dropZoneData.layout) {
                            return (zone.accept.scaffolds.indexOf(_this.state.dropZoneData.layout.type) >= 0);
                        }
                        else {
                            return false;
                        }
                    }
                    return true;
                }
                else {
                    return (_this.state.dropZoneData.data instanceof actions_1.DragData.DataExpression);
                }
            }
            else {
                return false;
            }
        })
            .map(function (zone, idx) { return (React.createElement(dropzone_1.DropZoneView, { key: "m" + idx, onDragEnter: function (data) {
                var dropAction = zone.dropAction;
                if (dropAction.axisInference) {
                    return function () {
                        new actions_1.Actions.BindDataToAxis(layout, dropAction.axisInference.property, dropAction.axisInference.appendToProperty, data, true).dispatch(_this.props.store.dispatcher);
                        return true;
                    };
                }
                if (dropAction.extendPlotSegment) {
                    return function () {
                        new actions_1.Actions.ExtendPlotSegment(layout, data.type).dispatch(_this.props.store.dispatcher);
                        return true;
                    };
                }
            }, zone: zone, zoom: _this.state.zoom })); });
    };
    ChartEditorView.prototype.renderDropZones = function () {
        var _this = this;
        var _a = this.props.store, chart = _a.chart, chartState = _a.chartState;
        if (!this.state.dropZoneData) {
            return null;
        }
        return (React.createElement("g", null, core_1.zipArray(chart.elements, chartState.elements)
            .filter(function (_a) {
            var _b = __read(_a, 1), e = _b[0];
            return core_1.Prototypes.isType(e.classID, "plot-segment");
        })
            .map(function (_a) {
            var _b = __read(_a, 2), layout = _b[0], layoutState = _b[1];
            return (React.createElement("g", { key: "m" + layout._id }, _this.renderDropZoneForMarkLayout(layout, layoutState)));
        })));
    };
    ChartEditorView.prototype.doZoom = function (factor) {
        var _a = this.state.zoom, scale = _a.scale, centerX = _a.centerX, centerY = _a.centerY;
        var fixPoint = core_1.Geometry.unapplyZoom(this.state.zoom, {
            x: this.state.viewWidth / 2,
            y: this.state.viewHeight / 2,
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
    // eslint-disable-next-line
    ChartEditorView.prototype.render = function () {
        var _this = this;
        var width = this.state.viewWidth;
        var height = this.state.viewHeight;
        var transform = "translate(" + this.state.zoom.centerX + "," + this.state.zoom.centerY + ") scale(" + this.state.zoom.scale + ")";
        return (React.createElement("div", { className: "chart-editor-view" },
            React.createElement("div", { className: "chart-editor-canvas-view", ref: "canvasContainer" },
                React.createElement("svg", { className: "canvas-view", ref: "canvas", x: 0, y: 0, width: width, height: height },
                    React.createElement("defs", null, renderer_1.renderSVGDefs(this.state.graphics)),
                    React.createElement("rect", { className: "interaction-handler", ref: "canvasInteraction", x: 0, y: 0, width: width, height: height }),
                    this.renderChartCanvas(),
                    this.renderBoundsGuides(),
                    React.createElement("g", { className: "graphics", transform: transform }, this.renderGraphics()),
                    this.renderSnappingGuides(),
                    this.renderHandles(),
                    this.renderDropZones(),
                    this.renderEditingLink(),
                    this.renderCreatingComponent()),
                this.renderControls()),
            React.createElement("div", { className: "canvas-controls" },
                React.createElement("div", { className: "canvas-controls-left" }),
                React.createElement("div", { className: "canvas-controls-right" },
                    React.createElement(controls_1.Button, { icon: "ZoomIn", onClick: function () {
                            _this.doZoom(1.1);
                        } }),
                    React.createElement(controls_1.Button, { icon: "ZoomOut", onClick: function () {
                            _this.doZoom(1 / 1.1);
                        } }),
                    React.createElement(controls_1.Button, { icon: "ZoomToFit", onClick: function () {
                            var newZoom = _this.getFitViewZoom(_this.state.viewWidth, _this.state.viewHeight);
                            if (!newZoom) {
                                return;
                            }
                            _this.setState({
                                zoom: newZoom,
                            });
                        } }),
                    React.createElement(controls_1.Button, { icon: "rect-zoom", title: "Rectangle zoom", onClick: function () {
                            new actions_1.Actions.SetCurrentTool("rectangle-zoom").dispatch(_this.props.store.dispatcher);
                        } }))),
            this.state.isSolving ? (React.createElement("div", { className: "solving-hint" },
                React.createElement("div", { className: "el-box" },
                    React.createElement("img", { src: R.getSVGIcon("loading") }),
                    strings_1.strings.app.working))) : null));
    };
    return ChartEditorView;
}(React.Component));
exports.ChartEditorView = ChartEditorView;
//# sourceMappingURL=chart_editor.js.map