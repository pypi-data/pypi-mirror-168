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
var core_1 = require("../../../core");
var specification_1 = require("../../../core/specification");
var actions_1 = require("../../actions");
var app_store_1 = require("../app_store");
var selection_1 = require("../selection");
// eslint-disable-next-line
function default_1(REG) {
    REG.add(actions_1.Actions.AddGlyph, function (action) {
        this.saveHistory();
        var glyph = this.chartManager.addGlyph(action.classID, this.dataset.tables[0].name);
        this.currentSelection = new selection_1.GlyphSelection(null, glyph);
        this.currentGlyph = glyph;
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.RemoveGlyph, function (action) {
        this.saveHistory();
        this.chartManager.removeGlyph(action.glyph);
        this.currentSelection = null;
        this.currentGlyph = null;
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.SetGlyphAttribute, function (action) {
        this.saveHistory();
        if (action.mapping == null) {
            delete action.glyph.mappings[action.attribute];
        }
        else {
            action.glyph.mappings[action.attribute] = action.mapping;
        }
        this.solveConstraintsAndUpdateGraphics();
    });
    REG.add(actions_1.Actions.UpdateGlyphAttribute, function (action) {
        var _this = this;
        this.saveHistory();
        for (var key in action.updates) {
            if (!Object.prototype.hasOwnProperty.call(action.updates, key)) {
                continue;
            }
            delete action.glyph.mappings[key];
        }
        this.forAllGlyph(action.glyph, function (glyphState) {
            for (var key in action.updates) {
                if (!Object.prototype.hasOwnProperty.call(action.updates, key)) {
                    continue;
                }
                glyphState.attributes[key] = action.updates[key];
                _this.addPresolveValue(core_1.Solver.ConstraintStrength.STRONG, glyphState.attributes, key, action.updates[key]);
            }
        });
        this.solveConstraintsAndUpdateGraphics();
    });
    // eslint-disable-next-line
    REG.add(actions_1.Actions.AddMarkToGlyph, function (action) {
        var e_1, _a;
        var _this = this;
        this.saveHistory();
        //cant add plot-segment in glyph
        if (core_1.Prototypes.isType(action.classID, "plot-segment")) {
            return;
        }
        var mark = this.chartManager.createObject(action.classID);
        for (var key in action.properties) {
            mark.properties[key] = action.properties[key];
        }
        // Make sure name don't duplicate
        if (this.chartManager.isNameUsed(mark.properties.name)) {
            mark.properties.name = this.chartManager.findUnusedName(mark.properties.name);
        }
        this.chartManager.addMarkToGlyph(mark, action.glyph);
        var attributesSet = false;
        var _loop_1 = function (attr) {
            if (Object.prototype.hasOwnProperty.call(action.mappings, attr)) {
                var _a = __read(action.mappings[attr], 2), value_1 = _a[0], mapping = _a[1];
                if (mapping != null) {
                    if (mapping.type == specification_1.MappingType._element) {
                        var elementMapping = mapping;
                        action.glyph.constraints.push({
                            type: "snap",
                            attributes: {
                                element: mark._id,
                                attribute: attr,
                                targetElement: elementMapping.element,
                                targetAttribute: elementMapping.attribute,
                                gap: 0,
                            },
                        });
                    }
                    else {
                        mark.mappings[attr] = mapping;
                    }
                }
                if (value_1 != null) {
                    var idx_1 = action.glyph.marks.indexOf(mark);
                    this_1.forAllGlyph(action.glyph, function (glyphState) {
                        glyphState.marks[idx_1].attributes[attr] = value_1;
                        _this.addPresolveValue(core_1.Solver.ConstraintStrength.STRONG, glyphState.marks[idx_1].attributes, attr, value_1);
                    });
                }
                attributesSet = true;
            }
        };
        var this_1 = this;
        for (var attr in action.mappings) {
            _loop_1(attr);
        }
        // Logic for first marks
        if (!attributesSet) {
            switch (action.classID) {
                case "mark.rect":
                case "mark.nested-chart":
                case "mark.textbox":
                case "mark.image":
                    {
                        mark.mappings.x1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix1",
                        };
                        mark.mappings.y1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy1",
                        };
                        mark.mappings.x2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix2",
                        };
                        mark.mappings.y2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy2",
                        };
                        // Move anchor to bottom
                        // action.glyph.marks[0].mappings["y"] = <Specification.ParentMapping>{ type: "parent", parentAttribute: "iy1" };
                    }
                    break;
                case "mark.line":
                    {
                        mark.mappings.x1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix1",
                        };
                        mark.mappings.y1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy1",
                        };
                        mark.mappings.x2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix2",
                        };
                        mark.mappings.y2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy2",
                        };
                    }
                    break;
                case "mark.symbol":
                case "mark.text":
                case "mark.icon":
                    {
                        mark.mappings.x = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "icx",
                        };
                        mark.mappings.y = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "icy",
                        };
                    }
                    break;
                case "mark.data-axis":
                    {
                        mark.mappings.x1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix1",
                        };
                        mark.mappings.y1 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy1",
                        };
                        mark.mappings.x2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "ix1",
                        };
                        mark.mappings.y2 = {
                            type: specification_1.MappingType.parent,
                            parentAttribute: "iy2",
                        };
                    }
                    break;
            }
        }
        if (action.classID == "mark.nested-chart") {
            // Add column names to the mark
            var columnNameMap = {};
            try {
                for (var _b = __values(this.getTable(action.glyph.table).columns), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var column = _c.value;
                    columnNameMap[column.name] = column.name;
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
            mark.properties.columnNameMap = columnNameMap;
        }
        this.currentSelection = new selection_1.MarkSelection(this.findPlotSegmentForGlyph(action.glyph), action.glyph, action.glyph.marks[action.glyph.marks.length - 1]);
        this.currentGlyph = action.glyph;
        this.solveConstraintsAndUpdateGraphics();
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
    });
    REG.add(actions_1.Actions.RemoveMarkFromGlyph, function (action) {
        this.saveHistory();
        // We never delete the anchor
        if (action.mark.classID == "mark.anchor") {
            return;
        }
        this.chartManager.removeMarkFromGlyph(action.mark, action.glyph);
        this.currentSelection = null;
        this.emit(app_store_1.AppStore.EVENT_SELECTION);
        this.solveConstraintsAndUpdateGraphics();
    });
}
exports.default = default_1;
//# sourceMappingURL=glyph.js.map