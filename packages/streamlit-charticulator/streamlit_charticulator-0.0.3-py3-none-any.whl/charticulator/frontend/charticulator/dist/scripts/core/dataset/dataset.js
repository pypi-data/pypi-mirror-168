"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.rawColumnPostFix = exports.tableTypeName = exports.TableType = exports.DataKind = exports.DataType = void 0;
var strings_1 = require("../../strings");
var specification_1 = require("../specification");
Object.defineProperty(exports, "DataType", { enumerable: true, get: function () { return specification_1.DataType; } });
Object.defineProperty(exports, "DataKind", { enumerable: true, get: function () { return specification_1.DataKind; } });
var TableType;
(function (TableType) {
    /** The main table with data for the chart */
    TableType["Main"] = "Main";
    /** Table with source_id and target_id columns for links, can contain additional columns with data */
    TableType["Links"] = "Links";
    /** TelLs to nested chart that table is parent chart table with all data */
    TableType["ParentMain"] = "ParentMain";
    /** TelLs to nested chart that table is parent links table of the chart with all data */
    TableType["ParentLinks"] = "ParentLinks";
    /** The main table with data for images */
    TableType["Image"] = "Image";
})(TableType = exports.TableType || (exports.TableType = {}));
exports.tableTypeName = (_a = {},
    _a[TableType.Main] = strings_1.strings.dataset.tableTitleColumns,
    _a[TableType.Links] = strings_1.strings.dataset.tableTitleLinks,
    _a[TableType.Image] = strings_1.strings.dataset.tableTitleImages,
    _a[TableType.ParentLinks] = "",
    _a[TableType.ParentMain] = "",
    _a);
exports.rawColumnPostFix = "_raw";
//# sourceMappingURL=dataset.js.map