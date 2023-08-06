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
exports.Dataflow = exports.Legends = exports.Guides = exports.Links = exports.PlotSegments = exports.Charts = exports.Glyphs = exports.Constraints = exports.Scales = exports.Marks = void 0;
/**
 * Module contains basic elements of charts:
 *
 * * Marks elements {@link "core/prototypes/marks/index"} are "bricks" of charticulator. Module contains descriptions of rectangle, image, symbol, text, e.t.c
 *
 * * Plot segments  {@link "core/prototypes/plot_segments/index"} container of glyphs to arrange them on the chart
 *
 * * Chart {@link "core/prototypes/charts/index"} highest level element, contains all other elements like plot segments, marks, legends e.t.c
 *
 * * Scales {@link "core/prototypes/plot_segments/index"} map data valus into pixels and sizes of elements(marks)
 *
 * * Links {@link "core/prototypes/links/index"}
 *
 * * Legends {@link "core/prototypes/legends/index"}
 *
 * * Guides {@link "core/prototypes/guides/index"} helper non visual elements to allign other elements
 *
 * * Glyphs {@link "core/prototypes/glyphs/index"} is container of other elements on plot segmets
 *
 * * Dataflow {@link "core/prototypes/dataflow/index"} uses for connecting elements to dataset
 *
 * @packageDocumentation
 * @preferred
 */
var Charts = require("./charts");
exports.Charts = Charts;
var Constraints = require("./constraints");
exports.Constraints = Constraints;
var Dataflow = require("./dataflow");
exports.Dataflow = Dataflow;
var Glyphs = require("./glyphs");
exports.Glyphs = Glyphs;
var Guides = require("./guides");
exports.Guides = Guides;
var Legends = require("./legends");
exports.Legends = Legends;
var Links = require("./links");
exports.Links = Links;
var Marks = require("./marks");
exports.Marks = Marks;
var PlotSegments = require("./plot_segments");
exports.PlotSegments = PlotSegments;
var Scales = require("./scales");
exports.Scales = Scales;
var cache_1 = require("./cache");
Object.defineProperty(exports, "ObjectClassCache", { enumerable: true, get: function () { return cache_1.ObjectClassCache; } });
__exportStar(require("./common"), exports);
__exportStar(require("./state"), exports);
Charts.registerClasses();
Glyphs.registerClasses();
Marks.registerClasses();
Links.registerClasses();
Legends.registerClasses();
Guides.registerClasses();
Scales.registerClasses();
PlotSegments.registerClasses();
Constraints.registerClasses();
//# sourceMappingURL=index.js.map