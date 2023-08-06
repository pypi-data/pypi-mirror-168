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
exports.GuideClass = exports.GuidePropertyNames = exports.GuideAttributeNames = void 0;
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
var common_1 = require("../common");
var glyphs_1 = require("../glyphs");
var charts_1 = require("../charts");
var strings_1 = require("../../../strings");
var GuideAttributeNames;
(function (GuideAttributeNames) {
    GuideAttributeNames["value"] = "value";
    GuideAttributeNames["computedBaselineValue"] = "computedBaselineValue";
})(GuideAttributeNames = exports.GuideAttributeNames || (exports.GuideAttributeNames = {}));
var GuidePropertyNames;
(function (GuidePropertyNames) {
    GuidePropertyNames["axis"] = "axis";
    GuidePropertyNames["baseline"] = "baseline";
})(GuidePropertyNames = exports.GuidePropertyNames || (exports.GuidePropertyNames = {}));
var GuideClass = /** @class */ (function (_super) {
    __extends(GuideClass, _super);
    function GuideClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [
            GuideAttributeNames.value,
            GuideAttributeNames.computedBaselineValue,
        ];
        _this.attributes = {
            value: {
                name: GuideAttributeNames.value,
                type: Specification.AttributeType.Number,
            },
            computedBaselineValue: {
                name: GuideAttributeNames.computedBaselineValue,
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    GuideClass.prototype.initializeState = function () {
        this.state.attributes.value = 0;
        this.state.attributes.computedBaselineValue = 0;
    };
    GuideClass.prototype.getAxis = function () {
        return this.object.properties.axis;
    };
    GuideClass.prototype.getParentType = function () {
        var classID = this.parent.object.classID;
        var rectGlyph = common_1.isType(classID, glyphs_1.RectangleGlyph.classID);
        var rectChart = common_1.isType(classID, charts_1.RectangleChart.classID);
        return { rectChart: rectChart, rectGlyph: rectGlyph };
    };
    // eslint-disable-next-line
    GuideClass.prototype.buildConstraints = function (solver) {
        var _a = this.getParentType(), rectGlyph = _a.rectGlyph, rectChart = _a.rectChart;
        if (rectGlyph) {
            switch (this.object.properties.baseline) {
                case "center":
                case "middle": {
                    var _b = __read(solver.attrs(this.state.attributes, [
                        GuideAttributeNames.value,
                        GuideAttributeNames.computedBaselineValue,
                    ]), 2), computedBaselineValue = _b[1];
                    solver.addLinear(solver_1.ConstraintStrength.HARD, this.state.attributes.value, [[-1, computedBaselineValue]]);
                    break;
                }
                case "left": {
                    this.computeBaselineFromParentAttribute(solver, ["width"], function (_a, value) {
                        var _b = __read(_a, 1), width = _b[0];
                        return [
                            [-0.5, width],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "right": {
                    this.computeBaselineFromParentAttribute(solver, ["width"], function (_a, value) {
                        var _b = __read(_a, 1), width = _b[0];
                        return [
                            [+0.5, width],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "top": {
                    this.computeBaselineFromParentAttribute(solver, ["height"], function (_a, value) {
                        var _b = __read(_a, 1), height = _b[0];
                        return [
                            [+0.5, height],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "bottom": {
                    this.computeBaselineFromParentAttribute(solver, ["height"], function (_a, value) {
                        var _b = __read(_a, 1), height = _b[0];
                        return [
                            [-0.5, height],
                            [+1, value],
                        ];
                    });
                    break;
                }
            }
        }
        else if (rectChart) {
            switch (this.object.properties.baseline) {
                case "center": {
                    this.computeBaselineFromParentAttribute(solver, ["cx"], function (_a, value) {
                        var _b = __read(_a, 1), cx = _b[0];
                        return [
                            [+1, cx],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "middle": {
                    this.computeBaselineFromParentAttribute(solver, ["cy"], function (_a, value) {
                        var _b = __read(_a, 1), cy = _b[0];
                        return [
                            [+1, cy],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "left": {
                    this.computeBaselineFromParentAttribute(solver, ["width", "marginLeft"], function (_a, value) {
                        var _b = __read(_a, 2), width = _b[0], marginLeft = _b[1];
                        return [
                            [-0.5, width],
                            [+1, marginLeft],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "right": {
                    this.computeBaselineFromParentAttribute(solver, ["width", "marginRight"], function (_a, value) {
                        var _b = __read(_a, 2), width = _b[0], marginRight = _b[1];
                        return [
                            [+0.5, width],
                            [-1, marginRight],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "top": {
                    this.computeBaselineFromParentAttribute(solver, ["height", "marginTop"], function (_a, value) {
                        var _b = __read(_a, 2), height = _b[0], marginTop = _b[1];
                        return [
                            [+0.5, height],
                            [-1, marginTop],
                            [+1, value],
                        ];
                    });
                    break;
                }
                case "bottom": {
                    this.computeBaselineFromParentAttribute(solver, ["height", "marginBottom"], function (_a, value) {
                        var _b = __read(_a, 2), height = _b[0], marginBottom = _b[1];
                        return [
                            [-0.5, height],
                            [+1, marginBottom],
                            [+1, value],
                        ];
                    });
                    break;
                }
            }
        }
    };
    GuideClass.prototype.computeBaselineFromParentAttribute = function (solver, parentAttributeNames, rhsFn) {
        var parentAttrs = this.parent.state.attributes;
        var parentAttributeVariables = solver.attrs(parentAttrs, parentAttributeNames);
        // parentAttributeNames.forEach(parentAttributeName => solver.makeConstant(parentAttrs, parentAttributeName));
        var _a = __read(solver.attrs(this.state.attributes, [
            GuideAttributeNames.value,
            GuideAttributeNames.computedBaselineValue,
        ]), 2), value = _a[0], computedBaselineValue = _a[1];
        solver.makeConstant(this.state.attributes, GuideAttributeNames.value);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, computedBaselineValue]], rhsFn(parentAttributeVariables, value));
    };
    GuideClass.prototype.getLinkAnchors = function () {
        return [];
    };
    /** Get handles given current state */
    // eslint-disable-next-line max-lines-per-function
    GuideClass.prototype.getHandles = function () {
        var inf = [-1000, 1000];
        var value = this.state.attributes.value;
        var _a = this.object.properties, axis = _a.axis, baseline = _a.baseline;
        var _b = this.getParentType(), rectChart = _b.rectChart, rectGlyph = _b.rectGlyph;
        var handleLineGlyph = function () {
            return [
                {
                    type: "line",
                    axis: axis,
                    actions: [
                        {
                            type: "attribute-value-mapping",
                            attribute: GuideAttributeNames.value,
                            source: GuideAttributeNames.value,
                        },
                    ],
                    value: value,
                    span: inf,
                },
            ];
        };
        var handleRelativeLine = function (reference) {
            return [
                {
                    type: "relative-line",
                    axis: axis,
                    actions: [
                        {
                            type: "attribute-value-mapping",
                            attribute: GuideAttributeNames.value,
                            source: GuideAttributeNames.value,
                        },
                    ],
                    reference: reference,
                    sign: 1,
                    value: value,
                    span: inf,
                },
            ];
        };
        var parentAttrs = this.parent.state.attributes;
        if (rectGlyph) {
            switch (baseline) {
                case "center":
                case "middle": {
                    return handleLineGlyph();
                }
                case "left": {
                    return handleRelativeLine(+parentAttrs.ix1);
                }
                case "right": {
                    return handleRelativeLine(+parentAttrs.ix2);
                }
                case "top": {
                    return handleRelativeLine(+parentAttrs.iy2);
                }
                case "bottom": {
                    return handleRelativeLine(+parentAttrs.iy1);
                }
            }
        }
        else if (rectChart) {
            switch (baseline) {
                case "center": {
                    return handleRelativeLine(+parentAttrs.cx);
                }
                case "middle": {
                    return handleRelativeLine(+parentAttrs.cy);
                }
                case "left": {
                    return handleRelativeLine(+parentAttrs.x1);
                }
                case "right": {
                    return handleRelativeLine(+parentAttrs.x2);
                }
                case "top": {
                    return handleRelativeLine(+parentAttrs.y2);
                }
                case "bottom": {
                    return handleRelativeLine(+parentAttrs.y1);
                }
            }
        }
    };
    GuideClass.prototype.getSnappingGuides = function () {
        var _this = this;
        var snappingGuideAxis = function (attribute, value) {
            return {
                type: _this.getAxis(),
                value: value,
                attribute: attribute,
                visible: true,
                visualType: common_1.SnappingGuidesVisualTypes.Guide,
                priority: 1,
            };
        };
        var r = [
            snappingGuideAxis(GuideAttributeNames.computedBaselineValue, this.state.attributes.computedBaselineValue),
        ];
        return r;
    };
    GuideClass.prototype.getAttributePanelWidgets = function (manager) {
        var widgets = [];
        var labels;
        var options;
        var icons;
        if (this.object.properties.axis === "x") {
            var hOptions = ["left", "center", "right"];
            options = hOptions;
            labels = [
                strings_1.strings.alignment.left,
                strings_1.strings.alignment.center,
                strings_1.strings.alignment.right,
            ];
            icons = [
                "AlignHorizontalLeft",
                "AlignHorizontalCenter",
                "AlignHorizontalRight",
            ];
        }
        else {
            var vOptions = ["top", "middle", "bottom"];
            options = vOptions;
            labels = [
                strings_1.strings.alignment.top,
                strings_1.strings.alignment.middle,
                strings_1.strings.alignment.bottom,
            ];
            icons = [
                "AlignVerticalTop",
                "AlignVerticalCenter",
                "AlignVerticalBottom",
            ];
        }
        widgets.push(manager.verticalGroup({ header: strings_1.strings.objects.guides.guide }, [
            manager.inputSelect({ property: GuidePropertyNames.baseline }, {
                type: "dropdown",
                showLabel: true,
                labels: labels,
                options: options,
                icons: icons,
                label: strings_1.strings.objects.guides.baseline,
                searchSection: strings_1.strings.objects.guides.guide,
            }),
            manager.mappingEditor(strings_1.strings.objects.guides.offset, GuideAttributeNames.value, {
                defaultValue: this.state.attributes.value,
                searchSection: strings_1.strings.objects.guides.guide,
            }),
        ]));
        return widgets;
    };
    GuideClass.prototype.getTemplateParameters = function () {
        var properties = [
            {
                objectID: this.object._id,
                target: {
                    attribute: GuidePropertyNames.baseline,
                },
                type: Specification.AttributeType.Enum,
                default: this.object.properties.baseline,
            },
            {
                objectID: this.object._id,
                target: {
                    attribute: GuideAttributeNames.computedBaselineValue,
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.computedBaselineValue,
            },
        ];
        if (this.object.mappings.value &&
            this.object.mappings.value.type === Specification.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: GuideAttributeNames.value,
                },
                type: Specification.AttributeType.Number,
                default: this.state.attributes.value,
            });
        }
        return {
            properties: properties,
        };
    };
    GuideClass.classID = "guide.guide";
    GuideClass.type = "guide";
    GuideClass.metadata = {
        displayName: "Guide",
        iconPath: "guide/x",
    };
    GuideClass.defaultProperties = {
        baseline: null,
    };
    return GuideClass;
}(chart_element_1.ChartElementClass));
exports.GuideClass = GuideClass;
//# sourceMappingURL=guide.js.map