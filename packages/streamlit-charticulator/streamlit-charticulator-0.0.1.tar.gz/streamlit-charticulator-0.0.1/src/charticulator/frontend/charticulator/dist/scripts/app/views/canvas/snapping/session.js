"use strict";
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
exports.SnappingSession = void 0;
var SnappingSession = /** @class */ (function () {
    function SnappingSession(guides, handle, threshold, findClosest) {
        this.handle = handle;
        this.threshold = threshold;
        this.candidates = [];
        this.currentCandidates = null;
        this.findClosestSnappingGuide = findClosest;
        switch (handle.type) {
            case "line":
                {
                    var lineHandle_1 = handle;
                    // Get all guides
                    this.candidates = guides.filter(function (g) {
                        return (g.guide.type == lineHandle_1.axis ||
                            g.guide.type == "angular" ||
                            g.guide.type == "radial" ||
                            g.guide.type == "point");
                    });
                }
                break;
            case "point":
                {
                    // Get all guides
                    this.candidates = guides.filter(function (g) {
                        return (g.guide.type == "x" ||
                            g.guide.type == "y" ||
                            g.guide.type == "angular" ||
                            g.guide.type == "radial" ||
                            g.guide.type == "point");
                    });
                }
                break;
        }
    }
    SnappingSession.prototype.giveProrityToPoint = function (a, b) {
        var _a, _b, _c, _d;
        var aPriority = (_b = (_a = a.guide) === null || _a === void 0 ? void 0 : _a.priority) !== null && _b !== void 0 ? _b : 0;
        var bPriority = (_d = (_c = b.guide) === null || _c === void 0 ? void 0 : _c.priority) !== null && _d !== void 0 ? _d : 0;
        if (aPriority > 0 || bPriority > 0) {
            return bPriority - aPriority;
        }
        else {
            if (a.guide.type === "point" && b.guide.type !== "point") {
                return -1;
            }
            else if (a.guide.type === "point" && b.guide.type === "point") {
                return 0;
            }
            else {
                return 1;
            }
        }
    };
    // eslint-disable-next-line
    SnappingSession.prototype.handleDrag = function (e) {
        var e_1, _a, e_2, _b;
        var _c, _d;
        var EPSILON = 1e-5;
        switch (this.handle.type) {
            case "line":
                {
                    var minGuide = null;
                    var minDistance = null;
                    var minXGuide = null;
                    var minXDistance = null;
                    var minYGuide = null;
                    var minYDistance = null;
                    try {
                        for (var _e = __values(this.candidates.sort(this.giveProrityToPoint)), _f = _e.next(); !_f.done; _f = _e.next()) {
                            var g = _f.value;
                            var guide = g.guide;
                            if (this.findClosestSnappingGuide) {
                                if (guide.type == "y") {
                                    var dY = Math.abs(guide.value - e.value);
                                    if (dY < minYDistance || minYDistance == null) {
                                        minYDistance = dY;
                                        minYGuide = g;
                                    }
                                }
                                else if (guide.type == "x") {
                                    var dX = Math.abs(guide.value - e.value);
                                    if (dX < minXDistance || minXDistance == null) {
                                        minXDistance = dX;
                                        minXGuide = g;
                                    }
                                }
                                else {
                                    var guide_1 = g.guide;
                                    var d = Math.abs(guide_1.value - e.value);
                                    if (d < this.threshold &&
                                        (minDistance == null || d < minDistance - EPSILON)) {
                                        minDistance = d;
                                        minGuide = g;
                                    }
                                }
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                    if (this.findClosestSnappingGuide) {
                        if (((_c = this.handle) === null || _c === void 0 ? void 0 : _c.axis) === "y") {
                            if (minYGuide) {
                                this.currentCandidates = [minYGuide];
                            }
                        }
                        if (((_d = this.handle) === null || _d === void 0 ? void 0 : _d.axis) === "x") {
                            if (minXGuide) {
                                this.currentCandidates = [minXGuide];
                            }
                        }
                    }
                    else {
                        if (minGuide) {
                            this.currentCandidates = [minGuide];
                        }
                        else {
                            this.currentCandidates = null;
                        }
                    }
                }
                break;
            case "point":
                {
                    var minXGuide = null;
                    var minXDistance = null;
                    var minYGuide = null;
                    var minYDistance = null;
                    try {
                        for (var _g = __values(this.candidates.sort(this.giveProrityToPoint)), _h = _g.next(); !_h.done; _h = _g.next()) {
                            var g = _h.value;
                            var guide = g.guide;
                            if (this.findClosestSnappingGuide) {
                                // Find closest point
                                if (g.guide.type == "point") {
                                    var polarGuide = g.guide;
                                    var dX = Math.abs(polarGuide.angle - e.x);
                                    var dY = Math.abs(polarGuide.radius - e.y);
                                    if (dX < minXDistance || minXDistance == null) {
                                        minXDistance = dX;
                                        minXGuide = g;
                                    }
                                    if (dY < minYDistance || minYDistance == null) {
                                        minYDistance = dY;
                                        minYGuide = g;
                                    }
                                }
                                else if (guide.type == "y") {
                                    var dY = Math.abs(guide.value - e.y);
                                    if (dY < minYDistance || minYDistance == null) {
                                        minYDistance = dY;
                                        minYGuide = g;
                                    }
                                }
                                else if (guide.type == "x") {
                                    var dX = Math.abs(guide.value - e.x);
                                    if (dX < minXDistance || minXDistance == null) {
                                        minXDistance = dX;
                                        minXGuide = g;
                                    }
                                }
                            }
                            else {
                                // Filter guides by threshold
                                if (g.guide.type == "point") {
                                    var polarGuide = g.guide;
                                    var d = Math.sqrt((polarGuide.angle - e.x) *
                                        (polarGuide.angle - e.x) +
                                        (polarGuide.radius - e.y) *
                                            (polarGuide.radius - e.y));
                                    if (d < this.threshold &&
                                        (minYDistance == null || d < minYDistance - EPSILON)) {
                                        minYDistance = d;
                                        minYGuide = g;
                                        minXDistance = d;
                                        minXGuide = g;
                                    }
                                }
                                else if (guide.type == "x") {
                                    var d = Math.abs(guide.value - e.x);
                                    if (d < this.threshold &&
                                        (minXDistance == null || d < minXDistance - EPSILON)) {
                                        minXDistance = d;
                                        minXGuide = g;
                                    }
                                }
                                else if (guide.type == "y") {
                                    var d = Math.abs(guide.value - e.y);
                                    if (d < this.threshold &&
                                        (minYDistance == null || d < minYDistance - EPSILON)) {
                                        minYDistance = d;
                                        minYGuide = g;
                                    }
                                }
                            }
                        }
                    }
                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                    finally {
                        try {
                            if (_h && !_h.done && (_b = _g.return)) _b.call(_g);
                        }
                        finally { if (e_2) throw e_2.error; }
                    }
                    this.currentCandidates = [];
                    if (minXGuide) {
                        this.currentCandidates.push(minXGuide);
                    }
                    if (minYGuide) {
                        this.currentCandidates.push(minYGuide);
                    }
                }
                break;
        }
    };
    // eslint-disable-next-line
    SnappingSession.prototype.handleEnd = function (e) {
        var e_3, _a, e_4, _b;
        var result = [];
        try {
            for (var _c = __values(this.handle.actions), _d = _c.next(); !_d.done; _d = _c.next()) {
                var action = _d.value;
                var source = action.source || "value";
                if (e[source] === undefined) {
                    continue;
                }
                var value = e[source];
                if (action.minimum != null) {
                    value = Math.max(action.minimum, value);
                }
                if (action.maximum != null) {
                    value = Math.min(action.maximum, value);
                }
                switch (action.type) {
                    case "attribute-value-mapping":
                        {
                            result.push({
                                type: "value-mapping",
                                attribute: action.attribute,
                                value: value,
                            });
                        }
                        break;
                    case "property":
                        {
                            result.push({
                                type: "property",
                                property: action.property,
                                field: action.field,
                                value: value,
                            });
                        }
                        break;
                    case "attribute":
                        {
                            var didSnap = false;
                            if (source == "value") {
                                if (this.currentCandidates &&
                                    this.currentCandidates.length == 1) {
                                    var candidate = this.currentCandidates[0];
                                    result.push({
                                        type: "snap",
                                        attribute: action.attribute,
                                        snapElement: candidate.element,
                                        snapAttribute: candidate.guide
                                            .attribute,
                                    });
                                    didSnap = true;
                                }
                            }
                            if (source == "x" || source == "y") {
                                try {
                                    for (var _e = (e_4 = void 0, __values(this.currentCandidates.sort(this.giveProrityToPoint))), _f = _e.next(); !_f.done; _f = _e.next()) {
                                        var candidate = _f.value;
                                        if (candidate.guide
                                            .type === "point") {
                                            if (source == "x") {
                                                result.push({
                                                    type: "snap",
                                                    attribute: action.attribute,
                                                    snapElement: candidate.element,
                                                    snapAttribute: candidate.guide
                                                        .angleAttribute,
                                                });
                                                didSnap = true;
                                            }
                                            if (source == "y") {
                                                result.push({
                                                    type: "snap",
                                                    attribute: action.attribute,
                                                    snapElement: candidate.element,
                                                    snapAttribute: candidate.guide
                                                        .radiusAttribute,
                                                });
                                                didSnap = true;
                                            }
                                        }
                                        else if (source ==
                                            candidate.guide.type) {
                                            result.push({
                                                type: "snap",
                                                attribute: action.attribute,
                                                snapElement: candidate.element,
                                                snapAttribute: candidate.guide
                                                    .attribute,
                                            });
                                            didSnap = true;
                                        }
                                    }
                                }
                                catch (e_4_1) { e_4 = { error: e_4_1 }; }
                                finally {
                                    try {
                                        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                                    }
                                    finally { if (e_4) throw e_4.error; }
                                }
                            }
                            if (!didSnap) {
                                result.push({
                                    type: "move",
                                    attribute: action.attribute,
                                    value: value,
                                });
                            }
                        }
                        break;
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_3) throw e_3.error; }
        }
        // switch (this.handle.type) {
        //     case "line": {
        //         let lineBound = this.handle as Prototypes.Handles.Line;
        //         if (this.currentCandidates && this.currentCandidates.length == 1) {
        //             let candidate = this.currentCandidates[0];
        //             result.push({
        //                 type: "snap",
        //                 attribute: lineBound.attribute,
        //                 snapElement: candidate.element,
        //                 snapAttribute: (candidate.guide as Prototypes.SnappingGuides.Axis).attribute
        //             });
        //         } else {
        //             result.push({
        //                 type: "move",
        //                 attribute: lineBound.attribute,
        //                 value: e.newValue
        //             });
        //         }
        //     } break;
        //     case "relative-line": {
        //         let relativeLine = this.handle as Prototypes.Handles.RelativeLine;
        //         result.push({
        //             type: "move",
        //             attribute: relativeLine.attribute,
        //             value: e.newValue
        //         });
        //     } break;
        //     case "point": {
        //         let pointBound = this.handle as Prototypes.Handles.Point;
        //         let didX: boolean = false;
        //         let didY: boolean = false;
        //         if (this.currentCandidates) {
        //             for (let candidate of this.currentCandidates) {
        //                 let attr: string;
        //                 switch ((candidate.guide as Prototypes.SnappingGuides.Axis).type) {
        //                     case "x": {
        //                         didX = true;
        //                         attr = pointBound.xAttribute;
        //                     } break;
        //                     case "y": {
        //                         didY = true;
        //                         attr = pointBound.yAttribute;
        //                     } break;
        //                 }
        //                 result.push({
        //                     type: "snap",
        //                     attribute: attr,
        //                     snapElement: candidate.element,
        //                     snapAttribute: (candidate.guide as Prototypes.SnappingGuides.Axis).attribute
        //                 });
        //             }
        //             if (!didX) {
        //                 result.push({
        //                     type: "move",
        //                     attribute: pointBound.xAttribute,
        //                     value: e.newXValue
        //                 });
        //             }
        //             if (!didY) {
        //                 result.push({
        //                     type: "move",
        //                     attribute: pointBound.yAttribute,
        //                     value: e.newYValue
        //                 });
        //             }
        //         }
        //     } break;
        // }
        return result;
    };
    SnappingSession.prototype.getCurrentCandidates = function () {
        return this.currentCandidates;
    };
    return SnappingSession;
}());
exports.SnappingSession = SnappingSession;
//# sourceMappingURL=session.js.map