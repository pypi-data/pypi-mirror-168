"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.TableView = void 0;
/**
 * See {@link DatasetView} or {@link TableView}
 * @packageDocumentation
 * @preferred
 */
var React = require("react");
var utils_1 = require("../../utils");
var react_1 = require("@fluentui/react");
/**
 * Component for displaying data samples on loading or in context menu of {@link DatasetView}
 *
 * ![Table view](media://table_view.png)
 *
 * ![Table view](media://table_view_leftside.png)
 */
var TableView = /** @class */ (function (_super) {
    __extends(TableView, _super);
    function TableView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TableView.prototype.render = function () {
        var _this = this;
        var table = this.props.table;
        var onTypeChange = this.props.onTypeChange;
        var maxRows = table.rows.length;
        if (this.props.maxRows != null) {
            if (maxRows > this.props.maxRows) {
                maxRows = this.props.maxRows;
            }
        }
        return (React.createElement("table", { className: "charticulator__dataset-table-view" },
            React.createElement("thead", null,
                React.createElement("tr", null, table.columns
                    .filter(function (c) { return !c.metadata.isRaw; })
                    .map(function (c) { return (React.createElement("th", { key: c.name }, c.name)); }))),
            React.createElement("tbody", null,
                onTypeChange && (React.createElement("tr", { key: -1 }, table.columns
                    .filter(function (c) { return !c.metadata.isRaw; })
                    .map(function (c, index) {
                    var convertableTypes = utils_1.getConvertableTypes(c.type, table.rows.slice(0, 10).map(function (row) { return row[c.name]; }));
                    return (React.createElement("td", { key: c.name + "-" + index }, React.createElement(react_1.Dropdown, { onChange: function (ev, newType) {
                            onTypeChange(c.name, newType.key);
                            _this.forceUpdate();
                        }, styles: {
                            title: {
                                borderWidth: "0px",
                            },
                        }, selectedKey: c.type, options: convertableTypes.map(function (type) {
                            var str = type.toString();
                            return {
                                key: type,
                                text: str[0].toUpperCase() + str.slice(1),
                            };
                        }) })));
                }))),
                table.rows.slice(0, maxRows).map(function (r) { return (React.createElement("tr", { key: r._id }, table.columns
                    .filter(function (c) { return !c.metadata.isRaw; })
                    .map(function (c, index) {
                    if (c.metadata.rawColumnName) {
                        return (React.createElement("td", { key: c.name + "-" + index }, r[c.metadata.rawColumnName] != null &&
                            r[c.metadata.rawColumnName].toString()));
                    }
                    else {
                        return (React.createElement("td", { key: c.name + "-" + index }, r[c.name] != null && r[c.name].toString()));
                    }
                }))); }),
                table.rows.length > maxRows ? (React.createElement("tr", null, table.columns
                    .filter(function (c) { return !c.metadata.isRaw; })
                    .map(function (c, i) {
                    return i == 0 ? (React.createElement("td", { key: i },
                        "(",
                        table.rows.length - maxRows,
                        " more rows)")) : (React.createElement("td", { key: i }, "..."));
                }))) : null)));
    };
    return TableView;
}(React.Component));
exports.TableView = TableView;
//# sourceMappingURL=table_view.js.map