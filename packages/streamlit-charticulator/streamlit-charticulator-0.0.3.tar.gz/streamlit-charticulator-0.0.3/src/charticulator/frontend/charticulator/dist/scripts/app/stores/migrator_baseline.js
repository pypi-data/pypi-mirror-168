"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.upgradeGuidesToBaseline = void 0;
var specification_1 = require("../../core/specification");
var guides_1 = require("../../core/prototypes/guides");
var core_1 = require("../../core");
var prototypes_1 = require("../../core/prototypes");
var nested_chart_1 = require("../../core/prototypes/marks/nested_chart");
var CommonPropertyNames;
(function (CommonPropertyNames) {
    CommonPropertyNames["name"] = "name";
    CommonPropertyNames["gap"] = "gap";
})(CommonPropertyNames || (CommonPropertyNames = {}));
var DeletedAttributeNames;
(function (DeletedAttributeNames) {
    DeletedAttributeNames["value2"] = "value2";
})(DeletedAttributeNames || (DeletedAttributeNames = {}));
var DeletedPropertyNames;
(function (DeletedPropertyNames) {
    DeletedPropertyNames["value"] = "value";
    DeletedPropertyNames["value2"] = "value2";
})(DeletedPropertyNames || (DeletedPropertyNames = {}));
/** Upgrade old versions of chart spec and state to newer version */
function upgradeGuidesToBaseline(appStoreState) {
    upgradeScope(appStoreState.chart, appStoreState.chartState);
    return appStoreState;
}
exports.upgradeGuidesToBaseline = upgradeGuidesToBaseline;
function upgradeScope(parentElement, parentState) {
    upgradeChartGuides(parentElement, parentState);
    upgradeGlyphGuides(parentElement, parentState);
}
function upgradeChartGuides(parentElement, parentState) {
    // get chart guides
    var chartGuideRefs = find(parentElement.elements, parentState.elements, function (element) { return element.classID === guides_1.GuideClass.classID; });
    chartGuideRefs.forEach(function (ref) {
        var element = ref.element, state = ref.state;
        // convert mappings to actual values
        var parentMapping = element.mappings.value;
        if (parentMapping && parentMapping.type === specification_1.MappingType.parent) {
            var parentAttribute = parentMapping.parentAttribute;
            // set value to actual mapped attr value
            state.attributes[guides_1.GuideAttributeNames.value] =
                parentState.attributes[parentAttribute];
            // remove the mapping
            delete element.mappings.value;
        }
        else {
            // guides should not be mapped to anything other than parent
            // Notify user?
        }
        // find other elements constrained to this chartElementItem
        parentElement.constraints.forEach(function (constraint) {
            if (constraint.type === "snap" &&
                constraint.attributes.targetElement === element._id) {
                changeConstraintTarget(element, constraint, +state.attributes[guides_1.GuideAttributeNames.value], parentElement.elements, parentState.elements);
            }
        });
        // add new properties
        addNewGuideProperties(element, state);
        // remove deleted properties / attributes
        removeOldGuideProperties(element, state);
    });
}
function upgradeGlyphGuides(parentElement, parentState, nested) {
    if (nested === void 0) { nested = false; }
    parentElement.glyphs.forEach(function (glyph) {
        // collect and separate marks from guides
        var guides = {};
        glyph.marks.forEach(function (mark) {
            if (prototypes_1.isType(mark.classID, guides_1.GuideClass.classID)) {
                guides[mark._id] = mark;
            }
            else if (prototypes_1.isType(mark.classID, nested_chart_1.NestedChartElementClass.classID)) {
                var nc = mark;
                upgradeGlyphGuides(nc.properties.specification, null, true); // nested charts do not store in ChartState
            }
        });
        // get element which uses this glyph
        var related = find(parentElement.elements, parentState && parentState.elements, function (element) {
            var ps = element;
            return ps.glyph === glyph._id;
        });
        // look at constraints
        glyph.constraints.forEach(function (constraint) {
            if (constraint.type === "snap") {
                var id = constraint.attributes.targetElement;
                var guide = guides[id];
                if (guide &&
                    constraint.attributes.targetAttribute === DeletedAttributeNames.value2) {
                    // make a new guide
                    var newGuide_1 = createGuide(guide.properties[guides_1.GuidePropertyNames.axis], guide, +guide.properties[DeletedPropertyNames.value] +
                        +guide.properties[CommonPropertyNames.gap]);
                    // add new guide
                    glyph.marks.push(newGuide_1.element);
                    // add state instances
                    related.forEach(function (ref) {
                        var s = ref.state;
                        if (s && s.glyphs) {
                            s.glyphs.forEach(function (glyphState) {
                                glyphState.marks.push(newGuide_1.state);
                            });
                        }
                    });
                    if (nested) {
                        // nested charts store in mappings
                        var valueMapping = {
                            type: specification_1.MappingType.value,
                            value: newGuide_1.state.attributes[guides_1.GuideAttributeNames.value],
                        };
                        newGuide_1.element.mappings.value = valueMapping;
                    }
                    // point to new guide
                    constraint.attributes.targetElement = newGuide_1.element._id;
                    constraint.attributes.targetAttribute =
                        guides_1.GuideAttributeNames.computedBaselineValue;
                }
            }
        });
        // if (guide.mappings) {
        // TODO guides should not be mapped!
        // }
        for (var _id in guides) {
            var guide = guides[_id];
            // add new properties to guide
            addNewGuideProperties(guide);
            // delete old properties
            removeOldGuideProperties(guide);
            // modify all state instances
            related.forEach(function (ref) {
                var s = ref.state;
                if (s && s.glyphs) {
                    s.glyphs.forEach(function (glyphState) {
                        glyphState.marks.forEach(function (markState) {
                            // add new properties to guide
                            addNewGuideProperties(null, markState);
                            // delete old properties
                            removeOldGuideProperties(null, markState);
                        });
                    });
                }
            });
        }
    });
}
function find(elements, states, predicate) {
    var refs = [];
    elements.forEach(function (element, index) {
        if (predicate(element)) {
            var state = states && states[index];
            refs.push({ element: element, index: index, state: state });
        }
    });
    return refs;
}
function changeConstraintTarget(element, constraint, guideValue, elementCollection, stateCollection) {
    if (!element) {
        throw new Error("constraint bound to unknown element");
    }
    if (!element.properties) {
        throw new Error("constraint target element has no properties");
    }
    var gap = +element.properties[CommonPropertyNames.gap];
    if (constraint.attributes.targetAttribute === DeletedAttributeNames.value2 &&
        gap) {
        // create a 2nd guide to insert, based on gap property of first
        var axis = element.properties[guides_1.GuidePropertyNames.axis];
        var value_1 = guideValue + gap;
        var newGuide = createGuide(axis, element, value_1);
        elementCollection.push(newGuide.element);
        stateCollection.push(newGuide.state);
        constraint.attributes.targetElement = newGuide.element._id;
        // find constraint object and make value attribute match
        var constrained = find(elementCollection, stateCollection, function (element) { return element._id === constraint.attributes.element; });
        constrained.forEach(function (ref) {
            var name = constraint.attributes.attribute;
            ref.state.attributes[name] = value_1;
        });
    }
    constraint.attributes.targetAttribute = "computedBaselineValue";
}
function addNewGuideProperties(element, state) {
    if (element) {
        var defaultBaseline = "center";
        element.properties[guides_1.GuidePropertyNames.baseline] = defaultBaseline;
    }
    if (state) {
        state.attributes[guides_1.GuideAttributeNames.computedBaselineValue] =
            state.attributes[guides_1.GuideAttributeNames.value];
    }
}
function removeOldGuideProperties(element, state) {
    if (element) {
        delete element.properties[CommonPropertyNames.gap];
        delete element.properties[DeletedPropertyNames.value]; // unused property in original schema
        delete element.properties[DeletedPropertyNames.value2]; // unused property in original schema
    }
    if (state) {
        delete state.attributes[DeletedAttributeNames.value2];
    }
}
function createGuide(axis, originalGuide, value) {
    var defaultBaselineH = "center";
    var defaultBaselineV = "middle";
    var element = {
        _id: core_1.uniqueID(),
        classID: "guide.guide",
        properties: {
            baseline: axis === "y" ? defaultBaselineV : defaultBaselineH,
            name: (originalGuide.properties[CommonPropertyNames.name] || "Guide") + " gap",
            axis: axis,
        },
        mappings: {},
    };
    var state = {
        attributes: {
            value: value,
            computedBaselineValue: value,
        },
    };
    return { element: element, state: state };
}
//# sourceMappingURL=migrator_baseline.js.map