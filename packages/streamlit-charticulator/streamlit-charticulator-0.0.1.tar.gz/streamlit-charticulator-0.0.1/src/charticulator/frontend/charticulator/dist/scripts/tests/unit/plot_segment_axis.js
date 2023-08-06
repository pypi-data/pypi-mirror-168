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
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var chai_1 = require("chai");
var specification_1 = require("../../core/specification");
var actions_1 = require("../../app/actions/actions");
var drag_data_1 = require("../../app/actions/drag_data");
var core_1 = require("./../../core");
var mock_1 = require("./mock");
var base_1 = require("../../core/prototypes/plot_segments/region_2d/base");
describe("Plot segment", function () {
    // The directory containing test cases
    before(function () { return __awaiter(void 0, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, core_1.initialize()];
                case 1:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    }); });
    it("binding data to axis adds property", function (done) {
        var e_1, _a;
        var plotsegmentProperty = "xData";
        var appStore = mock_1.createMockStore();
        var mainTable = appStore.dataset.tables[0];
        var firstColumn = mainTable.columns[0];
        var aggregation = core_1.Expression.getDefaultAggregationFunction(firstColumn.type, specification_1.DataKind.Categorical);
        var expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(core_1.Expression.variable(firstColumn.name).toString())).toString();
        try {
            for (var _b = __values(core_1.Prototypes.forEachObject(appStore.chart)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (core_1.Prototypes.isType(item.object.classID, "plot-segment")) {
                    var plotSegment_1 = item.object;
                    appStore.dispatcher.dispatch(new actions_1.BindDataToAxis(plotSegment_1, plotsegmentProperty, null, new drag_data_1.DataExpression(mainTable, expression, firstColumn.type, firstColumn.metadata, null, null, null, null), true));
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
        var plotSegment = appStore.chart.elements[0];
        var properties = plotSegment.properties;
        var plotsegmentPropertyValue = properties[plotsegmentProperty];
        chai_1.expect(plotsegmentPropertyValue.type).to.equal(firstColumn.metadata.kind);
        chai_1.expect(plotsegmentPropertyValue.valueType).to.equal(firstColumn.type);
        chai_1.expect(plotsegmentPropertyValue.side).to.equal("default");
        chai_1.expect(plotsegmentPropertyValue.numericalMode).to.oneOf([null, undefined]);
        chai_1.expect(plotsegmentPropertyValue.rawExpression).to.equal("first(Month)");
        chai_1.expect(plotsegmentPropertyValue.expression).to.equal(expression);
        chai_1.expect(plotsegmentPropertyValue.gapRatio).to.closeTo(0.1, 0.001);
        chai_1.expect(plotsegmentPropertyValue.dataKind).to.equal(firstColumn.metadata.kind);
        chai_1.expect(plotsegmentPropertyValue.autoDomainMin).to.equal(true);
        chai_1.expect(plotsegmentPropertyValue.autoDomainMax).to.equal(true);
        chai_1.expect(plotsegmentPropertyValue.offset).to.equal(0);
        done();
    }).timeout(10000);
    it("update plotsegments doesn't change properties", function (done) {
        var e_2, _a;
        var plotsegmentProperty = "xData";
        var appStore = mock_1.createMockStore();
        var mainTable = appStore.dataset.tables[0];
        var firstColumn = mainTable.columns[0];
        var aggregation = core_1.Expression.getDefaultAggregationFunction(firstColumn.type, specification_1.DataKind.Categorical);
        var expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(core_1.Expression.variable(firstColumn.name).toString())).toString();
        try {
            for (var _b = __values(core_1.Prototypes.forEachObject(appStore.chart)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                if (core_1.Prototypes.isType(item.object.classID, "plot-segment")) {
                    var plotSegment_2 = item.object;
                    appStore.dispatcher.dispatch(new actions_1.BindDataToAxis(plotSegment_2, plotsegmentProperty, null, new drag_data_1.DataExpression(mainTable, expression, firstColumn.type, firstColumn.metadata, null, null, null, null), false));
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
        appStore.dispatcher.dispatch(new actions_1.UpdatePlotSegments());
        var plotSegment = appStore.chart.elements[0];
        var properties = plotSegment.properties;
        var plotsegmentPropertyValue = properties[plotsegmentProperty];
        chai_1.expect(plotsegmentPropertyValue.type).to.equal(firstColumn.metadata.kind);
        chai_1.expect(plotsegmentPropertyValue.valueType).to.equal(firstColumn.type);
        chai_1.expect(plotsegmentPropertyValue.side).to.equal("default");
        chai_1.expect(plotsegmentPropertyValue.rawExpression).to.equal("first(Month)");
        chai_1.expect(plotsegmentPropertyValue.numericalMode).to.oneOf([null, undefined]);
        chai_1.expect(plotsegmentPropertyValue.expression).to.equal(expression);
        chai_1.expect(plotsegmentPropertyValue.gapRatio).to.equal(0.1);
        chai_1.expect(plotsegmentPropertyValue.dataKind).to.equal(firstColumn.metadata.kind);
        chai_1.expect(plotsegmentPropertyValue.autoDomainMin).to.equal(true);
        chai_1.expect(plotsegmentPropertyValue.autoDomainMax).to.equal(true);
        done();
    }).timeout(10000);
    //categorical - categorical sub layout
    it("update plotsegments sub layout property", function (done) {
        var e_3, _a, e_4, _b;
        var plotsegmentXDataProperty = "xData";
        var plotsegmentYDataProperty = "yData";
        var appStore = mock_1.createMockStore();
        var mainTable = appStore.dataset.tables[0];
        var firstColumn = mainTable.columns[0];
        var aggregation = core_1.Expression.getDefaultAggregationFunction(firstColumn.type, specification_1.DataKind.Categorical);
        var expression = core_1.Expression.functionCall(aggregation, core_1.Expression.parse(core_1.Expression.variable(firstColumn.name).toString())).toString();
        var numericColumn = mainTable.columns.find(function (column) { return column.type == specification_1.DataType.Number; });
        var numericColumnAggregation = core_1.Expression.getDefaultAggregationFunction(numericColumn.type, specification_1.DataKind.Numerical);
        var numericColumnExpression = core_1.Expression.functionCall(numericColumnAggregation, core_1.Expression.parse(core_1.Expression.variable(numericColumn.name).toString())).toString();
        try {
            for (var _c = __values(core_1.Prototypes.forEachObject(appStore.chart)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var item = _d.value;
                if (core_1.Prototypes.isType(item.object.classID, "plot-segment")) {
                    var plotSegment_3 = item.object;
                    // X data
                    appStore.dispatcher.dispatch(new actions_1.BindDataToAxis(plotSegment_3, plotsegmentXDataProperty, null, new drag_data_1.DataExpression(mainTable, expression, firstColumn.type, firstColumn.metadata, null, null, null, null), false));
                    //yData
                    appStore.dispatcher.dispatch(new actions_1.BindDataToAxis(plotSegment_3, plotsegmentYDataProperty, null, new drag_data_1.DataExpression(mainTable, numericColumnExpression, numericColumn.type, numericColumn.metadata, null, null, null, null), false));
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_3) throw e_3.error; }
        }
        appStore.dispatcher.dispatch(new actions_1.UpdatePlotSegments());
        var plotSegment = appStore.chart.elements[0];
        var properties = plotSegment.properties;
        chai_1.expect(properties.sublayout.type).to.equal(base_1.Region2DSublayoutType.Overlap);
        try {
            //switch to categorical
            for (var _e = __values(core_1.Prototypes.forEachObject(appStore.chart)), _f = _e.next(); !_f.done; _f = _e.next()) {
                var item = _f.value;
                if (core_1.Prototypes.isType(item.object.classID, "plot-segment")) {
                    var plotSegment_4 = item.object;
                    // X data
                    appStore.dispatcher.dispatch(new actions_1.BindDataToAxis(plotSegment_4, plotsegmentYDataProperty, null, new drag_data_1.DataExpression(mainTable, expression, firstColumn.type, firstColumn.metadata, null, null, null, null), false));
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_4) throw e_4.error; }
        }
        appStore.dispatcher.dispatch(new actions_1.UpdatePlotSegments());
        chai_1.expect(properties.sublayout.type).to.equal(base_1.Region2DSublayoutType.Grid);
        done();
    }).timeout(10000);
});
//# sourceMappingURL=plot_segment_axis.js.map