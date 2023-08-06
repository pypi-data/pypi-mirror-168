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
var core_1 = require("../../core");
var migrator_1 = require("../../app/stores/migrator");
var utils_1 = require("./utils");
var configuration_1 = require("../configuration");
describe("Chart Solver", function () {
    // Scan for test cases
    var cases = [
        "base/" + utils_1.pathPrefix + "/bar-chart.json",
        "base/" + utils_1.pathPrefix + "/side-by-side.json",
    ];
    // Run tests
    cases.forEach(function (filename) {
        it(filename, function () { return __awaiter(void 0, void 0, void 0, function () {
            var state, manager, solvedState, expectedState;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: 
                    // The solver has to be initialized, other options can be omitted
                    return [4 /*yield*/, core_1.initialize()];
                    case 1:
                        // The solver has to be initialized, other options can be omitted
                        _a.sent();
                        return [4 /*yield*/, utils_1.loadJSON(filename)];
                    case 2:
                        state = (_a.sent()).state;
                        state = new migrator_1.Migrator().migrate(state, configuration_1.APP_VERSION);
                        manager = new core_1.Prototypes.ChartStateManager(state.chart, state.dataset, null, utils_1.makeDefaultAttributes(state));
                        manager.solveConstraints();
                        // Solve a second time to converge to higher precision
                        // This is necessary because the solver attempts to keep the current values
                        // with a weighting mechanism by adding lambda ||x-x0||^2 to the loss function.
                        // When starting from scratch, this weighting causes the solved values to bias
                        // towards the default values. This bias is in the magnitude of 0.1.
                        // A second solveConstraints call can reduce it to 1e-5.
                        manager.solveConstraints();
                        solvedState = manager.chartState;
                        expectedState = state.chartState;
                        // Test if solvedState deep equals expectedState with tolerance
                        utils_1.expect_deep_approximately_equals(solvedState, expectedState, 2);
                        return [2 /*return*/];
                }
            });
        }); });
    });
});
//# sourceMappingURL=chart-solver.js.map