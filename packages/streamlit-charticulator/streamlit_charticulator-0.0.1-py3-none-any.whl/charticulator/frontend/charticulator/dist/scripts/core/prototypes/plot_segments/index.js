"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerClasses = void 0;
/**
 * Plotsegmets are high level elements of charticulator responsible for layout and arrange other elements (glyph's and marks)
 *
 * ![Plot segmets](media://plotsegmets_scaffolds.png)
 *
 * Segment can have different sublayouts: stacked x, stacked y, grid, packing e.tc
 *
 * ![Plot segmets sublayout](media://cartesian_plot_segment.png) ![Polar plot segmets sublayout](media://sublayout_polar.png)
 *
 * All plot segmets extends {@link PlotSegmentClass} class.
 *
 * Charticulator has different plot segmets:
 *
 * {@link LineGuide} - puts elements on the one line
 *
 * {@link MapPlotSegment} - special plot segmet to draw a map. Uses {@link StaticMapService} class to workd with Bing and Google services
 *
 * {@link CartesianPlotSegment} - classic plot segmet with x and y axis coordinates
 *
 * ![Cartesian plot segmets](media://cartesian_plot.png)
 *
 * {@link CurvePlotSegment} - puts elements on cruve drawn by user.
 *
 * ![Curve plot](media://curve_plot.png)
 *
 * {@link PolarPlotSegment} - plot segmets with polar coordinates
 *
 * ![Polar plot segmets](media://polar_plot.png)
 *
 * @packageDocumentation
 * @preferred
 */
var object_1 = require("../object");
var line_1 = require("./line");
var map_1 = require("./map");
var region_2d_1 = require("./region_2d");
var axis_1 = require("./axis");
Object.defineProperty(exports, "defaultAxisStyle", { enumerable: true, get: function () { return axis_1.defaultAxisStyle; } });
var region_2d_2 = require("./region_2d");
Object.defineProperty(exports, "CartesianPlotSegment", { enumerable: true, get: function () { return region_2d_2.CartesianPlotSegment; } });
Object.defineProperty(exports, "CurvePlotSegment", { enumerable: true, get: function () { return region_2d_2.CurvePlotSegment; } });
Object.defineProperty(exports, "PolarPlotSegment", { enumerable: true, get: function () { return region_2d_2.PolarPlotSegment; } });
var plot_segment_1 = require("./plot_segment");
Object.defineProperty(exports, "PlotSegmentClass", { enumerable: true, get: function () { return plot_segment_1.PlotSegmentClass; } });
function registerClasses() {
    object_1.ObjectClasses.Register(line_1.LineGuide);
    object_1.ObjectClasses.Register(map_1.MapPlotSegment);
    object_1.ObjectClasses.Register(region_2d_1.CartesianPlotSegment);
    object_1.ObjectClasses.Register(region_2d_1.CurvePlotSegment);
    object_1.ObjectClasses.Register(region_2d_1.PolarPlotSegment);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map