"use strict";
/**
 * ![Chart levels](media://glyph-levels.png)
 *
 * The Chart-level specification includes chart elements, layout constraints between them, and scales. The most important chart element is
 * a plot segment, which lays out glyphs according to its scaffolds and/or
 * axes, and transforms them according to its coordinate system, scales specify how data is mapped to attributes
 * such as width, height, and color, and they can be shared among several
 * marks. Legends visualize the scales used in the chart.
 *
 * @packageDocumentation
 * @preferred
 */
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerClasses = exports.RectangleGlyph = exports.GlyphClass = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Specification = require("../../specification");
var solver_1 = require("../../solver");
var common_1 = require("../common");
var strings_1 = require("../../../strings");
var GlyphClass = /** @class */ (function (_super) {
    __extends(GlyphClass, _super);
    function GlyphClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GlyphClass.createDefault = function (table) {
        var glyph = _super.createDefault.call(this);
        glyph.table = table;
        glyph.constraints = [];
        glyph.marks = [];
        return glyph;
    };
    GlyphClass.metadata = {
        iconPath: "glyph",
        displayName: "Glyph",
    };
    return GlyphClass;
}(common_1.ObjectClass));
exports.GlyphClass = GlyphClass;
var RectangleGlyph = /** @class */ (function (_super) {
    __extends(RectangleGlyph, _super);
    function RectangleGlyph() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Get a list of elemnt attributes
        _this.attributeNames = [
            "x1",
            "y1",
            "x2",
            "y2",
            "x",
            "y",
            "width",
            "height",
            "ix1",
            "iy1",
            "ix2",
            "iy2",
            "icx",
            "icy",
        ];
        _this.attributes = {
            x1: {
                name: "x1",
                type: Specification.AttributeType.Number,
            },
            y1: {
                name: "y1",
                type: Specification.AttributeType.Number,
            },
            x2: {
                name: "x2",
                type: Specification.AttributeType.Number,
            },
            y2: {
                name: "y2",
                type: Specification.AttributeType.Number,
            },
            x: {
                name: "x",
                type: Specification.AttributeType.Number,
            },
            y: {
                name: "y",
                type: Specification.AttributeType.Number,
            },
            width: {
                name: "width",
                type: Specification.AttributeType.Number,
                defaultRange: [30, 200],
            },
            height: {
                name: "height",
                type: Specification.AttributeType.Number,
                defaultRange: [30, 200],
            },
            ix1: {
                name: "ix1",
                type: Specification.AttributeType.Number,
            },
            iy1: {
                name: "iy1",
                type: Specification.AttributeType.Number,
            },
            ix2: {
                name: "ix2",
                type: Specification.AttributeType.Number,
            },
            iy2: {
                name: "iy2",
                type: Specification.AttributeType.Number,
            },
            icx: {
                name: "icx",
                type: Specification.AttributeType.Number,
            },
            icy: {
                name: "icy",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    // Initialize the state of a mark so that everything has a valid value
    RectangleGlyph.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
        attrs.width = 60;
        attrs.height = 100;
        attrs.x1 = attrs.x - attrs.width / 2;
        attrs.y1 = attrs.y - attrs.height / 2;
        attrs.x2 = attrs.x + attrs.width / 2;
        attrs.y2 = attrs.y + attrs.height / 2;
        attrs.ix1 = -attrs.width / 2;
        attrs.iy1 = -attrs.height / 2;
        attrs.ix2 = +attrs.width / 2;
        attrs.iy2 = +attrs.height / 2;
        attrs.icx = 0;
        attrs.icy = 0;
    };
    // Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles)
    // eslint-disable-next-line
    RectangleGlyph.prototype.buildIntrinsicConstraints = function (solver) {
        var _a = __read(solver.attrs(this.state.attributes, [
            "x1",
            "y1",
            "x2",
            "y2",
            "x",
            "y",
            "width",
            "height",
            "ix1",
            "iy1",
            "ix2",
            "iy2",
            "icx",
            "icy",
        ]), 14), x1 = _a[0], y1 = _a[1], x2 = _a[2], y2 = _a[3], x = _a[4], y = _a[5], width = _a[6], height = _a[7], ix1 = _a[8], iy1 = _a[9], ix2 = _a[10], iy2 = _a[11], icx = _a[12], icy = _a[13];
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, x2],
            [-1, x1],
        ], [[1, width]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, y2],
            [-1, y1],
        ], [[1, height]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, ix2],
            [-1, ix1],
        ], [[1, width]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, iy2],
            [-1, iy1],
        ], [[1, height]]);
        // solver.addLinear(ConstraintStrength.HARD, 0, [[2, cx]], [[1, x1], [1, x2]]);
        // solver.addLinear(ConstraintStrength.HARD, 0, [[2, cy]], [[1, y1], [1, y2]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, ix1],
            [1, ix2],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
            [1, iy1],
            [1, iy2],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, icx]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, icy]]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, x]], [
            [0.5, x2],
            [0.5, x1],
            [1, solver.attr(this.state.marks[0].attributes, "x")],
        ]);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, y]], [
            [0.5, y2],
            [0.5, y1],
            [1, solver.attr(this.state.marks[0].attributes, "y")],
        ]);
    };
    RectangleGlyph.prototype.getAlignmentGuides = function () {
        var attrs = this.state.attributes;
        return [
            {
                type: "x",
                value: attrs.ix1,
                attribute: "ix1",
                visible: true,
            },
            {
                type: "x",
                value: attrs.ix2,
                attribute: "ix2",
                visible: true,
            },
            {
                type: "x",
                value: attrs.icx,
                attribute: "icx",
                visible: true,
            },
            {
                type: "y",
                value: attrs.iy1,
                attribute: "iy1",
                visible: true,
            },
            {
                type: "y",
                value: attrs.iy2,
                attribute: "iy2",
                visible: true,
            },
            {
                type: "y",
                value: attrs.icy,
                attribute: "icy",
                visible: true,
            },
        ];
    };
    RectangleGlyph.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var ix1 = attrs.ix1, iy1 = attrs.iy1, ix2 = attrs.ix2, iy2 = attrs.iy2;
        var inf = [-10000, 10000];
        return [
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "ix1" }],
                value: ix1,
                span: inf,
            },
            {
                type: "line",
                axis: "x",
                actions: [{ type: "attribute", attribute: "ix2" }],
                value: ix2,
                span: inf,
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "iy1" }],
                value: iy1,
                span: inf,
            },
            {
                type: "line",
                axis: "y",
                actions: [{ type: "attribute", attribute: "iy2" }],
                value: iy2,
                span: inf,
            },
        ];
    };
    RectangleGlyph.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.sectionHeader(strings_1.strings.objects.dimensions),
            manager.mappingEditor(strings_1.strings.objects.width, "width", {}),
            manager.mappingEditor(strings_1.strings.objects.height, "height", {}),
        ];
    };
    RectangleGlyph.classID = "glyph.rectangle";
    RectangleGlyph.type = "glyph";
    return RectangleGlyph;
}(GlyphClass));
exports.RectangleGlyph = RectangleGlyph;
function registerClasses() {
    common_1.ObjectClasses.Register(RectangleGlyph);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map