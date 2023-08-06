"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !exports.hasOwnProperty(p)) __createBinding(exports, m, p);
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
exports.ChartRenderer = exports.facetRows = void 0;
var common_1 = require("../../common");
var Prototypes = require("../../prototypes");
var coordinate_system_1 = require("../coordinate_system");
var elements_1 = require("../elements");
function facetRows(rows, indices, columns) {
    var e_1, _a;
    if (columns == null) {
        return [indices];
    }
    else {
        var facets = new common_1.MultistringHashMap();
        var _loop_1 = function (index) {
            var row = rows[index];
            var facetValues = columns.map(function (c) { return row[c]; });
            if (facets.has(facetValues)) {
                facets.get(facetValues).push(index);
            }
            else {
                facets.set(facetValues, [index]);
            }
        };
        try {
            for (var indices_1 = __values(indices), indices_1_1 = indices_1.next(); !indices_1_1.done; indices_1_1 = indices_1.next()) {
                var index = indices_1_1.value;
                _loop_1(index);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (indices_1_1 && !indices_1_1.done && (_a = indices_1.return)) _a.call(indices_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return Array.from(facets.values());
    }
}
exports.facetRows = facetRows;
/**
 * The class is responsible for rendering the visual part of the chart (coordinates, elements such as glyph marks e.t.c).
 * The module calls methods {@link MarkClass.getGraphics} implemented in each marks (rect, image, text, symbol e.t.c)
 *
 */
var ChartRenderer = /** @class */ (function () {
    function ChartRenderer(manager, renderEvents) {
        this.manager = manager;
        this.renderEvents = renderEvents;
        this.manager = manager;
    }
    /**
     * Render marks in a glyph
     * @returns an array of groups with the same size as glyph.marks
     */
    ChartRenderer.prototype.renderGlyphMarks = function (plotSegment, plotSegmentState, coordinateSystem, offset, glyph, state, index) {
        var _this = this;
        return common_1.zipArray(glyph.marks, state.marks).map(function (_a) {
            var _b = __read(_a, 2), mark = _b[0], markState = _b[1];
            if (!mark.properties.visible) {
                return null;
            }
            var cls = _this.manager.getMarkClass(markState);
            var g = cls.getGraphics(coordinateSystem, offset, index, _this.manager, state.emphasized);
            if (g != null) {
                g.selectable = {
                    plotSegment: plotSegment,
                    glyphIndex: index,
                    rowIndices: plotSegmentState.dataRowIndices[index],
                    enableTooltips: cls.object.properties.enableTooltips,
                    enableContextMenu: cls.object.properties.enableContextMenu,
                    enableSelection: cls.object.properties.enableSelection,
                };
                return elements_1.makeGroup([g]);
            }
            else {
                return null;
            }
        });
    };
    /**
     * Method calls getGraphics method of {@link Mark} objects to get graphical representation of element
     * @param dataset Dataset of charticulator
     * @param chart Chart object
     * @param chartState State of chart and chart elements
     */
    // eslint-disable-next-line
    ChartRenderer.prototype.renderChart = function (dataset, chart, chartState) {
        var e_2, _a, e_3, _b;
        var graphics = [];
        // Chart background
        var bg = this.manager.getChartClass(chartState).getBackgroundGraphics();
        if (bg) {
            graphics.push(bg);
        }
        var linkGroup = elements_1.makeGroup([]);
        graphics.push(linkGroup);
        var elementsAndStates = common_1.zipArray(chart.elements, chartState.elements);
        try {
            // Render layout graphics
            for (var elementsAndStates_1 = __values(elementsAndStates), elementsAndStates_1_1 = elementsAndStates_1.next(); !elementsAndStates_1_1.done; elementsAndStates_1_1 = elementsAndStates_1.next()) {
                var _c = __read(elementsAndStates_1_1.value, 2), element = _c[0], elementState = _c[1];
                if (!element.properties.visible) {
                    continue;
                }
                // Render marks if this is a plot segment
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    var plotSegmentState = elementState;
                    var mark = common_1.getById(chart.glyphs, plotSegment.glyph);
                    var plotSegmentClass = this.manager.getPlotSegmentClass(plotSegmentState);
                    var coordinateSystem = plotSegmentClass.getCoordinateSystem();
                    // Render glyphs
                    var glyphArrays = [];
                    try {
                        for (var _d = (e_3 = void 0, __values(plotSegmentState.glyphs.entries())), _e = _d.next(); !_e.done; _e = _d.next()) {
                            var _f = __read(_e.value, 2), glyphIndex = _f[0], glyphState = _f[1];
                            var anchorX = glyphState.marks[0].attributes.x;
                            var anchorY = glyphState.marks[0].attributes.y;
                            var offsetX = glyphState.attributes.x - anchorX;
                            var offsetY = glyphState.attributes.y - anchorY;
                            var g_1 = this.renderGlyphMarks(plotSegment, plotSegmentState, coordinateSystem, { x: offsetX, y: offsetY }, mark, glyphState, glyphIndex);
                            glyphArrays.push(g_1);
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (_e && !_e.done && (_b = _d.return)) _b.call(_d);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                    // Transpose glyphArrays so each mark is in a layer
                    var glyphElements = common_1.transpose(glyphArrays).map(function (x) { return elements_1.makeGroup(x); });
                    var gGlyphs = elements_1.makeGroup(glyphElements);
                    gGlyphs.transform = coordinateSystem.getBaseTransform();
                    var g = plotSegmentClass.getPlotSegmentGraphics(gGlyphs, this.manager);
                    // render plotsegment background elements
                    var gBackgroundElements = elements_1.makeGroup([]);
                    var plotSegmentBackgroundElements = plotSegmentClass.getPlotSegmentBackgroundGraphics(this.manager);
                    gBackgroundElements.elements.push(plotSegmentBackgroundElements);
                    var gElement = elements_1.makeGroup([]);
                    gElement.elements.push(gBackgroundElements);
                    gElement.elements.push(g);
                    gElement.key = element._id;
                    graphics.push(gElement);
                }
                else if (Prototypes.isType(element.classID, "mark")) {
                    var cs = new coordinate_system_1.CartesianCoordinates({ x: 0, y: 0 });
                    var gElement = elements_1.makeGroup([]);
                    var elementClass = this.manager.getMarkClass(elementState);
                    var g = elementClass.getGraphics(cs, { x: 0, y: 0 }, null, this.manager);
                    gElement.elements.push(g);
                    gElement.key = element._id;
                    graphics.push(gElement);
                }
                else {
                    var gElement = elements_1.makeGroup([]);
                    var elementClass = this.manager.getChartElementClass(elementState);
                    var g = elementClass.getGraphics(this.manager);
                    gElement.elements.push(g);
                    gElement.key = element._id;
                    graphics.push(gElement);
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (elementsAndStates_1_1 && !elementsAndStates_1_1.done && (_a = elementsAndStates_1.return)) _a.call(elementsAndStates_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        var chartEventHandlerRect = elements_1.makeRect(chartState.attributes.x1, chartState.attributes.y1, chartState.attributes.x2, chartState.attributes.y2, {
            fillColor: null,
            opacity: 1,
        });
        // don't need to handle other events by chart.
        if (chart.properties.enableContextMenu) {
            chartEventHandlerRect.selectable = {
                plotSegment: null,
                glyphIndex: null,
                rowIndices: null,
                enableTooltips: false,
                enableContextMenu: chart.properties.enableContextMenu !== undefined
                    ? chart.properties.enableContextMenu
                    : true,
                enableSelection: false,
            };
        }
        return elements_1.makeGroup(__spread([chartEventHandlerRect], graphics));
    };
    ChartRenderer.prototype.renderControls = function (chart, chartState, zoom) {
        var e_4, _a;
        var elementsAndStates = common_1.zipArray(chart.elements, chartState.elements);
        var controls = [];
        try {
            // Render control graphics
            for (var elementsAndStates_2 = __values(elementsAndStates), elementsAndStates_2_1 = elementsAndStates_2.next(); !elementsAndStates_2_1.done; elementsAndStates_2_1 = elementsAndStates_2.next()) {
                var _b = __read(elementsAndStates_2_1.value, 2), element = _b[0], elementState = _b[1];
                if (!element.properties.visible) {
                    continue;
                }
                // Render plotsegment controls
                if (Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegmentState = elementState;
                    var plotSegmentClass = this.manager.getPlotSegmentClass(plotSegmentState);
                    var plotSegmentBackgroundControlElements = plotSegmentClass.renderControls(this.manager, zoom);
                    controls = controls.concat(plotSegmentBackgroundControlElements);
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (elementsAndStates_2_1 && !elementsAndStates_2_1.done && (_a = elementsAndStates_2.return)) _a.call(elementsAndStates_2);
            }
            finally { if (e_4) throw e_4.error; }
        }
        return controls;
    };
    ChartRenderer.prototype.render = function () {
        var _a;
        var group = this.renderChart(this.manager.dataset, this.manager.chart, this.manager.chartState);
        if ((_a = this.renderEvents) === null || _a === void 0 ? void 0 : _a.afterRendered) {
            this.renderEvents.afterRendered();
        }
        return group;
    };
    return ChartRenderer;
}());
exports.ChartRenderer = ChartRenderer;
__exportStar(require("./text_measurer"), exports);
//# sourceMappingURL=index.js.map