"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.getSortedCategories = exports.updateWidgetCategoriesByExpression = exports.transformDataToCategoryItemsWithIds = exports.getOnConfirmFunction = exports.transformOnResetCategories = exports.JoinSymbol = exports.shouldShowTickFormatForTickExpression = exports.transformOrderByExpression = exports.parseDerivedColumnsExpression = exports.getColumnNameByExpression = exports.getColumnByExpression = exports.getTableColumns = void 0;
var common_1 = require("../../common");
var index_1 = require("../../index");
var types_1 = require("../../../core/specification/types");
var specification_1 = require("../../../core/specification");
var expression_1 = require("../../../core/expression");
function getTableColumns(manager) {
    var store = manager.store;
    var storeTable = store.getTables()[0];
    return common_1.deepClone(storeTable.columns);
}
exports.getTableColumns = getTableColumns;
function getColumnByExpression(manager, expression) {
    var store = manager.store;
    var storeTable = store.getTables()[0];
    var parsed = index_1.Expression.parse(expression);
    var expression1;
    // console.log(parsed);
    if (parsed instanceof index_1.Expression.FunctionCall) {
        expression1 = parsed.args[0].toString();
        // expression1 = expression?.split("`").join("");
        //need to provide date.year() etc.
        // expression1 = this.parseDerivedColumnsExpression(expression);
    }
    var currentColumn = common_1.deepClone(storeTable.columns).filter(function (column) { return column.displayName === expression1; });
    return currentColumn;
}
exports.getColumnByExpression = getColumnByExpression;
function getColumnNameByExpression(expression) {
    var columnName;
    var parsed = index_1.Expression.parse(expression);
    if (parsed instanceof index_1.Expression.FunctionCall) {
        columnName = parsed.args[0].toString();
    }
    return columnName;
}
exports.getColumnNameByExpression = getColumnNameByExpression;
function parseDerivedColumnsExpression(expression) {
    var DATE_DERIVED_PREDIX = "date.";
    if (expression.startsWith(DATE_DERIVED_PREDIX)) {
        //data.year(DATE) -> DATE
        return expression.match(/\(([^)]+)\)/)[1];
    }
    return expression;
}
exports.parseDerivedColumnsExpression = parseDerivedColumnsExpression;
function transformOrderByExpression(expression) {
    if ((expression.indexOf("`") < 0 && expression.split(" ").length >= 2) ||
        expression_1.Variable.isNonEnglishVariableName(expression)) {
        return expression_1.Variable.VariableNameToString(expression);
    }
    else {
        return expression;
    }
}
exports.transformOrderByExpression = transformOrderByExpression;
function shouldShowTickFormatForTickExpression(data, manager) {
    var showInputFormat = true;
    try {
        //check tick data type
        if (data.tickDataExpression) {
            var extendedManager = manager;
            var chartManager = extendedManager.store.chartManager;
            var table = chartManager.getTable(extendedManager.store.getTables()[0].name);
            var tickDataExpression = chartManager.dataflow.cache.parse(data.tickDataExpression);
            var c = table.getRowContext(0);
            var tickData = tickDataExpression.getValue(c);
            //if string -> hide input format
            if (typeof tickData === "string") {
                showInputFormat = false;
            }
        }
    }
    catch (ex) {
        console.log(ex);
        showInputFormat = true;
    }
    return showInputFormat;
}
exports.shouldShowTickFormatForTickExpression = shouldShowTickFormatForTickExpression;
function isNumbers(array) {
    return typeof array[0] === "number";
}
function numbersSortFunction(a, b) {
    return a - b;
}
exports.JoinSymbol = ", ";
function getStingValueFromCategoryItemsWithIds(itemWithId) {
    var item = itemWithId[0];
    if (isNumbers(item)) {
        if (Array.isArray(item)) {
            return item.sort(numbersSortFunction).join(exports.JoinSymbol);
        }
        else {
            return item;
        }
    }
    else {
        if (Array.isArray(item)) {
            return item.sort().join(exports.JoinSymbol);
        }
        else {
            return item;
        }
    }
}
/**
 * Transform data to sting array
 * [
 * [[data], id],
 * [....]
 * ]
 * @param itemsWithIds
 * @return unique string array
 */
function transformOnResetCategories(itemsWithIds) {
    var data = itemsWithIds.map(function (itemWithId) {
        return getStingValueFromCategoryItemsWithIds(itemWithId);
    });
    var uniqueValues = new Set(data);
    return __spread(uniqueValues);
}
exports.transformOnResetCategories = transformOnResetCategories;
function getOnConfirmFunction(datasetAxisData, items, itemsWithIds, data) {
    try {
        var newDataOrder = __spread(datasetAxisData);
        var new_order = [];
        var _loop_1 = function (i) {
            var idxForItem = [];
            for (var j = 0; j < itemsWithIds.length; j++) {
                var item = itemsWithIds[j];
                var stringSortedValue = getStingValueFromCategoryItemsWithIds(item);
                if (stringSortedValue === items[i]) {
                    idxForItem.push(item[1]);
                }
            }
            var _loop_2 = function (j) {
                var foundItem = newDataOrder.find(function (item) { return item[1] === idxForItem[j]; });
                new_order.push(foundItem);
            };
            for (var j = 0; j < idxForItem.length; j++) {
                _loop_2(j);
            }
        };
        for (var i = 0; i < items.length; i++) {
            _loop_1(i);
        }
        var getItem_1 = function (item) {
            if (data.valueType == specification_1.DataType.Number) {
                return "" + item;
            }
            return item;
        };
        data.order = new_order.map(function (item) { return getItem_1(item[0]); });
        data.orderMode = types_1.OrderMode.order;
        data.categories = new_order.map(function (item) { return getItem_1(item[0]); });
    }
    catch (e) {
        console.log(e);
    }
}
exports.getOnConfirmFunction = getOnConfirmFunction;
function transformDataToCategoryItemsWithIds(data) {
    return data.map(function (item, idx) { return [item, idx]; });
}
exports.transformDataToCategoryItemsWithIds = transformDataToCategoryItemsWithIds;
function updateWidgetCategoriesByExpression(widgetData) {
    var newWidgetData = [];
    var transformedWidgetData = transformDataToCategoryItemsWithIds(widgetData);
    transformedWidgetData.map(function (item) {
        var stringValueForItem = getStingValueFromCategoryItemsWithIds(item);
        newWidgetData.push(stringValueForItem);
    });
    return newWidgetData;
}
exports.updateWidgetCategoriesByExpression = updateWidgetCategoriesByExpression;
function getSortedCategories(itemsWithIds) {
    var sortedData;
    if (itemsWithIds[0] && isNumbers(itemsWithIds[0][0])) {
        sortedData = transformOnResetCategories(itemsWithIds.sort(function (firstItem, secondItem) {
            if (isNumbers(firstItem[0]) && isNumbers(secondItem[0])) {
                return firstItem[0][0] - secondItem[0][0];
            }
            return 0;
        }));
    }
    else {
        sortedData = transformOnResetCategories(itemsWithIds).sort();
    }
    return sortedData;
}
exports.getSortedCategories = getSortedCategories;
//# sourceMappingURL=utils.js.map