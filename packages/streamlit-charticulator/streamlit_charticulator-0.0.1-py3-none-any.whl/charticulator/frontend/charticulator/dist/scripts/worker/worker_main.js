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
Object.defineProperty(exports, "__esModule", { value: true });
exports.CharticulatorWorkerProcess = void 0;
var Core = require("../core");
var communication_1 = require("./communication");
var CharticulatorWorkerProcess = /** @class */ (function (_super) {
    __extends(CharticulatorWorkerProcess, _super);
    function CharticulatorWorkerProcess() {
        var _this = _super.call(this) || this;
        _this.registerRPC("initialize", _this.initialize.bind(_this));
        _this.registerRPC("solveChartConstraints", _this.solveChartConstraints.bind(_this));
        return _this;
    }
    CharticulatorWorkerProcess.prototype.initialize = function (config) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, Core.initialize(config)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    CharticulatorWorkerProcess.prototype.solveChartConstraints = function (chart, chartState, dataset, preSolveValues, mappingOnly) {
        if (preSolveValues === void 0) { preSolveValues = null; }
        if (mappingOnly === void 0) { mappingOnly = false; }
        if (preSolveValues != null && preSolveValues.length > 0) {
            return this.doSolveChartConstraints(chart, chartState, dataset, function (solver) {
                var e_1, _a;
                try {
                    for (var preSolveValues_1 = __values(preSolveValues), preSolveValues_1_1 = preSolveValues_1.next(); !preSolveValues_1_1.done; preSolveValues_1_1 = preSolveValues_1.next()) {
                        var _b = __read(preSolveValues_1_1.value, 4), strength = _b[0], attrs = _b[1], attr = _b[2], value = _b[3];
                        solver.solver.addEqualToConstant(strength, solver.solver.attr(attrs, attr), value);
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (preSolveValues_1_1 && !preSolveValues_1_1.done && (_a = preSolveValues_1.return)) _a.call(preSolveValues_1);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
            }, mappingOnly);
        }
        return this.doSolveChartConstraints(chart, chartState, dataset, null, mappingOnly);
    };
    CharticulatorWorkerProcess.prototype.doSolveChartConstraints = function (chart, chartState, dataset, additional, mappingOnly) {
        if (additional === void 0) { additional = null; }
        if (mappingOnly === void 0) { mappingOnly = false; }
        var chartManager = new Core.Prototypes.ChartStateManager(chart, dataset, chartState);
        chartManager.solveConstraints(additional, mappingOnly);
        return chartState;
    };
    return CharticulatorWorkerProcess;
}(communication_1.WorkerHostProcess));
exports.CharticulatorWorkerProcess = CharticulatorWorkerProcess;
new CharticulatorWorkerProcess();
//# sourceMappingURL=worker_main.js.map