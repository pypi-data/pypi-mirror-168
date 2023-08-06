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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
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
exports.AppStore = exports.EditorType = void 0;
var core_1 = require("../../core");
var base_1 = require("../../core/store/base");
var actions_1 = require("../actions");
var indexed_db_1 = require("../backend/indexed_db");
var template_1 = require("../template");
var utils_1 = require("../utils");
var chart_display_1 = require("../views/canvas/chart_display");
var action_handlers_1 = require("./action_handlers");
var defaults_1 = require("./defaults");
var history_manager_1 = require("./history_manager");
var migrator_1 = require("./migrator");
var selection_1 = require("./selection");
var dataset_1 = require("../../core/dataset");
var specification_1 = require("../../core/specification");
var types_1 = require("../../core/specification/types");
var numerical_legend_1 = require("../../core/prototypes/legends/numerical_legend");
var plot_segments_1 = require("../../core/prototypes/plot_segments");
var prototypes_1 = require("../../core/prototypes");
var base_2 = require("../../core/prototypes/plot_segments/region_2d/base");
var data_types_1 = require("../../core/dataset/data_types");
var utils_2 = require("../../core/prototypes/plot_segments/utils");
var axis_1 = require("../../core/prototypes/plot_segments/axis");
var group_by_1 = require("../../core/prototypes/group_by");
var EditorType;
(function (EditorType) {
    EditorType["Nested"] = "nested";
    EditorType["Embedded"] = "embedded";
    EditorType["NestedEmbedded"] = "nestedembedded";
    EditorType["Chart"] = "chart";
})(EditorType = exports.EditorType || (exports.EditorType = {}));
var AppStore = /** @class */ (function (_super) {
    __extends(AppStore, _super);
    function AppStore(worker, dataset) {
        var _this = _super.call(this, null) || this;
        /** Is this app a nested chart editor? */
        _this.editorType = EditorType.Chart;
        /** Should we disable the FileView */
        _this.disableFileView = false;
        _this.selectedGlyphIndex = {};
        _this.localeFileFormat = {
            delimiter: ",",
            numberFormat: {
                remove: ",",
                decimal: ".",
            },
            currency: '["$", ""]',
            group: "[3]",
            utcTimeZone: true,
        };
        _this.searchString = "";
        _this.collapseOrExpandPanelsType = types_1.CollapseOrExpandPanels.Expand;
        _this.actionHandlers = new action_handlers_1.ActionHandlerRegistry();
        _this.propertyExportName = new Map();
        _this.registeredExportTemplateTargets = new Map();
        _this.preSolveValues = [];
        _this.getDataKindByType = function (type) {
            switch (type) {
                case types_1.AxisDataBindingType.Categorical:
                    return specification_1.DataKind.Categorical;
                case types_1.AxisDataBindingType.Numerical:
                    return specification_1.DataKind.Numerical;
                case types_1.AxisDataBindingType.Default:
                    return specification_1.DataKind.Categorical;
                default:
                    return specification_1.DataKind.Categorical;
            }
        };
        /** Register action handlers */
        action_handlers_1.registerActionHandlers(_this.actionHandlers);
        _this.worker = worker;
        _this.backend = new indexed_db_1.IndexedDBBackend();
        _this.historyManager = new history_manager_1.HistoryManager();
        _this.dataset = dataset;
        _this.newChartEmpty();
        _this.solveConstraintsAndUpdateGraphics();
        _this.messageState = new Map();
        _this.registerExportTemplateTarget("Charticulator Template", function (template) {
            return {
                getProperties: function () {
                    var _a;
                    return [
                        {
                            displayName: "Name",
                            name: "name",
                            type: "string",
                            default: ((_a = template.specification.properties) === null || _a === void 0 ? void 0 : _a.name) || "template",
                        },
                    ];
                },
                getFileName: function (props) { return props.name + ".tmplt"; },
                generate: function () {
                    return new Promise(function (resolve) {
                        var r = utils_1.b64EncodeUnicode(JSON.stringify(template, null, 2));
                        resolve(r);
                    });
                },
            };
        });
        return _this;
    }
    AppStore.prototype.setPropertyExportName = function (propertyName, value) {
        this.propertyExportName.set("" + propertyName, value);
    };
    AppStore.prototype.getPropertyExportName = function (propertyName) {
        return this.propertyExportName.get("" + propertyName);
    };
    AppStore.prototype.saveState = function () {
        return {
            version: CHARTICULATOR_PACKAGE.version,
            dataset: this.dataset,
            chart: this.chart,
            chartState: this.chartState,
        };
    };
    AppStore.prototype.saveDecoupledState = function () {
        var state = this.saveState();
        return core_1.deepClone(state);
    };
    AppStore.prototype.loadState = function (state) {
        var _this = this;
        this.currentSelection = null;
        this.selectedGlyphIndex = {};
        this.dataset = state.dataset;
        this.originDataset = state.dataset;
        this.chart = state.chart;
        this.chartState = state.chartState;
        this.version = state.version;
        this.chartManager = new core_1.Prototypes.ChartStateManager(this.chart, this.dataset, this.chartState, {}, {}, this.chartManager.getOriginChart());
        this.chartManager.onUpdate(function () {
            _this.solveConstraintsAndUpdateGraphics();
        });
        this.emit(AppStore.EVENT_DATASET);
        this.emit(AppStore.EVENT_GRAPHICS);
        this.emit(AppStore.EVENT_SELECTION);
    };
    AppStore.prototype.saveHistory = function () {
        this.historyManager.addState(this.saveDecoupledState());
        try {
            this.emit(AppStore.EVENT_GRAPHICS);
        }
        catch (ex) {
            console.error(ex);
        }
    };
    AppStore.prototype.renderSVG = function () {
        var svg = '<?xml version="1.0" standalone="no"?>' +
            chart_display_1.renderChartToString(this.dataset, this.chart, this.chartState);
        return svg;
    };
    AppStore.prototype.renderLocalSVG = function () {
        return __awaiter(this, void 0, void 0, function () {
            var svg;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, chart_display_1.renderChartToLocalString(this.dataset, this.chart, this.chartState)];
                    case 1:
                        svg = _a.sent();
                        return [2 /*return*/, '<?xml version="1.0" standalone="no"?>' + svg];
                }
            });
        });
    };
    AppStore.prototype.handleAction = function (action) {
        this.actionHandlers.handleAction(this, action);
    };
    AppStore.prototype.backendOpenChart = function (id) {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var chart, state;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, this.backend.get(id)];
                    case 1:
                        chart = _b.sent();
                        this.currentChartID = id;
                        this.historyManager.clear();
                        state = new migrator_1.Migrator().migrate(chart.data.state, CHARTICULATOR_PACKAGE.version);
                        this.loadState(state);
                        (_a = this.chartManager) === null || _a === void 0 ? void 0 : _a.resetDifference();
                        return [2 /*return*/];
                }
            });
        });
    };
    // removes unused scale objecs
    AppStore.prototype.updateChartState = function () {
        var _this = this;
        function hasMappedProperty(mappings, scaleId) {
            for (var map in mappings) {
                if (mappings[map].type === specification_1.MappingType.scale ||
                    mappings[map].type === specification_1.MappingType.expressionScale) {
                    if (mappings[map].scale === scaleId) {
                        return true;
                    }
                }
            }
            return false;
        }
        var chart = this.chart;
        function scaleFilter(scale) {
            return !(chart.elements.find(function (element) {
                var mappings = element.mappings;
                if (mappings) {
                    return hasMappedProperty(mappings, scale._id);
                }
                return false;
            }) != null ||
                chart.glyphs.find(function (glyph) {
                    return (glyph.marks.find(function (mark) {
                        var mappings = mark.mappings;
                        if (mappings) {
                            return hasMappedProperty(mappings, scale._id);
                        }
                        return false;
                    }) != null);
                }));
        }
        chart.scales
            .filter(scaleFilter)
            .forEach(function (scale) { return _this.chartManager.removeScale(scale); });
        chart.scaleMappings = chart.scaleMappings.filter(function (scaleMapping) {
            return chart.scales.find(function (scale) { return scale._id === scaleMapping.scale; });
        });
    };
    AppStore.prototype.backendSaveChart = function () {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var chart, svg, _b, _c, png;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        if (!(this.currentChartID != null)) return [3 /*break*/, 5];
                        return [4 /*yield*/, this.backend.get(this.currentChartID)];
                    case 1:
                        chart = _d.sent();
                        this.updateChartState();
                        chart.data.state = this.saveState();
                        _b = utils_1.stringToDataURL;
                        _c = ["image/svg+xml"];
                        return [4 /*yield*/, this.renderLocalSVG()];
                    case 2:
                        svg = _b.apply(void 0, _c.concat([_d.sent()]));
                        return [4 /*yield*/, utils_1.renderDataURLToPNG(svg, {
                                mode: "thumbnail",
                                thumbnail: [200, 150],
                            })];
                    case 3:
                        png = _d.sent();
                        chart.metadata.thumbnail = png.toDataURL();
                        return [4 /*yield*/, this.backend.put(chart.id, chart.data, chart.metadata)];
                    case 4:
                        _d.sent();
                        (_a = this.chartManager) === null || _a === void 0 ? void 0 : _a.resetDifference();
                        this.emit(AppStore.EVENT_GRAPHICS);
                        this.emit(AppStore.EVENT_SAVECHART);
                        _d.label = 5;
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    AppStore.prototype.backendSaveChartAs = function (name) {
        return __awaiter(this, void 0, void 0, function () {
            var state, svg, _a, _b, png, id;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        this.updateChartState();
                        state = this.saveState();
                        _a = utils_1.stringToDataURL;
                        _b = ["image/svg+xml"];
                        return [4 /*yield*/, this.renderLocalSVG()];
                    case 1:
                        svg = _a.apply(void 0, _b.concat([_c.sent()]));
                        return [4 /*yield*/, utils_1.renderDataURLToPNG(svg, {
                                mode: "thumbnail",
                                thumbnail: [200, 150],
                            })];
                    case 2:
                        png = _c.sent();
                        return [4 /*yield*/, this.backend.create("chart", {
                                state: state,
                                name: name,
                            }, {
                                name: name,
                                dataset: this.dataset.name,
                                thumbnail: png.toDataURL(),
                            })];
                    case 3:
                        id = _c.sent();
                        this.currentChartID = id;
                        this.emit(AppStore.EVENT_GRAPHICS);
                        this.emit(AppStore.EVENT_SAVECHART);
                        return [2 /*return*/, id];
                }
            });
        });
    };
    AppStore.prototype.setupNestedEditor = function (callback, type) {
        var _this = this;
        this.editorType = type;
        this.disableFileView = true;
        this.emit(AppStore.EVENT_IS_NESTED_EDITOR);
        this.addListener(AppStore.EVENT_NESTED_EDITOR_EDIT, function () {
            _this.updateChartState();
            callback(_this.chart);
        });
    };
    AppStore.prototype.registerExportTemplateTarget = function (name, ctor) {
        this.registeredExportTemplateTargets.set(name, ctor);
    };
    AppStore.prototype.unregisterExportTemplateTarget = function (name) {
        this.registeredExportTemplateTargets.delete(name);
    };
    AppStore.prototype.listExportTemplateTargets = function () {
        var r = [];
        this.registeredExportTemplateTargets.forEach(function (x, i) {
            r.push(i);
        });
        return r;
    };
    AppStore.prototype.createExportTemplateTarget = function (name, template) {
        return this.registeredExportTemplateTargets.get(name)(template);
    };
    AppStore.prototype.getTable = function (name) {
        if (this.dataset != null) {
            return this.dataset.tables.filter(function (d) { return d.name == name; })[0];
        }
        else {
            return null;
        }
    };
    AppStore.prototype.getTables = function () {
        return this.dataset.tables;
    };
    AppStore.prototype.getColumnVector = function (table, columnName) {
        return table.rows.map(function (d) { return d[columnName]; });
    };
    AppStore.prototype.saveSelectionState = function () {
        var selection = {};
        if (this.currentSelection instanceof selection_1.ChartElementSelection) {
            selection.selection = {
                type: "chart-element",
                chartElementID: this.currentSelection.chartElement._id,
            };
        }
        if (this.currentSelection instanceof selection_1.GlyphSelection) {
            selection.selection = {
                type: "glyph",
                glyphID: this.currentSelection.glyph._id,
            };
        }
        if (this.currentSelection instanceof selection_1.MarkSelection) {
            selection.selection = {
                type: "mark",
                glyphID: this.currentSelection.glyph._id,
                markID: this.currentSelection.mark._id,
            };
        }
        if (this.currentGlyph) {
            selection.currentGlyphID = this.currentGlyph._id;
        }
        return selection;
    };
    AppStore.prototype.loadSelectionState = function (selectionState) {
        if (selectionState == null) {
            return;
        }
        var selection = selectionState.selection;
        if (selection != null) {
            if (selection.type == "chart-element") {
                var chartElement = core_1.getById(this.chart.elements, selection.chartElementID);
                if (chartElement) {
                    this.currentSelection = new selection_1.ChartElementSelection(chartElement);
                }
            }
            if (selection.type == "glyph") {
                var glyphID = selection.glyphID;
                var glyph = core_1.getById(this.chart.glyphs, glyphID);
                var plotSegment = core_1.getById(this.chart.elements, selection.chartElementID);
                if (plotSegment && glyph) {
                    this.currentSelection = new selection_1.GlyphSelection(plotSegment, glyph);
                    this.currentGlyph = glyph;
                }
            }
            if (selection.type == "mark") {
                var glyphID = selection.glyphID;
                var markID = selection.markID;
                var glyph = core_1.getById(this.chart.glyphs, glyphID);
                var plotSegment = core_1.getById(this.chart.elements, selection.chartElementID);
                if (plotSegment && glyph) {
                    var mark = core_1.getById(glyph.marks, markID);
                    if (mark) {
                        this.currentSelection = new selection_1.MarkSelection(plotSegment, glyph, mark);
                        this.currentGlyph = glyph;
                    }
                }
            }
        }
        if (selectionState.currentGlyphID) {
            var glyph = core_1.getById(this.chart.glyphs, selectionState.currentGlyphID);
            if (glyph) {
                this.currentGlyph = glyph;
            }
        }
        this.emit(AppStore.EVENT_SELECTION);
    };
    AppStore.prototype.setSelectedGlyphIndex = function (plotSegmentID, glyphIndex) {
        this.selectedGlyphIndex[plotSegmentID] = glyphIndex;
    };
    AppStore.prototype.getSelectedGlyphIndex = function (plotSegmentID) {
        var plotSegment = this.chartManager.getClassById(plotSegmentID);
        if (!plotSegment) {
            return 0;
        }
        if (Object.prototype.hasOwnProperty.call(this.selectedGlyphIndex, plotSegmentID)) {
            var idx = this.selectedGlyphIndex[plotSegmentID];
            if (idx >= plotSegment.state.dataRowIndices.length) {
                this.selectedGlyphIndex[plotSegmentID] = 0;
                return 0;
            }
            else {
                return idx;
            }
        }
        else {
            this.selectedGlyphIndex[plotSegmentID] = 0;
            return 0;
        }
    };
    AppStore.prototype.getMarkIndex = function (mark) {
        return this.chart.glyphs.indexOf(mark);
    };
    AppStore.prototype.forAllGlyph = function (glyph, callback) {
        var e_1, _a, e_2, _b;
        try {
            for (var _c = __values(core_1.zipArray(this.chart.elements, this.chartState.elements)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), element = _e[0], elementState = _e[1];
                if (core_1.Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    var plotSegmentState = elementState;
                    if (plotSegment.glyph == glyph._id) {
                        try {
                            for (var _f = (e_2 = void 0, __values(plotSegmentState.glyphs)), _g = _f.next(); !_g.done; _g = _f.next()) {
                                var glyphState = _g.value;
                                callback(glyphState, plotSegment, plotSegmentState);
                            }
                        }
                        catch (e_2_1) { e_2 = { error: e_2_1 }; }
                        finally {
                            try {
                                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                            }
                            finally { if (e_2) throw e_2.error; }
                        }
                    }
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
    };
    AppStore.prototype.addPresolveValue = function (strength, state, attr, value) {
        this.preSolveValues.push([strength, state, attr, value]);
    };
    /** Given the current selection, find a reasonable plot segment for a glyph */
    AppStore.prototype.findPlotSegmentForGlyph = function (glyph) {
        var e_3, _a;
        if (this.currentSelection instanceof selection_1.MarkSelection ||
            this.currentSelection instanceof selection_1.GlyphSelection) {
            if (this.currentSelection.glyph == glyph) {
                return this.currentSelection.plotSegment;
            }
        }
        if (this.currentSelection instanceof selection_1.ChartElementSelection) {
            if (core_1.Prototypes.isType(this.currentSelection.chartElement.classID, "plot-segment")) {
                var plotSegment = this.currentSelection
                    .chartElement;
                if (plotSegment.glyph == glyph._id) {
                    return plotSegment;
                }
            }
        }
        try {
            for (var _b = __values(this.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var elem = _c.value;
                if (core_1.Prototypes.isType(elem.classID, "plot-segment")) {
                    var plotSegment = elem;
                    if (plotSegment.glyph == glyph._id) {
                        return plotSegment;
                    }
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
    };
    // eslint-disable-next-line
    AppStore.prototype.scaleInference = function (context, options) {
        var e_4, _a, e_5, _b, e_6, _c;
        var _this = this;
        var _d;
        // Figure out the source table
        var tableName = null;
        if (context.glyph) {
            tableName = context.glyph.table;
        }
        if (context.chart) {
            tableName = context.chart.table;
        }
        // Figure out the groupBy
        var groupBy = null;
        if (context.glyph) {
            // Find plot segments that use the glyph.
            this.chartManager.enumeratePlotSegments(function (cls) {
                if (cls.object.glyph == context.glyph._id) {
                    groupBy = cls.object.groupBy;
                }
            });
        }
        var table = this.getTable(tableName);
        // compares the ranges of two expression to determine similarity
        var compareDomainRanges = function (scaleID, expression) {
            var scaleClass = _this.chartManager.getClassById(scaleID);
            // compare only numerical scales
            if (!core_1.Prototypes.isType(scaleClass.object.classID, "scale.linear<number,number>")) {
                return false;
            }
            var values = _this.chartManager.getGroupedExpressionVector(table.name, groupBy, expression);
            var min = Math.min.apply(Math, __spread(values));
            var max = Math.min.apply(Math, __spread(values));
            var domainMin = scaleClass.object.properties.domainMin;
            var domainMax = scaleClass.object.properties.domainMax;
            var domainRange = Math.abs(domainMin - domainMax) * 2;
            if (domainMin - domainRange < min && min < domainMax + domainRange) {
                return true;
            }
            if (domainMin - domainRange < max && max < domainMax + domainRange) {
                return true;
            }
            return false;
        };
        // If there is an existing scale on the same column in the table, return that one
        if (!((_d = options.hints) === null || _d === void 0 ? void 0 : _d.newScale)) {
            var getExpressionUnit_1 = function (expr) {
                var parsed = core_1.Expression.parse(expr);
                // In the case of an aggregation function
                if (parsed instanceof core_1.Expression.FunctionCall) {
                    var args0 = parsed.args[0];
                    if (args0 instanceof core_1.Expression.Variable) {
                        var column = core_1.getByName(table.columns, args0.name);
                        if (column) {
                            return column.metadata.unit;
                        }
                    }
                }
                return null; // unit is unknown
            };
            var findScale = function (mappings) {
                for (var name_1 in mappings) {
                    if (!Object.prototype.hasOwnProperty.call(mappings, name_1)) {
                        continue;
                    }
                    if (mappings[name_1].type == specification_1.MappingType.scale) {
                        var scaleMapping = mappings[name_1];
                        if (scaleMapping.scale != null) {
                            if ((compareDomainRanges(scaleMapping.scale, options.expression) ||
                                scaleMapping.expression == options.expression) &&
                                (core_1.compareMarkAttributeNames(options.markAttribute, scaleMapping.attribute) ||
                                    !options.markAttribute ||
                                    !scaleMapping.attribute)) {
                                var scaleObject = core_1.getById(_this.chart.scales, scaleMapping.scale);
                                if (scaleObject.outputType == options.outputType) {
                                    return scaleMapping.scale;
                                }
                            }
                            // TODO: Fix this part
                            if (getExpressionUnit_1(scaleMapping.expression) ==
                                getExpressionUnit_1(options.expression) &&
                                getExpressionUnit_1(scaleMapping.expression) != null) {
                                var scaleObject = core_1.getById(_this.chart.scales, scaleMapping.scale);
                                if (scaleObject.outputType == options.outputType) {
                                    return scaleMapping.scale;
                                }
                            }
                        }
                    }
                }
                return null;
            };
            try {
                for (var _e = __values(this.chart.elements), _f = _e.next(); !_f.done; _f = _e.next()) {
                    var element = _f.value;
                    if (core_1.Prototypes.isType(element.classID, "plot-segment")) {
                        var plotSegment = element;
                        if (plotSegment.table != table.name) {
                            continue;
                        }
                        var glyph = core_1.getById(this.chart.glyphs, plotSegment.glyph);
                        if (!glyph) {
                            continue;
                        }
                        try {
                            for (var _g = (e_5 = void 0, __values(glyph.marks)), _h = _g.next(); !_h.done; _h = _g.next()) {
                                var element_1 = _h.value;
                                var foundScale = findScale(element_1.mappings);
                                if (foundScale) {
                                    return foundScale;
                                }
                            }
                        }
                        catch (e_5_1) { e_5 = { error: e_5_1 }; }
                        finally {
                            try {
                                if (_h && !_h.done && (_b = _g.return)) _b.call(_g);
                            }
                            finally { if (e_5) throw e_5.error; }
                        }
                    }
                    else {
                        var foundScale = findScale(element.mappings);
                        if (foundScale) {
                            return foundScale;
                        }
                    }
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
                }
                finally { if (e_4) throw e_4.error; }
            }
            if (this.chart.scaleMappings) {
                try {
                    for (var _j = __values(this.chart.scaleMappings), _k = _j.next(); !_k.done; _k = _j.next()) {
                        var scaleMapping = _k.value;
                        if ((compareDomainRanges(scaleMapping.scale, options.expression) ||
                            scaleMapping.expression == options.expression) &&
                            ((scaleMapping.attribute &&
                                core_1.compareMarkAttributeNames(scaleMapping.attribute, options.markAttribute)) ||
                                !scaleMapping.attribute)) {
                            var scaleObject = core_1.getById(this.chart.scales, scaleMapping.scale);
                            if (scaleObject && scaleObject.outputType == options.outputType) {
                                return scaleMapping.scale;
                            }
                        }
                    }
                }
                catch (e_6_1) { e_6 = { error: e_6_1 }; }
                finally {
                    try {
                        if (_k && !_k.done && (_c = _j.return)) _c.call(_j);
                    }
                    finally { if (e_6) throw e_6.error; }
                }
            }
        }
        var values = this.chartManager.getGroupedExpressionVector(table.name, groupBy, options.expression);
        // Infer a new scale for this item
        var scaleClassID = core_1.Prototypes.Scales.inferScaleType((values === null || values === void 0 ? void 0 : values.length) > 0 &&
            typeof values[0] === "string" &&
            !data_types_1.isBase64Image(values[0])
            ? specification_1.DataType.String
            : options.valueType, (values === null || values === void 0 ? void 0 : values.length) > 0 && typeof values[0] === "string"
            ? specification_1.DataKind.Categorical
            : options.valueKind, 
        // options.valueKind,
        options.outputType);
        if (scaleClassID != null) {
            var newScale = this.chartManager.createObject(scaleClassID);
            newScale.properties.name = this.chartManager.findUnusedName("Scale");
            newScale.inputType = options.valueType;
            newScale.outputType = options.outputType;
            this.chartManager.addScale(newScale);
            var scaleClass = this.chartManager.getClassById(newScale._id);
            var parentMainTable = this.getTables().find(function (table) { return table.type === dataset_1.TableType.ParentMain; });
            if (parentMainTable) {
                table = parentMainTable;
            }
            var rangeImage = null;
            if (scaleClassID === "scale.categorical<image,image>" &&
                options.valueType === specification_1.DataType.Image) {
                rangeImage = this.chartManager.getGroupedExpressionVector(table.name, groupBy, options.expression);
                scaleClass.inferParameters(this.chartManager.getGroupedExpressionVector(table.name, groupBy, "first(" + core_1.ImageKeyColumn + ")" // get ID column values for key
                ), __assign(__assign({}, options.hints), { extendScaleMax: true, extendScaleMin: true, rangeImage: rangeImage }));
            }
            else {
                scaleClass.inferParameters(this.chartManager.getGroupedExpressionVector(table.name, groupBy, options.expression), __assign(__assign({}, options.hints), { extendScaleMax: true, extendScaleMin: true, rangeImage: rangeImage }));
            }
            return newScale._id;
        }
        else {
            return null;
        }
    };
    AppStore.prototype.isLegendExistForScale = function (scale) {
        var e_7, _a;
        try {
            // See if we already have a legend
            for (var _b = __values(this.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (core_1.Prototypes.isType(element.classID, "legend")) {
                    if (element.properties.scale == scale) {
                        return true;
                    }
                }
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_7) throw e_7.error; }
        }
        return false;
    };
    // eslint-disable-next-line
    AppStore.prototype.toggleLegendForScale = function (scale, mapping, plotSegment) {
        var e_8, _a;
        var _this = this;
        var scaleObject = core_1.getById(this.chartManager.chart.scales, scale);
        try {
            // See if we already have a legend
            for (var _b = __values(this.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (core_1.Prototypes.isType(element.classID, "legend")) {
                    if (element.properties.scale == scale) {
                        this.chartManager.removeChartElement(element);
                        return;
                    }
                }
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_8) throw e_8.error; }
        }
        var newLegend;
        // Categorical-color scale
        if (scaleObject.classID == "scale.categorical<string,color>") {
            if (mapping && mapping.valueIndex != undefined) {
                newLegend = this.chartManager.createObject("legend.custom");
            }
            else {
                newLegend = this.chartManager.createObject("legend.categorical");
            }
            newLegend.properties.scale = scale;
            newLegend.mappings.x = {
                type: specification_1.MappingType.parent,
                parentAttribute: "x2",
            };
            newLegend.mappings.y = {
                type: specification_1.MappingType.parent,
                parentAttribute: "y2",
            };
            this.chartManager.chart.mappings.marginRight = {
                type: specification_1.MappingType.value,
                value: 100,
            };
        }
        // Numerical-color scale
        if (scaleObject.classID == "scale.linear<number,color>" ||
            scaleObject.classID == "scale.linear<integer,color>") {
            newLegend = this.chartManager.createObject("legend.numerical-color");
            newLegend.properties.scale = scale;
            newLegend.mappings.x = {
                type: specification_1.MappingType.parent,
                parentAttribute: "x2",
            };
            newLegend.mappings.y = {
                type: specification_1.MappingType.parent,
                parentAttribute: "y2",
            };
            this.chartManager.chart.mappings.marginRight = {
                type: specification_1.MappingType.value,
                value: 100,
            };
        }
        // Numerical-number scale
        if (scaleObject.classID == "scale.linear<number,number>" ||
            scaleObject.classID == "scale.linear<integer,number>") {
            if (!plotSegment) {
                console.log("Numerical-number legend needs plot segment parameter.");
                return;
            }
            newLegend = this.chartManager.createObject("legend.numerical-number");
            var properties = newLegend.properties;
            properties.scale = scale;
            var legendAttributes = [
                numerical_legend_1.NumericalNumberLegendAttributeNames.x1,
                numerical_legend_1.NumericalNumberLegendAttributeNames.y1,
                numerical_legend_1.NumericalNumberLegendAttributeNames.x2,
                numerical_legend_1.NumericalNumberLegendAttributeNames.y2,
            ];
            var targetAttributes_1;
            if (prototypes_1.isType(plotSegment.object.classID, "plot-segment.polar")) {
                switch (mapping.attribute) {
                    case "height": {
                        // radial
                        targetAttributes_1 = ["a1r1x", "a1r1y", "a1r2x", "a1r2y"];
                        properties.axis.side = "default";
                        break;
                    }
                    case "width": {
                        // angular
                        legendAttributes = [
                            numerical_legend_1.NumericalNumberLegendAttributeNames.cx,
                            numerical_legend_1.NumericalNumberLegendAttributeNames.cy,
                            numerical_legend_1.NumericalNumberLegendAttributeNames.radius,
                            numerical_legend_1.NumericalNumberLegendAttributeNames.startAngle,
                            numerical_legend_1.NumericalNumberLegendAttributeNames.endAngle,
                        ];
                        targetAttributes_1 = ["cx", "cy", "radial2", "angle1", "angle2"];
                        properties.axis.side = "default";
                        properties.polarAngularMode = true;
                        break;
                    }
                }
            }
            else {
                switch (mapping.attribute) {
                    case "height": {
                        targetAttributes_1 = ["x1", "y1", "x1", "y2"];
                        properties.axis.side = "default";
                        break;
                    }
                    case "width": {
                        targetAttributes_1 = ["x1", "y1", "x2", "y1"];
                        properties.axis.side = "opposite";
                        break;
                    }
                    default: {
                        targetAttributes_1 = ["x1", "y1", "x1", "y2"];
                        properties.axis.side = "default";
                        break;
                    }
                }
            }
            legendAttributes.forEach(function (attribute, i) {
                // //snap legend to plot segment
                _this.chartManager.chart.constraints.push({
                    type: "snap",
                    attributes: {
                        element: newLegend._id,
                        attribute: attribute,
                        targetElement: plotSegment.object._id,
                        targetAttribute: targetAttributes_1[i],
                        gap: 0,
                    },
                });
            });
        }
        if (newLegend) {
            var mappingOptions = {
                type: specification_1.MappingType.scale,
                table: mapping.table,
                expression: mapping.expression,
                valueType: mapping.valueType,
                scale: scaleObject._id,
                allowSelectValue: mapping && mapping.valueIndex != undefined,
            };
            newLegend.mappings.mappingOptions = mappingOptions;
            this.chartManager.addChartElement(newLegend);
        }
    };
    AppStore.prototype.getRepresentativeGlyphState = function (glyph) {
        var e_9, _a;
        try {
            // Is there a plot segment using this glyph?
            for (var _b = __values(this.chart.elements), _c = _b.next(); !_c.done; _c = _b.next()) {
                var element = _c.value;
                if (core_1.Prototypes.isType(element.classID, "plot-segment")) {
                    var plotSegment = element;
                    if (plotSegment.glyph == glyph._id) {
                        var state = this.chartManager.getClassById(plotSegment._id)
                            .state;
                        return state.glyphs[0];
                    }
                }
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_9) throw e_9.error; }
        }
        return null;
    };
    AppStore.prototype.solveConstraintsAndUpdateGraphics = function (mappingOnly) {
        var _this = this;
        if (mappingOnly === void 0) { mappingOnly = false; }
        this.solveConstraintsInWorker(mappingOnly).then(function () {
            _this.emit(AppStore.EVENT_GRAPHICS);
        });
    };
    AppStore.prototype.solveConstraintsInWorker = function (mappingOnly) {
        if (mappingOnly === void 0) { mappingOnly = false; }
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.solverStatus = {
                            solving: true,
                        };
                        this.emit(AppStore.EVENT_SOLVER_STATUS);
                        return [4 /*yield*/, this.worker.solveChartConstraints(this.chart, this.chartState, this.dataset, this.preSolveValues, mappingOnly)];
                    case 1:
                        _a.sent();
                        this.preSolveValues = [];
                        this.solverStatus = {
                            solving: false,
                        };
                        this.emit(AppStore.EVENT_SOLVER_STATUS);
                        return [2 /*return*/];
                }
            });
        });
    };
    AppStore.prototype.newChartEmpty = function () {
        var _this = this;
        this.currentSelection = null;
        this.selectedGlyphIndex = {};
        this.currentTool = null;
        this.currentToolOptions = null;
        this.chart = defaults_1.createDefaultChart(this.dataset, this.editorType === EditorType.Chart);
        this.chartManager = new core_1.Prototypes.ChartStateManager(this.chart, this.dataset);
        this.chartManager.onUpdate(function () {
            _this.solveConstraintsAndUpdateGraphics();
        });
        this.chartState = this.chartManager.chartState;
    };
    AppStore.prototype.deleteSelection = function () {
        var sel = this.currentSelection;
        this.currentSelection = null;
        this.emit(AppStore.EVENT_SELECTION);
        if (sel instanceof selection_1.ChartElementSelection) {
            new actions_1.Actions.DeleteChartElement(sel.chartElement).dispatch(this.dispatcher);
        }
        if (sel instanceof selection_1.MarkSelection) {
            new actions_1.Actions.RemoveMarkFromGlyph(sel.glyph, sel.mark).dispatch(this.dispatcher);
        }
        if (sel instanceof selection_1.GlyphSelection) {
            new actions_1.Actions.RemoveGlyph(sel.glyph).dispatch(this.dispatcher);
        }
    };
    AppStore.prototype.handleEscapeKey = function () {
        if (this.currentTool) {
            this.currentTool = null;
            this.emit(AppStore.EVENT_CURRENT_TOOL);
            return;
        }
        if (this.currentSelection) {
            new actions_1.Actions.ClearSelection().dispatch(this.dispatcher);
        }
    };
    AppStore.prototype.getClosestSnappingGuide = function (point) {
        var e_10, _a;
        var _this = this;
        var chartClass = this.chartManager.getChartClass(this.chartManager.chartState);
        var boundsGuides = chartClass.getSnappingGuides();
        var chartGuides = boundsGuides.map(function (bounds) {
            return {
                element: null,
                guide: bounds,
            };
        });
        var elements = this.chartManager.chart.elements;
        var elementStates = this.chartManager.chartState.elements;
        core_1.zipArray(elements, elementStates).forEach(function (_a) {
            var _b = __read(_a, 2), layout = _b[0], layoutState = _b[1];
            var layoutClass = _this.chartManager.getChartElementClass(layoutState);
            chartGuides = chartGuides.concat(layoutClass.getSnappingGuides().map(function (bounds) {
                return {
                    element: layout,
                    guide: bounds,
                };
            }));
        });
        var minYDistance = null;
        var minXDistance = null;
        var minYGuide = null;
        var minXGuide = null;
        try {
            for (var chartGuides_1 = __values(chartGuides), chartGuides_1_1 = chartGuides_1.next(); !chartGuides_1_1.done; chartGuides_1_1 = chartGuides_1.next()) {
                var g = chartGuides_1_1.value;
                var guide = g.guide;
                // Find closest point
                if (guide.type == "y") {
                    var dY = Math.abs(guide.value - point.y);
                    if (dY < minYDistance || minYDistance == null) {
                        minYDistance = dY;
                        minYGuide = g;
                    }
                }
                else if (guide.type == "x") {
                    var dX = Math.abs(guide.value - point.x);
                    if (dX < minXDistance || minXDistance == null) {
                        minXDistance = dX;
                        minXGuide = g;
                    }
                }
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (chartGuides_1_1 && !chartGuides_1_1.done && (_a = chartGuides_1.return)) _a.call(chartGuides_1);
            }
            finally { if (e_10) throw e_10.error; }
        }
        return [minXGuide, minYGuide];
    };
    AppStore.prototype.buildChartTemplate = function () {
        var builder = new template_1.ChartTemplateBuilder(this.chart, this.dataset, this.chartManager, CHARTICULATOR_PACKAGE.version);
        var template = builder.build();
        return template;
    };
    AppStore.prototype.verifyUserExpressionWithTable = function (inputString, table, options) {
        if (options === void 0) { options = {}; }
        if (table != null) {
            var dfTable_1 = this.chartManager.dataflow.getTable(table);
            var rowIterator = function () {
                var i;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            i = 0;
                            _a.label = 1;
                        case 1:
                            if (!(i < dfTable_1.rows.length)) return [3 /*break*/, 4];
                            return [4 /*yield*/, dfTable_1.getRowContext(i)];
                        case 2:
                            _a.sent();
                            _a.label = 3;
                        case 3:
                            i++;
                            return [3 /*break*/, 1];
                        case 4: return [2 /*return*/];
                    }
                });
            };
            return core_1.Expression.verifyUserExpression(inputString, __assign({ data: rowIterator() }, options));
        }
        else {
            return core_1.Expression.verifyUserExpression(inputString, __assign({}, options));
        }
    };
    // eslint-disable-next-line
    AppStore.prototype.updateScales = function () {
        var _this = this;
        try {
            var updatedScales_1 = [];
            // eslint-disable-next-line
            var updateScalesInternal_1 = function (scaleId, mappings, context) {
                if (updatedScales_1.find(function (scale) { return scale === scaleId; })) {
                    return;
                }
                var scale = core_1.Prototypes.findObjectById(_this.chart, scaleId);
                // prevent updating if auto scale is disabled
                if (!scale.properties.autoDomainMin &&
                    !scale.properties.autoDomainMin) {
                    return;
                }
                var filteredMappings = mappings
                    .flatMap(function (el) {
                    return Object.keys(el.mappings).map(function (key) {
                        return {
                            element: el,
                            key: key,
                            mapping: el.mappings[key],
                        };
                    });
                })
                    .filter(function (mapping) {
                    return mapping.mapping.type === specification_1.MappingType.scale &&
                        mapping.mapping.scale === scaleId;
                });
                // Figure out the groupBy
                var groupBy = null;
                if (context.glyph) {
                    // Find plot segments that use the glyph.
                    _this.chartManager.enumeratePlotSegments(function (cls) {
                        if (cls.object.glyph == context.glyph._id) {
                            groupBy = cls.object.groupBy;
                        }
                    });
                }
                filteredMappings.forEach(function (mapping) {
                    var _a, _b;
                    var scaleClass = _this.chartManager.getClassById(scaleId);
                    var values = [];
                    var newScale = true;
                    var reuseRange = false;
                    var extendScale = true;
                    // special case for legend to draw column names
                    if (mapping.element.classID === "legend.custom") {
                        var table = _this.chartManager.dataflow.getTable(mapping.mapping.table);
                        var parsedExpression = _this.chartManager.dataflow.cache.parse(mapping.mapping.expression);
                        values = parsedExpression.getValue(table);
                        newScale = true;
                        extendScale = true;
                        reuseRange = true;
                    }
                    else {
                        if (scale.classID == "scale.categorical<string,color>") {
                            newScale = true;
                            extendScale = true;
                            reuseRange = true;
                        }
                        else {
                            newScale = false;
                            extendScale = true;
                            reuseRange = true;
                        }
                        values = _this.chartManager.getGroupedExpressionVector(mapping.mapping.table, groupBy, mapping.mapping.expression);
                    }
                    scaleClass.inferParameters(values, {
                        newScale: newScale,
                        reuseRange: reuseRange,
                        extendScaleMax: extendScale,
                        extendScaleMin: extendScale,
                        rangeNumber: [
                            (_a = scale.mappings.rangeMin) === null || _a === void 0 ? void 0 : _a.value,
                            (_b = scale.mappings.rangeMax) === null || _b === void 0 ? void 0 : _b.value,
                        ],
                    });
                    updatedScales_1.push(scaleId);
                });
            };
            var chartElements_1 = this.chart.elements;
            var legendScales_1 = chartElements_1
                .filter(function (el) { return core_1.Prototypes.isType(el.classID, "legend"); })
                .flatMap(function (el) {
                return el.properties.scale;
            });
            legendScales_1.forEach(function (scale) {
                updateScalesInternal_1(scale, chartElements_1, {
                    chart: _this.chart,
                    glyph: null,
                });
                _this.chart.glyphs.forEach(function (gl) {
                    return updateScalesInternal_1(scale, gl.marks, {
                        chart: _this.chart,
                        glyph: gl,
                    });
                });
            });
            var resetOfScales = this.chart.scales.filter(function (other) { return !legendScales_1.find(function (l) { return l === other._id; }); });
            resetOfScales.forEach(function (scale) {
                if (scale.properties.autoDomainMax || scale.properties.autoDomainMin) {
                    updateScalesInternal_1(scale._id, chartElements_1, {
                        chart: _this.chart,
                        glyph: null,
                    });
                    _this.chart.glyphs.forEach(function (gl) {
                        return updateScalesInternal_1(scale._id, gl.marks, {
                            chart: _this.chart,
                            glyph: gl,
                        });
                    });
                }
            });
        }
        catch (ex) {
            console.error("Updating of scales failed with error", ex);
        }
    };
    // eslint-disable-next-line
    AppStore.prototype.updatePlotSegments = function () {
        var _this = this;
        // Get plot segments to update with new data
        var plotSegments = this.chart.elements.filter(function (element) { return core_1.Prototypes.isType(element.classID, "plot-segment"); });
        // eslint-disable-next-line
        plotSegments.forEach(function (plot) {
            var table = _this.dataset.tables.find(function (table) { return table.name === plot.table; });
            // xData
            var xDataProperty = plot.properties
                .xData;
            if (xDataProperty && xDataProperty.expression) {
                var xData = new actions_1.DragData.DataExpression(table, xDataProperty.expression, xDataProperty.valueType, {
                    kind: xDataProperty.type === "numerical" &&
                        xDataProperty.numericalMode === "temporal"
                        ? specification_1.DataKind.Temporal
                        : xDataProperty.dataKind
                            ? xDataProperty.dataKind
                            : _this.getDataKindByType(xDataProperty.type),
                    orderMode: xDataProperty.orderMode
                        ? xDataProperty.orderMode
                        : xDataProperty.valueType === "string" ||
                            xDataProperty.valueType === "number"
                            ? types_1.OrderMode.order
                            : null,
                    order: xDataProperty.order != undefined
                        ? xDataProperty.order
                        : xDataProperty.orderByCategories
                            ? xDataProperty.orderByCategories
                            : null,
                    orderByExpression: xDataProperty.orderByExpression !== undefined
                        ? xDataProperty.orderByExpression
                        : null,
                }, xDataProperty.rawExpression);
                _this.bindDataToAxis({
                    property: base_2.PlotSegmentAxisPropertyNames.xData,
                    dataExpression: xData,
                    object: plot,
                    appendToProperty: null,
                    type: xDataProperty.type,
                    numericalMode: xDataProperty.numericalMode,
                    autoDomainMax: xDataProperty.autoDomainMax,
                    autoDomainMin: xDataProperty.autoDomainMin,
                    domainMin: xDataProperty.domainMin,
                    domainMax: xDataProperty.domainMax,
                    defineCategories: true,
                });
            }
            // yData
            var yDataProperty = plot.properties
                .yData;
            if (yDataProperty && yDataProperty.expression) {
                var yData = new actions_1.DragData.DataExpression(table, yDataProperty.expression, yDataProperty.valueType, {
                    kind: yDataProperty.type === "numerical" &&
                        yDataProperty.numericalMode === "temporal"
                        ? specification_1.DataKind.Temporal
                        : yDataProperty.dataKind
                            ? yDataProperty.dataKind
                            : _this.getDataKindByType(yDataProperty.type),
                    orderMode: yDataProperty.orderMode
                        ? yDataProperty.orderMode
                        : yDataProperty.valueType === "string"
                            ? types_1.OrderMode.order
                            : null,
                    order: yDataProperty.order !== undefined ? yDataProperty.order : null,
                }, yDataProperty.rawExpression);
                _this.bindDataToAxis({
                    property: base_2.PlotSegmentAxisPropertyNames.yData,
                    dataExpression: yData,
                    object: plot,
                    appendToProperty: null,
                    type: yDataProperty.type,
                    numericalMode: yDataProperty.numericalMode,
                    autoDomainMax: yDataProperty.autoDomainMax,
                    autoDomainMin: yDataProperty.autoDomainMin,
                    domainMin: yDataProperty.domainMin,
                    domainMax: yDataProperty.domainMax,
                    defineCategories: true,
                });
            }
            var axisProperty = plot.properties
                .axis;
            if (axisProperty && axisProperty.expression) {
                var axisData = new actions_1.DragData.DataExpression(table, axisProperty.expression !== undefined
                    ? axisProperty.expression
                    : null, axisProperty.valueType !== undefined ? axisProperty.valueType : null, {
                    kind: axisProperty.type === "numerical" &&
                        axisProperty.numericalMode === "temporal"
                        ? specification_1.DataKind.Temporal
                        : axisProperty.dataKind
                            ? axisProperty.dataKind
                            : _this.getDataKindByType(axisProperty.type),
                    orderMode: axisProperty.orderMode
                        ? axisProperty.orderMode
                        : axisProperty.valueType === "string"
                            ? types_1.OrderMode.order
                            : null,
                    order: axisProperty.order !== undefined ? axisProperty.order : null,
                }, axisProperty.rawExpression);
                _this.bindDataToAxis({
                    property: base_2.PlotSegmentAxisPropertyNames.axis,
                    dataExpression: axisData,
                    object: plot,
                    appendToProperty: null,
                    type: axisProperty.type,
                    numericalMode: axisProperty.numericalMode
                        ? axisProperty.numericalMode
                        : null,
                    autoDomainMax: axisProperty.autoDomainMax,
                    autoDomainMin: axisProperty.autoDomainMin,
                    domainMin: axisProperty.domainMin,
                    domainMax: axisProperty.domainMax,
                    defineCategories: true,
                });
            }
        });
    };
    AppStore.prototype.updateDataAxes = function () {
        var _this = this;
        var mapElementWithTable = function (table) { return function (el) {
            return {
                table: table,
                element: el,
            };
        }; };
        var bindAxis = function (dataAxisElement, expression, axisProperty, dataAxis, appendToProperty) {
            if (appendToProperty === void 0) { appendToProperty = null; }
            var axisData = new actions_1.DragData.DataExpression(_this.dataset.tables.find(function (t) { return t.name == dataAxisElement.table; }), expression, axisProperty.valueType, {
                kind: axisProperty.type === "numerical" &&
                    axisProperty.numericalMode === "temporal"
                    ? specification_1.DataKind.Temporal
                    : axisProperty.dataKind
                        ? axisProperty.dataKind
                        : _this.getDataKindByType(axisProperty.type),
                orderMode: axisProperty.orderMode
                    ? axisProperty.orderMode
                    : axisProperty.valueType === "string"
                        ? types_1.OrderMode.order
                        : null,
                order: axisProperty.order,
            }, axisProperty.rawExpression);
            _this.bindDataToAxis({
                property: base_2.PlotSegmentAxisPropertyNames.axis,
                dataExpression: axisData,
                object: dataAxis,
                appendToProperty: appendToProperty,
                type: axisProperty.type,
                numericalMode: axisProperty.numericalMode,
                autoDomainMax: axisProperty.autoDomainMax,
                autoDomainMin: axisProperty.autoDomainMin,
                domainMin: axisProperty.domainMin,
                domainMax: axisProperty.domainMax,
                defineCategories: false,
            });
        };
        var table = this.dataset.tables.find(function (t) { return t.type === dataset_1.TableType.Main; });
        this.chart.elements
            .map(mapElementWithTable(table.name))
            .concat(this.chart.glyphs.flatMap(function (gl) {
            return gl.marks.map(mapElementWithTable(gl.table));
        }))
            .filter(function (element) {
            return core_1.Prototypes.isType(element.element.classID, "mark.data-axis");
        })
            .forEach(function (dataAxisElement) {
            var dataAxis = dataAxisElement.element;
            var axisProperty = dataAxis.properties
                .axis;
            if (axisProperty) {
                var expression = axisProperty.expression;
                bindAxis(dataAxisElement, expression, axisProperty, dataAxis);
            }
            var dataExpressions = dataAxis.properties.dataExpressions;
            // remove all and added again
            dataAxis.properties.dataExpressions = [];
            dataExpressions.forEach(function (dataExpression, index) {
                var axisProperty = dataAxis.properties
                    .axis;
                if (axisProperty) {
                    var expression = dataExpression.expression;
                    bindAxis(dataAxisElement, expression, axisProperty, dataAxis, "dataExpressions");
                    // save old name/id of expression to hold binding marks to those axis points
                    dataAxis.properties.dataExpressions[index].name =
                        dataExpression.name;
                }
            });
        });
    };
    AppStore.prototype.getBindingByDataKind = function (kind) {
        switch (kind) {
            case specification_1.DataKind.Numerical:
                return types_1.AxisDataBindingType.Numerical;
            case specification_1.DataKind.Temporal:
            case specification_1.DataKind.Ordinal:
            case specification_1.DataKind.Categorical:
                return types_1.AxisDataBindingType.Categorical;
        }
    };
    // eslint-disable-next-line
    AppStore.prototype.bindDataToAxis = function (options) {
        var e_11, _a;
        var _b, _c, _d;
        var object = options.object, property = options.property, appendToProperty = options.appendToProperty, dataExpression = options.dataExpression;
        this.normalizeDataExpression(dataExpression);
        var groupExpression = dataExpression.expression;
        var valueType = dataExpression.valueType;
        var propertyValue = object.properties[options.property];
        var type = dataExpression.type
            ? options.type
            : this.getBindingByDataKind(options.dataExpression.metadata.kind);
        var rawColumnExpression = dataExpression.rawColumnExpression;
        if (rawColumnExpression &&
            dataExpression.valueType !== specification_1.DataType.Date &&
            (options.dataExpression.metadata.kind === specification_1.DataKind.Ordinal ||
                options.dataExpression.metadata.kind === specification_1.DataKind.Categorical)) {
            groupExpression = rawColumnExpression;
            valueType = specification_1.DataType.String;
        }
        var objectProperties = object.properties[options.property];
        var expression = appendToProperty === "dataExpressions" && propertyValue
            ? propertyValue.expression
            : groupExpression;
        var column = utils_2.getColumnNameByExpression(expression);
        var orderByCategories = [];
        var dataBinding = {
            type: options.type || type,
            // Don't change current expression (use current expression), if user appends data expression ()
            expression: expression,
            rawExpression: dataExpression.rawColumnExpression != undefined
                ? dataExpression.rawColumnExpression
                : expression,
            valueType: valueType !== undefined ? valueType : null,
            gapRatio: (propertyValue === null || propertyValue === void 0 ? void 0 : propertyValue.gapRatio) === undefined ? 0.1 : propertyValue.gapRatio,
            visible: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.visible) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.visible : true,
            side: (propertyValue === null || propertyValue === void 0 ? void 0 : propertyValue.side) || "default",
            style: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.style) ||
                core_1.deepClone(plot_segments_1.defaultAxisStyle),
            numericalMode: options.numericalMode != undefined ? options.numericalMode : null,
            dataKind: dataExpression.metadata.kind != undefined
                ? dataExpression.metadata.kind
                : null,
            order: dataExpression.metadata.order !== undefined
                ? dataExpression.metadata.order
                : null,
            orderMode: dataExpression.metadata.orderMode !== undefined
                ? dataExpression.metadata.orderMode
                : null,
            autoDomainMax: options.autoDomainMax != undefined ? options.autoDomainMax : true,
            autoDomainMin: options.autoDomainMin != undefined ? options.autoDomainMin : true,
            tickFormat: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.tickFormat) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.tickFormat
                : null,
            tickDataExpression: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.tickDataExpression) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.tickDataExpression
                : null,
            tickFormatType: (_b = objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.tickFormatType) !== null && _b !== void 0 ? _b : types_1.TickFormatType.None,
            domainMin: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMin) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMin
                : null,
            domainMax: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMax) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMax
                : null,
            dataDomainMin: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMin) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMin
                : null,
            dataDomainMax: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMax) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.domainMax
                : null,
            enablePrePostGap: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.enablePrePostGap) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.enablePrePostGap
                : null,
            categories: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.categories) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.categories
                : null,
            allCategories: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.allCategories) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.allCategories
                : (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.categories) !== undefined
                    ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.categories
                    : null,
            scrollPosition: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.scrollPosition) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.scrollPosition
                : 0,
            allowScrolling: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.allowScrolling) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.allowScrolling
                : false,
            windowSize: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.windowSize) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.windowSize
                : 10,
            barOffset: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.barOffset) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.barOffset
                : 0,
            offset: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.offset) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.offset
                : 0,
            onTop: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.onTop) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.onTop
                : false,
            enableSelection: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.enableSelection) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.enableSelection
                : false,
            orderByCategories: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.orderByCategories) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.orderByCategories
                : orderByCategories,
            orderByExpression: column,
            numberOfTicks: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.numberOfTicks) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.numberOfTicks
                : axis_1.AxisRenderer.DEFAULT_TICKS_NUMBER,
            autoNumberOfTicks: (objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.autoNumberOfTicks) !== undefined
                ? objectProperties === null || objectProperties === void 0 ? void 0 : objectProperties.autoNumberOfTicks
                : true,
        };
        var expressions = [groupExpression];
        if (appendToProperty) {
            if (object.properties[appendToProperty] == null) {
                object.properties[appendToProperty] = [
                    { name: core_1.uniqueID(), expression: groupExpression },
                ];
            }
            else {
                object.properties[appendToProperty].push({
                    name: core_1.uniqueID(),
                    expression: groupExpression,
                });
            }
            expressions = object.properties[appendToProperty].map(function (x) { return x.expression; });
            if (object.properties[property] == null) {
                object.properties[property] = dataBinding;
            }
            else {
                dataBinding = object.properties[property];
            }
        }
        else {
            object.properties[property] = dataBinding;
        }
        var groupBy = this.getGroupingExpression(object);
        var values = [];
        if (appendToProperty == "dataExpressions" &&
            dataBinding.domainMax != undefined &&
            dataBinding.domainMin != undefined) {
            // save current range of scale if user adds data
            values = values.concat(dataBinding.domainMax, dataBinding.domainMin);
        }
        try {
            for (var expressions_1 = __values(expressions), expressions_1_1 = expressions_1.next(); !expressions_1_1.done; expressions_1_1 = expressions_1.next()) {
                var expr = expressions_1_1.value;
                if (expr) {
                    var r = this.chartManager.getGroupedExpressionVector(dataExpression.table.name, groupBy, expr);
                    values = values.concat(r);
                }
            }
        }
        catch (e_11_1) { e_11 = { error: e_11_1 }; }
        finally {
            try {
                if (expressions_1_1 && !expressions_1_1.done && (_a = expressions_1.return)) _a.call(expressions_1);
            }
            finally { if (e_11) throw e_11.error; }
        }
        if (dataExpression.metadata) {
            switch (dataExpression.metadata.kind) {
                case core_1.Specification.DataKind.Categorical:
                case core_1.Specification.DataKind.Ordinal:
                    {
                        dataBinding.type = types_1.AxisDataBindingType.Categorical;
                        dataBinding.valueType = dataExpression.valueType;
                        var _e = this.getCategoriesForDataBinding(dataExpression.metadata, dataExpression.valueType, values), categories = _e.categories, order = _e.order;
                        dataBinding.orderByCategories = core_1.deepClone(categories);
                        dataBinding.order = order != undefined ? order : null;
                        dataBinding.allCategories = core_1.deepClone(categories);
                        if (dataBinding.windowSize == null ||
                            dataBinding.windowSize > dataBinding.allCategories.length) {
                            dataBinding.windowSize = (_d = (_c = dataBinding.allCategories) === null || _c === void 0 ? void 0 : _c.length) !== null && _d !== void 0 ? _d : Math.ceil(categories.length / 10);
                        }
                        dataBinding.categories = categories;
                        if (dataBinding.allowScrolling) {
                            var start = Math.floor(((categories.length - dataBinding.windowSize) / 100) *
                                dataBinding.scrollPosition);
                            dataBinding.categories = categories.slice(start, start + dataBinding.windowSize);
                        }
                    }
                    //reset tick data for categorical data
                    dataBinding.tickFormat = null;
                    dataBinding.tickDataExpression = null;
                    break;
                case core_1.Specification.DataKind.Numerical:
                    {
                        if (options.numericalMode === types_1.NumericalMode.Logarithmic) {
                            var scale = new core_1.Scale.LogarithmicScale();
                            scale.inferParameters(values);
                            if (dataBinding.allowScrolling) {
                                if (dataBinding.autoDomainMin) {
                                    dataBinding.dataDomainMin = scale.domainMin;
                                }
                                else {
                                    dataBinding.dataDomainMin = options.domainMin;
                                }
                                if (dataBinding.autoDomainMax) {
                                    dataBinding.dataDomainMax = scale.domainMax;
                                }
                                else {
                                    dataBinding.dataDomainMax = options.domainMax;
                                }
                            }
                            else {
                                if (dataBinding.autoDomainMin) {
                                    dataBinding.domainMin = scale.domainMin;
                                }
                                else {
                                    dataBinding.domainMin = options.domainMin;
                                }
                                if (dataBinding.autoDomainMax) {
                                    dataBinding.domainMax = scale.domainMax;
                                }
                                else {
                                    dataBinding.domainMax = options.domainMax;
                                }
                            }
                            dataBinding.type = types_1.AxisDataBindingType.Numerical;
                            dataBinding.numericalMode = types_1.NumericalMode.Logarithmic;
                        }
                        else {
                            var scale = new core_1.Scale.LinearScale();
                            scale.inferParameters(values);
                            if (dataBinding.allowScrolling) {
                                if (dataBinding.autoDomainMin) {
                                    dataBinding.dataDomainMin = scale.domainMin;
                                }
                                else {
                                    dataBinding.dataDomainMin = options.domainMin;
                                }
                                if (dataBinding.autoDomainMax) {
                                    dataBinding.dataDomainMax = scale.domainMax;
                                }
                                else {
                                    dataBinding.dataDomainMax = options.domainMax;
                                }
                            }
                            else {
                                if (dataBinding.autoDomainMin) {
                                    dataBinding.domainMin = scale.domainMin;
                                }
                                else {
                                    dataBinding.domainMin = options.domainMin;
                                }
                                if (dataBinding.autoDomainMax) {
                                    dataBinding.domainMax = scale.domainMax;
                                }
                                else {
                                    dataBinding.domainMax = options.domainMax;
                                }
                            }
                            dataBinding.type = types_1.AxisDataBindingType.Numerical;
                            dataBinding.numericalMode = types_1.NumericalMode.Linear;
                        }
                        if (options.defineCategories) {
                            dataBinding.categories = core_1.defineCategories(values);
                        }
                        if (dataBinding.windowSize == null) {
                            dataBinding.windowSize =
                                (dataBinding.domainMax - dataBinding.domainMin) / 10;
                        }
                        dataBinding.dataDomainMin = dataBinding.domainMin;
                        dataBinding.dataDomainMax = dataBinding.domainMax;
                    }
                    break;
                case core_1.Specification.DataKind.Temporal:
                    {
                        var scale = new core_1.Scale.DateScale();
                        scale.inferParameters(values, false);
                        if (dataBinding.autoDomainMin) {
                            dataBinding.domainMin = scale.domainMin;
                        }
                        else {
                            dataBinding.domainMin = options.domainMin;
                        }
                        if (dataBinding.autoDomainMax) {
                            dataBinding.domainMax = scale.domainMax;
                        }
                        else {
                            dataBinding.domainMax = options.domainMax;
                        }
                        dataBinding.type = types_1.AxisDataBindingType.Numerical;
                        dataBinding.numericalMode = types_1.NumericalMode.Temporal;
                        var categories = this.getCategoriesForDataBinding(dataExpression.metadata, dataExpression.valueType, values).categories;
                        dataBinding.allCategories = core_1.deepClone(categories);
                        dataBinding.categories = categories;
                        if (dataBinding.allowScrolling) {
                            var start = Math.floor(((categories.length - dataBinding.windowSize) / 100) *
                                dataBinding.scrollPosition);
                            dataBinding.categories = categories.slice(start, start + dataBinding.windowSize);
                        }
                    }
                    break;
            }
        }
        // Adjust sublayout option if current option is not available
        var props = object.properties;
        if (props.sublayout) {
            if (props.sublayout.type == base_2.Region2DSublayoutType.DodgeX ||
                props.sublayout.type == base_2.Region2DSublayoutType.DodgeY ||
                props.sublayout.type == base_2.Region2DSublayoutType.Grid) {
                if (props.xData && props.xData.type == "numerical") {
                    props.sublayout.type = base_2.Region2DSublayoutType.Overlap;
                }
                if (props.yData && props.yData.type == "numerical") {
                    props.sublayout.type = base_2.Region2DSublayoutType.Overlap;
                }
            }
            //set default sublayout type for Categorical - Categorical data
            if (props.xData &&
                props.xData.type == types_1.AxisDataBindingType.Categorical &&
                props.yData &&
                props.yData.type == types_1.AxisDataBindingType.Categorical) {
                if (props.sublayout.type == base_2.Region2DSublayoutType.Overlap) {
                    props.sublayout.type = base_2.Region2DSublayoutType.Grid;
                }
            }
        }
    };
    /**
     * Due to undefined "value" will not saved after JSON.stringfy, need to update all undefined "values" to null
     * deepClone uses JSON.stringfy to create copy of object. If object losses some property after copy
     * the function expect_deep_approximately_equals gives difference for identical tempalte/chart state
     * See {@link ChartStateManager.hasUnsavedChanges} for details
     * @param dataExpression Data expression for axis
     */
    AppStore.prototype.normalizeDataExpression = function (dataExpression) {
        if (dataExpression.metadata) {
            if (dataExpression.metadata.order === undefined) {
                dataExpression.metadata.order = null;
            }
            if (dataExpression.metadata.orderMode === undefined) {
                dataExpression.metadata.orderMode = null;
            }
            if (dataExpression.metadata.rawColumnName === undefined) {
                dataExpression.metadata.rawColumnName = null;
            }
            if (dataExpression.metadata.unit === undefined) {
                dataExpression.metadata.unit = null;
            }
            if (dataExpression.metadata.kind === undefined) {
                dataExpression.metadata.kind = null;
            }
            if (dataExpression.metadata.isRaw === undefined) {
                dataExpression.metadata.isRaw = null;
            }
            if (dataExpression.metadata.format === undefined) {
                dataExpression.metadata.format = null;
            }
            if (dataExpression.metadata.examples === undefined) {
                dataExpression.metadata.examples = null;
            }
            if (dataExpression.scaleID === undefined) {
                dataExpression.scaleID = null;
            }
            if (dataExpression.type === undefined) {
                dataExpression.type = null;
            }
            if (dataExpression.rawColumnExpression === undefined) {
                dataExpression.rawColumnExpression = null;
            }
            if (dataExpression.valueType === undefined) {
                dataExpression.valueType = null;
            }
        }
    };
    AppStore.prototype.getCategoriesForOrderByColumn = function (orderExpression, expression, data) {
        var parsed = core_1.Expression.parse(expression);
        var groupByExpression = null;
        if (parsed instanceof core_1.Expression.FunctionCall) {
            groupByExpression = parsed.args[0].toString();
            groupByExpression = groupByExpression === null || groupByExpression === void 0 ? void 0 : groupByExpression.split("`").join("");
            //need to provide date.year() etc.
            groupByExpression = utils_2.parseDerivedColumnsExpression(groupByExpression);
        }
        var table = this.getTables()[0].name;
        var df = new core_1.Prototypes.Dataflow.DataflowManager(this.dataset);
        var getExpressionVector = function (expression, table, groupBy) {
            var newExpression = utils_2.transformOrderByExpression(expression);
            groupBy.expression = utils_2.transformOrderByExpression(groupBy.expression);
            var expr = core_1.Expression.parse(newExpression);
            var tableContext = df.getTable(table);
            var indices = groupBy
                ? new group_by_1.CompiledGroupBy(groupBy, df.cache).groupBy(tableContext)
                : core_1.makeRange(0, tableContext.rows.length).map(function (x) { return [x]; });
            return indices.map(function (is) {
                return expr.getValue(tableContext.getGroupedContext(is));
            });
        };
        var vectorData = getExpressionVector(data.orderByExpression, table, {
            expression: groupByExpression,
        });
        var items = vectorData.map(function (item) { return __spread(new Set(item)); });
        var newData = utils_2.updateWidgetCategoriesByExpression(items);
        return __spread(new Set(newData));
    };
    AppStore.prototype.getCategoriesForDataBinding = function (metadata, type, values) {
        var categories;
        var order;
        if (metadata.order && metadata.orderMode === types_1.OrderMode.order) {
            categories = metadata.order.slice();
            var scale_1 = new core_1.Scale.CategoricalScale();
            scale_1.inferParameters(values, metadata.orderMode);
            var newData_1 = new Array(scale_1.length);
            scale_1.domain.forEach(function (index, x) { return (newData_1[index] = x.toString()); });
            metadata.order = metadata.order.filter(function (value) {
                return scale_1.domain.has(value);
            });
            var newItems = newData_1.filter(function (category) { return !metadata.order.find(function (order) { return order === category; }); });
            categories = new Array(metadata.order.length);
            metadata.order.forEach(function (value, index) {
                categories[index] = value;
            });
            categories = categories.concat(newItems);
            order = metadata.order.concat(newItems);
        }
        else {
            var orderMode = types_1.OrderMode.alphabetically;
            var scale = new core_1.Scale.CategoricalScale();
            if (metadata.orderMode) {
                orderMode = metadata.orderMode;
            }
            if (type === "number") {
                values = values.sort(function (a, b) { return a - b; });
                orderMode = types_1.OrderMode.order;
            }
            scale.inferParameters(values, orderMode);
            categories = new Array(scale.length);
            scale.domain.forEach(function (index, x) { return (categories[index] = x.toString()); });
            if (type === "number") {
                metadata.order = categories;
            }
        }
        return { categories: categories, order: order };
    };
    AppStore.prototype.getGroupingExpression = function (object) {
        var e_12, _a;
        var groupBy = null;
        if (core_1.Prototypes.isType(object.classID, "plot-segment")) {
            groupBy = object.groupBy;
        }
        else {
            // Find groupBy for data-driven guide
            if (core_1.Prototypes.isType(object.classID, "mark")) {
                var _loop_1 = function (glyph) {
                    if (glyph.marks.indexOf(object) >= 0) {
                        // Found the glyph
                        this_1.chartManager.enumeratePlotSegments(function (cls) {
                            if (cls.object.glyph == glyph._id) {
                                groupBy = cls.object.groupBy;
                            }
                        });
                    }
                };
                var this_1 = this;
                try {
                    for (var _b = __values(this.chart.glyphs), _c = _b.next(); !_c.done; _c = _b.next()) {
                        var glyph = _c.value;
                        _loop_1(glyph);
                    }
                }
                catch (e_12_1) { e_12 = { error: e_12_1 }; }
                finally {
                    try {
                        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                    }
                    finally { if (e_12) throw e_12.error; }
                }
            }
        }
        return groupBy;
    };
    AppStore.prototype.getLocaleFileFormat = function () {
        return this.localeFileFormat;
    };
    AppStore.prototype.setLocaleFileFormat = function (value) {
        this.localeFileFormat = value;
    };
    AppStore.prototype.checkColumnsMapping = function (column, tableType, dataset) {
        var unmappedColumns = [];
        var dataTable = dataset.tables.find(function (t) { return t.type === tableType; });
        var found = dataTable === null || dataTable === void 0 ? void 0 : dataTable.columns.find(function (c) { return c.name === column.name; });
        if (!found) {
            unmappedColumns.push(column);
        }
        return unmappedColumns;
    };
    AppStore.prototype.setProperty = function (config) {
        if (config.property === "name" &&
            this.chartManager.isNameUsed(config.value)) {
            return;
        }
        this.saveHistory();
        if (config.field == null) {
            config.object.properties[config.property] = config.value;
        }
        else {
            var obj = config.object.properties[config.property];
            config.object.properties[config.property] = core_1.setField(obj, config.field, config.value);
        }
        if (config.noUpdateState) {
            this.emit(AppStore.EVENT_GRAPHICS);
        }
        else {
            this.solveConstraintsAndUpdateGraphics(config.noComputeLayout);
        }
    };
    AppStore.EVENT_IS_NESTED_EDITOR = "is-nested-editor";
    AppStore.EVENT_NESTED_EDITOR_EDIT = "nested-editor-edit";
    AppStore.EVENT_NESTED_EDITOR_CLOSE = "nested-editor-close";
    /** Fires when the dataset changes */
    AppStore.EVENT_DATASET = "dataset";
    /** Fires when the chart state changes */
    AppStore.EVENT_GRAPHICS = "graphics";
    /** Fires when the selection changes */
    AppStore.EVENT_SELECTION = "selection";
    /** Fires when the current tool changes */
    AppStore.EVENT_CURRENT_TOOL = "current-tool";
    /** Fires when solver status changes */
    AppStore.EVENT_SOLVER_STATUS = "solver-status";
    /** Fires when the chart was saved */
    AppStore.EVENT_SAVECHART = "savechart";
    /** Fires when user clicks Edit nested chart for embedded editor */
    AppStore.EVENT_OPEN_NESTED_EDITOR = "openeditor";
    return AppStore;
}(base_1.BaseStore));
exports.AppStore = AppStore;
//# sourceMappingURL=app_store.js.map