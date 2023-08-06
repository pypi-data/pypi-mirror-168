"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultVersionOfTemplate = exports.defaultFontSizeLegend = exports.defaultFontSize = exports.defaultFont = exports.createDefaultChart = exports.createDefaultTitle = exports.createDefaultPlotSegment = exports.createDefaultGlyph = void 0;
var core_1 = require("../../core");
var base_1 = require("../../core/prototypes/plot_segments/region_2d/base");
var specification_1 = require("../../core/specification");
/** Create a default glyph */
function createDefaultGlyph(tableName) {
    return {
        _id: core_1.uniqueID(),
        classID: "glyph.rectangle",
        properties: { name: "Glyph" },
        table: tableName,
        marks: [
            {
                _id: core_1.uniqueID(),
                classID: "mark.anchor",
                properties: { name: "Anchor" },
                mappings: {
                    x: {
                        type: specification_1.MappingType.parent,
                        parentAttribute: "icx",
                    },
                    y: {
                        type: specification_1.MappingType.parent,
                        parentAttribute: "icy",
                    },
                },
            },
        ],
        mappings: {},
        constraints: [],
    };
}
exports.createDefaultGlyph = createDefaultGlyph;
/** Create a default plot segment */
function createDefaultPlotSegment(table, glyph) {
    return {
        _id: core_1.uniqueID(),
        classID: "plot-segment.cartesian",
        glyph: glyph._id,
        table: table.name,
        filter: null,
        mappings: {
            x1: {
                type: specification_1.MappingType.parent,
                parentAttribute: "x1",
            },
            y1: {
                type: specification_1.MappingType.parent,
                parentAttribute: "y1",
            },
            x2: {
                type: specification_1.MappingType.parent,
                parentAttribute: "x2",
            },
            y2: {
                type: specification_1.MappingType.parent,
                parentAttribute: "y2",
            },
        },
        properties: {
            name: "PlotSegment1",
            visible: true,
            marginX1: 0,
            marginY1: 0,
            marginX2: 0,
            marginY2: 0,
            sublayout: {
                type: table.rows.length >= 100 ? "grid" : base_1.Region2DSublayoutType.DodgeX,
                order: null,
                ratioX: 0.1,
                ratioY: 0.1,
                align: {
                    x: base_1.SublayoutAlignment.Start,
                    y: base_1.SublayoutAlignment.Start,
                },
                grid: {
                    direction: base_1.GridDirection.X,
                    xCount: null,
                    yCount: null,
                    gridStartPosition: base_1.GridStartPosition.LeftTop,
                },
                packing: {
                    gravityX: 0.1,
                    gravityY: 0.1,
                    boxedX: null,
                    boxedY: null,
                },
                jitter: {
                    vertical: true,
                    horizontal: true,
                },
            },
        },
    };
}
exports.createDefaultPlotSegment = createDefaultPlotSegment;
/** Create a default chart title */
function createDefaultTitle(dataset) {
    return {
        _id: core_1.uniqueID(),
        classID: "mark.text",
        properties: {
            name: "Title",
            visible: true,
            alignment: { x: "middle", y: "top", xMargin: 0, yMargin: 30 },
            rotation: 0,
        },
        mappings: {
            x: {
                type: specification_1.MappingType.parent,
                parentAttribute: "cx",
            },
            y: {
                type: specification_1.MappingType.parent,
                parentAttribute: "oy2",
            },
            text: {
                type: specification_1.MappingType.value,
                value: dataset.name,
            },
            fontSize: {
                type: specification_1.MappingType.value,
                value: 24,
            },
            color: {
                type: specification_1.MappingType.value,
                value: { r: 0, g: 0, b: 0 },
            },
        },
    };
}
exports.createDefaultTitle = createDefaultTitle;
/** Create a default chart */
function createDefaultChart(dataset, createTitle) {
    var table = dataset.tables[0];
    var glyph = createDefaultGlyph(table.name);
    return {
        _id: core_1.uniqueID(),
        classID: "chart.rectangle",
        properties: {
            name: "Chart",
            backgroundColor: null,
            backgroundOpacity: 1,
            enableContextMenu: true,
            exposed: true,
        },
        mappings: {
            marginTop: {
                type: specification_1.MappingType.value,
                value: 80,
            },
            width: {
                type: specification_1.MappingType.value,
                value: 900,
            },
            height: {
                type: specification_1.MappingType.value,
                value: 600,
            },
        },
        glyphs: [glyph],
        elements: [
            createDefaultPlotSegment(table, glyph),
            createTitle ? createDefaultTitle(dataset) : null,
        ].filter(function (elem) { return elem != null; }),
        scales: [],
        scaleMappings: [],
        constraints: [],
        resources: [],
    };
}
exports.createDefaultChart = createDefaultChart;
exports.defaultFont = "Segoe UI";
exports.defaultFontSize = 12;
exports.defaultFontSizeLegend = 12;
exports.defaultVersionOfTemplate = "2.0.3";
//# sourceMappingURL=defaults.js.map