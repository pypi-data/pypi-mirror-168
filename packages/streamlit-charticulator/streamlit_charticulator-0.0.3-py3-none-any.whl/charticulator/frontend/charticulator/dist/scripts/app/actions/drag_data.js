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
Object.defineProperty(exports, "__esModule", { value: true });
exports.DataExpression = exports.DropZoneData = exports.ScaffoldType = exports.ObjectType = void 0;
var ObjectType = /** @class */ (function () {
    function ObjectType(classID, options) {
        if (options === void 0) { options = null; }
        this.classID = classID;
        this.options = options;
    }
    return ObjectType;
}());
exports.ObjectType = ObjectType;
var ScaffoldType = /** @class */ (function () {
    function ScaffoldType(type) {
        this.type = type;
    }
    return ScaffoldType;
}());
exports.ScaffoldType = ScaffoldType;
var DropZoneData = /** @class */ (function () {
    function DropZoneData() {
    }
    return DropZoneData;
}());
exports.DropZoneData = DropZoneData;
var DataExpression = /** @class */ (function (_super) {
    __extends(DataExpression, _super);
    function DataExpression(table, expression, valueType, metadata, rawColumnExpression, scaleID, allowSelectValue, type) {
        if (metadata === void 0) { metadata = null; }
        var _this = _super.call(this) || this;
        _this.table = table;
        _this.expression = expression;
        _this.valueType = valueType;
        _this.metadata = metadata;
        _this.rawColumnExpression = rawColumnExpression;
        _this.scaleID = scaleID;
        _this.allowSelectValue = allowSelectValue;
        _this.type = type;
        return _this;
    }
    return DataExpression;
}(DropZoneData));
exports.DataExpression = DataExpression;
//# sourceMappingURL=drag_data.js.map