"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createMockStore = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var stores_1 = require("./../../app/stores");
var core_1 = require("./../../core");
var default_dataset_1 = require("../../app/default_dataset");
function createMockStore() {
    var store = new stores_1.AppStore({
        solveChartConstraints: function (chart, chartState, dataset, preSolveValues, mappingOnly) {
            return new Promise(function (resolve) {
                var manager = new core_1.Prototypes.ChartStateManager(chart, dataset, null, {});
                manager.setState(chartState);
                manager.solveConstraints(null, mappingOnly);
                resolve(manager.chartState);
            });
        },
    }, default_dataset_1.makeDefaultDataset());
    store.saveHistory = function () { };
    return store;
}
exports.createMockStore = createMockStore;
//# sourceMappingURL=mock.js.map