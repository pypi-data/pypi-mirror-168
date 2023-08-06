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
exports.ClearSelection = exports.SelectMark = exports.Action = exports.objectDigest = void 0;
// Helper functions for digest
function objectDigest(obj) {
    return obj ? [obj.classID, obj._id] : null;
}
exports.objectDigest = objectDigest;
/**
 * Base class for all actions to describe all user interactions with charticulators objects
 * Actions dispatches by {@link BaseStore.dispatcher} method of the store.
 * List of charticulator app actions can be found in {@link "app/actions/actions"} module
 */
var Action = /** @class */ (function () {
    function Action() {
    }
    Action.prototype.dispatch = function (dispatcher) {
        dispatcher.dispatch(this);
    };
    Action.prototype.digest = function () {
        return { name: this.constructor.name };
    };
    return Action;
}());
exports.Action = Action;
/** Dispatches when user selects the mark on the chart */
var SelectMark = /** @class */ (function (_super) {
    __extends(SelectMark, _super);
    /**
     * @param plotSegment plot segment where mark was selected
     * @param glyph glyph where mark was selected (on a glyph editor or on a chart)
     * @param mark selected mark
     * @param glyphIndex index of glyph
     */
    function SelectMark(plotSegment, glyph, mark, glyphIndex) {
        if (glyphIndex === void 0) { glyphIndex = null; }
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.glyphIndex = glyphIndex;
        return _this;
    }
    SelectMark.prototype.digest = function () {
        return {
            name: "SelectMark",
            plotSegment: objectDigest(this.plotSegment),
            glyph: objectDigest(this.glyph),
            mark: objectDigest(this.mark),
            glyphIndex: this.glyphIndex,
        };
    };
    return SelectMark;
}(Action));
exports.SelectMark = SelectMark;
/** Dispatches when user reset selection of the mark on the chart */
var ClearSelection = /** @class */ (function (_super) {
    __extends(ClearSelection, _super);
    function ClearSelection() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ClearSelection.prototype.digest = function () {
        return {
            name: "ClearSelection",
        };
    };
    return ClearSelection;
}(Action));
exports.ClearSelection = ClearSelection;
//# sourceMappingURL=actions.js.map