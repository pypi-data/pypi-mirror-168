"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
Object.defineProperty(exports, "__esModule", { value: true });
var FileSaver = require("file-saver");
var file_saver_1 = require("file-saver");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var utils_1 = require("../../utils");
var app_store_1 = require("../app_store");
var migrator_1 = require("../migrator");
var config_1 = require("../../config");
var template_1 = require("../../template");
var application_1 = require("../../application");
/** Handlers for document-level actions such as Load, Save, Import, Export, Undo/Redo, Reset */
// eslint-disable-next-line
function default_1(REG) {
    // eslint-disable-next-line
    REG.add(actions_1.Actions.Export, function (action) {
        var _this = this;
        (function () { return __awaiter(_this, void 0, void 0, function () {
            var svg, blob, svgDataURL, _a, _b, containerScriptText, template, htmlString, blob;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (!(action.type == "svg")) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.renderLocalSVG()];
                    case 1:
                        svg = _c.sent();
                        blob = new Blob([svg], { type: "image/svg;charset=utf-8" });
                        file_saver_1.saveAs(blob, "charticulator.svg", true);
                        _c.label = 2;
                    case 2:
                        if (!(action.type == "png" || action.type == "jpeg")) return [3 /*break*/, 4];
                        _a = utils_1.stringToDataURL;
                        _b = ["image/svg+xml"];
                        return [4 /*yield*/, this.renderLocalSVG()];
                    case 3:
                        svgDataURL = _a.apply(void 0, _b.concat([_c.sent()]));
                        utils_1.renderDataURLToPNG(svgDataURL, {
                            mode: "scale",
                            scale: action.options.scale || 2,
                            background: "#ffffff",
                        }).then(function (png) {
                            png.toBlob(function (blob) {
                                file_saver_1.saveAs(blob, "charticulator." + (action.type == "png" ? "png" : "jpg"), true);
                            }, "image/" + action.type);
                        });
                        _c.label = 4;
                    case 4:
                        if (!(action.type == "html")) return [3 /*break*/, 7];
                        return [4 /*yield*/, fetch(config_1.getConfig().ContainerURL)];
                    case 5: return [4 /*yield*/, (_c.sent()).text()];
                    case 6:
                        containerScriptText = _c.sent();
                        template = core_1.deepClone(this.buildChartTemplate());
                        htmlString = "\n          <!DOCTYPE html>\n          <html>\n          <head>\n            <meta charset=\"utf-8\" />\n            <title>Charticulator HTML Export</title>\n            <script type=\"text/javascript\">" + containerScriptText + "</script>\n            <style type=\"text/css\">\n              #container {\n                display: block;\n                position: absolute;\n                left: 0; right: 0; top: 0; bottom: 0;\n              }\n            </style>\n          </head>\n          <body>\n            <div id=\"container\"></div>\n            <script type=\"text/javascript\">\n              CharticulatorContainer.initialize().then(function() {\n                const currentChart = " + JSON.stringify(this.chart) + ";\n                const chartState = " + JSON.stringify(this.chartState) + ";\n                const dataset = " + JSON.stringify(this.dataset) + ";\n                const template = " + JSON.stringify(template) + ";\n                const chartTemplate = new CharticulatorContainer.ChartTemplate(\n                  template\n                );\n                chartTemplate.reset();\n\n                const defaultTable = dataset.tables[0];\n                const columns = defaultTable.columns;\n                chartTemplate.assignTable(defaultTable.name, defaultTable.name);\n                for (const column of columns) {\n                  chartTemplate.assignColumn(\n                    defaultTable.name,\n                    column.name,\n                    column.name\n                  );\n                }\n\n                // links table\n                const linksTable = dataset.tables[1];\n                const links = linksTable && (linksTable.columns);\n                if (links) {\n                  chartTemplate.assignTable(linksTable.name, linksTable.name);\n                  for (const column of links) {\n                    chartTemplate.assignColumn(\n                      linksTable.name,\n                      column.name,\n                      column.name\n                    );\n                  }\n                }\n                const instance = chartTemplate.instantiate(dataset);\n\n                const { chart } = instance;\n\n                for (const property of template.properties) {\n                  if (property.target.attribute) {\n                    CharticulatorContainer.ChartTemplate.SetChartAttributeMapping(\n                      chart,\n                      property.objectID,\n                      property.target.attribute,\n                      {\n                        type: \"value\",\n                        value: property.default,\n                      }\n                    );\n                  }\n                  \n                }\n\n                const container = new CharticulatorContainer.ChartContainer({ chart: chart }, dataset);\n                const width = document.getElementById(\"container\").getBoundingClientRect().width;\n                const height = document.getElementById(\"container\").getBoundingClientRect().height;\n                container.mount(\"container\", width, height);\n                window.addEventListener(\"resize\", function() {\n                  container.resize(\n                    document.getElementById(\"container\").getBoundingClientRect().width,\n                    document.getElementById(\"container\").getBoundingClientRect().height\n                  );\n                });\n              });\n            </script>\n          </body>\n          </html>\n        ";
                        blob = new Blob([htmlString]);
                        file_saver_1.saveAs(blob, "charticulator.html", true);
                        _c.label = 7;
                    case 7: return [2 /*return*/];
                }
            });
        }); })();
    });
    REG.add(actions_1.Actions.ExportTemplate, function (action) {
        action.target.generate(action.properties).then(function (base64) {
            var byteCharacters = atob(base64);
            var byteNumbers = new Array(byteCharacters.length);
            for (var i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            var byteArray = new Uint8Array(byteNumbers);
            var blob = new Blob([byteArray], {
                type: "application/x-binary",
            });
            FileSaver.saveAs(blob, action.target.getFileName
                ? action.target.getFileName(action.properties)
                : "charticulator." + action.target.getFileExtension(action.properties));
        });
    });
    REG.add(actions_1.Actions.Save, function (action) {
        this.backendSaveChart()
            .then(function () {
            if (action.onFinish) {
                action.onFinish();
            }
        })
            .catch(function (error) {
            if (action.onFinish) {
                action.onFinish(error);
            }
        });
    });
    REG.add(actions_1.Actions.SaveAs, function (action) {
        this.backendSaveChartAs(action.saveAs)
            .then(function () {
            if (action.onFinish) {
                action.onFinish();
            }
        })
            .catch(function (error) {
            if (action.onFinish) {
                action.onFinish(error);
            }
        });
    });
    REG.add(actions_1.Actions.Open, function (action) {
        this.backendOpenChart(action.id)
            .then(function () {
            if (action.onFinish) {
                action.onFinish();
            }
        })
            .catch(function (error) {
            if (action.onFinish) {
                action.onFinish(error);
            }
        });
    });
    REG.add(actions_1.Actions.Load, function (action) {
        this.historyManager.clear();
        var state = new migrator_1.Migrator().migrate(action.projectData, CHARTICULATOR_PACKAGE.version);
        this.loadState(state);
    });
    REG.add(actions_1.Actions.ImportDataset, function (action) {
        this.currentChartID = null;
        this.dataset = action.dataset;
        this.originDataset = core_1.deepClone(this.dataset);
        this.historyManager.clear();
        this.newChartEmpty();
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.ImportChartAndDataset, function (action) {
        var _this = this;
        this.currentChartID = null;
        this.currentSelection = null;
        this.dataset = action.dataset;
        this.originDataset = core_1.deepClone(this.dataset);
        this.chart = action.specification;
        this.chartManager = new core_1.Prototypes.ChartStateManager(this.chart, this.dataset, null, {}, {}, action.originSpecification
            ? core_1.deepClone(action.originSpecification)
            : this.chartManager.getOriginChart());
        this.chartManager.onUpdate(function () {
            _this.solveConstraintsAndUpdateGraphics();
        });
        this.chartState = this.chartManager.chartState;
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.UpdatePlotSegments, function () {
        this.updatePlotSegments();
        this.solveConstraintsAndUpdateGraphics();
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
    });
    REG.add(actions_1.Actions.UpdateDataAxis, function () {
        this.updateDataAxes();
        this.updateScales();
        this.solveConstraintsAndUpdateGraphics();
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
    });
    REG.add(actions_1.Actions.ReplaceDataset, function (action) {
        var _this = this;
        this.currentChartID = null;
        this.currentSelection = null;
        this.dataset = action.dataset;
        this.originDataset = core_1.deepClone(this.dataset);
        this.chartManager = new core_1.Prototypes.ChartStateManager(this.chart, this.dataset, null, {}, {}, action.keepState ? this.chartManager.getOriginChart() : null);
        this.chartManager.onUpdate(function () {
            _this.solveConstraintsAndUpdateGraphics();
        });
        this.chartState = this.chartManager.chartState;
        this.updatePlotSegments();
        this.updateDataAxes();
        this.updateScales();
        this.solveConstraintsAndUpdateGraphics();
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
    });
    REG.add(actions_1.Actions.ConvertColumnDataType, function (action) {
        this.saveHistory();
        var table = this.dataset.tables.find(function (table) { return table.name === action.tableName; });
        if (!table) {
            return;
        }
        var column = table.columns.find(function (column) { return column.name === action.column; });
        if (!column) {
            return;
        }
        var originTable = this.originDataset.tables.find(function (table) { return table.name === action.tableName; });
        var originColumn = originTable.columns.find(function (column) { return column.name === action.column; });
        if (originColumn.metadata.rawColumnName) {
            originColumn = originTable.columns.find(function (column) { return column.name === originColumn.metadata.rawColumnName; });
        }
        var result = utils_1.convertColumns(table, column, originTable, action.type);
        if (result) {
            this.messageState.set("columnConvertError", result);
        }
        this.updatePlotSegments();
        this.updateDataAxes();
        this.updateScales();
        this.solveConstraintsAndUpdateGraphics();
        this.emit(app_store_1.AppStore.EVENT_DATASET);
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
    });
    REG.add(actions_1.Actions.Undo, function () {
        var state = this.historyManager.undo(this.saveDecoupledState());
        if (state) {
            var ss = this.saveSelectionState();
            this.loadState(state);
            this.loadSelectionState(ss);
        }
    });
    REG.add(actions_1.Actions.Redo, function () {
        var state = this.historyManager.redo(this.saveDecoupledState());
        if (state) {
            var ss = this.saveSelectionState();
            this.loadState(state);
            this.loadSelectionState(ss);
        }
    });
    REG.add(actions_1.Actions.Reset, function () {
        this.saveHistory();
        this.currentSelection = null;
        this.currentTool = null;
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
        this.emit(app_store_1.AppStore.EVENT_CURRENT_TOOL);
        this.newChartEmpty();
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.OpenNestedEditor, function (_a) {
        var _this = this;
        var options = _a.options, object = _a.object, property = _a.property;
        this.emit(app_store_1.AppStore.EVENT_OPEN_NESTED_EDITOR, options, object, property);
        var editorID = core_1.uniqueID();
        var newWindow = window.open("index.html#!nestedEditor=" + editorID, "nested_chart_" + options.specification._id);
        var listener = function (e) {
            if (e.origin == document.location.origin) {
                var data = e.data;
                if (data.id == editorID) {
                    switch (data.type) {
                        case "initialized" /* Initialized */:
                            {
                                var builder = new template_1.ChartTemplateBuilder(options.specification, options.dataset, _this.chartManager, CHARTICULATOR_PACKAGE.version);
                                var template = builder.build();
                                newWindow.postMessage({
                                    id: editorID,
                                    type: application_1.NestedEditorEventType.Load,
                                    specification: options.specification,
                                    dataset: options.dataset,
                                    width: options.width,
                                    template: template,
                                    height: options.height,
                                    filterCondition: options.filterCondition,
                                }, document.location.origin);
                            }
                            break;
                        case "save" /* Save */:
                            {
                                _this.setProperty({
                                    object: object,
                                    property: property.property,
                                    field: property.field,
                                    value: data.specification,
                                    noUpdateState: property.noUpdateState,
                                    noComputeLayout: property.noComputeLayout,
                                });
                            }
                            break;
                    }
                }
            }
        };
        window.addEventListener("message", listener);
    });
    REG.add(actions_1.Actions.SearchUpdated, function (action) {
        this.searchString = action.searchString;
        this.emit(app_store_1.AppStore.EVENT_GRAPHICS);
    });
    REG.add(actions_1.Actions.ExpandOrCollapsePanelsUpdated, function (action) {
        this.collapseOrExpandPanelsType = action.type;
        this.emit(app_store_1.AppStore.EVENT_GRAPHICS);
    });
}
exports.default = default_1;
//# sourceMappingURL=document.js.map