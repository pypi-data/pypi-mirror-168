"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CompiledFilter = void 0;
var CompiledFilter = /** @class */ (function () {
    function CompiledFilter(filter, cache) {
        if (filter.categories) {
            var expr_1 = cache.parse(filter.categories.expression);
            var map_1 = filter.categories.values;
            this.filter = function (context) {
                var val = expr_1.getStringValue(context);
                return (Object.prototype.hasOwnProperty.call(map_1, val) && map_1[val] == true);
            };
        }
        else if (filter.expression) {
            var expr_2 = cache.parse(filter.expression);
            this.filter = function (context) {
                return expr_2.getValue(context);
            };
        }
    }
    return CompiledFilter;
}());
exports.CompiledFilter = CompiledFilter;
//# sourceMappingURL=filter.js.map