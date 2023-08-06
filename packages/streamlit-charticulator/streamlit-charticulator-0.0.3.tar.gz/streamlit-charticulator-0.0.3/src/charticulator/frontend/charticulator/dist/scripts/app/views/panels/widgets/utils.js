"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDropzoneAcceptTables = void 0;
var dataset_1 = require("../../../../core/dataset");
function getDropzoneAcceptTables(manager, acceptLinksTable) {
    var acceptTables = [];
    try {
        var tables = manager.store.getTables();
        if (acceptLinksTable) {
            var linksTables = filterTablesByType(tables, [
                dataset_1.TableType.Links,
                dataset_1.TableType.ParentLinks,
            ]);
            acceptTables = transformTablesToAcceptTables(linksTables);
        }
        else {
            var mainTables = filterTablesByType(tables, [
                dataset_1.TableType.Main,
                dataset_1.TableType.Image,
                dataset_1.TableType.ParentMain,
            ]);
            acceptTables = transformTablesToAcceptTables(mainTables);
        }
        return acceptTables;
    }
    catch (ex) {
        console.log(ex);
    }
    return acceptTables;
}
exports.getDropzoneAcceptTables = getDropzoneAcceptTables;
function filterTablesByType(tables, types) {
    return tables.filter(function (table) { return types.includes(table.type); });
}
function transformTablesToAcceptTables(tables) {
    return tables.map(function (table) { return table.name; });
}
//# sourceMappingURL=utils.js.map