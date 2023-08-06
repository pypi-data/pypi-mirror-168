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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.LinearBooleanScale = exports.LinearBooleanScaleMode = exports.LinearColorScale = exports.LinearScale = void 0;
var strings_1 = require("../../../strings");
var common_1 = require("../../common");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var types_1 = require("../../specification/types");
var index_1 = require("./index");
var LinearScale = /** @class */ (function (_super) {
    __extends(LinearScale, _super);
    function LinearScale() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["rangeMin", "rangeMax"];
        _this.attributes = {
            rangeMin: {
                name: "rangeMin",
                type: Specification.AttributeType.Number,
                defaultValue: 0,
            },
            rangeMax: {
                name: "rangeMax",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    LinearScale.prototype.mapDataToAttribute = function (data) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var x1 = props.domainMin;
        var x2 = props.domainMax;
        var y1 = attrs.rangeMin;
        var y2 = attrs.rangeMax;
        return ((data - x1) / (x2 - x1)) * (y2 - y1) + y1;
    };
    LinearScale.prototype.buildConstraint = function (data, target, solver) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var x1 = props.domainMin;
        var x2 = props.domainMax;
        var k = (data - x1) / (x2 - x1);
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, target]], [
            [1 - k, solver.attr(attrs, "rangeMin")],
            [k, solver.attr(attrs, "rangeMax")],
        ]);
    };
    LinearScale.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.rangeMin = 0;
        attrs.rangeMax = 100;
    };
    LinearScale.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var s = new common_1.Scale.LinearScale();
        var values = column.filter(function (x) { return typeof x == "number"; });
        s.inferParameters(values);
        s.adjustDomain(options);
        if (options.extendScaleMin || props.domainMin === undefined) {
            props.domainMin = s.domainMin;
        }
        if (options.extendScaleMax || props.domainMax === undefined) {
            props.domainMax = s.domainMax;
        }
        if (!options.reuseRange) {
            if (options.rangeNumber) {
                attrs.rangeMin = options.rangeNumber[0];
                attrs.rangeMax = options.rangeNumber[1];
            }
            else {
                attrs.rangeMin = 0;
                attrs.rangeMax = 100;
            }
            if (!options.autoRange) {
                this.object.mappings.rangeMin = {
                    type: specification_1.MappingType.value,
                    value: attrs.rangeMin,
                };
                this.object.mappings.rangeMax = {
                    type: specification_1.MappingType.value,
                    value: attrs.rangeMax,
                };
            }
            if (options.startWithZero === "always") {
                this.object.mappings.rangeMin = {
                    type: specification_1.MappingType.value,
                    value: 0,
                };
            }
        }
    };
    LinearScale.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.sectionHeader(strings_1.strings.objects.dataAxis.domain),
            manager.inputNumber({ property: "domainMin" }, { label: strings_1.strings.objects.dataAxis.start, stopPropagation: true }),
            manager.inputNumber({ property: "domainMax" }, {
                label: strings_1.strings.objects.dataAxis.end,
                stopPropagation: true,
                styles: { marginBottom: "0.5rem" },
            }),
            manager.sectionHeader(strings_1.strings.objects.dataAxis.autoUpdateValues),
            manager.inputBoolean({
                property: "autoDomainMin",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.start,
            }),
            manager.inputBoolean({
                property: "autoDomainMax",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.end,
            }),
            manager.sectionHeader(strings_1.strings.objects.dataAxis.range),
            manager.mappingEditor(strings_1.strings.objects.dataAxis.start, "rangeMin", {
                defaultValue: 0,
                stopPropagation: true,
            }),
            manager.mappingEditor(strings_1.strings.objects.dataAxis.end, "rangeMax", {
                defaultAuto: true,
                stopPropagation: true,
            }),
        ];
    };
    LinearScale.prototype.getTemplateParameters = function () {
        var parameters = _super.prototype.getTemplateParameters.call(this);
        if (!parameters.properties) {
            parameters.properties = [];
        }
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                property: "domainMin",
            },
            type: Specification.AttributeType.Number,
        });
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                property: "domainMax",
            },
            type: Specification.AttributeType.Number,
        });
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                attribute: "rangeMin",
            },
            type: Specification.AttributeType.Number,
            default: null,
        });
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                attribute: "rangeMax",
            },
            type: Specification.AttributeType.Number,
            default: null,
        });
        return parameters;
    };
    LinearScale.classID = "scale.linear<number,number>";
    LinearScale.type = "scale";
    LinearScale.defaultMappingValues = {
        rangeMin: 0,
    };
    LinearScale.defaultProperties = {
        autoDomainMin: true,
        autoDomainMax: true,
    };
    return LinearScale;
}(index_1.ScaleClass));
exports.LinearScale = LinearScale;
function getDefaultGradient() {
    return {
        colorspace: types_1.Colorspace.Lab,
        colors: [
            { r: 255, g: 255, b: 255 },
            { r: 0, g: 0, b: 0 },
        ],
    };
}
var LinearColorScale = /** @class */ (function (_super) {
    __extends(LinearColorScale, _super);
    function LinearColorScale() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    LinearColorScale.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        var x1 = props.domainMin;
        var x2 = props.domainMax;
        var t = (data - x1) / (x2 - x1);
        var c = common_1.interpolateColors(props.range.colors, props.range.colorspace);
        return c(t);
    };
    // eslint-disable-next-line
    LinearColorScale.prototype.buildConstraint = function (
    // eslint-disable-next-line
    data, 
    // eslint-disable-next-line
    target, 
    // eslint-disable-next-line
    solver
    // eslint-disable-next-line
    ) { };
    // eslint-disable-next-line
    LinearColorScale.prototype.initializeState = function () { };
    LinearColorScale.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.LinearScale();
        var values = column.filter(function (x) { return typeof x == "number"; });
        s.inferParameters(values);
        if (options.extendScaleMin || props.domainMin === undefined) {
            props.domainMin = s.domainMin;
        }
        if (options.extendScaleMax || props.domainMax === undefined) {
            props.domainMax = s.domainMax;
        }
        if (!options.reuseRange) {
            props.range = getDefaultGradient();
        }
    };
    LinearColorScale.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.sectionHeader(strings_1.strings.objects.dataAxis.domain),
            manager.inputNumber({ property: "domainMin" }, { stopPropagation: true, label: strings_1.strings.objects.dataAxis.start }),
            manager.inputNumber({ property: "domainMax" }, {
                stopPropagation: true,
                label: strings_1.strings.objects.dataAxis.end,
                styles: { marginBottom: "0.5rem" },
            }),
            manager.sectionHeader(strings_1.strings.objects.dataAxis.autoUpdateValues),
            manager.inputBoolean({
                property: "autoDomainMin",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoMin,
            }),
            manager.inputBoolean({
                property: "autoDomainMax",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoMax,
                styles: { marginBottom: "0.5rem" },
            }),
            manager.sectionHeader(strings_1.strings.objects.dataAxis.gradient),
            manager.inputColorGradient({ property: "range", noComputeLayout: true }, true),
        ];
    };
    LinearColorScale.prototype.getTemplateParameters = function () {
        var parameters = _super.prototype.getTemplateParameters.call(this);
        if (!parameters.properties) {
            parameters.properties = [];
        }
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                property: "domainMin",
            },
            type: Specification.AttributeType.Number,
        });
        parameters.properties.push({
            objectID: this.object._id,
            target: {
                property: "domainMax",
            },
            type: Specification.AttributeType.Number,
        });
        return parameters;
    };
    LinearColorScale.classID = "scale.linear<number,color>";
    LinearColorScale.type = "scale";
    LinearColorScale.metadata = {
        displayName: strings_1.strings.objects.scale,
        iconPath: "scale/color",
    };
    LinearColorScale.defaultMappingValues = {
        range: getDefaultGradient(),
    };
    return LinearColorScale;
}(index_1.ScaleClass));
exports.LinearColorScale = LinearColorScale;
var LinearBooleanScaleMode;
(function (LinearBooleanScaleMode) {
    LinearBooleanScaleMode["GreaterThan"] = "Greater than";
    LinearBooleanScaleMode["LessThan"] = "Less than";
    LinearBooleanScaleMode["Between"] = "Between";
    LinearBooleanScaleMode["EqualTo"] = "Equal to";
    LinearBooleanScaleMode["GreaterThanOrEqualTo"] = "Greater than or equal to";
    LinearBooleanScaleMode["LessThanOrEqualTo"] = "Less than or equal to";
    LinearBooleanScaleMode["NotBetween"] = "Not between";
    LinearBooleanScaleMode["NotEqualTo"] = "Not Equal to";
})(LinearBooleanScaleMode = exports.LinearBooleanScaleMode || (exports.LinearBooleanScaleMode = {}));
var LinearBooleanScale = /** @class */ (function (_super) {
    __extends(LinearBooleanScale, _super);
    function LinearBooleanScale() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    LinearBooleanScale.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        var value = data;
        switch (props.mode) {
            case LinearBooleanScaleMode.GreaterThan:
                return value > props.min;
            case LinearBooleanScaleMode.GreaterThanOrEqualTo:
                return value >= props.min;
            case LinearBooleanScaleMode.LessThan:
                return value < props.max;
            case LinearBooleanScaleMode.LessThanOrEqualTo:
                return value <= props.max;
            case LinearBooleanScaleMode.EqualTo:
                return value == props.min;
            case LinearBooleanScaleMode.NotEqualTo:
                return value != props.min;
            case LinearBooleanScaleMode.Between:
                return value <= props.max && value >= props.min;
            case LinearBooleanScaleMode.NotBetween:
                return value > props.max || value < props.min;
        }
    };
    LinearBooleanScale.prototype.buildConstraint = function () {
        //ignore
    };
    LinearBooleanScale.prototype.initializeState = function () {
        //ignore
    };
    LinearBooleanScale.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.LinearScale();
        var values = column.filter(function (x) { return typeof x == "number"; });
        s.inferParameters(values);
        if (options.extendScaleMin || props.min === undefined) {
            props.min = s.domainMin;
        }
        if (options.extendScaleMax || props.max === undefined) {
            props.max = s.domainMax;
        }
        props.mode = LinearBooleanScaleMode.GreaterThan;
    };
    LinearBooleanScale.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var minMax = [];
        var isEqual = props.mode === LinearBooleanScaleMode.EqualTo ||
            props.mode === LinearBooleanScaleMode.NotEqualTo;
        if (props.mode === LinearBooleanScaleMode.GreaterThan ||
            props.mode === LinearBooleanScaleMode.GreaterThanOrEqualTo ||
            props.mode === LinearBooleanScaleMode.Between ||
            props.mode === LinearBooleanScaleMode.NotBetween ||
            props.mode === LinearBooleanScaleMode.EqualTo ||
            props.mode === LinearBooleanScaleMode.NotEqualTo) {
            minMax.push(manager.vertical(this.object.inputType === Specification.DataType.Date
                ? manager.inputDate({ property: "min" }, {
                    label: isEqual
                        ? strings_1.strings.objects.scales.date
                        : strings_1.strings.objects.scales.startDate,
                })
                : manager.inputNumber({ property: "min" }, {
                    stopPropagation: true,
                    label: isEqual
                        ? strings_1.strings.objects.scales.value
                        : strings_1.strings.objects.scales.minimumValue,
                })));
        }
        if (props.mode === LinearBooleanScaleMode.LessThan ||
            props.mode === LinearBooleanScaleMode.LessThanOrEqualTo ||
            props.mode === LinearBooleanScaleMode.Between ||
            props.mode === LinearBooleanScaleMode.NotBetween) {
            minMax.push(this.object.inputType === Specification.DataType.Date
                ? manager.inputDate({ property: "max" }, { label: strings_1.strings.objects.scales.endDate })
                : manager.inputNumber({ property: "max" }, {
                    stopPropagation: true,
                    label: strings_1.strings.objects.scales.maximumValue,
                }));
        }
        return __spread([
            manager.sectionHeader(strings_1.strings.typeDisplayNames.boolean),
            manager.inputSelect({ property: "mode" }, {
                type: "dropdown",
                options: [
                    LinearBooleanScaleMode.GreaterThan,
                    LinearBooleanScaleMode.GreaterThanOrEqualTo,
                    LinearBooleanScaleMode.LessThan,
                    LinearBooleanScaleMode.LessThanOrEqualTo,
                    LinearBooleanScaleMode.EqualTo,
                    LinearBooleanScaleMode.NotEqualTo,
                    LinearBooleanScaleMode.Between,
                    LinearBooleanScaleMode.NotBetween,
                ],
                labels: [
                    LinearBooleanScaleMode.GreaterThan,
                    LinearBooleanScaleMode.GreaterThanOrEqualTo,
                    LinearBooleanScaleMode.LessThan,
                    LinearBooleanScaleMode.LessThanOrEqualTo,
                    LinearBooleanScaleMode.EqualTo,
                    LinearBooleanScaleMode.NotEqualTo,
                    LinearBooleanScaleMode.Between,
                    LinearBooleanScaleMode.NotBetween,
                ],
                showLabel: true,
                label: strings_1.strings.objects.scales.mode,
            })
        ], minMax);
    };
    LinearBooleanScale.prototype.getTemplateParameters = function () {
        var parameters = _super.prototype.getTemplateParameters.call(this);
        var props = this.object.properties;
        if (!parameters.properties) {
            parameters.properties = [];
        }
        if (props.mode === LinearBooleanScaleMode.GreaterThan ||
            props.mode === LinearBooleanScaleMode.GreaterThanOrEqualTo) {
            parameters.properties.push({
                objectID: this.object._id,
                target: {
                    property: "min",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.min,
            });
        }
        if (props.mode === LinearBooleanScaleMode.LessThan ||
            props.mode === LinearBooleanScaleMode.LessThanOrEqualTo) {
            parameters.properties.push({
                objectID: this.object._id,
                target: {
                    property: "max",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.max,
            });
        }
        if (props.mode === LinearBooleanScaleMode.Between ||
            props.mode === LinearBooleanScaleMode.NotBetween) {
            parameters.properties.push({
                objectID: this.object._id,
                target: {
                    property: "min",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.min,
            });
            parameters.properties.push({
                objectID: this.object._id,
                target: {
                    property: "max",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.max,
            });
        }
        if (props.mode === LinearBooleanScaleMode.EqualTo ||
            props.mode === LinearBooleanScaleMode.NotEqualTo) {
            parameters.properties.push({
                objectID: this.object._id,
                target: {
                    property: "min",
                },
                type: Specification.AttributeType.Number,
                default: this.object.properties.min,
            });
        }
        return parameters;
    };
    LinearBooleanScale.classID = "scale.linear<number,boolean>";
    LinearBooleanScale.type = "scale";
    LinearBooleanScale.defaultMappingValues = {
        min: 0,
        max: 1,
        mode: LinearBooleanScaleMode.GreaterThan,
    };
    return LinearBooleanScale;
}(index_1.ScaleClass));
exports.LinearBooleanScale = LinearBooleanScale;
//# sourceMappingURL=linear.js.map