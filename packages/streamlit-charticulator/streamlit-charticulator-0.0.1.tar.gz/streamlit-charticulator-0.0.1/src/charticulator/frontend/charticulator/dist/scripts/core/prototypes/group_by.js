"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CompiledGroupBy = void 0;
var common_1 = require("../common");
var CompiledGroupBy = /** @class */ (function () {
    function CompiledGroupBy(groupBy, cache) {
        if (groupBy.expression) {
            var expr_1 = cache.parse(groupBy.expression);
            this.groupBy = function (table) {
                var indices = common_1.makeRange(0, table.rows.length);
                var groups = common_1.gather(indices, function (i) {
                    return expr_1.getStringValue(table.getRowContext(i));
                });
                return groups;
            };
        }
    }
    return CompiledGroupBy;
}());
exports.CompiledGroupBy = CompiledGroupBy;
//# sourceMappingURL=group_by.js.map