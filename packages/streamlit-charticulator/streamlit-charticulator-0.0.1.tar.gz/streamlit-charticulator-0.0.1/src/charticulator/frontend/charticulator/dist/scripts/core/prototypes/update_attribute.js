"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.snapToAttribute = exports.onUpdateAttribute = void 0;
var utils_1 = require("../common/utils");
var common_1 = require("./common");
var object_1 = require("./object");
var plot_segments_1 = require("./plot_segments");
function onUpdateAttribute(manager, elementID, attribute, value) {
    var e_1, _a, e_2, _b;
    var found = utils_1.zipArray(manager.chart.elements, manager.chartState.elements).find(function (_a) {
        var _b = __read(_a, 1), element = _b[0];
        return element._id === elementID;
    });
    if (found) {
        var elementState = found[1];
        elementState.attributes[attribute] = value;
    }
    else {
        try {
            for (var _c = __values(utils_1.zipArray(manager.chart.elements, manager.chartState.elements)), _d = _c.next(); !_d.done; _d = _c.next()) {
                var _e = __read(_d.value, 2), element = _e[0], elementState = _e[1];
                if (object_1.isType(element.classID, plot_segments_1.CartesianPlotSegment.type)) {
                    var plotSegment = element;
                    var plotSegmentState = elementState;
                    try {
                        for (var _f = (e_2 = void 0, __values(plotSegmentState.glyphs)), _g = _f.next(); !_g.done; _g = _f.next()) {
                            var glyphState = _g.value;
                            var glyph = common_1.findObjectById(manager.chart, plotSegment.glyph);
                            var found_1 = utils_1.zipArray(glyph.marks, glyphState.marks).find(function (_a) {
                                var _b = __read(_a, 1), element = _b[0];
                                return element._id === elementID;
                            });
                            if (found_1) {
                                var elementState_1 = found_1[1];
                                elementState_1.attributes[attribute] = value;
                            }
                        }
                    }
                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                    finally {
                        try {
                            if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                        }
                        finally { if (e_2) throw e_2.error; }
                    }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
}
exports.onUpdateAttribute = onUpdateAttribute;
function snapToAttribute(manager, chartConstraints, objectId, attrName, attrValue) {
    chartConstraints
        .filter(function (constraint) {
        return constraint.type == "snap" &&
            constraint.attributes.targetAttribute === attrName &&
            constraint.attributes.targetElement === objectId;
    })
        .forEach(function (constraint) {
        onUpdateAttribute(manager, constraint.attributes.element, constraint.attributes.attribute, attrValue);
    });
}
exports.snapToAttribute = snapToAttribute;
//# sourceMappingURL=update_attribute.js.map