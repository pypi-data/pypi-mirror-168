"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
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
var core_1 = require("../../../core");
var dataset_1 = require("../../../core/dataset");
var specification_1 = require("../../../core/specification");
var actions_1 = require("../../actions");
var registry_1 = require("./registry");
// eslint-disable-next-line
function default_1(REG) {
    // Internal registry of mark-level action handlers
    var MR = new registry_1.ActionHandlerRegistry();
    MR.add(actions_1.Actions.UpdateMarkAttribute, function (action) {
        var _this = this;
        var _loop_1 = function (key) {
            if (!Object.prototype.hasOwnProperty.call(action.updates, key)) {
                return "continue";
            }
            delete action.mark.mappings[key];
            action.glyph.constraints = action.glyph.constraints.filter(function (c) {
                if (c.type == "snap") {
                    if (c.attributes.element == action.mark._id &&
                        c.attributes.attribute == key) {
                        return false;
                    }
                }
                return true;
            });
        };
        for (var key in action.updates) {
            _loop_1(key);
        }
        this.forAllGlyph(action.glyph, function (glyphState) {
            var e_1, _a;
            try {
                for (var _b = __values(core_1.zipArray(action.glyph.marks, glyphState.marks)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), mark = _d[0], markState = _d[1];
                    if (mark == action.mark) {
                        for (var key in action.updates) {
                            if (!Object.prototype.hasOwnProperty.call(action.updates, key)) {
                                continue;
                            }
                            markState.attributes[key] = action.updates[key];
                            _this.addPresolveValue(core_1.Solver.ConstraintStrength.WEAK, markState.attributes, key, action.updates[key]);
                        }
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
        });
    });
    MR.add(actions_1.Actions.SetObjectProperty, function (action) {
        // check name property. Names of objects are unique
        if (action.property === "name" &&
            this.chartManager.isNameUsed(action.value)) {
            return;
        }
        if (action.field == null) {
            action.object.properties[action.property] = action.value;
        }
        else {
            var obj = action.object.properties[action.property];
            action.object.properties[action.property] = core_1.setField(obj, action.field, action.value);
        }
    });
    MR.add(actions_1.Actions.SetMarkAttribute, function (action) {
        if (action.mapping == null) {
            delete action.mark.mappings[action.attribute];
        }
        else {
            action.mark.mappings[action.attribute] = action.mapping;
            action.glyph.constraints = action.glyph.constraints.filter(function (c) {
                if (c.type == "snap") {
                    if (c.attributes.element == action.mark._id &&
                        c.attributes.attribute == action.attribute) {
                        return false;
                    }
                }
                return true;
            });
        }
    });
    MR.add(actions_1.Actions.UnmapMarkAttribute, function (action) {
        delete action.mark.mappings[action.attribute];
    });
    MR.add(actions_1.Actions.SnapMarks, function (action) {
        var _this = this;
        var idx1 = action.glyph.marks.indexOf(action.mark);
        if (idx1 < 0) {
            return;
        }
        // let elementState = this.markState.elements[idx1];
        var idx2 = action.glyph.marks.indexOf(action.targetMark);
        if (idx2 < 0) {
            return;
        }
        // let targetElementState = this.markState.elements[idx2];
        // elementState.attributes[action.attribute] = targetElementState.attributes[action.targetAttribute];
        // Remove any existing attribute mapping
        delete action.mark.mappings[action.attribute];
        // Remove any existing snapping
        action.glyph.constraints = action.glyph.constraints.filter(function (c) {
            if (c.type == "snap") {
                if (c.attributes.element == action.mark._id &&
                    c.attributes.attribute == action.attribute) {
                    return false;
                }
            }
            return true;
        });
        action.glyph.constraints.push({
            type: "snap",
            attributes: {
                element: action.mark._id,
                attribute: action.attribute,
                targetElement: action.targetMark._id,
                targetAttribute: action.targetAttribute,
                gap: 0,
            },
        });
        // Force the states to be equal
        this.forAllGlyph(action.glyph, function (glyphState) {
            var elementState = glyphState.marks[idx1];
            var targetElementState = glyphState.marks[idx2];
            elementState.attributes[action.attribute] =
                targetElementState.attributes[action.targetAttribute];
            _this.addPresolveValue(core_1.Solver.ConstraintStrength.STRONG, elementState.attributes, action.attribute, targetElementState.attributes[action.targetAttribute]);
        });
    });
    MR.add(actions_1.Actions.MarkActionGroup, function (action) {
        var e_2, _a;
        try {
            for (var _b = __values(action.actions), _c = _b.next(); !_c.done; _c = _b.next()) {
                var item = _c.value;
                // Recursively handle group actions
                MR.handleAction(this, item);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
    });
    // The entry point for mark actions
    REG.add(actions_1.Actions.MarkAction, function (mainAction) {
        this.saveHistory();
        MR.handleAction(this, mainAction);
        // Solve constraints only after all actions are processed
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.MapDataToMarkAttribute, function (action) {
        var _a, _b, _c;
        this.saveHistory();
        var inferred = (action.hints && action.hints.scaleID) ||
            this.scaleInference({
                glyph: action.glyph,
                chart: {
                    table: action.expressionTable,
                },
            }, {
                expression: action.expression,
                valueType: action.valueType,
                valueKind: action.valueMetadata.kind,
                outputType: action.attributeType,
                hints: action.hints,
                markAttribute: action.attribute,
            });
        if (inferred != null) {
            if (action.valueType == core_1.Specification.DataType.Image &&
                action.valueType === core_1.Specification.DataType.Image) {
                action.mark.mappings[action.attribute] = {
                    type: specification_1.MappingType.expressionScale,
                    table: (_a = action.expressionTable) !== null && _a !== void 0 ? _a : action.glyph.table,
                    expression: "first(" + core_1.ImageKeyColumn + ")",
                    valueExpression: action.expression,
                    valueType: action.valueType,
                    scale: inferred,
                    attribute: action.attribute,
                    valueIndex: action.hints && action.hints.allowSelectValue != undefined
                        ? 0
                        : null,
                };
            }
            else {
                action.mark.mappings[action.attribute] = {
                    type: specification_1.MappingType.scale,
                    table: (_b = action.expressionTable) !== null && _b !== void 0 ? _b : action.glyph.table,
                    expression: action.expression,
                    valueType: action.valueType,
                    scale: inferred,
                    attribute: action.attribute,
                    valueIndex: action.hints && action.hints.allowSelectValue != undefined
                        ? 0
                        : null,
                };
            }
            if (!this.chart.scaleMappings.find(function (scaleMapping) { return scaleMapping.scale === inferred; })) {
                this.chart.scaleMappings.push(__assign(__assign({}, action.mark.mappings[action.attribute]), { attribute: action.attribute }));
            }
        }
        else {
            if ((action.valueType == core_1.Specification.DataType.Boolean ||
                action.valueType == core_1.Specification.DataType.String ||
                action.valueType == core_1.Specification.DataType.Number ||
                action.valueType == core_1.Specification.DataType.Date) &&
                action.attributeType == core_1.Specification.AttributeType.Text) {
                var format = void 0;
                // don't apply format to numbers if data kind is categorical to draw as are
                if (action.valueMetadata.kind === dataset_1.DataKind.Categorical) {
                    format = undefined;
                }
                else if (action.valueType == core_1.Specification.DataType.Number) {
                    // If the valueType is a number and kind is not categorical, use a format
                    format = ".1f";
                }
                else if (action.valueType == core_1.Specification.DataType.Date) {
                    // If the valueType is a date and kind is not categorical, use a format
                    format = "%m/%d/%Y";
                }
                action.mark.mappings[action.attribute] = {
                    type: specification_1.MappingType.text,
                    table: (_c = action.expressionTable) !== null && _c !== void 0 ? _c : action.glyph.table,
                    textExpression: new core_1.Expression.TextExpression([
                        { expression: core_1.Expression.parse(action.expression), format: format },
                    ]).toString(),
                };
            }
        }
        this.solveConstraintsAndUpdateGraphics();
    });
}
exports.default = default_1;
//# sourceMappingURL=mark.js.map