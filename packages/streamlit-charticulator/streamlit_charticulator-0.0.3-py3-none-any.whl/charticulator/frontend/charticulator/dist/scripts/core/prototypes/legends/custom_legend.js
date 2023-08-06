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
exports.CustomLegendClass = void 0;
var categorical_legend_1 = require("./categorical_legend");
var strings_1 = require("../../../strings");
var CustomLegendClass = /** @class */ (function (_super) {
    __extends(CustomLegendClass, _super);
    function CustomLegendClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CustomLegendClass.prototype.getAttributePanelWidgets = function (manager) {
        var widget = _super.prototype.getAttributePanelWidgets.call(this, manager);
        var scale = this.getScale();
        if (scale) {
            widget.push(manager.vertical(manager.label(strings_1.strings.objects.colors, {
                addMargins: true,
                searchSection: strings_1.strings.objects.colors,
            }), manager.horizontal([1], manager.scaleEditor("mappingOptions", strings_1.strings.objects.legend.editColors))));
        }
        return widget;
    };
    CustomLegendClass.classID = "legend.custom";
    CustomLegendClass.type = "legend";
    CustomLegendClass.metadata = {
        displayName: strings_1.strings.objects.legend.legend,
        iconPath: "CharticulatorLegend",
        creatingInteraction: {
            type: "point",
            mapping: { x: "x", y: "y" },
        },
    };
    return CustomLegendClass;
}(categorical_legend_1.CategoricalLegendClass));
exports.CustomLegendClass = CustomLegendClass;
//# sourceMappingURL=custom_legend.js.map