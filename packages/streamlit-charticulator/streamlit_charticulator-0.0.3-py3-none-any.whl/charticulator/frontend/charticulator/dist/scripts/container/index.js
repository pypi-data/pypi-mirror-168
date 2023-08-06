"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !exports.hasOwnProperty(p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Chart container module responsible to draw chart on the DOM.
 *
 * {@link ChartComponent} responsible to draw the chart on the DOM. The method {@link renderGraphicalElementSVG} uses it to render the main element of the chart
 *
 * {@link ChartContainer} uses to draw the chart outside of charticulator editor. This class uses {@link ChartComponent} inside for rendering the chart.
 * It's main part of Power BI extension and export as HTML (See {@link "app/actions/actions".Export} for details about export to HTML)
 *
 * {@link "container/chart_template".ChartTemplate} describes the chart itself. Responsible to instantiate the template on loading (in editor, in container of Power BI Visual or in HTML)
 * The interface {@link "core/specification/template".ChartTemplate} describes main parts of template structure.
 *
 * @packageDocumentation
 * @preferred
 */
var chart_component_1 = require("./chart_component");
Object.defineProperty(exports, "ChartComponent", { enumerable: true, get: function () { return chart_component_1.ChartComponent; } });
var chart_template_1 = require("./chart_template");
Object.defineProperty(exports, "ChartTemplate", { enumerable: true, get: function () { return chart_template_1.ChartTemplate; } });
var container_1 = require("./container");
Object.defineProperty(exports, "ChartContainer", { enumerable: true, get: function () { return container_1.ChartContainer; } });
__exportStar(require("../core"), exports);
//# sourceMappingURL=index.js.map