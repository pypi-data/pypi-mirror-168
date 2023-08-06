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
exports.initialize = exports.ColorUtils = exports.Utils = exports.Dataset = exports.Graphics = exports.Solver = exports.Prototypes = exports.Specification = exports.Expression = void 0;
/**
 * # Core documentation
 *
 * ## Actions {@link "core/actions/index"}
 * The module contains all actions available in the charticulator.
 *
 * ## Common {@link "core/common/index"}
 *
 * Contains several modules such as
 *
 * * {@link "core/common/color"} to work with colors
 * * {@link "core/common/events"} event bus uses for notifying different parts of UI about updates.
 * * {@link "core/common/fetch"}
 * * {@link "core/common/math"} contains math operations for geometry
 * * {@link "core/common/scales"} scales for map data values to properties of graphic elements
 * * {@link "core/common/unique_id"} id generator for all objects used in charticulator
 * * {@link "core/common/utils"} contains different helper functions
 *
 * ## Dataset {@link "core/dataset/index"}
 *
 * The module is responsible for loading data from *.csv/*.tsv files and parse them
 *
 * ## Expression {@link "core/expression/index"}
 *
 * Describes all supported expressions in the charticulator and helper functions for process date on binding to elements
 *
 * ## Graphics {@link "core/graphics/index"}
 *
 * Contains logic responsible  for rendering elements and coordinate systems
 *
 * ## Prototypes {@link "core/prototypes/index"}
 *
 * Contains bricks of the chart: *Marks*({@link "core/prototypes/marks/index"}) (rect, image, symbol, text e.t.c.), Legends, Links, Plot Segments e.t.c
 *
 * * Declares the properties and attributes of a class of object (chart, chart element, glyph, mark) in the spec
 *
 * * Including default attribute values and property values
 *
 * * Generate graphical elements (if any) for ChartRenderer
 *
 * * Generate constraints (if any) for the constraint solver
 *
 * * Declare widgets (if any) for the attribute panel
 *
 * ### Difference between “attribute” and “property”
 *
 * Attribute (e.g., height on a rect mark):
 *
 * * Defined on the object state (an object can have multiple instances, each instance has its own state)
 * * Variable among the instances of the object
 * * Can involve in constraint solving
 * * Can be bound to data
 *
 * Property (e.g., anchor on a text mark):
 *
 * * Defined directly on the object specification
 * * Same across all instances of the object
 * * Does not involve in constraint solving
 * * Cannot be bound to data
 *
 * ## Solver {@link "core/solver/index"}
 *
 * Wrapping over lscg-solver package to convert chart co constrains.
 *
 * ## Specification {@link "core/specification/index"}
 *
 * It contains interfaces for the chart template. The template describes the internal structure of the chart.
 *
 * ## Store {@link "core/store/base"}
 *
 * @packageDocumentation
 * @preferred
 */
__exportStar(require("./common"), exports);
var config_1 = require("./config");
Object.defineProperty(exports, "getConfig", { enumerable: true, get: function () { return config_1.getConfig; } });
var Dataset = require("./dataset");
exports.Dataset = Dataset;
var Expression = require("./expression");
exports.Expression = Expression;
var Graphics = require("./graphics");
exports.Graphics = Graphics;
var Prototypes = require("./prototypes");
exports.Prototypes = Prototypes;
var Solver = require("./solver");
exports.Solver = Solver;
var Specification = require("./specification");
exports.Specification = Specification;
var Utils = require("./common/utils");
exports.Utils = Utils;
var ColorUtils = require("./common/color");
exports.ColorUtils = ColorUtils;
__exportStar(require("./actions"), exports);
var config_2 = require("./config");
var wasm_solver_1 = require("./solver/wasm_solver");
function initialize(config) {
    config_2.setConfig(config);
    return wasm_solver_1.initialize();
}
exports.initialize = initialize;
//# sourceMappingURL=index.js.map