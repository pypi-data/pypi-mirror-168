"use strict";
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
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var chai_1 = require("chai");
var index_1 = require("../../app/index");
var index_2 = require("../../app/index");
var specification_1 = require("../../core/specification");
var types_1 = require("../../core/specification/types");
var strings_1 = require("../../strings");
var utils_1 = require("./utils");
var app_1 = require("../../app");
var core_1 = require("../../core");
var serializer_1 = require("./serializer");
var utils_2 = require("../unit/utils");
var config = require("../../../config.test.yml");
var workerBundle = require("raw-loader?esModule=false!../../../dist/scripts/worker.bundle.js");
describe("Charticulator", function () {
    chai_1.use(serializer_1.matchSnapshot);
    var application = null;
    // The directory containing test cases
    before(function (done) {
        viewport.set(1920, 977);
        this.timeout(utils_1.mediumTimeOut);
        var blob = new Blob([workerBundle], { type: "application/javascript" });
        var workerScript = URL.createObjectURL(blob);
        var container = document.createElement("div");
        container.id = "container";
        document.querySelector("body").appendChild(container);
        application = new index_1.Application();
        application
            .initialize(config, "container", {
            workerScriptContent: workerScript,
        }, {
            currency: "$",
            thousandsDelimiter: ",",
            decemalDelimiter: ".",
        }, true)
            .then(function () {
            utils_1.closeStartMenuPanel();
            done();
        });
    });
    it("application is defined", function (done) {
        var isDone = chai_1.expect(application).to.not.null &&
            chai_1.expect(application.appStore).to.not.null;
        done();
    }).timeout(utils_1.longTimeOut);
    xit("binds data to X axis", function () { return __awaiter(void 0, void 0, void 0, function () {
        var store, plotSegments;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    store = application.appStore;
                    plotSegments = __spread(utils_1.findElementsByClassID(store.chart, "plot-segment"));
                    plotSegments.forEach(function (ps) {
                        var column = store.dataset.tables[0].columns[0];
                        var aggregation = core_1.Expression.getDefaultAggregationFunction(column.type, specification_1.DataKind.Categorical);
                        var expression = core_1.Expression.functionCall(aggregation, core_1.Expression.variable(column.name)).toString();
                        new index_2.Actions.BindDataToAxis(ps.object, "xData", null, new app_1.DragData.DataExpression(store.dataset.tables[0], expression, specification_1.DataType.String, {
                            kind: specification_1.DataKind.Categorical,
                            orderMode: types_1.OrderMode.order,
                            order: strings_1.strings.dataset.months,
                        }, expression), false).dispatch(store.dispatcher);
                    });
                    // wait the solver
                    return [4 /*yield*/, utils_2.waitSolver()];
                case 1:
                    // wait the solver
                    _a.sent();
                    chai_1.expect(utils_1.getChartCanvas()).to.matchSnapshot();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    it("open mushrooms chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/mushrooms.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    it("open bump_chart chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/bump_chart.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    it("open bubble_chart chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/bubble_chart.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    xit("open 200_Mushrooms chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/200_Mushrooms.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    xit("open World_Population_2017 chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/World_Population_2017.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // test checks that charticulator opens saved chart correctly
    it("open nightingale chart", function () { return __awaiter(void 0, void 0, void 0, function () {
        var chartFilePath, _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    chartFilePath = "base/" + utils_1.pathPrefix + "/nightingale.chart";
                    _a = testOpenChart;
                    _b = [application];
                    return [4 /*yield*/, utils_2.loadJSON(chartFilePath)];
                case 1: return [4 /*yield*/, _a.apply(void 0, _b.concat([_c.sent()]))];
                case 2:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    xit("creates column names legend", function () { return __awaiter(void 0, void 0, void 0, function () {
        var panel, dataColumnsSelector, columns;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, utils_1.clickOnButtonByTitle("Legend")];
                case 1:
                    _a.sent();
                    panel = utils_1.getLinkTypePanel();
                    //panel is active
                    chai_1.expect(panel).to.not.null;
                    // switch legend type to "column names"
                    return [4 /*yield*/, utils_1.clickOnButtonByTitle("Column names")];
                case 2:
                    // switch legend type to "column names"
                    _a.sent();
                    dataColumnsSelector = panel.querySelector(".charticulator__data-field-selector");
                    columns = dataColumnsSelector.querySelectorAll("span.el-text");
                    // select all coulmns
                    columns.forEach(function (column) { return column.click(); });
                    //click to create legend button
                    return [4 /*yield*/, utils_1.clickOnButtonByTitle("Create Legend")];
                case 3:
                    //click to create legend button
                    _a.sent();
                    return [4 /*yield*/, utils_2.waitSolver()];
                case 4:
                    _a.sent();
                    chai_1.expect(utils_1.getChartCanvas()).to.matchSnapshot();
                    return [2 /*return*/];
            }
        });
    }); }).timeout(utils_1.longTimeOut);
    // it("import default template", async () => {
    //   const chartFilePath = `base/${pathPrefix}/default.chart`;
    //   await testOpenChart(application, await loadJSON(chartFilePath));
    //
    //   const templateFilePath = `base/${pathPrefix}/default.tmplt`;
    //   await testImport(
    //     application.appStore,
    //     await loadJSON(templateFilePath),
    //     application.appStore.dataset
    //   );
    // }).timeout(longTimeOut);
});
// .timeout(longTimeOut);
function testOpenChart(application, chartFile) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    application.appStore.dispatcher.dispatch(new index_2.Actions.Load(chartFile.state));
                    return [4 /*yield*/, utils_2.waitSolver()];
                case 1:
                    _a.sent();
                    chai_1.expect(utils_1.getChartCanvas()).to.matchSnapshot();
                    return [2 /*return*/];
            }
        });
    });
}
function testImport(store, templateFile, dataset) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    store.dispatcher.dispatch(new index_2.Actions.ImportChartAndDataset(templateFile.specification, dataset, {}));
                    return [4 /*yield*/, utils_2.waitSolver()];
                case 1:
                    _a.sent();
                    chai_1.expect(utils_1.getChartCanvas()).to.matchSnapshot();
                    return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=application_ui.test.js.map