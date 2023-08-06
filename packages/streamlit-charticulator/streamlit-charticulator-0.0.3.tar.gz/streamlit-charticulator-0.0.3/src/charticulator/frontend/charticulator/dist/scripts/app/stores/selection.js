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
exports.MarkSelection = exports.GlyphSelection = exports.ChartElementSelection = exports.Selection = void 0;
/** Base class for selections */
var Selection = /** @class */ (function () {
    function Selection() {
    }
    return Selection;
}());
exports.Selection = Selection;
/** ChartElement selection */
var ChartElementSelection = /** @class */ (function (_super) {
    __extends(ChartElementSelection, _super);
    function ChartElementSelection(chartElement) {
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        return _this;
    }
    return ChartElementSelection;
}(Selection));
exports.ChartElementSelection = ChartElementSelection;
/** Glyph selection */
var GlyphSelection = /** @class */ (function (_super) {
    __extends(GlyphSelection, _super);
    function GlyphSelection(plotSegment, glyph) {
        if (plotSegment === void 0) { plotSegment = null; }
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.glyph = glyph;
        return _this;
    }
    return GlyphSelection;
}(Selection));
exports.GlyphSelection = GlyphSelection;
/** Mark selection */
var MarkSelection = /** @class */ (function (_super) {
    __extends(MarkSelection, _super);
    function MarkSelection(plotSegment, glyph, mark) {
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.glyph = glyph;
        _this.mark = mark;
        return _this;
    }
    return MarkSelection;
}(Selection));
exports.MarkSelection = MarkSelection;
//# sourceMappingURL=selection.js.map