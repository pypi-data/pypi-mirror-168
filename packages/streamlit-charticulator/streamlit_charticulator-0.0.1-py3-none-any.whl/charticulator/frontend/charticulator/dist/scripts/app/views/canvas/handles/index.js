"use strict";
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
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.HandlesView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var input_curve_1 = require("./input_curve");
var text_alignment_1 = require("./text_alignment");
var point_1 = require("./point");
var distance_ratio_1 = require("./distance_ratio");
var angle_1 = require("./angle");
var margin_1 = require("./margin");
var gap_ratio_1 = require("./gap_ratio");
var relative_line_1 = require("./relative_line");
var line_1 = require("./line");
var HandlesView = /** @class */ (function (_super) {
    __extends(HandlesView, _super);
    function HandlesView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // eslint-disable-next-line
    HandlesView.prototype.renderHandle = function (handle) {
        var e_1, _a;
        var isHandleSnapped = false;
        if (this.props.isAttributeSnapped) {
            try {
                for (var _b = __values(handle.actions), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var action = _c.value;
                    if (action.type == "attribute") {
                        isHandleSnapped =
                            isHandleSnapped || this.props.isAttributeSnapped(action.attribute);
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        switch (handle.type) {
            case "point": {
                return (React.createElement(point_1.PointHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, snapped: isHandleSnapped, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "line": {
                return (React.createElement(line_1.LineHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, snapped: isHandleSnapped, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "relative-line": {
                return (React.createElement(relative_line_1.RelativeLineHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "gap-ratio": {
                return (React.createElement(gap_ratio_1.GapRatioHandleView, { zoom: this.props.zoom, active: this.props.active, visible: false, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "margin": {
                return (React.createElement(margin_1.MarginHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "angle": {
                return (React.createElement(angle_1.AngleHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "distance-ratio": {
                return (React.createElement(distance_ratio_1.DistanceRatioHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "text-alignment": {
                return (React.createElement(text_alignment_1.TextAlignmentHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
            case "input-curve": {
                return (React.createElement(input_curve_1.InputCurveHandleView, { zoom: this.props.zoom, active: this.props.active, visible: this.props.visible, onDragStart: this.props.onDragStart, handle: handle }));
            }
        }
    };
    HandlesView.prototype.render = function () {
        var _this = this;
        return (React.createElement("g", null, this.props.handles.map(function (b, idx) { return (React.createElement("g", { key: "m" + idx }, _this.renderHandle(b))); })));
    };
    return HandlesView;
}(React.Component));
exports.HandlesView = HandlesView;
//# sourceMappingURL=index.js.map